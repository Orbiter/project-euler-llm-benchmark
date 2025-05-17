import os
import json
import time
import queue
import base64
import urllib3
import requests
import threading
from PIL import Image
from io import BytesIO
from enum import Enum, auto
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import List, Dict, Optional

def ollama_pull(api_base='http://localhost:11434', model='llama3.2:latest') -> bool:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.request("POST", f"{api_base}/api/pull", verify=False,
                                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                                json={"model": model, "stream": False})
    response.raise_for_status()
    data = response.json()
    return not data.get("error", False)

def ollama_delete(api_base='http://localhost:11434', model='llama3.2:latest') -> bool:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.request("DELETE", f"{api_base}/api/delete", verify=False,
                                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                                json={"model": model})
    return response.status_code == 200

def ollama_list(api_base='http://localhost:11434') -> dict:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(f"{api_base}/api/tags", verify=False)
    response.raise_for_status()
    data = response.json()
    return {
        entry['model']: {
            'parameter_size': entry['details']['parameter_size'][:-1],
            'quantization_level': entry['details']['quantization_level'][1:2]
        }
        for entry in data['models']
    }

def ollama_chat_endpoints(api_base='http://localhost:11434', model_name='llama3.2:latest') -> dict:
    if isinstance(api_base, str): api_base = [api_base]
    
    # check if the endpoint servers are online and the model is available
    for api_stub in api_base:
        try:
            print(f"Loading model list from server {api_stub} to check for model {model_name}...")
            list = ollama_list(api_stub)
            if model_name not in list:
                # pull the model if it is not available
                print(f"Model {model_name} is not available on server {api_stub}. Pulling the model...")
                ollama_pull(api_stub, model_name)
                print(f"Model {model_name} is now available on server {api_stub}.")
        except Exception as e:
            # the server is not available
            # remove the server from the list
            print(f"Server {api_stub} is not available: {e}")
            api_base.remove(api_stub)

    # return the endpoint object with the model name    
    return {
        "name": model_name,
        "model": model_name,
        "key": "",
        "endpoints": [f"{api_stub}/v1/chat/completions" for api_stub in api_base],
    }

def hex2base64(hex_string) -> str:
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

