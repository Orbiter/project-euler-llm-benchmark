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
from urllib.parse import urlparse
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import Callable, List, Optional

@dataclass
class Endpoint:
    store_name: str                             # Name of the endpoint, used to store the model in the solutions
    model_name: str                             # Model name that is used in the api request
    key: str                                    # API key (if required)
    url: str                                    # URL of the endpoint
    _context_size: Optional[float] = None       # kilo-number of tokens
    _publication_date: Optional[str] = None     # ISO-short date, like 2025-09-19
    _quantization_level: Optional[int] = None   # number of bits per weight
    
    def get_dict(self) -> dict:
        return {
            "store_name": self.store_name,
            "model_name": self.model_name,
            "key": self.key,
            "url": self.url,
            "_context_size": self._context_size,
            "_publication_date": self._publication_date,
            "_quantization_level": self._quantization_level
        }

def get_ollama_url_stub(endpoint: Endpoint) -> str:
    """Get the base URL for the ollama API"""
    return urllib3.util.url.parse_url(endpoint.url)._replace(path='').url

def ollama_delete(endpoint: dict) -> bool:
    api_base = get_ollama_url_stub(endpoint)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.request("DELETE", f"{api_base}/api/delete", verify=False,
                                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                                json={"model": endpoint.model_name})
    return response.status_code == 200

def ollama_list(endpoint) -> dict:
    """
    Try to read models from an Ollama-compatible endpoint (/api/tags).
    If that fails (e.g., it's actually an OpenAI-compatible server),
    fall back to /v1/models and map IDs to 'unknown' details.
    """
    # Build base URL (e.g. http://host:port)
    api_base = get_ollama_url_stub(endpoint)

    # We intentionally allow self-signed dev servers
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # ---- Attempt 1: Ollama /api/tags ----
    try:
        resp = requests.get(f"{api_base}/api/tags", verify=False, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            entry["model"]: {
                "parameter_size": entry["details"]["parameter_size"][:-1],
                "quantization_level": entry["details"]["quantization_level"][1:2],
            }
            for entry in data.get("models", [])
        }
    except (requests.RequestException, ValueError, KeyError, TypeError):
        # Any HTTP/JSON/schema issue -> try OpenAI-compatible fallback
        pass

    # ---- Attempt 2: OpenAI-compatible /v1/models ----
    try:
        headers = {}
        if getattr(endpoint, "key", None):
            headers["Authorization"] = f"Bearer {endpoint.key}"

        resp = requests.get(
            f"{api_base}/v1/models", headers=headers, verify=False, timeout=5
        )
        resp.raise_for_status()
        data = resp.json()

        # Map to the same return shape; details are unknown here
        return {
            m["id"]: {
                "parameter_size": "unknown",
                "quantization_level": "unknown",
            }
            for m in data.get("data", [])
        }
    except (requests.RequestException, ValueError, KeyError, TypeError):
        # Both strategies failed; return empty so caller can handle it
        return {}

def ollama_check_exist(endpoint: Endpoint) -> bool:
    list = ollama_list(endpoint)
    return endpoint.model_name in list

def ollama_pull(endpoint: Endpoint) -> dict:
    # Try to pull the model from the endpoint. If that does not work, we simply return.
    # Failure can be due to the model already being present, network issues, etc.,
    # we try to move on anyway.
    if endpoint.key: return endpoint # endpoints with a key are not an ollama server
    
    # don't load the model if it is already present
    if ollama_check_exist(endpoint):
        return endpoint

    # pull the model if it is not available
    api_base = get_ollama_url_stub(endpoint)
    print(f"Model {endpoint.model_name} is not available on server {api_base}. Pulling the model...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.request("POST", f"{api_base}/api/pull", verify=False,
                                    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                                    json={"model": endpoint.model_name, "stream": False})
        if response.status_code != 200:
            print(f"Failed to pull model {endpoint.model_name} from server {api_base}. Status code: {response.status_code}, Response: {response.text}")
            return endpoint
        data = response.json()
        if data.get("error", False):
            print(f"Error pulling Model {endpoint.model_name} from server {api_base}.")
        else:
            print(f"Model {endpoint.model_name} is now available on server {api_base}.")
    except requests.RequestException as e:
        print(f"Error during model pull request: {e}")
    return endpoint

def hex2base64(hex_string) -> str:
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

