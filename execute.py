import os
import re
import json
import shutil
import builtins
import traceback
import subprocess
import multiprocessing
from io import StringIO
from ollama_client import Endpoint
from argparse import ArgumentParser
from contextlib import redirect_stdout
from benchmark import read_benchmark, write_benchmark

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

def execute_python_code_worker(code, output_queue):
    # Define allowed built-ins
    safe_builtins = [
        'abs', 'all', 'any', 'ascii', 'bin', 'bin', 'bool', 'bytearray',
        'bytes', 'callable', 'chr', 'chr', 'complex', 'delattr', 'dict', 'dict',
        'dir', 'divmod', 'enumerate', 'eval', 'exit', 'filter', 'float',
        'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
        'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals',
        'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'property',
        'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
        'sorted', 'str', 'sum', 'tuple', 'type', 'vars', 'zip',
        'ZeroDivisionError', 'ValueError'
    ]
    allowed_builtins = {name: getattr(builtins, name) for name in safe_builtins}

    # Define allowed modules
    allowed_module_names = [
        'math', 'itertools', 'random', 'collections', 'datetime', 'string',
        'sympy', 'heapq', 'decimal', 'numpy', 'fractions']
    allowed_modules = {name: __import__(name) for name in allowed_module_names}

    # Custom __import__ function to restrict imports
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in allowed_modules:
            return allowed_modules[name]
        else:
            raise ImportError(f"Importing module '{name}' is not allowed.")

    # Add the custom __import__ to allowed built-ins
    allowed_builtins['__import__'] = safe_import

    # Define the restricted global environment
    restricted_globals = {
        '__builtins__': allowed_builtins,
        '__import__': safe_import,
        '__name__': '__main__',    # Add this line
        '__file__': None,          # Optional but recommended for consistency
        '__package__': None,       # Optional but recommended
        **allowed_modules,         # Inject allowed modules into the global scope
    }

    # Capture the output
    f = StringIO()
    try:
        with redirect_stdout(f):
            exec(code, restricted_globals)
        output = f.getvalue()
    except Exception as e:
        # Capture the traceback
        error_trace = traceback.format_exc()
        output = f"Error executing code: {e}\nTraceback:\n{error_trace}"
    output_queue.put({"output": output})

def execute_python_code(code, timeout=10):
    output_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=execute_python_code_worker, args=(code, output_queue))
    process.start()
    process.join(timeout)
    
    if process.is_alive():
        process.terminate()
        process.join()
        return "Error: Code execution timed out."
    
    try:
        result = output_queue.get_nowait()
        if "output" in result:
            return result["output"]
        elif "error" in result:
            return result["error"]
        else:
            return "Error: Unknown issue occurred during code execution."
    except multiprocessing.queues.Empty:
        return "Error: No output received from the executed code."

def execute_clojure_code(code, timeout=10):
    # Fix common issues with LLM-generated Clojure code
    # 1. Remove namespace declarations (they don't work well with -e flag)
    code = re.sub(r'\(ns\s+[\w\.\-]+(?:\s+\(:[^\)]+\))*\s*\)', '', code, flags=re.MULTILINE)

    # 2. Fallback: If there's a -main function, add a call to it at the end
    # (Template tells LLMs not to use -main, but this handles cases where instruction is ignored)
    if re.search(r'\(defn\s+-main\s*\[', code):
        code = code.rstrip() + '\n(-main)'

    try:
        # Execute the Clojure program using the Clojure CLI with a timeout
        result = subprocess.run(
            ["clj", "-M", "-e", code],  # Use the `-e` flag to evaluate the program directly
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Return output as a string
            timeout=timeout       # Set a timeout
        )
        #print(result)
        # Capture the output
        output = result.stdout.strip()  # Remove any extra whitespace
        return output

    except subprocess.TimeoutExpired:
        # Handle the timeout
        return "Error: Clojure program execution timed"
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"Error executing code: {e}\nTraceback:\n{error_trace}"
    
def extract_class_name(java_code):
    """
    Extracts the public class name from the Java code.
    """
    match = re.search(r"public\s+class\s+(\w+)", java_code)
    if match:
        return match.group(1)
    raise ValueError("No public class found in the Java code")