def ollama_chat(
    endpoint,
    prompt: str = 'Hello World',
    base64_image: str = None,
    temperature: float = 0.0,
    max_tokens: int = 8192
) -> tuple[str, int, float]:
    """
    Function to interact with the Ollama API for chat completions.
    
    Args:
        endpoint (dict): Dictionary containing endpoint information.
        prompt (str): The prompt to send to the model.
        base64_image (str): Base64 encoded image string (optional).
        temperature (float): Temperature for randomness in response.
        max_tokens (int): Maximum number of tokens for the response.
        
    Returns:
        tuple: A tuple containing the model's response, total tokens used, and tokens per second.
    """

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Prepare the API endpoint URL
    stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>", "<|end_header_id|>", "<EOS_TOKEN>", "</s>", "<|end|>"]

    # Set headers and payload
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if endpoint.get("key", ""):
        headers['Authorization'] = 'Bearer ' + endpoint["key"]

    modelname = endpoint["model"]
    messages = []
    messages.append({"role": "system", "content": "You are a helpful assistant"})
    
    # special requirements of certain models
    if modelname.startswith("o1") or modelname.startswith("gpt-o1"): temperature = 1.0
    if modelname.startswith("qwen3"): temperature = 0.6

    if modelname.startswith("4o") or modelname.startswith("gpt-4o") or modelname.startswith("gpt-3.5"):
        # reduce number of stoptokes to 4
        stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>"]

    if base64_image:
        image_type = "jpeg"
        #base64_magic = {"/9j/": "jpeg", "iVBO": "png", "Qk": "bmp", "R0lG": "gif", "SUkq": "tiff", "SUkr": "tiff", "TU0A": "tiff", "GkXf": "webp", "UklG": "webp"}
        base64_magic = {"/9j/": "jpeg", "iVBO": "png", "R0lG": "gif"} # only jpeg and png are allowed as data type; however all of the types above (but gif!) are supported by the API
        for magic, itype in base64_magic.items():
            if base64_image.startswith(magic):
                #print(f"Detected {itype} image")
                image_type = itype
                break
        # If this is a gif we must convert it to png
        if image_type == "gif":
            #print("Converting gif to png")
            image = Image.open(BytesIO(base64.b64decode(base64_image)))
            png_image = BytesIO()
            image.save(png_image, format="PNG")
            base64_image = base64.b64encode(png_image.getvalue()).decode('utf-8')
            image_type = "png"

        # Add the image to the message
        image_url_object = {"url": f"data:image/{image_type};base64,{base64_image}"}
        usermessage = {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": image_url_object}
        ]}
    else:
        usermessage = {"role": "user", "content": prompt}
    messages.append(usermessage)

    if modelname.startswith("o1") or modelname.startswith("4o"):
        stoptokens = []

    payload = {
        "model": modelname,
        "messages": messages,
        "response_format": { "type": "text" },
        "temperature": temperature, # ollama default: 0.8
        "top_k": 20,    # reduces the probability of generating nonsense: high = more diverse, low = more focused; ollama default: 40
        "top_p": 0.95,  # works together with top_k: high = more diverse, low = more focused; ollama default: 0.9
        "min_p": 0,     # alternative to top_p: p is minimum probability for a token to be considered; ollama default: 0.0
        "stream": False
    }
    if len(stoptokens) > 0 and not modelname.startswith("o4"):
        payload["stop"] = stoptokens
    if modelname.startswith("o1") or modelname.startswith("o4"):
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

    # use the endpoints array as failover mechanism
    endpoint_url_list = endpoint["endpoints"]
    failure_exception = Exception("No endpoint available or failure without exception")
    for failover_count in range(len(endpoint_url_list)):
        try:
            #print(payload)
            t0 = time.time()
            response = requests.post(endpoint["endpoints"][failover_count], headers=headers, json=payload, verify=False)
            t1 = time.time()
            #print(response)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # print(f"Failed to access api: {e}")
            # Get the error message from the response
            if response:
                try:
                    #print(response.text)
                    data = response.json()
                    message = data.get('message', {})
                    content = message.get('content', '')
                    failure_exception = Exception(f"API request failed: {content}")
                    continue
                except json.JSONDecodeError:
                    failure_exception = Exception(f"API request failed: {e}")
                    continue

        # Parse the response
        try:
            #print(response.text)
            data = response.json()
            usage = data.get('usage', {})
            total_tokens = usage.get('total_tokens', 0)
            token_per_second = total_tokens / (t1 - t0)
            #print(f"Total tokens: {total_tokens}, tokens per second: {token_per_second:.2f}")
            choices = data.get('choices', [])
            if len(choices) == 0:
                failure_exception = Exception("No response from the API: " + str(data))
                continue
            message = choices[0].get('message', {})
            answer = message.get('content', '')
            return answer, total_tokens, token_per_second
        except json.JSONDecodeError as e:
            failure_exception = Exception(f"Failed to parse JSON response from the API: {e}")
            continue

    # If we reach here, all endpoints failed
    raise failure_exception

multimodal_cache = {}

def test_multimodal(endpoints) -> bool:
    modelname = endpoints["model"]
    cached_result = multimodal_cache.get(modelname, None)
    if cached_result is not None:
        return cached_result

    image_path = "llmtest/testimage.png"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    try:
        answer, total_tokens, token_per_second = ollama_chat(endpoints, prompt="what is in the image", base64_image=base64_image)
        result = "42" in answer
        if result:
            print(f"Model {modelname} is multimodal.")
        multimodal_cache[modelname] = result
        return result
    except Exception as e:
        return False


busy_waiting_time = 1 # seconds


class ServerStatus(Enum):
    """
    Enum for server status.
    This enum is used to track the status of each server in the load balancer.
    The status can be either AVAILABLE or BUSY.
    This is used to manage the load balancing of tasks across multiple servers.
    The load balancer will only assign tasks to servers that are AVAILABLE.
    The status of each server is updated as tasks are assigned and completed.
    The status is also used to track the current task being processed by each server.

    Args:
        Enum (_type_): _description_
    """
    AVAILABLE = auto()
    BUSY = auto()

