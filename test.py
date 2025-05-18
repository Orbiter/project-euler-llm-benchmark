import os
from argparse import ArgumentParser
from benchmark import read_benchmark, write_benchmark
from ollama_client import ollama_list

def test(api_base, endpoint_name, model_name, language, overwrite_existing, overwrite_failed, max_problem_number=100, think=False, no_think=False):
    # call inference.py
    cmd = f"python3.12 inference.py --language {language} --api_base {api_base}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    if max_problem_number == 200: cmd += " --n200"
    if overwrite_existing: cmd += " --overwrite_existing"
    if overwrite_failed: cmd += " --overwrite_failed"
    if think: cmd += " --think"
    if no_think: cmd += " --no_think"
    print(f"Running command: {cmd}")
    os.system(cmd)

    # call codeextraction.py
    cmd = f"python3.12 codeextraction.py --language {language}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    if think: cmd += " --think"
    if no_think: cmd += " --no_think"
    print(f"Running command: {cmd}")
    os.system(cmd)

    # call execute.py
    cmd = f"python3.12 execute.py --language {language}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    if think: cmd += " --think"
    if no_think: cmd += " --no_think"
    print(f"Running command: {cmd}")
    os.system(cmd)

def main():
    parser = ArgumentParser(description="Run the complete pipeline to execute solutions and store results in a JSON file.")
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
    api_base = args.api_base
    model_name = args.model
    max_problem_number = 100
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999
    overwrite_existing = args.overwrite_existing
    overwrite_failed = args.overwrite_failed
    endpoint_name = args.endpoint

    # find models to test
    models = []
    model_dict = ollama_list()
    if args.allmodels:
        if endpoint_name:
            raise Exception("The --allmodels option cannot be used in combination with --endpoint.")
        
        models = list(model_dict.keys())
        print(f"Found {len(models)} models in ollama.")
    else:
        models = [model_name]

    # get languages
    languages = args.language.split(',')
    
    # loop over all models
    for model in models:

        # loop over all languages
        for language in languages:

            print(f"Testing model {model} with language {language}")
            bench_name = f"{language}-{max_problem_number}"

            # in every loop we load the benchmark.json again because it might have been updated
            benchmark = read_benchmark()
            model_benchmark_name = model
            if args.think: model_benchmark_name += "-think"
            if args.no_think: model_benchmark_name += "-no_think"
            entry = benchmark.get(model_benchmark_name, {})

            # add metadata to benchmark.json
            if not model_benchmark_name in benchmark or not bench_name in benchmark[model_benchmark_name] or overwrite_existing or overwrite_failed:
                # run the model; this writes a news entry to benchmark.json
                test(api_base, endpoint_name, model, language, overwrite_existing, overwrite_failed, max_problem_number, think = args.think, no_think = args.no_think)
                # load benchmark.json again because the test has updated it
                benchmark = read_benchmark()
                # because testing can be interrupted, there is no guarantee that the entry is present
                entry = benchmark.get(model_benchmark_name, {})
                
            # check if attributes parameter_size and quantization_level are present in benchmark.json
            parameter_size = model_dict.get(model,{}).get('parameter_size', None)
            if parameter_size:
                try:
                    parameter_size = float(parameter_size)
                except ValueError:
                    print(f"Warning: Could not convert parameter_size '{parameter_size}' to float for model {model}")
                    parameter_size = None 
            quantization_level = model_dict.get(model,{}).get('parameter_size', None)
            if quantization_level:
                try:
                    quantization_level = int(quantization_level)
                except ValueError:
                    print(f"Warning: Could not convert quantization_level '{quantization_level}' to int for model {model}")
                    quantization_level = None
            if not '_parameter_size' in entry and parameter_size: entry['_parameter_size'] = parameter_size
            if not '_quantization_level' in entry and quantization_level: entry['_quantization_level'] = quantization_level
            entry = dict(sorted(entry.items(), key=lambda item: item[0]))
            benchmark[model_benchmark_name] = entry

            # write the updated benchmark file
            write_benchmark(benchmark)

if __name__ == "__main__":
    main()
