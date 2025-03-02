import json
from argparse import ArgumentParser

# load benchmark and sort it by averge score
with open('benchmark.json', 'r', encoding='utf-8') as json_file:
    benchmark = json.load(json_file)


# scan through the benchmark to find some attributes of the results
maxkey = 0 # the maximum length of the model name
coeff_java = 0 # the coefficient for the java benchmark relative to python
coeff_java_count = 0
coeff_rust = 0 # the coefficient for the rust benchmark relative to python
coeff_rust_count = 0
coeff_clojure = 0 # the coefficient for the clojure benchmark relative to python
coeff_clojure_count = 0
for key, value in benchmark.items():
    # first find largest key entry
    if len(key) > maxkey: maxkey = len(key)
    bench_python_100_v = value.get('python-100', '')
    bench_java_100_v = value.get('java-100', '')
    bench_rust_100_v = value.get('rust-100', '')
    bench_clojure_100_v = value.get('clojure-100', '')
    if bench_python_100_v != '':
        bench_python_100 = float(bench_python_100_v)
        if bench_python_100 > 0:
            if bench_java_100_v != '':
                bench_java_100 = float(bench_java_100_v)
                coeff_java += bench_java_100 / bench_python_100
                coeff_java_count += 1
            if bench_rust_100_v != '':
                bench_rust_100 = float(bench_rust_100_v)
                coeff_rust += bench_rust_100 / bench_python_100
                coeff_rust_count += 1
            if bench_clojure_100_v != '':
                bench_clojure_100 = float(bench_clojure_100_v)
                coeff_clojure += bench_clojure_100 / bench_python_100
                coeff_clojure_count += 1
coeff_java = coeff_java / coeff_java_count if coeff_java_count > 0 else 0
coeff_rust = coeff_rust / coeff_rust_count if coeff_rust_count > 0 else 0
coeff_clojure = coeff_clojure / coeff_clojure_count if coeff_clojure_count > 0 else 0

# Enrich the benchmark with a combined score from the single python, java, rust, and clojure scores.
# We do the following weights on the scores:
# - python: 4
# - java: 3
# - rust: 2
# - clojure: 1
# In case that not all scores are available, we compute guessed scores based on the coefficients computed before
# This should only be required for models which are very costly to compute (like models used over API).
for key, value in benchmark.items():
    bench_python_100_v = value.get('python-100', '')
    bench_java_100_v = value.get('java-100', '')
    bench_rust_100_v = value.get('rust-100', '')
    bench_clojure_100_v = value.get('clojure-100', '')
    bench_score = 0.0
    if bench_python_100_v != '':
        bench_score += 4.0 * float(bench_python_100_v)
        bench_score += 3.0 * float(bench_java_100_v) if bench_java_100_v != '' else 3 * coeff_java * float(bench_python_100_v)
        bench_score += 2.0 * float(bench_rust_100_v) if bench_rust_100_v != '' else 2 * coeff_rust * float(bench_python_100_v)
        bench_score += float(bench_clojure_100_v) if bench_clojure_100_v != '' else coeff_clojure * float(bench_python_100_v)
        bench_score = bench_score / 10.0
    # write the average score back to the benchmark
    benchmark[key]['_bench_score'] = bench_score

# sort the benchmark by average score
benchmark = dict(sorted(benchmark.items(), key=lambda item: item[1]['_bench_score'], reverse=True))

with open('README.md', 'r', encoding='utf-8') as md_file:
    readme = md_file.read()

# find markdown-table in the README.md
table = ""
start = False
for line in readme.split("\n"):
    if line.startswith("| Model"):
        start = True
    if start:
        table += line + "\n"
    # detect end of table: this happens when an empty line is found
    if start and line == "":
        break

print(table)

