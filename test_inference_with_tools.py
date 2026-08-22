import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


def load_tool_module():
    path = Path(__file__).with_name("inference-with-tools.py")
    spec = importlib.util.spec_from_file_location("inference_with_tools", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


tools = load_tool_module()


class JavaScriptToolSyntaxTests(unittest.TestCase):
    def test_javascript_preflight_runs_before_tool_inference_setup(self):
        with patch.object(
            sys,
            "argv",
            ["inference-with-tools.py", "--language", "javascript"],
        ), patch.object(
            tools,
            "ensure_javascript_runtime",
            side_effect=RuntimeError("Node.js preflight failed"),
        ) as preflight, patch.object(tools.os, "chdir") as chdir:
            with self.assertRaisesRegex(RuntimeError, "Node.js preflight failed"):
                tools.main()

        preflight.assert_called_once_with()
        chdir.assert_not_called()

    def test_javascript_tool_prompt_removes_fences_and_complete_example(self):
        template_path = Path(__file__).with_name("templates") / "template_javascript.md"
        template = template_path.read_text(encoding="utf-8")

        prompt = tools.build_tool_prompt(template, "Add two numbers.", "javascript")

        self.assertNotIn("Wrap your code", prompt)
        self.assertNotIn("EXAMPLE FORMAT", prompt)
        self.assertNotIn("let sum = 0", prompt)
        self.assertNotIn("This would output", prompt)
        self.assertNotIn("```", prompt)
        self.assertIn("Now solve the problem above", prompt)
        self.assertIn("Produce only runnable javascript source code", prompt)

    def test_tool_schema_advertises_javascript(self):
        syntax_tool = next(
            tool for tool in tools.TOOLS
            if tool["function"]["name"] == "syntax_check"
        )
        languages = syntax_tool["function"]["parameters"]["properties"]["language"]["enum"]

        self.assertIn("javascript", languages)
        self.assertEqual(tools.get_extension("javascript"), "js")
        self.assertEqual(
            tools.get_tooling_score_name("javascript", 200),
            "javascript-200-tool",
        )
        self.assertEqual(
            tools.get_tooling_series_name("javascript", 200),
            "javascript-200-tool-test",
        )

    def test_valid_javascript_passes_virtual_syntax_check(self):
        vfs = tools.VirtualFileSystem({"solution.js": "console.log(6 * 7);"})

        result = tools.run_syntax_check(
            vfs, {"language": "javascript", "path": "solution.js"}
        )

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "Syntax OK")
        self.assertEqual(result.stderr, "")

    def test_invalid_javascript_fails_virtual_syntax_check(self):
        vfs = tools.VirtualFileSystem({"solution.js": "const answer = ;"})

        result = tools.run_syntax_check(
            vfs, {"language": "javascript", "path": "solution.js"}
        )

        self.assertEqual(result.exit_code, 1)
        self.assertIn("SyntaxError", result.stderr)


if __name__ == "__main__":
    unittest.main()
