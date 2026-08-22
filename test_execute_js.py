import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

import execute_js


class JavaScriptExecutionTests(unittest.TestCase):
    def tearDown(self):
        execute_js.ensure_javascript_runtime.cache_clear()

    def test_permission_model_and_heap_limit_are_enabled(self):
        self.assertIn("--permission", execute_js.NODE_FLAGS)
        self.assertIn("--no-addons", execute_js.NODE_FLAGS)
        self.assertIn("--no-global-search-paths", execute_js.NODE_FLAGS)
        self.assertIn(
            f"--max-old-space-size={execute_js.MAX_HEAP_MIB}",
            execute_js.NODE_FLAGS,
        )

    def test_complex_bigint_and_typed_array_computation(self):
        code = """
const limit = 10000;
const composite = new Uint8Array(limit);
let sum = 0n;
for (let number = 2; number < limit; number++) {
    if (composite[number]) continue;
    sum += BigInt(number);
    for (let multiple = number * number; multiple < limit; multiple += number) {
        composite[multiple] = 1;
    }
}
console.log(sum);
"""
        self.assertEqual(execute_js.execute_javascript_code(code), "5736396")

    def test_syntax_error_is_reported(self):
        exit_code, stdout, stderr = execute_js.syntax_check_javascript("const x = ;")

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("SyntaxError", stderr)

    def test_node_capabilities_are_not_exposed(self):
        output = execute_js.execute_javascript_code(
            "console.log(typeof process, typeof require, typeof fetch, typeof setTimeout)"
        )

        self.assertEqual(output, "undefined undefined undefined undefined")

    def test_dynamic_code_and_context_escape_are_blocked(self):
        eval_output = execute_js.execute_javascript_code("eval('console.log(42)')")
        escape_output = execute_js.execute_javascript_code(
            "console.log.constructor('return process')()"
        )

        self.assertIn("Code generation from strings disallowed", eval_output)
        self.assertIn("Code generation from strings disallowed", escape_output)

    def test_timeout_is_enforced(self):
        self.assertEqual(
            execute_js.execute_javascript_code("while (true) {}", timeout=0.2),
            "Error: JavaScript program execution timed out",
        )

    def test_source_and_output_limits_are_enforced(self):
        self.assertEqual(
            execute_js.validate_javascript_code_safety("x" * 1_000_001)[0], 1
        )

        limited_runner = execute_js.JAVASCRIPT_RUNNER.replace(
            "const outputLimit = 1000000;", "const outputLimit = 10;"
        )
        with patch.object(execute_js, "JAVASCRIPT_RUNNER", limited_runner):
            output = execute_js.execute_javascript_code("console.log('12345678901')")
        self.assertIn("Output limit exceeded", output)

    def test_preflight_uses_the_exact_sandbox_flags(self):
        execute_js.ensure_javascript_runtime.cache_clear()
        with patch.object(execute_js, "_secure_node_binary", return_value="node"), patch.object(
            execute_js.subprocess,
            "run",
            return_value=CompletedProcess([], 0, "", ""),
        ) as run:
            self.assertEqual(execute_js.ensure_javascript_runtime(), "node")

        command = run.call_args.args[0]
        self.assertEqual(command, ["node", *execute_js.NODE_FLAGS, "-e", ""])

    def test_preflight_reports_node_startup_failure(self):
        execute_js.ensure_javascript_runtime.cache_clear()
        with patch.object(execute_js, "_secure_node_binary", return_value="node"), patch.object(
            execute_js.subprocess,
            "run",
            return_value=CompletedProcess([], 1, "", "unsupported flag"),
        ):
            with self.assertRaisesRegex(RuntimeError, "Node.js preflight failed"):
                execute_js.ensure_javascript_runtime()


if __name__ == "__main__":
    unittest.main()
