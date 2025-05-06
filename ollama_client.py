import os
import json
import time
import base64
import urllib3
import requests
from PIL import Image
from io import BytesIO
from argparse import ArgumentParser

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

def ollama_chat(endpoints, prompt='Hello World', base64_image=None, temperature=0.0, max_tokens=8192) -> tuple:

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Prepare the API endpoint URL
    stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>", "<|end_header_id|>", "<EOS_TOKEN>", "</s>", "<|end|>"]

    # Set headers and payload
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if endpoints.get("key", ""):
        headers['Authorization'] = 'Bearer ' + endpoints["key"]

    modelname = endpoints["model"]
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

    try:
        #print(payload)
        t0 = time.time()
        response = requests.post(endpoints["endpoints"][0], headers=headers, json=payload, verify=False)
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
                raise Exception(f"API request failed: {content}")
            except json.JSONDecodeError:
                raise Exception(f"API request failed: {e}")

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
            raise Exception("No response from the API: " + str(data))
        message = choices[0].get('message', {})
        answer = message.get('content', '')
        return answer, total_tokens, token_per_second
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from the API: {e}")

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
