#!/usr/bin/env python3
import ast
import base64
import json
import math
import os
import posixpath
import shutil
import subprocess
import sys
import tempfile
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from io import BytesIO
from typing import Dict, List, Tuple

import requests
from PIL import Image

from benchmark import read_benchmark, write_benchmark
from llm_client import (
    Endpoint,
    ollama_pull,
    openai_api_check_exist,
    openai_api_list,
)
from llm_modal_test import ensure_model_capabilities


SYSTEM_PROMPT = (
    "You are a coding agent operating in a virtual workspace. "
    "You can only act by calling the provided tools. "
    "Use this workflow: inspect the workspace, read files when needed, write or "
    "rewrite complete files, run syntax checks, and continue until the program is ready. "
    "When the final program is ready, call deliver_code exactly once. "
    "Do not end with plain text. Every assistant turn must contain a tool call. "
    "If you need to explain progress, put that explanation in the assistant message that accompanies the tool call. "
    "Return runnable source code with no markdown fences in delivered content."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": (
                "List the current virtual workspace files. Use this first when you need "
                "to discover what files exist."
            ),
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
            "description": (
                "Read one virtual workspace file by relative path. Use this to inspect "
                "existing code before editing."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Virtual workspace-relative file path.",
                        "minLength": 1,
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
            "description": (
                "Create or fully replace one virtual workspace file. The content must be "
                "the complete file contents, not a diff."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Virtual workspace-relative file path.",
                        "minLength": 1,
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
            "name": "delete_file",
            "description": "Delete one virtual workspace file by relative path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Virtual workspace-relative file path.",
                        "minLength": 1,
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
            "name": "rename_file",
            "description": (
                "Rename or move one virtual workspace file from `source_path` to "
                "`destination_path`."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "Existing virtual workspace-relative file path.",
                        "minLength": 1,
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "New virtual workspace-relative file path.",
                        "minLength": 1,
                    },
                },
                "required": ["source_path", "destination_path"],
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
                "Check syntax for python, java, rust, or clojure. Provide exactly one of "
                "`path` or `content`. Prefer `path` after writing a file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Language to check.",
                        "enum": ["python", "java", "rust", "clojure"],
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional virtual workspace-relative file path.",
                        "minLength": 1,
                    },
                    "content": {
                        "type": "string",
                        "description": "Optional inline code content.",
                        "minLength": 1,
                    },
                },
                "required": ["language"],
                "oneOf": [
                    {"required": ["path"]},
                    {"required": ["content"]},
                ],
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
                "Evaluate a mathematical expression for planning or verification. "
                "Use only for arithmetic, not for general code execution."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate.",
                        "minLength": 1,
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
                "Finish the task and deliver the final runnable program. Provide exactly "
                "one of `path` or `content`. Call this only when the code is complete."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional virtual workspace-relative file path to deliver.",
                        "minLength": 1,
                    },
                    "content": {
                        "type": "string",
                        "description": "Optional full code content to deliver directly.",
                        "minLength": 1,
                    },
                },
                "oneOf": [
                    {"required": ["path"]},
                    {"required": ["content"]},
                ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

MAX_TOOL_CALLS = 12
@dataclass
class State:
    max_tool_calls: int = MAX_TOOL_CALLS
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

    def delete_file(self, path: str) -> None:
        del self.files[path]

    def rename_file(self, source_path: str, destination_path: str) -> None:
        self.files[destination_path] = self.files.pop(source_path)


def read_template(template_path):
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def get_extension(language):
    if language == "java":
        return "java"
    if language == "rust":
        return "rs"
    if language == "python":
        return "py"
    if language == "clojure":
        return "clj"
    raise Exception(f"Unsupported language: {language}")


def log(message: str) -> None:
    print(f"[tool-inference] {message}")


def preview_text(text: str, limit: int = 160) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def summarize_tool_args(tool_name: str, parsed_args: dict) -> str:
    if tool_name in {"read_file", "write_file", "delete_file", "deliver_code"}:
        path = parsed_args.get("path")
        if path:
            return f"path={path}"
    if tool_name == "rename_file":
        source_path = parsed_args.get("source_path")
        destination_path = parsed_args.get("destination_path")
        if source_path and destination_path:
            return f"source_path={source_path} destination_path={destination_path}"
    if tool_name == "syntax_check":
        language = parsed_args.get("language", "?")
        path = parsed_args.get("path")
        if path:
            return f"language={language} path={path}"
        return f"language={language} inline-content"
    if tool_name == "calculator":
        expr = parsed_args.get("expression", "")
        return f"expression={preview_text(expr, 80)}"
    return ""


def summarize_response(response_json: dict) -> str:
    message = response_json.get("choices", [{}])[0].get("message", {})
    chunk = extract_text_content(message.get("content"))
    tool_calls = message.get("tool_calls") or []
    if tool_calls:
        first_call = tool_calls[0]
        function = first_call.get("function", {})
        tool_name = function.get("name") or first_call.get("name") or "unknown_tool"
        raw_args = function.get("arguments", "")
        try:
            parsed_args = json.loads(raw_args) if raw_args else {}
        except json.JSONDecodeError:
            parsed_args = {}
        detail = summarize_tool_args(tool_name, parsed_args)
        if chunk and detail:
            return f"model plans to {tool_name} ({detail}); note={preview_text(chunk, 120)}"
        if detail:
            return f"model plans to {tool_name} ({detail})"
        if chunk:
            return f"model plans to {tool_name}; note={preview_text(chunk, 120)}"
        return f"model plans to {tool_name}"
    if chunk:
        return f"model replied without a tool call: {preview_text(chunk, 120)}"
    return "model returned neither tool call nor text"


def describe_next_agent_step(messages: List[dict], vfs: VirtualFileSystem) -> str:
    if not vfs.files:
        return "asking the agent to inspect the empty workspace and draft the first solution file"
    last_message = messages[-1] if messages else {}
    if last_message.get("role") == "tool":
        return "asking the agent to use the latest tool result and continue editing or deliver the final code"
    return "asking the agent to continue the coding loop with the next tool call"


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
        result = subprocess.run(["javac", source_path], capture_output=True, text=True)
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
    closing = {")": "(", "]": "[", "}": "{"}
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

    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
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


def extract_response_fields(response_json: dict) -> Tuple[str, str, str, str]:
    message = response_json.get("choices", [{}])[0].get("message", {})
    chunk = extract_text_content(message.get("content"))
    tool_calls = message.get("tool_calls") or []
    if not tool_calls:
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


def run_virtual_tool(vfs: VirtualFileSystem, tool_name: str, parsed_args: dict) -> ToolResult:
    if tool_name == "list_files":
        return ToolResult(exit_code=0, stdout="\n".join(vfs.list_files()), stderr="")

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

    if tool_name == "delete_file":
        try:
            path = normalize_virtual_path(parsed_args.get("path", ""))
        except ValueError as exc:
            return ToolResult(exit_code=1, stdout="", stderr=str(exc))
        if path not in vfs.files:
            return ToolResult(exit_code=1, stdout="", stderr=f"File not found: {path}")
        vfs.delete_file(path)
        return ToolResult(exit_code=0, stdout=f"Deleted {path}", stderr="")

    if tool_name == "rename_file":
        try:
            source_path = normalize_virtual_path(parsed_args.get("source_path", ""))
            destination_path = normalize_virtual_path(parsed_args.get("destination_path", ""))
        except ValueError as exc:
            return ToolResult(exit_code=1, stdout="", stderr=str(exc))
        if source_path not in vfs.files:
            return ToolResult(exit_code=1, stdout="", stderr=f"File not found: {source_path}")
        if destination_path in vfs.files:
            return ToolResult(
                exit_code=1,
                stdout="",
                stderr=f"Destination already exists: {destination_path}",
            )
        vfs.rename_file(source_path, destination_path)
        return ToolResult(
            exit_code=0,
            stdout=f"Renamed {source_path} to {destination_path}",
            stderr="",
        )

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
        ToolResult(exit_code=1, stdout="", stderr="deliver_code requires either path or content."),
        DeliveryResult(delivered=False),
    )