@dataclass
class Task:
    """
    Dataclass for task.
    This dataclass is used to represent a task that needs to be processed by a server.
    Each task has an ID and a dictionary of data that contains the actual task data.
    """
    id: int               # Unique identifier for the task
    description: str      # a short description of the task (for logging)
    model_name: str       # the model storage name
    model: str            # the actual model name
    prompt: str           # the prompt to be sent to the model
    base64_image: str     # the base64 encoded image to be sent to the model
    result_file_path: str # the path to the file where the result will be saved

@dataclass
class Server:
    """
    Dataclass for server.
    This dataclass is used to represent a server that can process tasks.
    Each server has an ID, an endpoint (URL), and a status that indicates whether the server is available or busy.
    The status is used to track the current task being processed by the server.
    """
    id: int # Unique identifier for the server
    endpoint: str # The endpoint (URL) of the server
    status: ServerStatus = ServerStatus.AVAILABLE # The status of the server (available or busy)
    current_task: Task = None  # Track the current task being processed

class LoadBalancer:
    """
    LoadBalancer class for managing task distribution across multiple servers.
    This class is responsible for distributing tasks to available servers and managing their status.
    - It uses a queue to manage tasks and a list of servers to distribute the load.
    - It will only assign tasks to servers that are AVAILABLE.
    - It implements backpressure to prevent overloading the servers.
    - It will wait for a server to become available before assigning a new task.
    - It will also retry failed tasks after a short delay.
    - The status of each server is updated as tasks are assigned and completed.
    """
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
            print(f"Processing task ID {task.id} on server {server.endpoint} with model {task.model}")
            
            t0 = time.time()
            answer, total_tokens, token_per_second = ollama_chat(
                {"name": task.model_name, "model": task.model, "key": "", "endpoints": [server.endpoint]}, 
                task.prompt, 
                base64_image=task.base64_image
            )
            t1 = time.time()
            print(f"Processed {task.description}, on {server.endpoint} with model {task.model} in {t1 - t0:.2f} seconds with {total_tokens} tokens ({token_per_second:.2f} tokens/sec)")
            
            # Save the response to a file
            with open(task.result_file_path, 'w', encoding='utf-8') as result_file:
                result_file.write(answer)
            
            # Store result and mark server available
            with self.lock:
                self.results[task.id] = answer
            self.mark_server_available(server)
                
        except Exception as e:
            # write a stack trace to std out
            import traceback
            traceback.print_exc()
            # Log the error and mark server available
            error_msg = f"Failed to process task ID {task.id} on {server.endpoint}: {str(e)}"
            if hasattr(e, 'response'):
                try:
                    error_details = e.response.json()
                    error_msg += f" | API Response: {error_details}"
                except:
                    error_msg += f" | Raw Response: {e.response.text}"
            print(error_msg)
            
            # Requeue the task if there was an error
            if task.id not in self.results:  # Only retry if not already succeeded
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
                    print(f"Server {server.endpoint} - Status: {server.status.name}, Current task ID: {server.current_task.id}")

        print("All servers finished processing.")

def main():
    parser = ArgumentParser(description="Testing the ollama API.")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM, default is http://localhost:11434')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--image', required=False, default=None, help='path to an image that shall be processed')
    
    # parse the arguments
    args = parser.parse_args()
    api_base = args.api_base.split(",") if "," in args.api_base else [args.api_base]
    endpoint_name = args.endpoint
    model_name = args.model
    image_path = args.image

    # load the endpoint file
    endpoints = {}
    if endpoint_name:
        print(f"Using endpoint {endpoint_name}")
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoints = json.load(file)
    else:
        endpoints = ollama_chat_endpoints(api_base, model_name)
    
    # test if the endpoint is a multimodal model
    if test_multimodal(endpoints):
        print("Endpoint is a multimodal model.")
    else:
        print("Endpoint is not a multimodal model.")

    # load the image, if a path is given
    base64_image = None
    if image_path:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # access the ollama API
    models_dict = ollama_list(api_base[0])
    for (model, attr) in models_dict.items():
        print(f"Model: {model}: {attr}")
    try:
        if base64_image:
            answer, total_tokens, token_per_second = ollama_chat(endpoints, prompt="what is in the image", base64_image=base64_image)
        else:
            answer, total_tokens, token_per_second = ollama_chat(endpoints)
    except Exception as e:
        answer = f"Error: {str(e)}"
    print(answer)

if __name__ == "__main__":
    main()
