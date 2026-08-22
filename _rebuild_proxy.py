#!/usr/bin/env python3
"""Rebuild proxy.py with ability-testing support."""

with open("proxy.py.backup-dont-touch", "r") as f:
    content = f.read()

# Read test code from external files to avoid nested quote issues
with open("_test_functions.txt") as f:
    test_code = f.read()

with open("_ability_helpers.txt") as f:
    helpers_code = f.read()

# 1. Fix imports
old_imports = "import sys\nimport json\nimport time\nimport argparse"
new_imports = "import os\nimport sys\nimport json\nimport base64\nimport time\nimport argparse"
content = content.replace(old_imports, new_imports)

# 2. Add _capabilities global
old_g = "_error_states:  Dict[str, dict] = {}             # url -> {error, ts, msg}\n_counters_lock = threading.Lock()                     # guards all dicts"
new_g = "_error_states:  Dict[str, dict] = {}             # url -> {error, ts, msg}\n_capabilities:    Dict[str, dict] = {}              # url -> capability flags\n_counters_lock = threading.Lock()                    # guards all dicts"
content = content.replace(old_g, new_g)

# 3. Insert test functions before _build_target
marker = "\ndef _build_target"
idx = content.find(marker)
if idx >= 0:
    content = content[:idx] + "\n" + test_code.strip() + "\n\n" + marker + content[idx+len(marker):]

# 4. Add ability helpers + cache population after load_endpoints return statement
old_ret = '     print("[proxy] Loaded " + str(len(endpoints)) + " endpoint(s) from " + path)\n    return endpoints\n\n\ndef main'
new_ret = helpers_code.strip() + '\n\n\n' + old_ret.split('\n\n\n')[1]  # preserve the rest
content = content.replace(old_ret, new_ret)

# 5. Add capabilities to api_endpoints response
old_api_fields = '"key_set":          bool(ep.key),'
new_api_fields = '"capabilities":        _capabilities.get(ep.url, {}),\n                 "key_set":          bool(ep.key),'
content = content.replace(old_api_fields, new_api_fields)

# 6. Add --test-abilities flag
old_parser_end = '"Path to endpoints config file (default: endpoints.json)")\n    args = parser.parse_args()\n\n    global _endpoints'
new_parser_end = '"Path to endpoints config file (default: endpoints.json)")\n    parser.add_argument("--test-abilities", action="store_true",\n                        help="Run vision/tooling/thinking/format tests for missing capability data")\n    args = parser.parse_args()\n\n    if args.test_abilities:\n        run_ability_tests(args.config)\n        return\n\n    global _endpoints'
content = content.replace(old_parser_end, new_parser_end)

with open("proxy.py", "w") as f:
    f.write(content)

print("Rebuild done - verifying...")
