import os
import json
import time
import base64
import threading
from typing import List
from argparse import ArgumentParser
from llm_model_test import complete_model_capabilities, has_complete_model_capabilities
from benchmark import read_benchmark, write_benchmark
from llm_client import openai_api_list, ensure_model_available, Endpoint, LoadBalancer, Server, Task, Response

def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def resolve_store_name(base_name: str, think: bool = False, no_think: bool = False) -> str:
    store_name = base_name
    if think:
        store_name += "-think"
    if no_think:
        store_name += "-no_think"
    return store_name

def process_problem_files(problems_dir, template_content, endpoints: List[Endpoint], language, max_problem_number=9999,
                          overwrite_existing=False, overwrite_failed=False, expected_solutions={},
                          think=False, no_think=False):
    print(f"Processing problems in {problems_dir} with language {language} and endpoint: {endpoints[0]}")
    store_name = endpoints[0].store_name
    solutions_dir = os.path.join('solutions', store_name, language)
    os.makedirs(solutions_dir, exist_ok=True)

    # Create load balancer with all available endpoints
    lb = LoadBalancer()
    lb.start_distribution()
    
    # ensure that the first endpoint is loaded, but fail loudly instead of
    # waiting forever when endpoint discovery is broken or the model is wrong.
    ensure_model_available(endpoints[0], attempts=3, fail_if_unavailable=True)

    # load server concurrently; they will download a model if that is not present so far.
    def load_endpoints():
        for endpoint in endpoints:
            try:
                loaded = ensure_model_available(endpoint, attempts=3, fail_if_unavailable=False)
            except Exception as e:
                print(f"Error loading endpoint {endpoint}: {e}")
                loaded = False
            if loaded:
                lb.add_server(Server(endpoint=endpoint))
            else:
                print(f"Failed to load endpoint {endpoint} after 3 attempts.")
    loading_thread = threading.Thread(target=load_endpoints, daemon=True)
    loading_thread.start()

    # determine model capabilities; cache them in benchmark.json
    benchmark = read_benchmark()
    entry = benchmark.get(store_name, {})
    is_vision = bool(entry.get('has_vision', False)) # we calculated the capabilities before, right after the start

    # iterate over all problem files and process them
    for problem_file in sorted(os.listdir(problems_dir)):
        if problem_file.startswith('.') or not problem_file.endswith('.txt'): continue
        problem_number = problem_file[:-4]  # Remove .txt extension
        if int(problem_number) > max_problem_number: break
        problem_path = os.path.join(problems_dir, problem_file)
        result_file_path = os.path.join(solutions_dir, f"{problem_number}.md")
        
        if not overwrite_existing and not overwrite_failed and os.path.exists(result_file_path):
            print(f"Skipping problem {problem_number} as it already has a solution.")
            continue
        
        # read problem content
        with open(problem_path, 'r', encoding='utf-8') as file:
            problem_content = file.read()

        # check for associated image
        base64_image = None
        possible_extensions = ["-0.png", "-0.jpg", "-0.gif"]
        for ext in possible_extensions:
            image_path = os.path.join(problems_dir, problem_number + ext)
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                break
        
        # check if the endpoint is vision-capable if we have an image
        if base64_image:
            if is_vision:
                print(f"Problem {problem_number} is handled with a vision-capable model.")
            else:
                print(f"Problem {problem_number} requires a vision-capable model for image processing but the model lacks vision support.")
                base64_image = None

        # Construct the prompt using the template
        prompt = template_content.replace('$$$PROBLEM$$$', problem_content)

        def save_solution(resonse: Response):
            # Save the solution to a file
            process_result_file_path = os.path.join(solutions_dir, f"{resonse.task.id}.md")
            with open(process_result_file_path, 'w', encoding='utf-8') as file:
                file.write(resonse.result)
            telemetry_result_file_path = os.path.join(solutions_dir, f"{resonse.task.id}.json")
            telemetry = {
                "duration_seconds": resonse.duration_seconds,
                "prompt_tokens": resonse.prompt_tokens,
                "completion_tokens": resonse.completion_tokens,
                "reasoning_tokens": resonse.reasoning_tokens,
            }
            with open(telemetry_result_file_path, 'w', encoding='utf-8') as file:
                json.dump(telemetry, file, indent=4)

        # Create task and add to load balancer
        task = Task(
            id = problem_number,
            description = f"problem {problem_number}, language {language}, model {store_name}",
            prompt = prompt,
            base64_image = base64_image,
            response_processing = save_solution,
            think = think,
            no_think = no_think,
        )    
        while not lb.add_task(task):
            print(f"Waiting to add task {problem_number} - queue full")
            time.sleep(1)
        print(f"Added problem {problem_number}, language {language}, model {store_name} to processing queue")

    # Wait for all tasks to complete
    print("Waiting for all problems to be processed...")
    lb.wait_completion()
    print("All problems processed!")