# produce new markdown-table from benchmark json
col_best = "Best<br/>Model<br/>for<br/>Size (GB)"
col_bench_score = "PE-<br/>Score"
col_memory_score = "Mem-<br/>Score"
col_size = "Size<br/>(*10^9 Params)"
col_quant = "Bits"
col_context = "Context Length<br/>(K)"
col_bench_100 = "PE-Bench-100 Details"

lowest_memory_amount = 9999 # to identify the best model for its class

newtable =  "| Model" + " "*(maxkey-5) + " | " + col_best + " | " + col_bench_score + " | " + col_memory_score + " | " + col_size + " | " + col_quant + " | " + col_context + " | " + col_bench_100 + " |\n"
newtable += "| :" + "-"*(maxkey-1) + " | " + "-"*(len(col_best)-1) + ": | " + "-"*(len(col_bench_score)-1) + ": | " + "-"*(len(col_memory_score)-1) + ": | " + "-"*(len(col_size)-1) + ": | " + "-"*(len(col_quant)-1) + ": | " + "-"*(len(col_context)-1)
newtable += ": | " + "-"*(len(col_bench_100)-1) + ": |\n"
for key, value in benchmark.items():
    size_v = value.get('_parameter_size', '')
    quant_v = value.get('_quantization_level', '')
    context_v = value.get('_context_size', '')
    bench_python_100_v = value.get('python-100', '')
    bench_java_100_v = value.get('java-100', '')
    bench_rust_100_v = value.get('rust-100', '')
    bench_clojure_100_v = value.get('clojure-100', '')
    bench_score_v = float(value.get('_bench_score', 0.0))
    memory_amount = size_v * float(quant_v) / 8.0 if quant_v and size_v and size_v > 0 else 9999 # required memory for the model in bytes
    memory_score_v = (100 * bench_score_v / memory_amount) if quant_v and size_v and size_v > 0 else ''

    best_model = False
    if memory_amount <= lowest_memory_amount:
        lowest_memory_amount = memory_amount
        best_model = True

    col_bench_score_vs = '' if bench_score_v == '' else "{:.2f}".format(bench_score_v)
    col_memory_score_vs = '' if memory_score_v == '' else "{:.0f}".format(memory_score_v)
    col_best_vs = "{:.2f}".format(memory_amount) if best_model else ''
    col_size_vs = str(size_v)
    col_quant_vs = str(quant_v)
    col_context_vs = str(context_v)
    col_bench_python_100_vs = str(bench_python_100_v)
    col_bench_java_100_vs = str(bench_java_100_v)
    col_bench_rust_100_vs = str(bench_rust_100_v)
    col_bench_clojure_100_vs = str(bench_clojure_100_v)

    if col_bench_python_100_vs == '': continue
    newtable += "| " + key + " "*(maxkey - len(key))
    newtable += " | " + " "*(8 - len(col_best_vs)) + col_best_vs
    newtable += " | " + " "*(6 - len(col_bench_score_vs)) + col_bench_score_vs
    newtable += " | " + " "*(6 - len(col_memory_score_vs)) + col_memory_score_vs
    newtable += " | " + " "*(6 - len(col_size_vs)) + col_size_vs
    newtable += " | " + " "*(4 - len(col_quant_vs)) + col_quant_vs
    newtable += " | " + " "*(4 - len(col_context_vs)) + col_context_vs

    benchdetails = ""
    benchdetails += "Python: " + col_bench_python_100_vs + ", "
    benchdetails += "Java: "   + col_bench_java_100_vs + ", "
    benchdetails += "Rust: "   + col_bench_rust_100_vs + ", "
    benchdetails += "Clojure: " + col_bench_clojure_100_vs
    newtable += " | " + benchdetails + " |\n"

newtable += "\n" # make sure that the table has an empty line again

print(newtable)

# now replace the old table with the new table in the readme file
new_readme = readme.replace(table, newtable)
#print(new_readme)

# store the new readme
with open('README.md', 'w', encoding='utf-8') as md_file:
    md_file.write(new_readme)
