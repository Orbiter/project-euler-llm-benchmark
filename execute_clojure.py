import re
import subprocess
import traceback


CLOJURE_BLOCKED_PATTERNS = [
    (r"\(require\s+'\[?clojure\.java\.io", "clojure.java.io is not allowed."),
    (r"\(require\s+'\[?clojure\.java\.shell", "clojure.java.shell is not allowed."),
    (r"\bclojure\.java\.io\b", "clojure.java.io is not allowed."),
    (r"\bclojure\.java\.shell\b", "clojure.java.shell is not allowed."),
    (r"\bslurp\b", "File reading is not allowed."),
    (r"\bspit\b", "File writing is not allowed."),
    (r"\bload-file\b", "Loading files is not allowed."),
    (r"\beval\b", "Dynamic evaluation is not allowed."),
    (r"\bload-string\b", "Dynamic evaluation is not allowed."),
    (r"\bread-string\b", "Dynamic evaluation is not allowed."),
    (r"\bSystem/exit\b", "System exit is not allowed."),
    (r"\bRuntime/getRuntime\b", "Runtime access is not allowed."),
    (r"\bProcessBuilder\.?\b", "Process execution is not allowed."),
    (r"\bjava\.io\.", "java.io access is not allowed."),
    (r"\bjava\.nio\.", "java.nio access is not allowed."),
    (r"\bjava\.net\.", "java.net access is not allowed."),
]


def validate_clojure_code_safety(code):
    for pattern, message in CLOJURE_BLOCKED_PATTERNS:
        if re.search(pattern, code):
            return 1, "", f"Unsafe Clojure code blocked: {message}"
    return 0, "Safety OK", ""


def syntax_check_clojure(code):
    exit_code, stdout, stderr = validate_clojure_code_safety(code)
    if exit_code != 0:
        return exit_code, stdout, stderr

    pairs = {"(": ")", "[": "]", "{": "}"}
    closing = {")": "(", "]": "[", "}": "{"}
    stack = []
    in_string = False
    escape = False
    line = 1

    for char in code:
        if char == "\n":
            line += 1
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == "\"":
                in_string = False
            continue
        if char == "\"":
            in_string = True
            continue
        if char in pairs:
            stack.append((char, line))
            continue
        if char in closing:
            if not stack or stack[-1][0] != closing[char]:
                return 1, "", f"Unmatched '{char}' at line {line}"
            stack.pop()

    if in_string:
        return 1, "", "Unterminated string literal"
    if stack:
        opener, opener_line = stack[-1]
        return 1, "", f"Unclosed '{opener}' from line {opener_line}"
    return 0, "Parentheses OK", ""


def execute_clojure_code(code, timeout=10):
    code = re.sub(r"\(ns\s+[\w\.\-]+(?:\s+\(:[^\)]+\))*\s*\)", "", code, flags=re.MULTILINE)

    if re.search(r"\(defn\s+-main\s*\[", code):
        code = code.rstrip() + "\n(-main)"

    try:
        exit_code, _, safety_error = validate_clojure_code_safety(code)
        if exit_code != 0:
            return f"Error: {safety_error}"
        result = subprocess.run(
            ["clj", "-M", "-e", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Clojure program execution timed"
    except Exception as exc:
        error_trace = traceback.format_exc()
        return f"Error executing code: {exc}\nTraceback:\n{error_trace}"
