import os
import re
import shutil
import subprocess
import tempfile


RUST_BLOCKED_PATTERNS = [
    (r"\bunsafe\b", "unsafe blocks are not allowed."),
    (r"\bextern\s+crate\b", "extern crate usage is not allowed."),
    (r"\bextern\s+\"[^\"]+\"", "FFI declarations are not allowed."),
    (r"\bstd::fs::", "Filesystem access is not allowed."),
    (r"\bstd::process::", "Process execution is not allowed."),
    (r"\bstd::net::", "Network access is not allowed."),
    (r"\bstd::os::", "OS-specific access is not allowed."),
    (r"\bstd::env::", "Environment access is not allowed."),
    (r"\bFile::", "Filesystem access is not allowed."),
    (r"\bOpenOptions::", "Filesystem access is not allowed."),
    (r"\bCommand::", "Process execution is not allowed."),
    (r"\bTcp(Stream|Listener)\b", "Network access is not allowed."),
    (r"\bUdpSocket\b", "Network access is not allowed."),
]


def validate_rust_code_safety(code):
    for pattern, message in RUST_BLOCKED_PATTERNS:
        if re.search(pattern, code):
            return 1, "", f"Unsafe Rust code blocked: {message}"
    return 0, "Safety OK", ""


def syntax_check_rust(code):
    exit_code, stdout, stderr = validate_rust_code_safety(code)
    if exit_code != 0:
        return exit_code, stdout, stderr

    temp_dir = tempfile.mkdtemp(prefix="opx_rust_")
    try:
        source_path = os.path.join(temp_dir, "main.rs")
        output_path = os.path.join(temp_dir, "main")
        with open(source_path, "w", encoding="utf-8") as handle:
            handle.write(code)
        result = subprocess.run(
            ["rustc", "--emit", "metadata", "-o", output_path, source_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return 0, "Syntax OK", ""
        stderr = (result.stderr or result.stdout or "Rust syntax check failed").strip()
        return 1, "", stderr
    except OSError as exc:
        return 1, "", f"Failed to run rustc: {exc}"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def execute_rust_code(code, timeout=10):
    temp_dir = tempfile.mkdtemp(prefix="temp_rust_")
    try:
        exit_code, _, safety_error = validate_rust_code_safety(code)
        if exit_code != 0:
            return f"Error: {safety_error}"
        rust_file_path = os.path.join(temp_dir, "rust.rs")
        with open(rust_file_path, "w", encoding="utf-8") as file:
            file.write(code)

        binary_path = os.path.join(temp_dir, "rust")
        compile_result = subprocess.run(
            ["rustc", "-A", "warnings", rust_file_path, "-o", binary_path],
            capture_output=True,
            text=True,
        )
        if compile_result.returncode != 0:
            return f"Error: Rust compilation failed: {compile_result.stderr}"

        try:
            exec_result = subprocess.run(
                [binary_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = exec_result.stdout.strip()
        except subprocess.TimeoutExpired:
            output = "Error: Rust program execution timed out"
        finally:
            if os.path.exists(binary_path):
                os.remove(binary_path)

        return output
    except subprocess.TimeoutExpired:
        return "Error: Rust program execution timed"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