def execute_java_code(code, timeout=10):
    try:
        # Extract the class name from the Java code
        class_name = extract_class_name(code)

        # Create a temporary directory to store the Java file
        temp_dir = "temp_java"
        os.makedirs(temp_dir, exist_ok=True)

        # Write the Java code to a file with the correct name
        java_file_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(java_file_path, "w", encoding="utf-8") as file:
            file.write(code)

        # Compile the Java code
        compile_result = subprocess.run(
            ["javac", java_file_path],  # Compile the Java file
            capture_output=True,        # Capture stdout and stderr
            text=True                   # Return output as a string
        )

        # Check if compilation was successful
        if compile_result.returncode != 0:
            print("Compilation Error:")
            print(compile_result.stderr)
            return "Error: Java compilation failed"

        # Execute the compiled Java program
        execute_result = subprocess.run(
            ["java", "-cp", temp_dir, class_name],  # Run the compiled class
            capture_output=True,                    # Capture stdout and stderr
            text=True,                              # Return output as a string
            timeout=timeout                         # Set a timeout
        )

        # Print the full stdout and stderr for debugging
        #print("Full stdout:", execute_result.stdout)
        #print("Full stderr:", execute_result.stderr)

        # Capture the output
        output = execute_result.stdout.strip()  # Remove any extra whitespace

        # Clean up the temporary directory
        for file_name in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Delete the file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Delete the directory
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        os.rmdir(temp_dir)  # Remove the now-empty directory

        return output

    except subprocess.TimeoutExpired:
        # Handle the timeout
        return "Error: Java program execution timed out"
    except ValueError as e:
        # Handle the case where no public class is found
        return f"Error: {str(e)}"

def execute_rust_code(code, timeout=10):
    #print(f"Executing Rust code: {code}")
    try:

        # Create a temporary directory to store the Rust file
        temp_dir = "temp_rust"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)

        # Write the Rust code to a file
        rust_file_path = os.path.join(temp_dir, "rust.rs")
        with open(rust_file_path, "w", encoding="utf-8") as file:
            file.write(code)

        # make the binary path; thats the same as the filename without the extension
        binary_path = os.path.join(temp_dir, "rust")

        # Compile the Rust program using the Rust compiler
        compile_result = subprocess.run(
            ["rustc", "-A", "warnings", rust_file_path, "-o", binary_path]
        )

        # Check if the compilation was successful
        if compile_result.returncode != 0:
            # Clean up temporary files
            if os.path.exists(rust_file_path):
                os.remove(rust_file_path)
            if os.path.exists(temp_dir):
                # in case that the directory is not empty ignore the error
                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass
            return f"Error: Rust compilation failed: {compile_result.stderr}"
        
        # Execute the Rust program
        try:
            exec_result = subprocess.run(
                [binary_path],
                capture_output=True,  # Capture stdout and stderr
                text=True,            # Return output as a string
                timeout=timeout       # Set a timeout
            )
            output = exec_result.stdout.strip()  # Remove any extra whitespace
        except subprocess.TimeoutExpired:
            # Handle the timeout
            output = "Error: Rust program execution timed out"
        finally:
            # Clean up temporary files
            if os.path.exists(binary_path):
                os.remove(binary_path)
            if os.path.exists(rust_file_path):
                os.remove(rust_file_path)
            if os.path.exists(temp_dir):
                # in case that the directory is not empty ignore the error
                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass
            
        return output

    except subprocess.TimeoutExpired:
        # Handle the timeout
        return "Error: Rust program execution timed"

def process_solutions(model_name, language, max_problem_number, expected_solutions):
    results_dir = os.path.join('solutions', model_name, language)
    solutions_json_path = os.path.join('solutions', model_name, language, 'solutions.json')
    extension = get_extension(language)

    if not os.path.exists(results_dir):
        raise Exception(f"Directory '{results_dir}' does not exist.")

    solutions = {}
    program_files = sorted(os.listdir(results_dir))
    for program_file in program_files:
        if program_file.startswith('.')  or not program_file.endswith('.' + extension): continue
        program_file_path = os.path.join(results_dir, program_file)
        extlen = len(extension) + 1
        problem_number = program_file[:-extlen]  # Remove extension
        if int(problem_number) > max_problem_number: break

        expected = expected_solutions.get(problem_number, None)
        output = execute_solution(program_file_path, expected)
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

def evaluate_solutions(solutions, model_name, language, max_problem_number, expected_solutions):

    if len(solutions) == max_problem_number:
        # evaluate the solutions by comparing with the expected results
        human_points = 0.0
        candidate_points = 0.0
        maxmimum_points = 0.0
        total_count = 0
        human_count = 0 # for comparison: using the likelihood of the human solution to virtually count the number of human solutions
        candidate_count = 0
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
            if solution == expected_solution:
                candidate_points += challenge_points
                candidate_count += 1
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
        series_name = f"{language}-{max_problem_number}"
        entry[series_name] = candidate_point_average
        benchmark[model_name] = entry

        # sort the benchmark with the highest points first, use the series name "python-100" as the key
        sorted_benchmark = dict(sorted(benchmark.items(), key=lambda item: -item[1].get("python-100", 0)))

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
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()
    store_name = args.model
    languages = args.language.split(',')
    max_problem_number = 100
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
                solutions = process_solutions(store_name, language, max_problem_number, expected_solutions)
                evaluate_solutions(solutions, store_name, language, max_problem_number, expected_solutions)
        else:
            solutions = process_solutions(store_name, language, max_problem_number, expected_solutions)
            evaluate_solutions(solutions, store_name, language, max_problem_number, expected_solutions)

if __name__ == "__main__":
    main()
