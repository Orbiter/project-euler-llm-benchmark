import os
import json
import time
import queue
import base64
import threading
from enum import Enum, auto
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import List, Dict, Optional
from benchmark import read_benchmark
from ollama_client import ollama_list, ollama_chat_endpoints, ollama_chat, test_multimodal

busy_waiting_time = 5 # seconds

class ServerStatus(Enum):
    AVAILABLE = auto()
    BUSY = auto()

@dataclass
class Task:
    id: int
    data: dict  # The actual task data to be processed

@dataclass
class Server:
    id: int
    endpoint: str
    status: ServerStatus = ServerStatus.AVAILABLE
    current_task: Task = None  # Track the current task being processed

class LoadBalancer:
    def __init__(self, servers: List[Server], max_queue_size: int = 1000):
        self.servers = servers
        self.task_queue = queue.Queue(maxsize=max_queue_size)
        self.available_servers = queue.Queue(maxsize=len(servers))
        self.lock = threading.Lock()
        self.results = {}
        
        # Initialize available servers queue
        for server in servers:
            self.available_servers.put(server)
        
    def add_task(self, task: Task):
        """Add a task to the processing queue with backpressure"""
        try:
            self.task_queue.put(task, block=True, timeout=1)
            return True
        except queue.Full:
            print("Task queue full - applying backpressure")
            return False
    
    def mark_server_available(self, server: Server):
        """Mark a server as available for new tasks"""
        with self.lock:
            server.status = ServerStatus.AVAILABLE
            server.current_task = None
            self.available_servers.put(server)
    
    def get_available_server(self, timeout: float = 10.0) -> Optional[Server]:
        """Get the next available server with timeout"""
        try:
            return self.available_servers.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def assign_task_to_server(self, task: Task, server: Server):
        """Assign task to server and mark it as busy"""
        with self.lock:
            server.status = ServerStatus.BUSY
            server.current_task = task
        
        threading.Thread(
            target=self.process_task_remote,
            args=(server,),
            daemon=True
        ).start()
    
    def process_task_remote(self, server: Server):
        """Process task on remote server"""
        task = server.current_task
        try:
            # Construct the prompt using the template
            prompt = task.data["template_content"].replace('$$$PROBLEM$$$', task.data["problem_content"])

            # attach soft thinking switches if asked
            if task.data["think"]: 
                prompt += " /think"
            if task.data["no_think"]: 
                prompt += " /no_think"
            
            # Create complete endpoint object that ollama_chat expects
            endpoint = {
                "name": task.data["model_name"],
                "model": task.data["model"],
                "key": "",
                "endpoints": [server.endpoint]  # Note: This must be a list
            }
            
            print(f"Processing problem {task.data["problem_number"]}, language {task.data["language"]} on {server.endpoint} with model {task.data['model']}")
            t0 = time.time()
            answer, total_tokens, token_per_second = ollama_chat(
                endpoint, 
                prompt, 
                base64_image=task.data["base64_image"]
            )
            t1 = time.time()
            print(f"Processed problem  {task.data["problem_number"]}, language {task.data["language"]} on {server.endpoint} with model {task.data['model']} in {t1 - t0:.2f} seconds with {total_tokens} tokens ({token_per_second:.2f} tokens/sec)")
            
            # Save the response to a file
            with open(task.data["result_file_path"], 'w', encoding='utf-8') as result_file:
                result_file.write(answer)
            
            # Store result and mark server available
            with self.lock:
                self.results[task.data["problem_number"]] = answer
            self.mark_server_available(server)
                
        except Exception as e:
            # write a stack trace to std out
            import traceback
            traceback.print_exc()
            # Log the error and mark server available
            error_msg = f"Failed to process problem {task.data["problem_number"]} on {server.endpoint}: {str(e)}"
            if hasattr(e, 'response'):
                try:
                    error_details = e.response.json()
                    error_msg += f" | API Response: {error_details}"
                except:
                    error_msg += f" | Raw Response: {e.response.text}"
            print(error_msg)
            
            # Requeue the task if there was an error
            if task.data["problem_number"] not in self.results:  # Only retry if not already succeeded
                self.add_task(task)
            self.mark_server_available(server)
    
    def start_distribution(self):
        """Start the task distribution process"""
        def distributor():
            while True:
                task = self.task_queue.get()
                assigned = False
                
                while not assigned:
                    server = self.get_available_server()
                    if server:
                        self.assign_task_to_server(task, server)
                        assigned = True
                    else:
                        # All servers busy, wait and try again
                        time.sleep(busy_waiting_time)
                
                self.task_queue.task_done()
        
        # Start distributor thread
        threading.Thread(target=distributor, daemon=True).start()
    
    def wait_completion(self):
        """Wait for all tasks to be processed"""
        self.task_queue.join()
        # Wait for all servers to finish their current tasks
        print("Waiting for all servers to finish processing...")
        while any(s.current_task != None for s in self.servers):
            time.sleep(busy_waiting_time)
            print("Still waiting for servers to finish...")
            # print out the current status of all servers
            for server in self.servers:
                if server.current_task:
                    print(f"Server {server.endpoint} - Status: {server.status.name}, Current Problem: {server.current_task.data["problem_number"]}")

        print("All servers finished processing.")

