import os
import json
from ollama_client import ollama_list
from argparse import ArgumentParser

def test(endpoint_name, model_name, language, skip_existing, max_problem_number=100):
    # call inference.py
    if endpoint_name:
        if skip_existing:
            if max_problem_number == 200:
                os.system(f"python3.12 inference.py --endpoint {endpoint_name} --language {language} --n200 --skip_existing")
            else:
                os.system(f"python3.12 inference.py --endpoint {endpoint_name} --language {language} --skip_existing")
        else:
            if max_problem_number == 200:
                os.system(f"python3.12 inference.py --endpoint {endpoint_name} --language {language} --n200")
            else:
                os.system(f"python3.12 inference.py --endpoint {endpoint_name} --language {language}")
    else:
        if skip_existing:
            if max_problem_number == 200:
                os.system(f"python3.12 inference.py --model {model_name} --language {language} --n200 --skip_existing")
            else:
                os.system(f"python3.12 inference.py --model {model_name} --language {language} --skip_existing")
        else:
            if max_problem_number == 200:
                os.system(f"python3.12 inference.py --model {model_name} --language {language} --n200")
            else:
                os.system(f"python3.12 inference.py --model {model_name} --language {language}")

    # call codeextraction.py
    if endpoint_name:
        os.system(f"python3.12 codeextraction.py --endpoint {endpoint_name} --language {language}")
    else:
        os.system(f"python3.12 codeextraction.py --model {model_name} --language {language}")

    # call execute.py
    if endpoint_name:
        os.system(f"python3.12 execute.py --endpoint {endpoint_name} --language {language}")
    else:
        os.system(f"python3.12 execute.py --model {model_name} --language {language}")

def main():
    parser = ArgumentParser(description="Run the complete pipeline to execute solutions and store results in a JSON file.")
    parser.add_argument('--allmodels', action='store_true', help='loop over all models provided by ollama and run those which are missing in benchmark.json')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python,java,rust,clojure', help='Name of the languages to test, default is python,java,rust,clojure')
    parser.add_argument('--skip_existing', action='store_true', help='if set, skip problems that already have a solution')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()
    model_name = args.model
    max_problem_number = 100
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999
    skip_existing = args.skip_existing
    endpoint_name = args.endpoint

    # iterate over all languages
    languages = args.language.split(',')
    for language in languages:
        bench_name = f"{language}-{max_problem_number}"

        if args.allmodels:
            if endpoint_name:
                raise Exception("The --allmodels option cannot be used in combination with --endpoint.")
            
            # loop over all models provided by ollama and run those which are missing in benchmark.json
            with open('benchmark.json', 'r', encoding='utf-8') as json_file:
                benchmark = json.load(json_file)
            # load models from ollama
            models = ollama_list()
            print(f"Found {len(models)} models in ollama.")
            for model in models:
                # in every loop we load the benchmark.json again because it might have been updated
                with open('benchmark.json', 'r', encoding='utf-8') as json_file:
                    benchmark = json.load(json_file)
                entry = benchmark.get(model, {})

                # add metadata to benchmark.json
                if not model in benchmark or not bench_name in benchmark[model]:
                    # run the model; this writes a news entry to benchmark.json
                    test(endpoint_name, model, language, skip_existing, max_problem_number)
                    # load benchmark.json again because the test has updated it
                    with open('benchmark.json', 'r', encoding='utf-8') as json_file:
                        benchmark = json.load(json_file)
                    # because testing can be interrupted, there is no guarantee that the entry is present
                    entry = benchmark.get(model, {})
                    
                # check if attributes parameter_size and quantization_level are present in benchmark.json
                if not '_parameter_size' in entry and models[model].get('parameter_size', None):
                    entry['_parameter_size'] = models[model].get('parameter_size', None)
                if not '_quantization_level' in entry and models[model].get('quantization_level', None):
                    entry['_quantization_level'] = models[model].get('quantization_level', None)
                entry = dict(sorted(entry.items(), key=lambda item: item[0]))
                benchmark[model] = entry

                # write the updated benchmark file
                with open('benchmark.json', 'w', encoding='utf-8') as json_file:
                    json.dump(benchmark, json_file, indent=4)
        else:
            test(endpoint_name, model_name, language, skip_existing)

if __name__ == "__main__":
    main()
