import json
from argparse import ArgumentParser

# load benchmark and sort it by averge score
with open('benchmark.json', 'r', encoding='utf-8') as json_file:
    benchmark = json.load(json_file)

for key, value in benchmark.items():
    bench_python_100_v = value.get('python-100', '')
    bench_java_100_v = value.get('java-100', '')
    bench_rust_100_v = value.get('rust-100', '')
    bench_clojure_100_v = value.get('clojure-100', '')
    bench_avg = 0
    n = 0
    if bench_python_100_v != '':
        bench_avg += 2 * bench_python_100_v
        n += 2  # double weight for python
    if bench_java_100_v != '':
        bench_avg += 2 * bench_java_100_v
        n += 2 # double weight for java
    if bench_rust_100_v != '':
        bench_avg += bench_rust_100_v
        n += 1
    if bench_clojure_100_v != '':
        bench_avg += bench_clojure_100_v
        n += 1
    bench_avg = bench_avg / n if n > 0 else 0
    # write the average score back to the benchmark
    benchmark[key]['_average_score'] = bench_avg

# sort the benchmark by average score
benchmark = dict(sorted(benchmark.items(), key=lambda item: item[1]['_average_score'], reverse=True))

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
# first find largest key entry
maxkey = 0
for key, value in benchmark.items():
    if len(key) > maxkey: maxkey = len(key)
col_best = "Best<br/>Model<br/>for<br/>Size (GB)"
col_score = "Eco-<br/>Score"
col_size = "Size<br/>(*10^9 Params)"
col_quant = "Bits"
col_context = "Context Length<br/>(K)"
col_bench_python_100 = "PE-Bench-Python-100"
col_bench_java_100 = "PE-Bench-Java-100"
col_bench_rust_100 = "PE-Bench-Rust-100"
col_bench_clojure_100 = "PE-Bench-Clojure-100"

lowest_memory_amount = 9999 # to identify the best model for its class

newtable =  "| Model" + " "*(maxkey-5) + " | " + col_best + " | " + col_score + " | " + col_size + " | " + col_quant + " | " + col_context + " | " + col_bench_python_100 + " | " + col_bench_java_100 + " | " + col_bench_rust_100 + " | " + col_bench_clojure_100 + " |\n"
newtable += "| :" + "-"*(maxkey-1) + " | " + "-"*(len(col_best)-1) + ": | " + "-"*(len(col_score)-1) + ": | " + "-"*(len(col_size)-1) + ": | " + "-"*(len(col_quant)-1) + ": | " + "-"*(len(col_context)-1)
newtable += ": | " + "-"*(len(col_bench_python_100)-1) + ": | " + "-"*(len(col_bench_java_100)-1) + ": | " + "-"*(len(col_bench_rust_100)-1) + ": | " + "-"*(len(col_bench_clojure_100)-1) + ": |\n"
for key, value in benchmark.items():
    size_v = value.get('_parameter_size', '')
    quant_v = value.get('_quantization_level', '')
    context_v = value.get('_context_size', '')
    bench_python_100_v = value.get('python-100', '')
    bench_java_100_v = value.get('java-100', '')
    bench_rust_100_v = value.get('rust-100', '')
    bench_clojure_100_v = value.get('clojure-100', '')
    bench_avg = value.get('_average_score', 0.0)
    memory_amount = size_v * float(quant_v) / 8.0 if quant_v and size_v and size_v > 0 else 9999 # required memory for the model in bytes
    score_v = (100 * bench_avg / memory_amount) if quant_v and size_v and size_v > 0 else ''

    best_model = False
    if memory_amount <= lowest_memory_amount:
        lowest_memory_amount = memory_amount
        best_model = True

    col_score_vs = '' if score_v == '' else "{:.0f}".format(score_v)
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
    newtable += " | " + " "*(len(col_best) - len(col_best_vs)) + col_best_vs
    newtable += " | " + " "*(len(col_score) - len(col_score_vs)) + col_score_vs
    newtable += " | " + " "*(len(col_size) - len(col_size_vs)) + col_size_vs
    newtable += " | " + " "*(len(col_quant) - len(col_quant_vs)) + col_quant_vs
    newtable += " | " + " "*(len(col_context) - len(col_context_vs)) + col_context_vs
    newtable += " | " + " "*(len(col_bench_python_100) - len(col_bench_python_100_vs)) + col_bench_python_100_vs
    newtable += " | " + " "*(len(col_bench_java_100) - len(col_bench_java_100_vs)) + col_bench_java_100_vs
    newtable += " | " + " "*(len(col_bench_rust_100) - len(col_bench_rust_100_vs)) + col_bench_rust_100_vs
    newtable += " | " + " "*(len(col_bench_clojure_100) - len(col_bench_clojure_100_vs)) + col_bench_clojure_100_vs
    newtable += " |\n"

newtable += "\n" # make sure that the table has an empty line again

print(newtable)

# now replace the old table with the new table in the readme file
new_readme = readme.replace(table, newtable)
#print(new_readme)

# store the new readme
with open('README.md', 'w', encoding='utf-8') as md_file:
    md_file.write(new_readme)
