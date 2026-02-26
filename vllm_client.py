"""
vLLM Client - Async concurrent client for vLLM OpenAI-compatible endpoints.

This module provides an async interface for running concurrent inference requests
against vLLM servers, optimized for high-throughput benchmarking scenarios.
"""

import os
import json
import time
import base64
import asyncio
import aiohttp
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any
from argparse import ArgumentParser


@dataclass
class VLLMEndpoint:
    """Configuration for a vLLM endpoint."""
    store_name: str          # Name used for storing results
    model_name: str          # Model name as reported by vLLM
    url: str                 # Full URL to the chat completions endpoint
    api_key: str = ""        # Optional API key
    
    def __str__(self):
        return f"VLLMEndpoint({self.store_name} @ {self.url})"


@dataclass
class Task:
    """A task to be processed by the vLLM server."""
    id: str                  # Unique identifier for the task
    description: str         # Human-readable description
    prompt: str              # The prompt to send to the model
    base64_image: str = None # Optional base64 encoded image
    callback: Callable[['Response'], None] = None  # Callback for processing response


@dataclass
class Response:
    """Response from the vLLM server."""
    task: Task
    result: str              # The model's response text
    total_tokens: int        # Total tokens used (prompt + completion)
    prompt_tokens: int       # Tokens in the prompt
    completion_tokens: int   # Tokens in the completion
    elapsed_time: float      # Time taken for the request
    tokens_per_second: float # Completion tokens per second
    success: bool = True     # Whether the request succeeded
    error: str = None        # Error message if failed