def handle_tool_call(
    state: State,
    vfs: VirtualFileSystem,
    messages: List[dict],
    assistant_content: str,
    tool_name: str,
    tool_id: str,
    tool_args_unescaped: str,
    problem_number: str,
) -> DeliveryResult:
    if not tool_name or not tool_args_unescaped:
        log(f"[{problem_number}] Model returned no tool call.")
        return DeliveryResult(delivered=False)

    try:
        parsed_args = json.loads(tool_args_unescaped)
    except json.JSONDecodeError:
        result = ToolResult(exit_code=1, stdout="", stderr="Tool arguments are not valid JSON.")
        delivery = DeliveryResult(delivered=False)
        log(f"[{problem_number}] Executing {tool_name}: invalid JSON arguments.")
    else:
        summary = summarize_tool_args(tool_name, parsed_args)
        if summary:
            log(f"[{problem_number}] Executing {tool_name}: {summary}")
        else:
            log(f"[{problem_number}] Executing {tool_name}.")
        if state.tool_call_counts.get(tool_name, 0) >= state.max_tool_calls:
            result = ToolResult(
                exit_code=1,
                stdout="",
                stderr=f"Tool {tool_name} is no longer available because it reached the call limit.",
            )
            delivery = DeliveryResult(delivered=False)
        else:
            state.tool_call_counts[tool_name] = state.tool_call_counts.get(tool_name, 0) + 1
            if tool_name == "deliver_code":
                result, delivery = handle_deliver_code(vfs, parsed_args)
            else:
                result = run_virtual_tool(vfs, tool_name, parsed_args)
                delivery = DeliveryResult(delivered=False)

    call_id = tool_id or "call_1"
    messages.append(
        {
            "role": "assistant",
            "content": assistant_content or "",
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
    log(
        f"[{problem_number}] Tool finished: {tool_name} exit={result.exit_code} "
        f"stdout={preview_text(result.stdout, 120) if result.stdout else ''} "
        f"stderr={preview_text(result.stderr, 120) if result.stderr else ''}"
    )
    return delivery


def build_user_message(prompt: str, base64_image: str = None) -> dict:
    if not base64_image:
        return {"role": "user", "content": prompt}

    image_type = "jpeg"
    magic_types = {"/9j/": "jpeg", "iVBO": "png", "R0lG": "gif"}
    for magic, candidate in magic_types.items():
        if base64_image.startswith(magic):
            image_type = candidate
            break
    if image_type == "gif":
        image = Image.open(BytesIO(base64.b64decode(base64_image)))
        png_image = BytesIO()
        image.save(png_image, format="PNG")
        base64_image = base64.b64encode(png_image.getvalue()).decode("utf-8")
        image_type = "png"

    return {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{image_type};base64,{base64_image}"}},
        ],
    }


def run_tool_agent(
    endpoint: Endpoint,
    prompt: str,
    problem_number: str,
    base64_image: str = None,
    think: bool = False,
    no_think: bool = False,
) -> str:
    state = State()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        build_user_message(prompt, base64_image=base64_image),
    ]
    vfs = VirtualFileSystem()
    url = endpoint.url
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if endpoint.key:
        headers["Authorization"] = f"Bearer {endpoint.key}"
    delivered = DeliveryResult(delivered=False)

    for turn in range(MAX_TOOL_CALLS * 4):
        payload = {
            "model": endpoint.model_name,
            "messages": messages,
            "tools": get_visible_tools(state),
            "tool_choice": "required",
            "parallel_tool_calls": False,
            "stream": False,
            "temperature": 0.0,
        }
        if no_think:
            payload["reasoning_effort"] = "none"
            payload["enable_thinking"] = False
        elif think:
            payload["enable_thinking"] = True

        log(
            f"[{problem_number}] Turn {turn + 1}: "
            f"{describe_next_agent_step(messages, vfs)}."
        )
        response = requests.post(url, headers=headers, json=payload, verify=False, timeout=600)
        response.raise_for_status()
        response_json = response.json()
        log(f"[{problem_number}] Turn {turn + 1}: {summarize_response(response_json)}")

        chunk, tool_name, tool_id, tool_args_unescaped = extract_response_fields(response_json)
        if chunk:
            log(f"[{problem_number}] Assistant text: {preview_text(chunk, 220)}")
        else:
            log(f"[{problem_number}] Assistant returned no text chunk.")

        if not tool_name:
            if chunk:
                messages.append({"role": "assistant", "content": chunk})
            raise RuntimeError(
                f"Model violated tool-calling contract on turn {turn + 1}: "
                "assistant response did not include a tool call."
            )

        delivery = handle_tool_call(
            state,
            vfs,
            messages,
            chunk,
            tool_name,
            tool_id,
            tool_args_unescaped,
            problem_number,
        )
        if delivery.delivered:
            log(f"[{problem_number}] deliver_code succeeded.")
            delivered = delivery
            break

    if not delivered.delivered:
        raise RuntimeError("Task is not complete until deliver_code is called.")
    return delivered.content


