from argparse import ArgumentParser
from llm_client import ollama_api_delete, Endpoint

def main():
    parser = ArgumentParser(description="Cleanup models: delete models from ollama endpoints")
    parser.add_argument('--api', action='append', help="Specify (multiple) backend OpenAI API endpoints (i.e. ollama); can be used multiple times")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM or a list of such urls (comma-separated), default is http://localhost:11434')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')

    args = parser.parse_args()
    
    api_base = args.api if args.api else args.api_base.split(",") if "," in args.api_base else [args.api_base]
    model_name = args.model

    for api_stub in api_base:
        try:
            endpoint = Endpoint(store_name=model_name, model_name=model_name, key="", url=f"{api_stub}/v1/chat/completions")
            ollama_api_delete(endpoint)
            print(f"Model {model_name} removed from {api_stub}.")
        except Exception as e:
            # the server is not available
            print(f"Server {api_stub} is not available: {e}")

if __name__ == "__main__":
    main()
