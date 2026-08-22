import unittest
import json
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from inference import build_endpoints
from llm_client import (
    Endpoint,
    _post_with_rate_limit_retry,
    ensure_model_available,
    get_openai_models_url,
    load_endpoint_file,
)


class EndpointHandlingTests(unittest.TestCase):
    def test_minimal_endpoint_file_uses_command_line_names(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "minimal.json"
            path.write_text(
                json.dumps({
                    "key": "super-secret-api-key",
                    "url": "https://example.com/v1/chat/completions",
                }),
                encoding="utf-8",
            )

            endpoint = load_endpoint_file(
                str(path),
                store_name="benchmark-name",
                model_name="provider/model",
            )

        self.assertEqual(endpoint.store_name, "benchmark-name")
        self.assertEqual(endpoint.model_name, "provider/model")
        self.assertIsNone(endpoint._context_size)
        self.assertIsNone(endpoint._publication_date)
        self.assertIsNone(endpoint._quantization_level)

    def test_minimal_endpoint_file_requires_both_names(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "minimal.json"
            path.write_text(
                json.dumps({
                    "key": "",
                    "url": "http://localhost:11434/v1/chat/completions",
                }),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "--store_name and --model_name"
            ):
                load_endpoint_file(str(path))

    @patch("llm_client.time.sleep")
    @patch("llm_client.requests.post")
    def test_429_waits_ten_seconds_and_retries(self, post, sleep):
        rate_limited = unittest.mock.Mock(status_code=429)
        successful = unittest.mock.Mock(status_code=200)
        post.side_effect = [rate_limited, successful]
        endpoint = Endpoint(
            store_name="remote",
            model_name="provider/model",
            key="super-secret-api-key",
            url="https://example.com/v1/chat/completions",
        )

        response = _post_with_rate_limit_retry(endpoint, stream=True)

        self.assertIs(response, successful)
        self.assertEqual(post.call_count, 2)
        sleep.assert_called_once_with(10)
        rate_limited.close.assert_called_once_with()

    def test_endpoint_repr_and_logs_redact_api_key(self):
        endpoint = Endpoint(
            store_name="remote",
            model_name="provider/model",
            key="super-secret-api-key",
            url="https://example.com/v1/chat/completions",
        )

        output = StringIO()
        with (
            patch("llm_client.openai_api_list", return_value={}),
            patch("llm_client.ollama_pull"),
            patch("llm_client.time.sleep"),
            redirect_stdout(output),
        ):
            print(f"Processing endpoint: {endpoint}")
            ensure_model_available(endpoint, attempts=1)

        logged = output.getvalue()
        self.assertNotIn("super-secret-api-key", repr(endpoint))
        self.assertNotIn("super-secret-api-key", logged)
        self.assertNotIn("key=", repr(endpoint))

    def test_models_url_preserves_provider_api_prefix(self):
        endpoint = Endpoint(
            store_name="remote",
            model_name="provider/model",
            key="secret",
            url="https://openrouter.ai/api/v1/chat/completions",
        )

        self.assertEqual(
            get_openai_models_url(endpoint),
            "https://openrouter.ai/api/v1/models",
        )

    @patch("llm_client.time.sleep")
    @patch("llm_client.openai_api_list", return_value={})
    @patch("llm_client.ollama_pull")
    def test_missing_model_is_always_pulled(self, pull, _list, _sleep):
        endpoint = Endpoint(
            store_name="remote",
            model_name="provider/model",
            key="secret",
            url="https://example.com/v1/chat/completions",
        )

        with self.assertRaises(RuntimeError):
            ensure_model_available(endpoint, attempts=3, fail_if_unavailable=True)
        self.assertEqual(pull.call_count, 3)

    @patch("llm_client.time.sleep")
    @patch("llm_client.openai_api_list", return_value={})
    @patch("llm_client.ollama_pull")
    def test_missing_ollama_model_still_fails_preflight(
        self, pull, _list, _sleep
    ):
        endpoint = Endpoint(
            store_name="local",
            model_name="missing",
            key="",
            url="http://localhost:11434/v1/chat/completions",
        )

        with self.assertRaises(RuntimeError):
            ensure_model_available(endpoint, attempts=2, fail_if_unavailable=True)
        self.assertEqual(pull.call_count, 2)

    def test_endpoint_file_controls_store_name(self):
        endpoint = build_endpoints(
            ["http://localhost:11434"],
            "inclusionai-ling-3.0-flash",
            "llama3.2:latest-no_think",
            "llama3.2:latest",
        )[0]

        self.assertEqual(endpoint.store_name, "ling-3.0-flash-no_think")
        self.assertEqual(endpoint.model_name, "inclusionai/ling-3.0-flash:free")


if __name__ == "__main__":
    unittest.main()
