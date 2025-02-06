import os
import json
import time
import urllib3
import requests
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

def ollama_chat(endpoint, prompt='Hello World', temperature=0.0, max_tokens=8192):

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
        messages.append({"content": "You are a helpful assistant", "role": "system"})
    if modelname.startswith("4o") or modelname.startswith("gpt-4o") or modelname.startswith("gpt-3.5"):
        # reduce number of stoptokes to 4
        stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>"]

    messages.append({"role": "user", "content": prompt})

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

def main():
    parser = ArgumentParser(description="Testing the ollama API.")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM, default is http://localhost:11434')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    
    # parse the arguments
    args = parser.parse_args()
    api_base = args.api_base
    endpoint_name = args.endpoint
    model_name = args.model

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
    
    # access the ollama API
    models_dict = ollama_list()
    for (model, attr) in models_dict.items():
        print(f"Model: {model}")
    answer, total_tokens, token_per_second = ollama_chat(endpoint)
    print(answer)

if __name__ == "__main__":
    main()