def process_single_problem(
    endpoint: Endpoint,
    language: str,
    problem_number: str,
    prompt: str,
    output_path: str,
    base64_image: str = None,
    think: bool = False,
    no_think: bool = False,
) -> None:
    code = run_tool_agent(
        endpoint,
        prompt,
        problem_number,
        base64_image=base64_image,
        think=think,
        no_think=no_think,
    )
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(code)
    log(f"Saved {language} solution for problem {problem_number} to {output_path}")


def prepare_endpoints(endpoints: List[Endpoint]) -> List[Endpoint]:
    available_endpoints = []
    for endpoint in endpoints:
        for _ in range(0, 3):
            try:
                ollama_pull(endpoint)
                if openai_api_check_exist(endpoint):
                    available_endpoints.append(endpoint)
                    break
            except Exception as e:
                print(f"Error loading endpoint {endpoint}: {e}")
        if endpoint not in available_endpoints:
            print(f"Failed to load endpoint {endpoint} after 3 attempts.")
    return available_endpoints


def build_tool_prompt(template_content: str, problem_content: str, language: str) -> str:
    prompt = template_content.replace("$$$PROBLEM$$$", problem_content)
    prompt = remove_code_block_instructions(prompt, language)
    return (
        f"{prompt}\n\n"
        "Additional instructions:\n"
        f"- Produce only runnable {language} source code.\n"
        "- Use the tools to draft files, inspect them, and check syntax before delivery.\n"
        "- Finish by calling deliver_code with the final full source code.\n"
        "- Do not return markdown fences or explanations in the delivered code.\n"
    )


