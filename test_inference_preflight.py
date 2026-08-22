import sys
import unittest
from unittest.mock import patch

import inference


class StandardInferencePreflightTests(unittest.TestCase):
    def test_javascript_preflight_runs_before_endpoint_setup(self):
        with patch.object(
            sys, "argv", ["inference.py", "--language", "javascript"]
        ), patch.object(
            inference,
            "ensure_javascript_runtime",
            side_effect=RuntimeError("Node.js preflight failed"),
        ) as preflight, patch.object(inference, "build_endpoints") as build_endpoints:
            with self.assertRaisesRegex(RuntimeError, "Node.js preflight failed"):
                inference.main()

        preflight.assert_called_once_with()
        build_endpoints.assert_not_called()

    def test_non_javascript_inference_skips_node_preflight(self):
        with patch.object(
            sys, "argv", ["inference.py", "--language", "python"]
        ), patch.object(inference, "ensure_javascript_runtime") as preflight, patch.object(
            inference,
            "build_endpoints",
            side_effect=RuntimeError("endpoint setup reached"),
        ):
            with self.assertRaisesRegex(RuntimeError, "endpoint setup reached"):
                inference.main()

        preflight.assert_not_called()


if __name__ == "__main__":
    unittest.main()
