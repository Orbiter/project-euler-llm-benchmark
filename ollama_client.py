import os
import json
import time
import base64
import urllib3
import requests
from PIL import Image
from io import BytesIO
from argparse import ArgumentParser


def ollama_list(api_base='http://localhost:11434'):
    # call api http://localhost:11434/api/tags with http get request
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    endpoint = f"{api_base}/api/tags"
    response = requests.get(endpoint, verify=False)
    response.raise_for_status()
    data = response.json()
    models_list = data['models']
    models_dict = {}
    for entry in models_list:
        # get parameter_size and quantization_level from data
        model = entry['model']
        details = entry['details']
        attr = {}
        parameter_size = details['parameter_size']
        quantization_level = details['quantization_level']
        parameter_size = parameter_size[:-1]
        try:
            parameter_size = float(parameter_size)
            attr['parameter_size'] = parameter_size
        except ValueError:
            pass
        quantization_level_char = quantization_level[1:2]
        try:
            quantization_level = int(quantization_level_char)
            attr['quantization_level'] = quantization_level
        except ValueError:
            pass
        models_dict[model] = attr
    return models_dict

def ollama_chat_endpoint(api_base='http://localhost:11434', model_name='llama3.2:latest'):
    endpoint = {
        "name": model_name,
        "model": model_name,
        "key": "",
        "endpoint": f"{api_base}/v1/chat/completions",
    }
    return endpoint

def hex2base64(hex_string):
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

def ollama_chat(endpoint, prompt='Hello World', base64_image=None, temperature=0.0, max_tokens=32768):

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
    
    # o1 has special requirements
    if modelname.startswith("o1") or modelname.startswith("gpt-o1"):
        temperature = 1.0 # o1 models need temperature 1.0
    else:
        messages.append({"role": "system", "content": "You are a helpful assistant"})
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
        "temperature": temperature,
        "response_format": { "type": "text" },
        "stream": False
    }
    if len(stoptokens) > 0:
        payload["stop"] = stoptokens
    if modelname.startswith("o1"):
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

    try:
        #print(payload)
        t0 = time.time()
        response = requests.post(endpoint["endpoint"], headers=headers, json=payload, verify=False)
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

def test_multimodal(endpoint):
    modelname = endpoint["model"]
    cached_result = multimodal_cache.get(modelname, None)
    if cached_result is not None:
        return cached_result

    image_path = "llmtest/testimage.png"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    try:
        answer, total_tokens, token_per_second = ollama_chat(endpoint, prompt="what is in the image", base64_image=base64_image)
        result = "42" in answer
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
    api_base = args.api_base
    endpoint_name = args.endpoint
    model_name = args.model
    image_path = args.image

    # load the endpoint file
    endpoint = {}
    if endpoint_name:
        print(f"Using endpoint {endpoint_name}")
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoint = json.load(file)
    else:
        endpoint = ollama_chat_endpoint(api_base, model_name)
    
    # test if the endpoint is a multimodal model
    if test_multimodal(endpoint):
        print("Endpoint is a multimodal model.")
    else:
        print("Endpoint is not a multimodal model.")

    # load the image, if a path is given
    base64_image = None
    if image_path:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # access the ollama API
    models_dict = ollama_list()
    for (model, attr) in models_dict.items():
        print(f"Model: {model}: {attr}")
    try:
        if base64_image:
            answer, total_tokens, token_per_second = ollama_chat(endpoint, prompt="what is in the image", base64_image=base64_image)
        else:
            answer, total_tokens, token_per_second = ollama_chat(endpoint)
    except Exception as e:
        answer = f"Error: {str(e)}"
    print(answer)

if __name__ == "__main__":
    main()