def remove_code_block_instructions(prompt: str, language: str) -> str:
    lines = prompt.splitlines()
    filtered_lines: List[str] = []
    skip_example_block = False

    for line in lines:
        stripped = line.strip()
        if stripped == f"- Wrap your code in a {language} code block using triple backticks":
            continue
        if stripped == "EXAMPLE FORMAT:":
            skip_example_block = True
            continue
        if skip_example_block:
            if stripped.startswith("This would output ") or stripped == "":
                if stripped.startswith("This would output "):
                    skip_example_block = False
                continue
            if stripped.startswith("```") or stripped.startswith("print("):
                continue
        filtered_lines.append(line)

    cleaned = "\n".join(filtered_lines)
    cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned


def process_problem_files(
    problems_dir,
    template_content,
    endpoints: List[Endpoint],
    language,
    max_problem_number=9999,
    overwrite_existing=False,
    overwrite_failed=False,
    expected_solutions={},
    think=False,
    no_think=False,
):
    del expected_solutions
    print(f"Processing problems in {problems_dir} with language {language} and endpoint: {endpoints[0]}")
    store_name = endpoints[0].store_name
    if think:
        store_name += "-think"
    if no_think:
        store_name += "-no_think"
    solutions_dir = os.path.join("solutions", store_name, language)
    os.makedirs(solutions_dir, exist_ok=True)
    extension = get_extension(language)

    while not openai_api_check_exist(endpoints[0]):
        ollama_pull(endpoints[0])

    available_endpoints = prepare_endpoints(endpoints)
    if not available_endpoints:
        raise Exception("No usable endpoints are available.")

    benchmark = read_benchmark()
    entry = benchmark.get(store_name, {})
    entry, entry_changed = ensure_model_capabilities(entry, available_endpoints[0], think=think, no_think=no_think)
    if entry_changed:
        benchmark[store_name] = entry
        write_benchmark(benchmark)
    has_tool_calling = bool(entry.get("tooling", False))

    if not has_tool_calling:
        raise Exception(f"Model {store_name} does not support tool calling on {available_endpoints[0].url}")
    is_vision = bool(entry.get("vision", False))

    problem_jobs = []
    for problem_file in sorted(os.listdir(problems_dir)):
        if problem_file.startswith(".") or not problem_file.endswith(".txt"):
            continue
        problem_number = problem_file[:-4]
        if int(problem_number) > max_problem_number:
            break

        output_path = os.path.join(solutions_dir, f"tool-{problem_number}.{extension}")
        if not overwrite_existing and not overwrite_failed and os.path.exists(output_path):
            print(f"Skipping problem {problem_number} as it already has a tool solution.")
            continue

        problem_path = os.path.join(problems_dir, problem_file)
        with open(problem_path, "r", encoding="utf-8") as file:
            problem_content = file.read()

        base64_image = None
        for ext in ["-0.png", "-0.jpg", "-0.gif"]:
            image_path = os.path.join(problems_dir, problem_number + ext)
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                break

        if base64_image and not is_vision:
            print(
                f"Problem {problem_number} requires a vision-capable model for image processing but the model lacks vision support."
            )
            base64_image = None

        prompt = build_tool_prompt(template_content, problem_content, language)
        problem_jobs.append((problem_number, prompt, output_path, base64_image))

    if not problem_jobs:
        print("No problems queued.")
        return

    with ThreadPoolExecutor(max_workers=len(available_endpoints)) as executor:
        future_to_problem = {}
        for index, (problem_number, prompt, output_path, base64_image) in enumerate(problem_jobs):
            endpoint = available_endpoints[index % len(available_endpoints)]
            future = executor.submit(
                process_single_problem,
                endpoint,
                language,
                problem_number,
                prompt,
                output_path,
                base64_image,
                think,
                no_think,
            )
            future_to_problem[future] = (problem_number, endpoint.store_name)
            print(f"Added problem {problem_number}, language {language}, model {endpoint.store_name} to processing queue")

        for future in as_completed(future_to_problem):
            problem_number, endpoint_name = future_to_problem[future]
            try:
                future.result()
                print(f"Processed problem {problem_number} with {endpoint_name}")
            except Exception as e:
                print(f"Failed problem {problem_number} with {endpoint_name}: {e}")

    print("All problems processed!")


