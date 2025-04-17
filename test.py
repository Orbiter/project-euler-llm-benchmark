import os
from argparse import ArgumentParser
from benchmark import read_benchmark, write_benchmark
from ollama_client import ollama_list

def test(endpoint_name, model_name, language, overwrite_existing, overwrite_failed, max_problem_number=100):
    # call inference.py
    cmd = f"python3.12 inference.py --language {language}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    if max_problem_number == 200: cmd += " --n200"
    if overwrite_existing: cmd += " --overwrite_existing"
    if overwrite_failed: cmd += " --overwrite_failed"
    os.system(cmd)

    # call codeextraction.py
    cmd = f"python3.12 codeextraction.py --language {language}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    os.system(cmd)

    # call execute.py
    cmd = f"python3.12 execute.py --language {language}"
    cmd += f" --endpoint {endpoint_name}" if endpoint_name else f" --model {model_name}"
    os.system(cmd)

def main():
    parser = ArgumentParser(description="Run the complete pipeline to execute solutions and store results in a JSON file.")
    parser.add_argument('--allmodels', action='store_true', help='loop over all models provided by ollama and run those which are missing in benchmark.json')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python,java,rust,clojure', help='Name of the languages to test, default is python,java,rust,clojure')
    parser.add_argument('--overwrite_existing', action='store_true', help='if set, re-calculate all problems that already have an answer')
    parser.add_argument('--overwrite_failed', action='store_true', help='if set, re-calculate those problems with wrong answers')
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
    overwrite_existing = args.overwrite_existing
    overwrite_failed = args.overwrite_failed
    endpoint_name = args.endpoint

    # find models to test
    models = []
    if args.allmodels:
        if endpoint_name:
            raise Exception("The --allmodels option cannot be used in combination with --endpoint.")
        
        models = list(ollama_list().keys())
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
            entry = benchmark.get(model, {})

            # add metadata to benchmark.json
            if not model in benchmark or not bench_name in benchmark[model] or overwrite_existing or overwrite_failed:
                # run the model; this writes a news entry to benchmark.json
                test(endpoint_name, model, language, overwrite_existing, overwrite_failed, max_problem_number)
                # load benchmark.json again because the test has updated it
                benchmark = read_benchmark()
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
            write_benchmark(benchmark)

if __name__ == "__main__":
    main()