def ollama_chat(
    endpoint: Endpoint,
    prompt: str = 'Hello World',
    base64_image: str = None,
    temperature: float = 0.0,
    max_tokens: int = 32768, # thats large and it requires that you set the context length in ollama to 65536
    stream: bool = True
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
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    if endpoint.key:
        headers['Authorization'] = f'Bearer {endpoint.key}'

    modelname = endpoint.model_name
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
        # "response_format": { "type": "text" }, # do NOT set this, some engines do not accept "text" as response format because it is not valid
        "temperature": temperature, # ollama default: 0.8
        "top_k": 20,    # reduces the probability of generating nonsense: high = more diverse, low = more focused; ollama default: 40
        "top_p": 0.95,  # works together with top_k: high = more diverse, low = more focused; ollama default: 0.9
        "min_p": 0,     # alternative to top_p: p is minimum probability for a token to be considered; ollama default: 0.0
        "stream": stream
    }
    if len(stoptokens) > 0 and not modelname.startswith("o4"):
        payload["stop"] = stoptokens
    if modelname.startswith("o1") or modelname.startswith("o4"):
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

    # use the endpoints array as failover mechanism
    response = None
    text_chunks = []
    read_timeout = 600 # seconds
    token_count = 0
    parsed_url = urlparse(endpoint.url)
    host = parsed_url.hostname or ""
    c0 = host[0] if host else "."
    #print(f"Calling model in strem mode: {stream}, payload: {json.dumps(payload)}")
    try:
        t0 = time.time()
        response = requests.post(
            endpoint.url,
            headers=headers,
            json=payload,
            verify=False,
            stream=stream,
            timeout=(60, read_timeout) # (connect_timeout, read_timeout))
        )
        #print(f"Response status: {response.status_code}")
        response.raise_for_status()
        #print(f"Response headers: {response.headers}")
        if stream:
            #print("Response (stream): ", end="", flush=True)
            timeouttime = t0 + read_timeout
            for line in response.iter_lines(decode_unicode=True):
                if time.time() > timeouttime: break # we simply silently terminate the stream after the timeout
                if not line: continue
                #print(line)
                if line.startswith("data: "):
                    payload_line = line[len("data: "):].strip()
                    if payload_line == "[DONE]":
                        print() # end progress line
                        break
                    try:
                        evt = json.loads(payload_line)
                        choices = evt.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            #print(delta)
                            if "content" in delta:
                                # delta may have attributes content or reasoning. Take whatever is non-empty
                                token = delta.get("content") or delta.get("reasoning")
                                if token:
                                    text_chunks.append(token)
                                    token_count += 1
                                    #print(token, end="", flush=True)
                                    if token_count % 100 == 0:
                                        print(c0, end="", flush=True) # print a dot for each 10 tokens to show progress
                    except Exception:
                        pass # robust against json parse errors
        t1 = time.time()
    except requests.exceptions.ReadTimeout as e:
        raise Exception(f"Read timeout while calling {endpoint.url} (timeout=600s). "
                        f"The model may be slow or the server overloaded.") from e
    except requests.exceptions.RequestException as e:
        # print(f"Failed to access api: {e}")
        # Get the error message from the response
        body = ""
        if hasattr(e, "response") and e.response is not None:
            try:
                body = (e.response.text or "")[:800].replace("\n", " ")
            except Exception:
                body = ""
        raise Exception(f"API request failed to {endpoint.url}: {e} | Body: {body}") from e

    # Parse the response
    try:
        if stream:
            answer = "".join(text_chunks).strip()
            total_tokens = len(text_chunks)
            token_per_second = 0.0 if (t1 - t0) <= 0 else total_tokens / (t1 - t0)
            if not answer: print(f"Empty streamed response from the API at {endpoint.url}")
        else:
            ctype = response.headers.get('Content-Type', '')
            text  = response.text or ''
            if not text.strip():
                raise Exception(f"Empty response body (status {response.status_code}) from {endpoint.url}")

            if 'json' not in ctype.lower():
                # possibly a html error page
                snippet = text[:800].replace('\n',' ')
                raise Exception(f"Non-JSON response (status {response.status_code}, Content-Type {ctype}): {snippet}")

            data = response.json()
            usage = data.get('usage', {})
            total_tokens = usage.get('total_tokens', 0)
            token_per_second = total_tokens / (t1 - t0)
            #print(f"Total tokens: {total_tokens}, tokens per second: {token_per_second:.2f}")
            choices = data.get('choices', [])
            if len(choices) == 0:
                raise Exception("No response from the API: " + str(data))
            message = choices[0].get('message', {})
            answer = message.get('content', '')
        return answer, total_tokens, token_per_second
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from the API: {e}")

def test_multimodal(endpoint: dict) -> bool:
    image_path = "llmtest/testimage.png"
    # test if the image exists in that path
    if not os.path.exists(image_path):
        raise Exception(f"Test image not found: {image_path}")
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    try:
        print(f"Testing multimodal capabilities of model {endpoint.store_name}...")
        answer, total_tokens, token_per_second = ollama_chat(endpoint, prompt="what is in the image", base64_image=base64_image)
        result = "42" in answer
        if result:
            print(f"Model {endpoint.store_name} is multimodal.")
        else:
            print(f"Model {endpoint.store_name} is not multimodal; it returned the following answer: {answer}")
        return result
    except Exception as e:
        print(f"Model {endpoint.store_name} is not multimodal; it created an error: {e}")
        return False

