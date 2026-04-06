import ast
import builtins
import faulthandler
import multiprocessing
import signal
import sys
import traceback
from contextlib import redirect_stdout
from io import StringIO


PYTHON_ALLOWED_MODULE_NAMES = [
    "heapq",
    "string",
    "datetime",
    "re",
    "math",
    "itertools",
    "functools",
    "operator",
    "collections",
    "bisect",
    "array",
    "decimal",
    "fractions",
    "statistics",
    "random",
    "sys",
]

PYTHON_ALLOWED_BUILTINS = [
    "abs", "bool", "chr", "complex", "divmod", "float", "hex", "int",
    "len", "oct", "ord", "pow", "round", "str", "sum", "max", "min",
    "ascii", "callable", "chr", "id",
    "all", "any", "enumerate", "filter", "iter", "map", "next", "range",
    "reversed", "slice", "sorted", "zip",
    "dict", "frozenset", "list", "set", "tuple",
    "isinstance", "issubclass", "type",
    "bin", "bytearray", "bytes", "hash",
    "print", "repr",
    "Exception", "StopIteration", "ValueError", "ZeroDivisionError",
    "OverflowError", "TypeError", "IndexError", "KeyError",
]


def validate_python_code_safety(code):
    try:
        tree = ast.parse(code, filename="<inline>")
    except SyntaxError as exc:
        location = f"line {exc.lineno}, column {exc.offset}"
        return 1, "", f"SyntaxError at {location}: {exc.msg}"

    allowed_builtin_names = set(PYTHON_ALLOWED_BUILTINS)
    allowed_builtin_names.add("setrecursionlimit")
    allowed_module_names = set(PYTHON_ALLOWED_MODULE_NAMES)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in allowed_module_names:
                    return 1, "", f"Importing module '{root}' is not allowed."
        elif isinstance(node, ast.ImportFrom):
            if node.level != 0 or not node.module:
                return 1, "", "Relative imports are not allowed."
            root = node.module.split(".")[0]
            if root not in allowed_module_names:
                return 1, "", f"Importing module '{root}' is not allowed."
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name in {"eval", "exec", "compile", "open", "input", "__import__"}:
                    return 1, "", f"Calling '{name}' is not allowed."
        elif isinstance(node, ast.Name):
            if node.id in {"eval", "exec", "compile", "open", "input"} and isinstance(node.ctx, ast.Load):
                if node.id not in allowed_builtin_names:
                    return 1, "", f"Using '{node.id}' is not allowed."

    return 0, "Safety OK", ""


def syntax_check_python(code, filename=""):
    try:
        ast.parse(code, filename=filename or "<inline>")
    except SyntaxError as exc:
        location = f"line {exc.lineno}, column {exc.offset}"
        return 1, "", f"SyntaxError at {location}: {exc.msg}"
    return validate_python_code_safety(code)


def execute_python_code_worker(code, output_queue):
    faulthandler.enable(file=sys.stderr, all_threads=True)
    if hasattr(signal, "SIGUSR1"):
        faulthandler.register(signal.SIGUSR1, file=sys.stderr, all_threads=True)
    if hasattr(signal, "SIGQUIT"):
        faulthandler.register(signal.SIGQUIT, file=sys.stderr, all_threads=True)

    allowed_builtins = {name: getattr(builtins, name) for name in PYTHON_ALLOWED_BUILTINS}
    allowed_builtins["setrecursionlimit"] = sys.setrecursionlimit

    allowed_modules = {name: __import__(name) for name in PYTHON_ALLOWED_MODULE_NAMES}

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in allowed_modules:
            return allowed_modules[name]
        raise ImportError(f"Importing module '{name}' is not allowed.")

    allowed_builtins["__import__"] = safe_import
    restricted_globals = {
        "__builtins__": allowed_builtins,
        "__import__": safe_import,
        "__name__": "__main__",
        "__file__": None,
        "__package__": None,
        **allowed_modules,
    }

    capture = StringIO()
    try:
        with redirect_stdout(capture):
            exec(code, restricted_globals)
        output = capture.getvalue()
    except Exception as exc:
        error_trace = traceback.format_exc()
        output = f"Error executing code: {exc}\nTraceback:\n{error_trace}"
    output_queue.put({"output": output})


def execute_python_code(code, timeout=10):
    exit_code, _, safety_error = syntax_check_python(code)
    if exit_code != 0:
        return f"Error: {safety_error}"
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
        if "error" in result:
            return result["error"]
        return "Error: Unknown issue occurred during code execution."
    except multiprocessing.queues.Empty:
        return "Error: No output received from the executed code."
