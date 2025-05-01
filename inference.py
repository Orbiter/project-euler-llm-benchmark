import os
import json
import base64
from argparse import ArgumentParser
from benchmark import read_benchmark, write_benchmark
from ollama_client import ollama_list, ollama_chat_endpoints, ollama_chat, test_multimodal

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
        #print(f"Problem {problem_number} expected solution: {actual_solution}")
        #print(f"Problem {problem_number} current solution: {solutions.get(problem_number, None)}")
        #print(f"Problem {problem_number} is solved: {problem_is_solved}")
        
        # if overwrite_failed is set, we skip this if it is solved and the flag is set
        if overwrite_failed and problem_is_solved:
            print(f"Skipping problem {problem_number} as it is already solved and overwrite_failed is set.")
            continue
        
        # start computing the solution
        with open(problem_path, 'r', encoding='utf-8') as file:
            problem_content = file.read()

        # Construct the prompt using the template
        prompt = template_content.replace('$$$PROBLEM$$$', problem_content)

        # attach soft thinking switches if asked
        if think: prompt += " /think"
        if no_think: prompt += " /no_think"
            
        # check if there is also an image in the problem. We take the problem_file, remove the extension ".txt"
        # and add either "-0.png", "-0.jpg" or "-0.gif"
        base64_image = None
        possible_extensions = ["-0.png", "-0.jpg", "-0.gif"]
        for ext in possible_extensions:
            image_path = os.path.join(problems_dir, problem_number + ext)
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                break
        
        # check if the endpoint is multimodal, we do this only if we have an image
        if base64_image:
            is_multimodal = test_multimodal(endpoints) # this is cached
            if is_multimodal:
                print(f"Problem {problem_number} is handled with multimodal model.")
            else:
                print(f"Problem {problem_number} requires a multimodal model for image processing but the model is not multimodal.")
                base64_image = None
                 
        try:
            answer, total_tokens, token_per_second = ollama_chat(endpoints, prompt, base64_image=base64_image)

            # Save the response to a file
            with open(result_file_path, 'w', encoding='utf-8') as result_file:
                result_file.write(answer)
            print(f"Processed problem {problem_number} and saved response to {result_file_path}")
        except NameError as e:
            print(f"NameError occurred: {e}")
            print(f"Available globals: {globals().keys()}")
        except Exception as e:
            print(f"Failed to process problem {problem_number}: {e}")

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