busy_waiting_time = 1 # seconds


@dataclass
class Task:
    """
    Dataclass for task.
    This dataclass is used to represent a task that needs to be processed by a server.
    Each task has an ID and a dictionary of data that contains the actual task data.
    """
    id: str             # Unique identifier for the task
    description: str    # a short description of the task (for logging)
    prompt: str         # the prompt to be sent to the model
    base64_image: str   # the base64 encoded image to be sent to the model
    response_processing: Callable[['Response'], None] # a function to process the result

@dataclass
class Response:
    """
    Dataclass for response.
    This dataclass is used to represent a response from the server.
    Each response has a task ID and the result of the task processing.
    """
    task: Task
    result: str         # The result of the task processing
    total_tokens: int   # Total tokens used in the response
    token_per_second: float # Tokens per second used in the response

@dataclass
class Server:
    """
    Dataclass for server.
    This dataclass is used to represent a server that can process tasks.
    Each server has an ID, an endpoint (URL), and a status that indicates whether the server is available or busy.
    The status is used to track the current task being processed by the server.
    """
    endpoint: Endpoint  # The endpoint of the server
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
    def __init__(self, max_queue_size: int = 1000):
        self.servers = []
        self.task_queue = queue.Queue[Task](maxsize=max_queue_size)
        self.available_servers = queue.Queue[Server]()
        self.lock = threading.Lock()
        
    def add_server(self, server: Server):
        """Add a server to the load balancer"""
        self.servers.append(server)
        self.available_servers.put(server)
        print(f"Server {get_ollama_url_stub(server.endpoint)} added to load balancer.")

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
            server.current_task = None
            self.available_servers.put(server)
    
    def get_available_server(self, timeout: float = 10.0) -> Optional[Server]:
        """Get the next available server with timeout"""
        try:
            # Remove and return the next available server from the queue.
            # The only way the server gets available is when the task is finished
            # and the task assignes its server back to the available_servers.
            return self.available_servers.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def assign_task_to_server(self, task: Task, server: Server):
        """Assign task to server and mark it as busy"""
        with self.lock:
            server.current_task = task
        
        threading.Thread(
            target=self.process_task_remote,
            args=(server,),
            daemon=True
        ).start()
    
    def process_task_remote(self, server: Server):
        """Process task on remote server"""
        task = server.current_task
        endpoint = server.endpoint
        try:
            #print(f"Processing task ID {task.id} on server {server.endpoint} with model {task.model}")
            t0 = time.time()
            answer, total_tokens, token_per_second = ollama_chat(
                endpoint,
                task.prompt, 
                base64_image=task.base64_image
            )
            t1 = time.time()
            # Call the response processing function
            response = Response(task, answer, total_tokens, token_per_second)
            task.response_processing(response)
            print(f"Processed {task.description}, on {server.endpoint.url} with model {endpoint.model_name} in {t1 - t0:.2f} seconds with {total_tokens} tokens ({token_per_second:.2f} tokens/sec)")
            
            # mark server available
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
            # make server available again
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
                    print(f"Server {server.endpoint.url} - Current task ID: {server.current_task.id}")

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
    endpoints:List[Endpoint] = []
    if endpoint_name:
        print(f"Using endpoint {endpoint_name}")
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoint_dict = json.load(file)
            endpoints = [
                Endpoint(
                    store_name=endpoint_dict["name"],
                    model_name=endpoint_dict["model"],
                    key=endpoint_dict["key"],
                    url=endpoint_dict["endpoint"]
                )
            ]
    else:
        endpoints = [
            Endpoint(store_name=model_name, model_name=model_name, key="",
                     url=f"{api_stub}/v1/chat/completions") for api_stub in api_base
        ]

    # test if the endpoint is a multimodal model
    if test_multimodal(endpoints[0]):
        print("Endpoint is a multimodal model.")
    else:
        print("Endpoint is not a multimodal model.")

    # load the image, if a path is given
    base64_image = None
    if image_path:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # access the ollama API
    models_dict = ollama_list(endpoints[0])
    for (model, attr) in models_dict.items():
        print(f"Model: {model}: {attr}")
    try:
        if base64_image:
            answer, total_tokens, token_per_second = ollama_chat(endpoints[0], prompt="what is in the image", base64_image=base64_image)
        else:
            answer, total_tokens, token_per_second = ollama_chat(endpoints[0])
    except Exception as e:
        answer = f"Error: {str(e)}"
    print(answer)

if __name__ == "__main__":
    main()