def build_endpoints(api_base: List[str], endpoint_name: str, store_name: str, model_name: str) -> List[Endpoint]:
    if endpoint_name:
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoint_dict = json.load(file)
            return [
                Endpoint(
                    store_name=store_name,
                    model_name=endpoint_dict["model"],
                    key=endpoint_dict["key"],
                    url=endpoint_dict["endpoint"],
                )
            ]

    return [
        Endpoint(store_name=store_name, model_name=model_name, key="",
                    url=f"{api_stub}/v1/chat/completions") for api_stub in api_base
    ]
    
def main():
    parser = ArgumentParser(description="Process Euler problems and send them to an LLM.")
    parser.add_argument('--api', action='append', help="Specify (multiple) backend OpenAI API endpoints (i.e. ollama); can be used multiple times")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM or a list of such urls (comma-separated), default is http://localhost:11434')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--allmodels', action='store_true', help='loop over all models provided by ollama and run those which are missing in benchmark.json')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--think', action='store_true', help='enable thinking mode via backend request parameters (when supported)')
    parser.add_argument('--no_think', action='store_true', help='disable thinking mode via backend request parameters (when supported)')
    parser.add_argument('--language', required=False, default='python,java,rust,clojure', help='Name of the languages to test, default is python,java,rust,clojure')
    parser.add_argument('--overwrite_existing', action='store_true', help='if set, re-calculate all problems that already have an answer')
    parser.add_argument('--overwrite_failed', action='store_true', help='if set, re-calculate those problems with wrong answers')
    parser.add_argument('--only_capabilities', action='store_true', help='if set, only the model capabilities (thinking, vision, tools, forms) are tested')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()
    
    api_base = args.api if args.api else args.api_base.split(",") if "," in args.api_base else [args.api_base]
    model_name = args.model
    language = args.language
    endpoint_name = args.endpoint
    store_name = resolve_store_name(model_name, think=args.think, no_think=args.no_think)
    max_problem_number = 200
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999

    endpoints = build_endpoints(api_base, endpoint_name, store_name, model_name)
    # determine model capabilities; cache them in benchmark.json
    benchmark = read_benchmark()
    entry = benchmark.get(store_name, {})
    if has_complete_model_capabilities(entry):
        print(f"Model capabilities already computed")
    else:
        ensure_model_available(endpoints[0], attempts=3, fail_if_unavailable=False)
        entry, entry_changed = complete_model_capabilities(entry, endpoints[0], think = args.think, no_think = args.no_think)
        if entry_changed:
            benchmark[store_name] = entry
            write_benchmark(benchmark)
    
    if args.only_capabilities:
        return # finish, we only tested the capabilities

    # cd to the local path to this script
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # load the expected solutions from the solutions.json file; needed for option --overwrite_failed
    expected_solutions = {}
    with open('solutions.json', 'r', encoding='utf-8') as json_file:
        expected_solutions = json.load(json_file)
        
    # iterate over all languages
    languages = args.language.split(',')
    for language in languages:
        bench_name = f"{language}-{max_problem_number}"
        
        problems_dir = 'problems'
        template_path = os.path.join('templates', 'template_' + language + '.md')

        if not os.path.exists(problems_dir):
            raise Exception(f"Problems directory {problems_dir} does not exist. You must create it using the problems_scraper.py script.")

        if not os.path.exists(template_path):
            raise Exception(f"Template file {template_path} does not exist.")

        template_content = read_template(template_path)

        if args.allmodels:
            if endpoint_name:
                raise Exception("The --allmodels option cannot be used in combination with --endpoint.")
            
            # loop over all models provided by ollama and run those which are missing in benchmark.json
            local_endpoint = Endpoint(store_name=store_name, model_name=model_name, key="", url=f"{api_base[0]}/v1/chat/completions")
            models = openai_api_list(local_endpoint)
            print(f"Found {len(models)} models in ollama.")
            for model in models:
                # in every loop we load the benchmark.json again because it might have been updated
                benchmark = read_benchmark()
                model_store_name = resolve_store_name(model, think=args.think, no_think=args.no_think)
                entry = benchmark.get(model_store_name, {})

                # add metadata to benchmark.json
                if model_store_name not in benchmark or bench_name not in benchmark[model_store_name]:
                    print(f"Inference: Using model {model} and language {language}")
                    endpoints = [
                        Endpoint(store_name=model_store_name, model_name=model, key="",
                                url=f"{api_stub}/v1/chat/completions") for api_stub in api_base
                    ]
                    process_problem_files(problems_dir, template_content, endpoints, language, max_problem_number = max_problem_number,
                                          overwrite_existing = args.overwrite_existing, overwrite_failed = args.overwrite_failed, expected_solutions = expected_solutions,
                                          think = args.think, no_think = args.no_think)
        else:
            # construct the endpoint object
            if endpoint_name:
                print(f"Inference: Using endpoint {endpoint_name} and language {language}")
            else:
                print(f"Inference: Using model {store_name} and language {language}")
            endpoints = build_endpoints(api_base, endpoint_name, store_name, model_name)
            
            # run the inference
            process_problem_files(problems_dir, template_content, endpoints, language, max_problem_number = max_problem_number,
                                  overwrite_existing = args.overwrite_existing, overwrite_failed = args.overwrite_failed, expected_solutions = expected_solutions,
                                  think = args.think, no_think = args.no_think)

if __name__ == "__main__":
    main()
