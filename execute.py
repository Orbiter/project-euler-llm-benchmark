import os
import re
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from llm_client import Endpoint
from argparse import ArgumentParser
from benchmark import read_benchmark, write_benchmark, sort_benchmark
from execute_clojure import execute_clojure_code
from execute_java import execute_java_code
from execute_python import execute_python_code
from execute_rust import execute_rust_code

def get_extension(language):
    if language == 'c': return 'c'
    elif language == 'r': return 'r'
    elif language == 'go': return 'go'
    elif language == 'c++': return 'cpp'
    elif language == 'lua': return 'lua'
    elif language == 'java': return 'java'
    elif language == 'lisp': return 'lisp'
    elif language == 'rust': return 'rs'
    elif language == 'ruby': return 'rb'
    elif language == 'perl': return 'pl'
    elif language == 'python': return 'py'
    elif language == 'prolog': return 'pl'
    elif language == 'matlab': return 'matlab'
    elif language == 'kotlin': return 'kt'
    elif language == 'clojure': return 'clj'
    elif language == 'fortran': return 'f'
    elif language == 'javascript': return 'js'
    else:
        raise Exception(f"Unsupported language: {language}")

def get_language_from_extension(extension):
    if extension == 'java': return 'java'
    elif extension == 'rs': return 'rust'
    elif extension == 'py': return 'python'
    elif extension == 'clj': return 'clojure'
    else:
        raise Exception(f"Unsupported extension: {extension}")

def get_problem_number_from_stem(stem):
    match = re.fullmatch(r'(?:tool-)?(\d+)', stem)
    if not match:
        raise ValueError(f"Unsupported solution filename: {stem}")
    return match.group(1)

def is_tool_solution_file(filename, extension):
    return filename.startswith('tool-') and filename.endswith('.' + extension)

def is_standard_solution_file(filename, extension):
    return (
        not filename.startswith('.')
        and not filename.startswith('tool-')
        and filename.endswith('.' + extension)
    )

def get_series_name(language, max_problem_number, tool_mode=False):
    if tool_mode:
        return f"{language}-tool-{max_problem_number}"
    return f"{language}-{max_problem_number}"

def process_solutions(model_name, language, max_problem_number, expected_solutions, tool_mode=False):
    results_dir = os.path.join('solutions', model_name, language)
    solutions_json_path = os.path.join('solutions', model_name, language, 'solutions.json')
    extension = get_extension(language)

    if not os.path.exists(results_dir):
        raise Exception(f"Directory '{results_dir}' does not exist.")

    solutions = {}
    tasks = []
    program_files = sorted(os.listdir(results_dir))
    for program_file in program_files:
        if tool_mode:
            if not is_tool_solution_file(program_file, extension): continue
        else:
            if not is_standard_solution_file(program_file, extension): continue
        program_file_path = os.path.join(results_dir, program_file)
        extlen = len(extension) + 1
        problem_number = get_problem_number_from_stem(program_file[:-extlen])
        if int(problem_number) > max_problem_number: break

        expected = expected_solutions.get(problem_number, None)
        tasks.append((program_file_path, expected))

    if tasks:
        max_workers = min(len(tasks), multiprocessing.cpu_count() or 1)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(_execute_solution_task, tasks))

        for problem_number, output in results:
            solutions[problem_number] = output

            # Write the solutions to a JSON file. We write this after each solution to avoid losing progress.
            with open(solutions_json_path, 'w', encoding='utf-8') as json_file:
                json.dump(solutions, json_file, indent=4)

    print(f"Executed all {language} files and saved results to {solutions_json_path}")
    return solutions

