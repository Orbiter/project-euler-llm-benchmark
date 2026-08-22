import json
import time
import unittest
from unittest.mock import Mock, patch

from llm_client import (
    Endpoint,
    LLMIncompleteResponse,
    LLMRequestTimeout,
    LoadBalancer,
    RateLimitRetryError,
    Response,
    Server,
    Task,
    _post_with_rate_limit_retry,
    openai_api_chat,
)


def make_endpoint():
    return Endpoint(
        store_name="test-model",
        model_name="test-model",
        key="",
        url="https://example.com/v1/chat/completions",
    )


class LLMRequestResilienceTests(unittest.TestCase):
    @patch("llm_client.time.sleep")
    @patch("llm_client.requests.post")
    def test_rate_limit_retries_are_bounded(self, post, sleep):
        responses = [Mock(status_code=429) for _ in range(3)]
        post.side_effect = responses

        with self.assertRaisesRegex(RateLimitRetryError, "after 2 retries"):
            _post_with_rate_limit_retry(make_endpoint(), max_retries=2)

        self.assertEqual(post.call_count, 3)
        self.assertEqual(sleep.call_count, 2)
        for response in responses:
            response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_overall_deadline_rejects_and_closes_partial_stream(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None

        def delayed_chunks(**_kwargs):
            yield b'data: {"choices":[{"delta":{"content":"partial"}}]}\n'
            time.sleep(0.03)
            yield b'data: {"choices":[{"delta":{"content":" output"}}]}\n'

        response.iter_content.side_effect = delayed_chunks
        post.return_value = response

        with self.assertRaisesRegex(LLMRequestTimeout, "Overall timeout"):
            openai_api_chat(
                make_endpoint(),
                overall_timeout=0.01,
                idle_timeout=1,
            )

        response.close.assert_called()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_successful_response_is_closed(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.headers = {"Content-Type": "application/json"}
        response.text = json.dumps({
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
        })
        post.return_value = response

        answer, *_ = openai_api_chat(make_endpoint(), stream=False)

        self.assertEqual(answer, "ok")
        response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_stream_without_completion_marker_is_rejected(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.iter_content.return_value = iter([
            b'data: {"choices":[{"delta":{"content":"partial"}}]}\n',
        ])
        post.return_value = response

        with self.assertRaisesRegex(LLMIncompleteResponse, "partial output was discarded"):
            openai_api_chat(make_endpoint())

        response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_completed_stream_is_saved(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.iter_content.return_value = iter([
            b'data: {"choices":[{"delta":{"content":"complete"},"finish_reason":null}]}\n',
            b'data: {"choices":[{"delta":{},"finish_reason":"stop"}],"usage":{"total_tokens":2}}\n',
            b'data: [DONE]\n',
        ])
        post.return_value = response

        answer, total_tokens, *_ = openai_api_chat(make_endpoint())

        self.assertEqual(answer, "complete")
        self.assertEqual(total_tokens, 2)
        response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_done_marker_without_space_or_newline_ends_stream(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.iter_content.return_value = iter([b"data:[DONE]"])
        post.return_value = response

        answer, *_ = openai_api_chat(make_endpoint())

        self.assertEqual(answer, "")
        response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_split_unterminated_finish_reason_ends_stream(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.iter_content.return_value = iter([
            b'data:{"choices":[{"delta":{"content":"ok"},',
            b'"finish_reason":"stop"}],"usage":{"total_tokens":1}}',
        ])
        post.return_value = response

        answer, total_tokens, *_ = openai_api_chat(make_endpoint())

        self.assertEqual(answer, "ok")
        self.assertEqual(total_tokens, 1)
        response.close.assert_called_once_with()

    @patch("llm_client._post_with_rate_limit_retry")
    def test_ollama_done_true_ends_stream(self, post):
        response = Mock(status_code=200)
        response.raise_for_status.return_value = None
        response.iter_content.return_value = iter([b'data:{"done":true}'])
        post.return_value = response

        answer, *_ = openai_api_chat(make_endpoint())

        self.assertEqual(answer, "")


class LoadBalancerRetryTests(unittest.TestCase):
    @patch("llm_client.openai_api_chat")
    def test_failed_task_is_requeued_and_then_saved(self, chat):
        chat.side_effect = [
            LLMRequestTimeout("timed out"),
            ("answer", 2, 1.0, {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "reasoning_tokens": None,
            }, 2.0),
        ]
        saved = Mock()
        task = Task("1", "problem 1", "prompt", None, saved)
        balancer = LoadBalancer(task_retries=1)
        balancer.add_server(Server(make_endpoint()))
        balancer.start_distribution()

        self.assertTrue(balancer.add_task(task))
        balancer.wait_completion()

        self.assertEqual(chat.call_count, 2)
        self.assertEqual(task.attempts, 2)
        saved.assert_called_once()
        self.assertIsInstance(saved.call_args.args[0], Response)
        self.assertEqual(balancer.task_queue.unfinished_tasks, 0)
        self.assertIsNone(balancer.servers[0].current_task)

    @patch("llm_client.openai_api_chat", side_effect=LLMRequestTimeout("timed out"))
    def test_task_stops_after_retry_budget(self, chat):
        task = Task("1", "problem 1", "prompt", None, Mock())
        balancer = LoadBalancer(task_retries=1)
        balancer.add_server(Server(make_endpoint()))
        balancer.start_distribution()

        self.assertTrue(balancer.add_task(task))
        balancer.wait_completion()

        self.assertEqual(chat.call_count, 2)
        self.assertEqual(task.attempts, 2)
        task.response_processing.assert_not_called()
        self.assertEqual(balancer.task_queue.unfinished_tasks, 0)


if __name__ == "__main__":
    unittest.main()