def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_problem_files(problems_dir, template_content, endpoints, language, max_problem_number=9999,
                          overwrite_existing=False, overwrite_failed=False, expected_solutions={},
                          think=False, no_think=False):
    model_name = endpoints["name"]
    if think: model_name += "-think"
    if no_think: model_name += "-no_think"
    results_dir = os.path.join('solutions', model_name, language)
    os.makedirs(results_dir, exist_ok=True)

    # get the solutions as computed so far (may be none at first run)
    solutions_json_path = os.path.join(results_dir, 'solutions.json') # may not exist yet
    solutions = {}
    if os.path.exists(solutions_json_path):
        with open(solutions_json_path, 'r', encoding='utf-8') as json_file:
            solutions = json.load(json_file)

    # Create load balancer with all available endpoints
    server_urls = endpoints["endpoints"]
    servers = [Server(id=i, endpoint=url) for i, url in enumerate(server_urls)]
    
    lb = LoadBalancer(servers)
    lb.start_distribution()

    # iterate over all problem files
    for problem_file in sorted(os.listdir(problems_dir)):
        if problem_file.startswith('.') or not problem_file.endswith('.txt'): continue
        problem_number = problem_file[:-4]  # Remove .txt extension
        if int(problem_number) > max_problem_number: break
        problem_path = os.path.join(problems_dir, problem_file)
        result_file_path = os.path.join(results_dir, f"{problem_number}.md")
        
        if not overwrite_existing and not overwrite_failed and os.path.exists(result_file_path):
            print(f"Skipping problem {problem_number} as it already has a solution.")
            continue

        # check if the problem is already solved
        actual_solution = expected_solutions.get(problem_number, {}).get('solution', None)
        problem_is_solved = problem_number in solutions and solutions[problem_number] == actual_solution
        
        if overwrite_failed and problem_is_solved:
            print(f"Skipping problem {problem_number} as it is already solved and overwrite_failed is set.")
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
        
        # check if the endpoint is multimodal if we have an image
        if base64_image:
            is_multimodal = test_multimodal(endpoints) # this is cached
            if is_multimodal:
                print(f"Problem {problem_number} is handled with multimodal model.")
            else:
                print(f"Problem {problem_number} requires a multimodal model for image processing but the model is not multimodal.")
                base64_image = None
        
        # Create task and add to load balancer
        task = Task(
            id=int(problem_number),
            data={
                "model_name": model_name, # the model storage name
                "model": endpoints.get("name", model_name),  # the actual model name
                "language": language,
                "problem_number": problem_number,
                "problem_content": problem_content,
                "template_content": template_content,
                "result_file_path": result_file_path,
                "base64_image": base64_image,
                "think": think,
                "no_think": no_think
            }
        )    
        while not lb.add_task(task):
            print(f"Waiting to add task {problem_number} - queue full")
            time.sleep(busy_waiting_time)
        print(f"Added problem {problem_number}, language {language}, model {model_name} to processing queue")

    # Wait for all tasks to complete
    print("Waiting for all problems to be processed...")
    lb.wait_completion()
    print("All problems processed!")

    # Save solutions to JSON
    with open(solutions_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(lb.results, json_file, indent=2)

def main():
    parser = ArgumentParser(description="Process Euler problems and send them to an LLM.")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM, default is http://localhost:11434')
    parser.add_argument('--allmodels', action='store_true', help='loop over all models provided by ollama and run those which are missing in benchmark.json')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--think', action='store_true', help='if set, the prompt will get an additional "/think" appended at the end')
    parser.add_argument('--no_think', action='store_true', help='if set, the prompt will get an additional "/no_think" appended at the end')
    parser.add_argument('--language', required=False, default='python,java,rust,clojure', help='Name of the languages to test, default is python,java,rust,clojure')
    parser.add_argument('--overwrite_existing', action='store_true', help='if set, re-calculate all problems that already have an answer')
    parser.add_argument('--overwrite_failed', action='store_true', help='if set, re-calculate those problems with wrong answers')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()

    api_base = args.api_base.split(",") if "," in args.api_base else [args.api_base]
    model_name = args.model
    language = args.language
    max_problem_number = 100
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999

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
        endpoint_name = args.endpoint
        
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
            models = ollama_list()
            print(f"Found {len(models)} models in ollama.")
            for model in models:
                # in every loop we load the benchmark.json again because it might have been updated
                benchmark = read_benchmark()
                entry = benchmark.get(model, {})

                # add metadata to benchmark.json
                if not model in benchmark or not bench_name in benchmark[model]:
                    print(f"Inference: Using model {model} and language {language}")
                    endpoints = ollama_chat_endpoints(api_base, model)
                    process_problem_files(problems_dir, template_content, endpoints, language, max_problem_number = max_problem_number,
                                          overwrite_existing = args.overwrite_existing, overwrite_failed = args.overwrite_failed, expected_solutions = expected_solutions,
                                          think = args.think, no_think = args.no_think)
        else:
            # construct the endpoint object
            endpoint = {}
            if endpoint_name:
                print(f"Inference: Using endpoint {endpoint_name} and language {language}")
                endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
                print(f"Using endpoint file {endpoint_path}")
                if not os.path.exists(endpoint_path):
                    raise Exception(f"Endpoint file {endpoint_path} does not exist.")
                with open(endpoint_path, 'r', encoding='utf-8') as file:
                    endpoint = json.load(file)
            else:
                print(f"Inference: Using model {model_name} and language {language}")
                # construct the endpoint object from command line arguments considering that ollama is the endpoint
                endpoints = ollama_chat_endpoints(api_base, model_name)
            
            # run the inference
            process_problem_files(problems_dir, template_content, endpoints, language, max_problem_number = max_problem_number,
                                  overwrite_existing = args.overwrite_existing, overwrite_failed = args.overwrite_failed, expected_solutions = expected_solutions,
                                  think = args.think, no_think = args.no_think)

if __name__ == "__main__":
    main()