def execute_solution(program_file_path, expected):
    extension = program_file_path.split('.')[-1]
    language = get_language_from_extension(extension)

    # load the program code
    with open(program_file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # In some cases the code extraction does not find code and considers the whole file as code.
    # Here it might be that the LLM did actually solve the problem by itself using reasoning.
    # If that happens, the answer might be anywhere in the content.
    code = code.strip() # in case there are empty lines at the end
    expected_solution = expected.get('solution', '') if expected else ''

    # Check if the expected solution appears anywhere in the content (for non-code responses)
    if expected_solution and len(expected_solution) > 0:
        # Remove commas and check if solution appears in content
        code_normalized = code.replace(',', '')
        if expected_solution in code_normalized:
            # Extract the context around the solution for logging
            idx = code_normalized.find(expected_solution)
            context_start = max(0, idx - 20)
            context_end = min(len(code_normalized), idx + len(expected_solution) + 20)
            context = code_normalized[context_start:context_end]
            print(f"Executed {program_file_path}: Found solution {expected_solution} in content: ...{context}...")
            return expected_solution

    # Otherwise, try to execute the code
    if True:
        # Execute the code and capture the output
        print(f"Running program: {program_file_path}")
        output = ""
        if language == 'python':
            output = execute_python_code(code)
        if language == 'clojure':
            output = execute_clojure_code(code)
        if language == 'java':
            output = execute_java_code(code)
        if language == 'rust':
            output = execute_rust_code(code)
    
        # if the output has several lines, we only want the last one
        #print(f"Executed {solution_code_path}, raw output:{output}")
        output = output.strip().split('\n')[-1]
        result = "** CORRECT **" if output == expected_solution else ".. incorrect .."
        print(f"Executed {program_file_path}: {output} - {result}")
        return output

def _execute_solution_task(args):
    program_file_path, expected = args
    problem_number = get_problem_number_from_stem(os.path.splitext(os.path.basename(program_file_path))[0])
    output = execute_solution(program_file_path, expected)
    return problem_number, output

def evaluate_solutions(solutions, model_name, language, max_problem_number, expected_solutions, tool_mode=False):

    if len(solutions) == max_problem_number:
        # evaluate the solutions by comparing with the expected results
        human_points = 0.0
        candidate_points = 0.0
        maxmimum_points = 0.0
        total_count = 0
        human_count = 0 # for comparison: using the likelihood of the human solution to virtually count the number of human solutions
        candidate_count = 0
        test_results = ['0'] * max_problem_number
        for problem_number in solutions:
            if problem_number not in expected_solutions:
                print(f"Problem {problem_number} not found in expected solutions.")
                continue
            expected = expected_solutions[problem_number]
            solution = solutions[problem_number]
            expected_solution = expected['solution']
            challenge_points = expected_solutions[problem_number]['points']
            solution_likelihood = expected_solutions[problem_number]['percentage_solved'] * 0.01
            human_count += solution_likelihood
            human_points += challenge_points * solution_likelihood
            maxmimum_points += challenge_points
            index = int(problem_number) - 1
            if solution == expected_solution:
                candidate_points += challenge_points
                candidate_count += 1
                if 0 <= index < max_problem_number:
                    test_results[index] = '1'
            elif 0 <= index < max_problem_number:
                test_results[index] = '0'
            total_count += 1

        human_point_average = round(human_points / total_count, 2)
        candidate_point_average = round(candidate_points / total_count, 2)
        total_point_average = round(maxmimum_points / total_count, 2)
        print(f"Maximum Points: {maxmimum_points}")
        print(f"Maximum Solution Count: {total_count}")
        print(f"Maximum Point Average: {total_point_average}")
        print(f"Human Points: {human_points}")
        print(f"Human Solution Count: {human_count}")
        print(f"Human Point Average: {human_point_average}")
        print(f"Candidate Points: {candidate_points}")
        print(f"Candidate Solution Count: {candidate_count}")
        print(f"Candidate Point Average: {candidate_point_average}")

        # open the benchmark file and update the points
        benchmark = read_benchmark()

        # update the benchmark entry
        entry = benchmark.get(model_name, {})
        series_name = get_series_name(language, max_problem_number, tool_mode=tool_mode)
        series_name_test = f"{series_name}-test"
        entry[series_name] = candidate_point_average
        entry[series_name_test] = ''.join(test_results)
        benchmark[model_name] = entry

        # sort the benchmark with the highest points first, average over all batch sizes
        sorted_benchmark = sort_benchmark(benchmark)

        # write the updated benchmark file
        write_benchmark(sorted_benchmark)
    else:
        print("Not all solutions were executed, so the benchmark was not updated.")

def main():
    parser = ArgumentParser(description="Execute solutions and store results in a JSON file.")
    parser.add_argument('--allmodels', action='store_true', help='loop over all models as provided by benchmark.json and run all of them')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--think', action='store_true', help='if set, the prompt will get an additional "/think" appended at the end')
    parser.add_argument('--no_think', action='store_true', help='if set, the prompt will get an additional "/no_think" appended at the end')
    parser.add_argument('--language', required=False, default='python,java,rust,clojure', help='Name of the programming language to use, default is python')
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
    parser.add_argument('--tool', action='store_true', help='execute tool-generated source files with the tool- prefix and store separate benchmark keys')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()
    store_name = args.model
    languages = args.language.split(',')
    max_problem_number = 200
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999
    endpoint_name = args.endpoint
    if endpoint_name:
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoint = Endpoint(**json.load(file))
            store_name = endpoint.store_name

    # modify the model name in case soft thinking switches are given
    if args.think: store_name += "-think"
    if args.no_think: store_name += "-no_think"
    
    with open('solutions.json', 'r', encoding='utf-8') as json_file:
        expected_solutions = json.load(json_file)

    for language in languages:
        if args.allmodels:
            # iterate over all models provided by benchmark.json and run all of them
            benchmark = read_benchmark()
            # the keys are the model names
            for store_name in benchmark:
                solutions = process_solutions(store_name, language, max_problem_number, expected_solutions, tool_mode=args.tool)
                evaluate_solutions(solutions, store_name, language, max_problem_number, expected_solutions, tool_mode=args.tool)
        else:
            solutions = process_solutions(store_name, language, max_problem_number, expected_solutions, tool_mode=args.tool)
            evaluate_solutions(solutions, store_name, language, max_problem_number, expected_solutions, tool_mode=args.tool)

if __name__ == "__main__":
    main()
