import shutil
import subprocess
from functools import lru_cache


MAX_CODE_BYTES = 1_000_000
MAX_OUTPUT_BYTES = 1_000_000
MAX_HEAP_MIB = 256
SYNTAX_CHECK_TIMEOUT = 10
PREFLIGHT_TIMEOUT = 5

NODE_FLAGS = (
    "--permission",
    "--no-addons",
    "--no-global-search-paths",
    "--disable-proto=throw",
    "--disallow-code-generation-from-strings",
    f"--max-old-space-size={MAX_HEAP_MIB}",
)

# Run solutions as plain scripts in a context containing ECMAScript built-ins but
# no Node globals such as process, require, module, fetch, or timers.
JAVASCRIPT_RUNNER = f"""
const fs = require("node:fs");
const vm = require("node:vm");
const code = fs.readFileSync(0, "utf8");
const timeout = Number(process.argv[1]);
const outputLimit = {MAX_OUTPUT_BYTES};
let outputBytes = 0;

function write(stream, values) {{
    const line = values.map(value => String(value)).join(" ") + "\\n";
    outputBytes += Buffer.byteLength(line);
    if (outputBytes > outputLimit) throw new Error("Output limit exceeded");
    stream.write(line);
}}

const safeConsole = Object.freeze({{
    log: (...values) => write(process.stdout, values),
    error: (...values) => write(process.stderr, values),
}});
const context = vm.createContext(
    {{console: safeConsole}},
    {{codeGeneration: {{strings: false, wasm: false}}, name: "benchmark"}},
);
new vm.Script(code, {{filename: "solution.js"}}).runInContext(
    context,
    {{timeout, breakOnSigint: true}},
);
"""


@lru_cache(maxsize=1)
def _secure_node_binary():
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Node.js is not installed or is not on PATH")

    help_result = subprocess.run(
        [node, "--help"], capture_output=True, text=True, timeout=5, env={}
    )
    help_text = help_result.stdout + help_result.stderr
    if "--permission" not in help_text or "--allow-net" not in help_text:
        raise RuntimeError(
            "This runner requires a Node.js version whose permission model "
            "restricts filesystem, subprocess, worker, and network access"
        )
    return node


@lru_cache(maxsize=1)
def ensure_javascript_runtime():
    """Fail early unless Node can launch with the benchmark sandbox flags."""
    node = _secure_node_binary()
    try:
        result = subprocess.run(
            [node, *NODE_FLAGS, "-e", ""],
            capture_output=True,
            text=True,
            timeout=PREFLIGHT_TIMEOUT,
            env={},
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"Node.js preflight failed: {exc}") from exc
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "unknown Node.js error").strip()
        raise RuntimeError(f"Node.js preflight failed: {error}")
    return node


def validate_javascript_code_safety(code):
    if not isinstance(code, str):
        return 1, "", "JavaScript code must be a string."
    if len(code.encode("utf-8")) > MAX_CODE_BYTES:
        return 1, "", f"JavaScript source exceeds the {MAX_CODE_BYTES}-byte limit."
    try:
        ensure_javascript_runtime()
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return 1, "", str(exc)
    return 0, "Safety OK", ""


def syntax_check_javascript(code):
    exit_code, stdout, stderr = validate_javascript_code_safety(code)
    if exit_code != 0:
        return exit_code, stdout, stderr

    try:
        result = subprocess.run(
            [ensure_javascript_runtime(), *NODE_FLAGS, "--check", "-"],
            input=code,
            capture_output=True,
            text=True,
            timeout=SYNTAX_CHECK_TIMEOUT,
            env={},
        )
        if result.returncode == 0:
            return 0, "Syntax OK", ""
        error = (result.stderr or result.stdout or "JavaScript syntax check failed").strip()
        return 1, "", error
    except subprocess.TimeoutExpired:
        return 1, "", "JavaScript syntax check timed out"
    except OSError as exc:
        return 1, "", f"Failed to run node: {exc}"


def execute_javascript_code(code, timeout=10):
    exit_code, _, safety_error = validate_javascript_code_safety(code)
    if exit_code != 0:
        return f"Error: {safety_error}"

    try:
        timeout_ms = max(1, int(float(timeout) * 1000))
        result = subprocess.run(
            [ensure_javascript_runtime(), *NODE_FLAGS, "-e", JAVASCRIPT_RUNNER, str(timeout_ms)],
            input=code,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={},
        )
        if result.returncode != 0:
            error = (result.stderr or "JavaScript execution failed").strip()
            return f"Error: JavaScript execution failed: {error}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: JavaScript program execution timed out"
    except (OSError, TypeError, ValueError) as exc:
        return f"Error: Failed to run node: {exc}"
