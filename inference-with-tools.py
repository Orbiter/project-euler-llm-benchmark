#!/usr/bin/env python3
import argparse
import ast
import json
import math
import posixpath
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import requests


SYSTEM_PROMPT = (
    "You are a coding agent working inside a virtual file system. You do not have "
    "access to the real shell or the real file system. Use the provided tools to "
    "inspect files, update files in the virtual file system, and check syntax. "
    "Prefer iterating by checking syntax after edits and fixing errors you "
    "observe. When the task is finished, you must call deliver_code to return the "
    "final code, either by passing the full code directly or by naming a file "
    "from the virtual file system. Do not stop before calling deliver_code. Use "
    "short answers."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files currently present in the virtual file system.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the virtual file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Virtual workspace-relative file path.",
                    }
                },
                "required": ["path"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Replace or create a file in the virtual file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Virtual workspace-relative file path.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Exact full file content.",
                    },
                },
                "required": ["path", "content"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "syntax_check",
            "description": (
                "Check syntax for python, java, rust, or clojure using inline code "
                "or a file from the virtual file system."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Language to check: python, java, rust, or clojure.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional virtual workspace-relative file path.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Optional inline code content.",
                    },
                },
                "required": ["language"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a mathematical Python expression and return the result."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate.",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deliver_code",
            "description": (
                "Deliver the final answer for the coding task. Provide either the "
                "full code directly in content or a path to a file in the virtual "
                "file system."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional virtual workspace-relative file path to deliver.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Optional full code content to deliver directly.",
                    },
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]


@dataclass
class State:
    silent_mode: bool = False
    stdout_needs_newline: bool = False
    max_tool_calls: int = 3
    tool_call_counts: Dict[str, int] = field(default_factory=dict)


@dataclass
class ToolResult:
    exit_code: int
    stdout: str
    stderr: str


@dataclass
class DeliveryResult:
    delivered: bool
    content: str = ""
    path: str = ""


@dataclass
class VirtualFileSystem:
    files: Dict[str, str] = field(default_factory=dict)

    def list_files(self) -> List[str]:
        return sorted(self.files)

    def read_file(self, path: str) -> str:
        return self.files[path]

    def write_file(self, path: str, content: str) -> None:
        self.files[path] = content


def usage(model: str, host: str, port: str) -> str:
    return (
        f"Usage: opx.py [options] <prompt>\n"
        f"Options:\n"
        f"  -m <model>      model name (default: {model})\n"
        f"  -h <host>       hostname (default: {host})\n"
        f"  -p <port>       port number (default: {port})\n"
        f"  --max-tool-calls <n>  max calls per tool (default: 3)\n"
        f"  -s              silent mode; print only final LLM output\n"
        f"  --help          show help and exit\n"
    )