async def vllm_chat(
    session: aiohttp.ClientSession,
    endpoint: VLLMEndpoint,
    prompt: str,
    base64_image: str = None,
    temperature: float = 0.0,
    max_tokens: int = 32768,
    timeout: int = 600
) -> tuple[str, int, int, int, float]:
    """
    Send a chat completion request to a vLLM server.
    
    Returns:
        tuple: (response_text, total_tokens, prompt_tokens, completion_tokens, elapsed_time)
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if endpoint.api_key:
        headers['Authorization'] = f'Bearer {endpoint.api_key}'
    
    # Build messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    if base64_image:
        # Vision request
        user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ]
        messages.append({"role": "user", "content": user_content})
    else:
        messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": endpoint.model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    t0 = time.time()
    
    async with session.post(
        endpoint.url,
        json=payload,
        headers=headers,
        timeout=aiohttp.ClientTimeout(total=timeout),
        ssl=False
    ) as response:
        response.raise_for_status()
        data = await response.json()
    
    elapsed = time.time() - t0
    
    # Parse response
    usage = data.get('usage', {})
    total_tokens = usage.get('total_tokens', 0)
    prompt_tokens = usage.get('prompt_tokens', 0)
    completion_tokens = usage.get('completion_tokens', 0)
    
    choices = data.get('choices', [])
    if not choices:
        raise Exception(f"No choices in response: {data}")
    
    answer = choices[0].get('message', {}).get('content', '')
    
    return answer, total_tokens, prompt_tokens, completion_tokens, elapsed


async def process_task(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    endpoint: VLLMEndpoint,
    task: Task,
    temperature: float = 0.0,
    max_tokens: int = 32768
) -> Response:
    """Process a single task with semaphore-controlled concurrency."""
    async with semaphore:
        try:
            answer, total_tokens, prompt_tokens, completion_tokens, elapsed = await vllm_chat(
                session=session,
                endpoint=endpoint,
                prompt=task.prompt,
                base64_image=task.base64_image,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            tps = completion_tokens / elapsed if elapsed > 0 else 0
            
            response = Response(
                task=task,
                result=answer,
                total_tokens=total_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                elapsed_time=elapsed,
                tokens_per_second=tps,
                success=True
            )
            
            print(f"✓ {task.description} | {completion_tokens} tokens | {elapsed:.1f}s | {tps:.1f} tok/s")
            
        except Exception as e:
            response = Response(
                task=task,
                result="",
                total_tokens=0,
                prompt_tokens=0,
                completion_tokens=0,
                elapsed_time=0,
                tokens_per_second=0,
                success=False,
                error=str(e)
            )
            print(f"✗ {task.description} | Error: {e}")
        
        # Execute callback if provided
        if task.callback:
            try:
                task.callback(response)
            except Exception as e:
                print(f"Callback error for {task.id}: {e}")
        
        return response


class VLLMConcurrentRunner:
    """
    Concurrent task runner for vLLM endpoints.
    
    Usage:
        runner = VLLMConcurrentRunner(endpoint, concurrency=8)
        runner.add_task(Task(...))
        runner.add_task(Task(...))
        results = await runner.run()
    """
    
    def __init__(
        self,
        endpoint: VLLMEndpoint,
        concurrency: int = 20,
        temperature: float = 0.0,
        max_tokens: int = 32768
    ):
        self.endpoint = endpoint
        self.concurrency = concurrency
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task):
        """Add a task to the queue."""
        self.tasks.append(task)
    
    def add_tasks(self, tasks: List[Task]):
        """Add multiple tasks to the queue."""
        self.tasks.extend(tasks)
    
    async def run(self) -> List[Response]:
        """Run all tasks concurrently and return responses."""
        if not self.tasks:
            print("No tasks to process.")
            return []
        
        print(f"\n{'='*60}")
        print(f"Starting {len(self.tasks)} tasks with concurrency={self.concurrency}")
        print(f"Endpoint: {self.endpoint.url}")
        print(f"Model: {self.endpoint.model_name}")
        print(f"{'='*60}\n")
        
        semaphore = asyncio.Semaphore(self.concurrency)
        
        connector = aiohttp.TCPConnector(
            limit=self.concurrency * 2,
            limit_per_host=self.concurrency * 2,
            ssl=False
        )
        
        t0 = time.time()
        
        async with aiohttp.ClientSession(connector=connector) as session:
            coros = [
                process_task(
                    session=session,
                    semaphore=semaphore,
                    endpoint=self.endpoint,
                    task=task,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                for task in self.tasks
            ]
            
            responses = await asyncio.gather(*coros, return_exceptions=True)
        
        elapsed = time.time() - t0
        
        # Handle any exceptions that slipped through
        results = []
        for i, resp in enumerate(responses):
            if isinstance(resp, Exception):
                results.append(Response(
                    task=self.tasks[i],
                    result="",
                    total_tokens=0,
                    prompt_tokens=0,
                    completion_tokens=0,
                    elapsed_time=0,
                    tokens_per_second=0,
                    success=False,
                    error=str(resp)
                ))
            else:
                results.append(resp)
        
        # Summary
        successful = sum(1 for r in results if r.success)
        total_completion_tokens = sum(r.completion_tokens for r in results)
        total_prompt_tokens = sum(r.prompt_tokens for r in results)
        
        print(f"\n{'='*60}")
        print(f"Completed: {successful}/{len(results)} tasks in {elapsed:.1f}s")
        print(f"Total tokens: {total_prompt_tokens + total_completion_tokens:,} (prompt: {total_prompt_tokens:,}, completion: {total_completion_tokens:,})")
        print(f"Throughput: {total_completion_tokens/elapsed:.1f} completion tokens/s")
        print(f"{'='*60}\n")
        
        return results


async def get_vllm_models(base_url: str, api_key: str = "") -> List[str]:
    """Fetch available models from a vLLM server."""
    url = base_url.rstrip('/') + '/v1/models'
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            response.raise_for_status()
            data = await response.json()
            return [m['id'] for m in data.get('data', [])]


def get_vllm_models_sync(base_url: str, api_key: str = "") -> List[str]:
    """Synchronous wrapper for get_vllm_models."""
    return asyncio.run(get_vllm_models(base_url, api_key))


async def main_async():
    """Test the vLLM client with a simple prompt."""
    parser = ArgumentParser(description="Test vLLM client")
    parser.add_argument('--url', default='http://localhost:1236', help='vLLM server base URL')
    parser.add_argument('--model', default=None, help='Model name (auto-detected if not specified)')
    parser.add_argument('--concurrency', type=int, default=20, help='Number of concurrent requests')
    parser.add_argument('--num_tasks', type=int, default=10, help='Number of test tasks to run')
    
    args = parser.parse_args()
    
    base_url = args.url.rstrip('/')
    chat_url = f"{base_url}/v1/chat/completions"
    
    # Auto-detect model if not specified
    model_name = args.model
    if not model_name:
        print(f"Fetching models from {base_url}...")
        models = await get_vllm_models(base_url)
        if not models:
            print("No models found!")
            return
        model_name = models[0]
        print(f"Using model: {model_name}")
    
    endpoint = VLLMEndpoint(
        store_name=model_name,
        model_name=model_name,
        url=chat_url
    )
    
    # Create test tasks
    runner = VLLMConcurrentRunner(
        endpoint=endpoint,
        concurrency=args.concurrency,
        max_tokens=256  # Short responses for testing
    )
    
    for i in range(args.num_tasks):
        runner.add_task(Task(
            id=f"test_{i:03d}",
            description=f"Test task {i}",
            prompt=f"In exactly one sentence, what is {i} + {i*2}?"
        ))
    
    results = await runner.run()
    
    # Print sample results
    print("\nSample responses:")
    for r in results[:3]:
        print(f"  [{r.task.id}] {r.result[:100]}...")


def main():
    """Entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
