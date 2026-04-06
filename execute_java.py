import os
import re
import shutil
import subprocess
import tempfile


JAVA_BLOCKED_PATTERNS = [
    (r"\bimport\s+java\.io\.", "java.io imports are not allowed."),
    (r"\bimport\s+java\.nio\.", "java.nio imports are not allowed."),
    (r"\bimport\s+java\.net\.", "java.net imports are not allowed."),
    (r"\bimport\s+java\.lang\.reflect\.", "Reflection imports are not allowed."),
    (r"\bimport\s+java\.lang\.ProcessBuilder\b", "ProcessBuilder is not allowed."),
    (r"\bimport\s+java\.lang\.Runtime\b", "Runtime is not allowed."),
    (r"\bProcessBuilder\b", "Process execution is not allowed."),
    (r"\bRuntime\s*\.\s*getRuntime\s*\(", "Runtime access is not allowed."),
    (r"\bSystem\s*\.\s*exit\s*\(", "System.exit is not allowed."),
    (r"\bClassLoader\b", "ClassLoader access is not allowed."),
    (r"\bjava\.io\.", "java.io access is not allowed."),
    (r"\bjava\.nio\.", "java.nio access is not allowed."),
    (r"\bjava\.net\.", "java.net access is not allowed."),
    (r"\bFiles\s*\.", "Filesystem access is not allowed."),
    (r"\bPaths\s*\.", "Filesystem path access is not allowed."),
    (r"\bFile(InputStream|OutputStream|Reader|Writer)?\b", "Filesystem access is not allowed."),
]


def extract_class_name(java_code):
    match = re.search(r"public\s+class\s+(\w+)", java_code)
    if match:
        return match.group(1)
    raise ValueError("No public class found in the Java code")


def validate_java_code_safety(code):
    for pattern, message in JAVA_BLOCKED_PATTERNS:
        if re.search(pattern, code):
            return 1, "", f"Unsafe Java code blocked: {message}"
    return 0, "Safety OK", ""


def syntax_check_java(code):
    exit_code, stdout, stderr = validate_java_code_safety(code)
    if exit_code != 0:
        return exit_code, stdout, stderr

    temp_dir = tempfile.mkdtemp(prefix="opx_java_")
    try:
        class_name = extract_class_name(code)
        source_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(source_path, "w", encoding="utf-8") as handle:
            handle.write(code)
        result = subprocess.run(["javac", source_path], capture_output=True, text=True)
        if result.returncode == 0:
            return 0, "Syntax OK", ""
        stderr = (result.stderr or result.stdout or "Java syntax check failed").strip()
        return 1, "", stderr
    except OSError as exc:
        return 1, "", f"Failed to run javac: {exc}"
    except ValueError as exc:
        return 1, "", str(exc)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def execute_java_code(code, timeout=10):
    temp_dir = tempfile.mkdtemp(prefix="temp_java_")
    try:
        exit_code, _, safety_error = validate_java_code_safety(code)
        if exit_code != 0:
            return f"Error: {safety_error}"
        class_name = extract_class_name(code)
        java_file_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(java_file_path, "w", encoding="utf-8") as file:
            file.write(code)

        compile_result = subprocess.run(
            ["javac", java_file_path],
            capture_output=True,
            text=True,
        )
        if compile_result.returncode != 0:
            print("Compilation Error:")
            print(compile_result.stderr)
            return "Error: Java compilation failed"

        execute_result = subprocess.run(
            ["java", "-cp", temp_dir, class_name],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return execute_result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Java program execution timed out"
    except ValueError as exc:
        return f"Error: {str(exc)}"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
