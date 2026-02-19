"""
Inference script for vLLM endpoints with concurrent request support.

This script processes Project Euler problems using a vLLM server with
configurable concurrency for high-throughput benchmarking.

Usage:
    python3 inference_vllm.py --url http://localhost:1236 --model "openai/gpt-oss-120b" --language python --concurrency 20
"""

import os
import json
import base64
import asyncio
from argparse import ArgumentParser
from vllm_client import VLLMEndpoint, VLLMConcurrentRunner, Task, Response, get_vllm_models_sync
from benchmark import read_benchmark, write_benchmark


def read_template(template_path: str) -> str:
    """Read a prompt template file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_expected_solutions() -> dict:
    """Load expected solutions from solutions.json."""
    with open('solutions.json', 'r', encoding='utf-8') as f:
        return json.load(f)


async def run_inference(
    endpoint: VLLMEndpoint,
    language: str,
    problems_dir: str,
    template_content: str,
    max_problem_number: int = 200,
    concurrency: int = 20,
    overwrite_existing: bool = False,
    overwrite_failed: bool = False,
    expected_solutions: dict = None,
    think: bool = False,
    no_think: bool = False
):
    """Run inference on all problems using vLLM with concurrency."""
    
    store_name = endpoint.store_name
    if think:
        store_name += "-think"
    if no_think:
        store_name += "-no_think"
    
    solutions_dir = os.path.join('solutions', store_name, language)
    os.makedirs(solutions_dir, exist_ok=True)
    
    print(f"\nProcessing problems for {store_name} in {language}")
    print(f"Solutions will be saved to: {solutions_dir}")
    
    # Collect tasks
    tasks = []
    
    for problem_file in sorted(os.listdir(problems_dir)):
        if problem_file.startswith('.') or not problem_file.endswith('.txt'):
            continue
        
        problem_number = problem_file[:-4]  # Remove .txt
        if int(problem_number) > max_problem_number:
            break
        
        result_file_path = os.path.join(solutions_dir, f"{problem_number}.md")
        
        # Skip if already exists (unless overwrite flags set)
        if os.path.exists(result_file_path):
            if overwrite_existing:
                pass # Proceed to overwrite
            elif overwrite_failed:
                # Check if the existing file looks like a failure
                with open(result_file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if len(content) < 10 or "Error" in content:
                    pass # Proceed to retry failure
                else:
                    print(f"Skipping problem {problem_number} - already has successful solution")
                    continue
            else:
                print(f"Skipping problem {problem_number} - already has solution")
                continue
        
        # Read problem content
        problem_path = os.path.join(problems_dir, problem_file)
        with open(problem_path, 'r', encoding='utf-8') as f:
            problem_content = f.read()
        
        # Check for associated image
        base64_image = None
        for ext in ["-0.png", "-0.jpg", "-0.gif"]:
            image_path = os.path.join(problems_dir, problem_number + ext)
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                break
        
        # Build prompt
        prompt = template_content.replace('$$$PROBLEM$$$', problem_content)
        if think:
            prompt += " /think"
        if no_think:
            prompt += " /no_think"
        
        # Create callback to save result
        def make_save_callback(file_path):
            def save_response(response: Response):
                if response.success:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(response.result)
            return save_response
        
        task = Task(
            id=problem_number,
            description=f"Problem {problem_number} ({language})",
            prompt=prompt,
            base64_image=base64_image,
            callback=make_save_callback(result_file_path)
        )
        tasks.append(task)
    
    if not tasks:
        print("No problems to process!")
        return
    
    print(f"\nQueued {len(tasks)} problems for processing")
    
    # Run with concurrency
    runner = VLLMConcurrentRunner(
        endpoint=endpoint,
        concurrency=concurrency,
        temperature=0.0,
        max_tokens=32768
    )
    runner.add_tasks(tasks)
    
    results = await runner.run()
    
    # Summary
    successful = sum(1 for r in results if r.success)
    print(f"\nInference complete: {successful}/{len(results)} problems solved")
    
    return results


def main():
    parser = ArgumentParser(description="Run Project Euler inference with vLLM concurrency")
    parser.add_argument('--url', required=True, help='vLLM server base URL (e.g., http://localhost:1236)')
    parser.add_argument('--model', default=None, help='Model name (auto-detected if not specified)')
    parser.add_argument('--store_name', default=None, help='Name to use for storing results (defaults to model name)')
    parser.add_argument('--language', default='python,java,rust,clojure', help='Programming language(s), comma-separated (default: python,java,rust,clojure)')
    parser.add_argument('--concurrency', type=int, default=20, help='Number of concurrent requests (default: 20)')
    parser.add_argument('--overwrite_existing', action='store_true', help='Overwrite existing solutions')
    parser.add_argument('--overwrite_failed', action='store_true', help='Overwrite failed solutions')
    parser.add_argument('--think', action='store_true', help='Append /think to prompts')
    parser.add_argument('--no_think', action='store_true', help='Append /no_think to prompts')
    parser.add_argument('--n100', action='store_true', help='Process first 100 problems')
    parser.add_argument('--n200', action='store_true', help='Process first 200 problems (default)')
    parser.add_argument('--n400', action='store_true', help='Process first 400 problems')
    parser.add_argument('--nall', action='store_true', help='Process all problems')
    
    args = parser.parse_args()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    # Determine max problems
    max_problem_number = 200
    if args.n100:
        max_problem_number = 100
    elif args.n400:
        max_problem_number = 400
    elif args.nall:
        max_problem_number = 9999
    
    # Build URL
    base_url = args.url.rstrip('/')
    chat_url = f"{base_url}/v1/chat/completions"
    
    # Auto-detect model if not specified
    model_name = args.model
    if not model_name:
        print(f"Fetching models from {base_url}...")
        models = get_vllm_models_sync(base_url)
        if not models:
            print("ERROR: No models found on server!")
            return
        model_name = models[0]
        print(f"Auto-detected model: {model_name}")
    
    store_name = args.store_name or model_name
    
    # Create endpoint
    endpoint = VLLMEndpoint(
        store_name=store_name,
        model_name=model_name,
        url=chat_url
    )
    
    # Load expected solutions
    expected_solutions = load_expected_solutions()
    
    # Process each language
    languages = [lang.strip() for lang in args.language.split(',')]
    
    for language in languages:
        problems_dir = 'problems'
        template_path = os.path.join('templates', f'template_{language}.md')
        
        if not os.path.exists(problems_dir):
            raise Exception(f"Problems directory not found: {problems_dir}")
        
        if not os.path.exists(template_path):
            print(f"WARNING: Template not found for {language}: {template_path}")
            continue
        
        template_content = read_template(template_path)
        
        asyncio.run(run_inference(
            endpoint=endpoint,
            language=language,
            problems_dir=problems_dir,
            template_content=template_content,
            max_problem_number=max_problem_number,
            concurrency=args.concurrency,
            overwrite_existing=args.overwrite_existing,
            overwrite_failed=args.overwrite_failed,
            expected_solutions=expected_solutions,
            think=args.think,
            no_think=args.no_think
        ))
    
    print("\n" + "="*60)
    print("Inference complete!")
    print("Next steps:")
    print(f"  python3 codeextraction.py --model {store_name} --language {args.language}")
    print(f"  python3 execute.py --model {store_name} --language {args.language}")
    print("="*60)


if __name__ == "__main__":
    main()