def parse_args(argv: List[str]) -> Tuple[argparse.Namespace, str]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-m", dest="model", default="qwen3.5:4b")
    parser.add_argument("-h", dest="host", default="localhost")
    parser.add_argument("-p", dest="port", default="11434")
    parser.add_argument("--max-tool-calls", dest="max_tool_calls", type=int, default=3)
    parser.add_argument("-s", dest="silent_mode", action="store_true")
    parser.add_argument("--help", action="store_true")
    parser.add_argument("prompt", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.help:
        print(usage(args.model, args.host, args.port), end="")
        raise SystemExit(0)

    prompt_parts = args.prompt
    if prompt_parts and prompt_parts[0] == "--":
        prompt_parts = prompt_parts[1:]
    if not prompt_parts:
        print(usage(args.model, args.host, args.port), file=sys.stderr, end="")
        raise SystemExit(1)
    if args.max_tool_calls < 1:
        print("--max-tool-calls must be at least 1", file=sys.stderr)
        raise SystemExit(1)
    return args, " ".join(prompt_parts)


def log(state: State, message: str) -> None:
    if state.silent_mode:
        return
    if state.stdout_needs_newline:
        print(file=sys.stderr)
        state.stdout_needs_newline = False
    print(f"[opx] {message}", file=sys.stderr)


def print_tool_output(state: State, output: str) -> None:
    if state.silent_mode or not output:
        return
    if state.stdout_needs_newline:
        print()
        state.stdout_needs_newline = False
    for line in output.splitlines() or [""]:
        print(f"[tool] {line}")


def append_extra_input(prompt: str) -> str:
    if sys.stdin.isatty():
        return prompt
    extra = sys.stdin.read()
    if not extra:
        return prompt
    return f"{prompt}\n\n```\n{extra}\n```"


def normalize_virtual_path(path: str) -> str:
    if not path:
        raise ValueError("Path must not be empty.")
    normalized = posixpath.normpath(path.replace("\\", "/"))
    if normalized in (".", ""):
        raise ValueError("Path must not be empty.")
    if normalized.startswith("../") or normalized == ".." or normalized.startswith("/"):
        raise ValueError("Path must be workspace-relative.")
    return normalized


def resolve_code_input(vfs: VirtualFileSystem, parsed_args: dict) -> Tuple[str, str]:
    raw_path = parsed_args.get("path", "")
    raw_content = parsed_args.get("content", "")

    if raw_path:
        path = normalize_virtual_path(raw_path)
        if path not in vfs.files:
            raise ValueError(f"File not found: {path}")
        return path, vfs.read_file(path)

    if raw_content:
        return "", raw_content

    raise ValueError("Either path or content is required.")


def syntax_check_python(code: str, filename: str) -> ToolResult:
    try:
        ast.parse(code, filename=filename or "<inline>")
        return ToolResult(exit_code=0, stdout="Syntax OK", stderr="")
    except SyntaxError as exc:
        location = f"line {exc.lineno}, column {exc.offset}"
        return ToolResult(exit_code=1, stdout="", stderr=f"SyntaxError at {location}: {exc.msg}")


def syntax_check_java(code: str) -> ToolResult:
    temp_dir = tempfile.mkdtemp(prefix="opx_java_")
    try:
        source_path = posixpath.join(temp_dir.replace("\\", "/"), "Main.java")
        with open(source_path, "w", encoding="utf-8") as handle:
            handle.write(code)
        result = subprocess.run(
            ["javac", source_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return ToolResult(exit_code=0, stdout="Syntax OK", stderr="")
        stderr = (result.stderr or result.stdout or "Java syntax check failed").strip()
        return ToolResult(exit_code=1, stdout="", stderr=stderr)
    except OSError as exc:
        return ToolResult(exit_code=1, stdout="", stderr=f"Failed to run javac: {exc}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def syntax_check_rust(code: str) -> ToolResult:
    temp_dir = tempfile.mkdtemp(prefix="opx_rust_")
    try:
        source_path = posixpath.join(temp_dir.replace("\\", "/"), "main.rs")
        output_path = posixpath.join(temp_dir.replace("\\", "/"), "main")
        with open(source_path, "w", encoding="utf-8") as handle:
            handle.write(code)
        result = subprocess.run(
            ["rustc", "--emit", "metadata", "-o", output_path, source_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return ToolResult(exit_code=0, stdout="Syntax OK", stderr="")
        stderr = (result.stderr or result.stdout or "Rust syntax check failed").strip()
        return ToolResult(exit_code=1, stdout="", stderr=stderr)
    except OSError as exc:
        return ToolResult(exit_code=1, stdout="", stderr=f"Failed to run rustc: {exc}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def syntax_check_clojure(code: str) -> ToolResult:
    pairs = {"(": ")", "[": "]", "{": "}"}
    closing = {")": "(",
        "]": "[",
        "}": "{",
    }
    stack: List[Tuple[str, int]] = []
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
                return ToolResult(exit_code=1, stdout="", stderr=f"Unmatched '{char}' at line {line}")
            stack.pop()

    if in_string:
        return ToolResult(exit_code=1, stdout="", stderr="Unterminated string literal")
    if stack:
        opener, opener_line = stack[-1]
        return ToolResult(exit_code=1, stdout="", stderr=f"Unclosed '{opener}' from line {opener_line}")
    return ToolResult(exit_code=0, stdout="Parentheses OK", stderr="")


def run_calculator(expression: str) -> ToolResult:
    if not expression or not expression.strip():
        return ToolResult(exit_code=1, stdout="", stderr="expression must not be empty.")

    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        return ToolResult(exit_code=1, stdout="", stderr=f"Invalid expression: {exc.msg}")

    allowed_names = {
        name: getattr(math, name)
        for name in dir(math)
        if not name.startswith("_")
    }
    allowed_names.update(
        {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
        }
    )

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Tuple,
        ast.List,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
    )

    for node in ast.walk(parsed):
        if not isinstance(node, allowed_nodes):
            return ToolResult(
                exit_code=1,
                stdout="",
                stderr=f"Unsupported expression element: {type(node).__name__}",
            )
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in allowed_names:
                return ToolResult(exit_code=1, stdout="", stderr="Unsupported function call.")
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            return ToolResult(exit_code=1, stdout="", stderr=f"Unknown name: {node.id}")

    try:
        value = eval(compile(parsed, "<calculator>", "eval"), {"__builtins__": {}}, allowed_names)
    except Exception as exc:
        return ToolResult(exit_code=1, stdout="", stderr=f"Calculation error: {exc}")

    return ToolResult(exit_code=0, stdout=str(value), stderr="")


def run_syntax_check(vfs: VirtualFileSystem, parsed_args: dict) -> ToolResult:
    language = (parsed_args.get("language") or "").strip().lower()
    if language not in {"python", "java", "rust", "clojure"}:
        return ToolResult(
            exit_code=1,
            stdout="",
            stderr="language must be one of: python, java, rust, clojure.",
        )

    try:
        filename, code = resolve_code_input(vfs, parsed_args)
    except ValueError as exc:
        return ToolResult(exit_code=1, stdout="", stderr=str(exc))

    if language == "python":
        return syntax_check_python(code, filename)
    if language == "java":
        return syntax_check_java(code)
    if language == "rust":
        return syntax_check_rust(code)
    return syntax_check_clojure(code)


def extract_text_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "".join(parts)
    return ""


def extract_response_fields(response_json: dict, state: State) -> Tuple[str, str, str, str]:
    message = response_json.get("choices", [{}])[0].get("message", {})
    chunk = extract_text_content(message.get("content"))
    tool_calls = message.get("tool_calls") or []
    if not tool_calls:
        log(state, "Model returned a final answer without a tool call.")
        return chunk, "", "", ""

    first_call = tool_calls[0]
    function = first_call.get("function", {})
    tool_name = function.get("name") or first_call.get("name") or ""
    tool_id = first_call.get("id", "")
    raw_args = function.get("arguments", "")
    return chunk, tool_name, tool_id, raw_args


def tool_result_json(tool_name: str, result: ToolResult) -> str:
    return json.dumps(
        {
            "tool": tool_name,
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    )


def get_visible_tools(state: State) -> List[dict]:
    visible_tools = []
    for tool in TOOLS:
        tool_name = tool["function"]["name"]
        if state.tool_call_counts.get(tool_name, 0) < state.max_tool_calls:
            visible_tools.append(tool)
    return visible_tools


def run_virtual_tool(state: State, vfs: VirtualFileSystem, tool_name: str, parsed_args: dict) -> ToolResult:
    if tool_name == "list_files":
        listing = "\n".join(vfs.list_files())
        return ToolResult(exit_code=0, stdout=listing, stderr="")

    if tool_name == "read_file":
        try:
            path = normalize_virtual_path(parsed_args.get("path", ""))
        except ValueError as exc:
            return ToolResult(exit_code=1, stdout="", stderr=str(exc))
        if path not in vfs.files:
            return ToolResult(exit_code=1, stdout="", stderr=f"File not found: {path}")
        return ToolResult(exit_code=0, stdout=vfs.read_file(path), stderr="")

    if tool_name == "write_file":
        try:
            path = normalize_virtual_path(parsed_args.get("path", ""))
        except ValueError as exc:
            return ToolResult(exit_code=1, stdout="", stderr=str(exc))
        vfs.write_file(path, parsed_args.get("content", ""))
        return ToolResult(exit_code=0, stdout=f"Wrote {path}", stderr="")

    if tool_name == "syntax_check":
        return run_syntax_check(vfs, parsed_args)

    if tool_name == "calculator":
        return run_calculator(parsed_args.get("expression", ""))

    return ToolResult(exit_code=1, stdout="", stderr=f"Unsupported tool: {tool_name}")


def handle_deliver_code(vfs: VirtualFileSystem, parsed_args: dict) -> Tuple[ToolResult, DeliveryResult]:
    raw_path = parsed_args.get("path", "")
    raw_content = parsed_args.get("content", "")

    if raw_path:
        try:
            path = normalize_virtual_path(raw_path)
        except ValueError as exc:
            return ToolResult(exit_code=1, stdout="", stderr=str(exc)), DeliveryResult(delivered=False)
        if path not in vfs.files:
            return (
                ToolResult(exit_code=1, stdout="", stderr=f"File not found: {path}"),
                DeliveryResult(delivered=False),
            )
        return (
            ToolResult(exit_code=0, stdout=f"Delivered {path}", stderr=""),
            DeliveryResult(delivered=True, content=vfs.read_file(path), path=path),
        )

    if raw_content:
        return (
            ToolResult(exit_code=0, stdout="Delivered inline content", stderr=""),
            DeliveryResult(delivered=True, content=raw_content, path=""),
        )

    return (
        ToolResult(
            exit_code=1,
            stdout="",
            stderr="deliver_code requires either path or content.",
        ),
        DeliveryResult(delivered=False),
    )


def handle_tool_call(
    state: State,
    vfs: VirtualFileSystem,
    messages: List[dict],
    tool_name: str,
    tool_id: str,
    tool_args_unescaped: str,
) -> DeliveryResult:
    if not tool_name or not tool_args_unescaped:
        return DeliveryResult(delivered=False)

    try:
        parsed_args = json.loads(tool_args_unescaped)
    except json.JSONDecodeError:
        return DeliveryResult(delivered=False)

    if state.tool_call_counts.get(tool_name, 0) >= state.max_tool_calls:
        result = ToolResult(
            exit_code=1,
            stdout="",
            stderr=f"Tool {tool_name} is no longer available because it reached the call limit.",
        )
        delivery = DeliveryResult(delivered=False)
    else:
        state.tool_call_counts[tool_name] = state.tool_call_counts.get(tool_name, 0) + 1
        log(
            state,
            f"Executing virtual tool: {tool_name} "
            f"({state.tool_call_counts[tool_name]}/{state.max_tool_calls}).",
        )
        if tool_name == "deliver_code":
            result, delivery = handle_deliver_code(vfs, parsed_args)
        else:
            result = run_virtual_tool(state, vfs, tool_name, parsed_args)
            delivery = DeliveryResult(delivered=False)
    print_tool_output(state, result.stdout if result.stdout else result.stderr)

    call_id = tool_id or "call_1"
    messages.append(
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": tool_args_unescaped,
                    },
                }
            ],
        }
    )
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call_id,
            "content": tool_result_json(tool_name, result),
        }
    )
    log(state, f"Virtual tool finished with exit code {result.exit_code}: {tool_name}.")
    return delivery


def main() -> int:
    args, prompt = parse_args(sys.argv[1:])
    state = State(silent_mode=args.silent_mode, max_tool_calls=args.max_tool_calls)
    prompt = append_extra_input(prompt)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    vfs = VirtualFileSystem()
    log(state, "Initialized conversation with system prompt and user prompt.")

    url = f"http://{args.host}:{args.port}/v1/chat/completions"
    reasoning_effort = "none"
    delivered = DeliveryResult(delivered=False)

    while True:
        log(state, "Starting agent loop turn.")
        visible_tools = get_visible_tools(state)
        payload = {
            "model": args.model,
            "reasoning_effort": reasoning_effort,
            "messages": messages,
            "tools": visible_tools,
            "stream": False,
        }

        log(state, f"Sending conversation to model {args.model} at {args.host}:{args.port}.")
        try:
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
        except requests.RequestException:
            print("Network error", file=sys.stderr)
            return 1

        try:
            response_json = response.json()
        except ValueError:
            print("Network error", file=sys.stderr)
            return 1

        chunk, tool_name, tool_id, tool_args_unescaped = extract_response_fields(response_json, state)
        if chunk:
            print(chunk, end="", flush=True)
            state.stdout_needs_newline = not chunk.endswith("\n")

        delivery = handle_tool_call(state, vfs, messages, tool_name, tool_id, tool_args_unescaped)
        if delivery.delivered:
            delivered = delivery
            continue

        if tool_name:
            log(state, "Tool result appended to the conversation; continuing the loop.")
            continue

        if state.stdout_needs_newline:
            print()
            state.stdout_needs_newline = False
        if not delivered.delivered:
            print("Error: task is not complete until deliver_code is called.", file=sys.stderr)
            return 1
        log(state, "Agent loop finished.")
        print(delivered.content, end="")
        if delivered.content and not delivered.content.endswith("\n"):
            print()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