def main():
    parser = ArgumentParser(description="Process Euler problems and send them to an LLM.")
    parser.add_argument("--api", action="append", help="Specify (multiple) backend OpenAI API endpoints (i.e. ollama); can be used multiple times")
    parser.add_argument("--api_base", required=False, default="http://localhost:11434", help="API base URL for the LLM or a list of such urls (comma-separated), default is http://localhost:11434")
    parser.add_argument("--endpoint", required=False, default="", help="Name of an <endpoint>.json file in the endpoints directory")
    parser.add_argument("--allmodels", action="store_true", help="loop over all models provided by ollama and run those which are missing in benchmark.json")
    parser.add_argument("--model", required=False, default="llama3.2:latest", help="Name of the model to use, default is llama3.2:latest")
    parser.add_argument("--think", action="store_true", help="enable thinking mode via backend request parameters (when supported)")
    parser.add_argument("--no_think", action="store_true", help="disable thinking mode via backend request parameters (when supported)")
    parser.add_argument("--language", required=False, default="python,java,rust,clojure", help="Name of the languages to test, default is python,java,rust,clojure")
    parser.add_argument("--overwrite_existing", action="store_true", help="if set, re-calculate all problems that already have an answer")
    parser.add_argument("--overwrite_failed", action="store_true", help="if set, re-calculate those problems with wrong answers")
    parser.add_argument("--n100", action="store_true", help="only 100 problems")
    parser.add_argument("--n200", action="store_true", help="only 200 problems")
    parser.add_argument("--n400", action="store_true", help="only 400 problems")
    parser.add_argument("--nall", action="store_true", help="all problems")

    args = parser.parse_args()
    api_base = args.api if args.api else args.api_base.split(",") if "," in args.api_base else [args.api_base]
    store_name = args.model
    max_problem_number = 200
    if args.n100:
        max_problem_number = 100
    if args.n200:
        max_problem_number = 200
    if args.n400:
        max_problem_number = 400
    if args.nall:
        max_problem_number = 9999

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    with open("solutions.json", "r", encoding="utf-8") as json_file:
        expected_solutions = json.load(json_file)

    languages = args.language.split(",")
    for language in languages:
        bench_name = f"{language}-{max_problem_number}"
        endpoint_name = args.endpoint
        problems_dir = "problems"
        template_path = os.path.join("templates", "template_" + language + ".md")

        if not os.path.exists(problems_dir):
            raise Exception(f"Problems directory {problems_dir} does not exist. You must create it using the problems_scraper.py script.")
        if not os.path.exists(template_path):
            raise Exception(f"Template file {template_path} does not exist.")

        template_content = read_template(template_path)

        if args.allmodels:
            if endpoint_name:
                raise Exception("The --allmodels option cannot be used in combination with --endpoint.")

            local_endpoint = Endpoint(store_name=store_name, model_name=store_name, key="", url=f"{api_base[0]}/v1/chat/completions")
            models = openai_api_list(local_endpoint)
            print(f"Found {len(models)} models in ollama.")
            for model in models:
                benchmark = read_benchmark()
                if model not in benchmark or bench_name not in benchmark[model]:
                    print(f"Inference with tools: Using model {model} and language {language}")
                    endpoints = [
                        Endpoint(store_name=model, model_name=model, key="", url=f"{api_stub}/v1/chat/completions")
                        for api_stub in api_base
                    ]
                    process_problem_files(
                        problems_dir,
                        template_content,
                        endpoints,
                        language,
                        max_problem_number=max_problem_number,
                        overwrite_existing=args.overwrite_existing,
                        overwrite_failed=args.overwrite_failed,
                        expected_solutions=expected_solutions,
                        think=args.think,
                        no_think=args.no_think,
                    )
        else:
            endpoints = []
            if endpoint_name:
                print(f"Inference with tools: Using endpoint {endpoint_name} and language {language}")
                endpoint_path = os.path.join("endpoints", f"{endpoint_name}.json")
                print(f"Using endpoint file {endpoint_path}")
                if not os.path.exists(endpoint_path):
                    raise Exception(f"Endpoint file {endpoint_path} does not exist.")
                with open(endpoint_path, "r", encoding="utf-8") as file:
                    endpoints = [Endpoint(**json.load(file))]
            else:
                print(f"Inference with tools: Using model {store_name} and language {language}")
                endpoints = [
                    Endpoint(store_name=store_name, model_name=store_name, key="", url=f"{api_stub}/v1/chat/completions")
                    for api_stub in api_base
                ]

            process_problem_files(
                problems_dir,
                template_content,
                endpoints,
                language,
                max_problem_number=max_problem_number,
                overwrite_existing=args.overwrite_existing,
                overwrite_failed=args.overwrite_failed,
                expected_solutions=expected_solutions,
                think=args.think,
                no_think=args.no_think,
            )


if __name__ == "__main__":
    main()
