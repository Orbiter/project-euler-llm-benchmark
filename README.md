# Project Euler LLM Benchmark

To identify the performance of Large Language Models to solve problems with domain-specific knowledge (here: programming)
we created a benchmark using the Project Euler series of challenging mathematical/computer programming problems.
Because we want to apply LLMs for coding with specific programming languages, we also want to measure how good
a LLM is at coding with that given programming language.

![Benchmark Results](benchmark_instruct.png)

![Benchmark Results](benchmark_thinking.png)

PE-Bench-200 evaluates solutions in five programming languages: Python, JavaScript, Java, Rust, and Clojure. JavaScript is a regular part of generation, execution, scoring, and publishing. JavaScript solutions run as plain ECMAScript programs in a restricted Node.js environment without external packages or access to the filesystem, network, subprocesses, or workers. Tool-mode results are currently excluded from publishing.

## Super-Human Performance
AI systems have achieved domain-specific super-human performance. In 1997, IBM’s “Deep Blue” defeated world chess champion Garry Kasparov, marking the first time a machine outperformed the best human player. Since then, AI has surpassed human ability in many games, including Go, where AlphaGo triumphed in 2016.

While Deep Blue was “super-human” because it exceeded the best human, our goal is to define super-human performance relative to the average human score in the Project Euler test. This allows us to express an AI’s performance as a multiplier of human ability.

With the Project Euler LLM Benchmark, we aim to quantify how strongly LLMs demonstrate super-human capabilities in the domain of programming. See the Motivation chapter below for details on our measurement approach.

## Results for PE-Bench-200
The five component benchmarks ("PE-Bench-Python-200", "PE-Bench-JavaScript-200", "PE-Bench-Java-200", "PE-Bench-Rust-200", and "PE-Bench-Clojure-200") measure the super-human performance factor for coding in Python, JavaScript, Java, Rust, and Clojure. The combined PE-200 Score uses language weights of 5, 4, 3, 2, and 1 respectively.

The **Performance Score** combines solution quality and generation speed. It is the product of the PE-200 Score and the effective token throughput, divided by 100. All published token-throughput measurements use a local Apple M1 Mac Studio (`Mac13,1` or `Mac13,2`) as the reference hardware. The **Mem Score** relates the PE-200 Score to the estimated model memory requirement. A blank value means that the required throughput or model-size measurement is unavailable.

Results are:

### Non-Thinking
| Model                                                                                            | Best<br/>Model<br/>for<br/>Size (GB) | PE-200-<br/>Score | Performance-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | JavaScript | Java | Rust | Clojure |
| :----------------------------------------------------------------------------------------------- | -----------------------------------: | ----------------: | ---------------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---------: | ---: | ---: | ------: |
| gpt-5.6-sol-no_think                                                                             |          |   72.8 |        |        |        |   16 | 1050 | 64.33 | 88.63 | 87.54 | 75.46 | 2.23 |
| nemotron-3-ultra-550b-a55b-no_think                                                              |     1100 |   66.1 |        |      6 |  550.0 |   16 | 1000 | 72.52 | 88.42 | 49.42 | 60.05 | 6.89 |
| muse-glimmer:30b-q8_0-dflash-no_think                                                            |    33.00 |   61.7 |     15 |    187 |     30 |    8 |  128 | 56.75 |      | 82.56 | 76.23 |  2.0 |
| hf.co/InternScience/Agents-A1-Q8_0-GGUF:Q8_0-no_think                                            |          |   56.8 |     48 |    148 |   35.0 |    8 |  256 | 59.61 |      | 76.03 | 35.04 | 4.57 |
| gpt-5.6-terra-no_think                                                                           |          |   56.4 |        |        |        |   16 | 1050 | 54.22 | 68.29 | 56.9 | 64.97 | 1.14 |
| deepseek-v4-flash-0731-no_think                                                                  |          |   56.3 |        |        |        |   16 | 1024 | 45.4 | 76.24 | 59.16 | 63.42 | 7.67 |
| hf.co/SC117/Agents-A1-MTP-APEX-GGUF:latest-no_think                                              |    26.25 |   55.0 |     47 |    210 |     35 |    4 |  256 | 64.73 |      | 57.04 | 27.87 | 1.75 |
| muse-glimmer:30b-nvfp4-dflash-no_think                                                           |    22.50 |   54.5 |     15 |    242 |     30 |    4 |  128 | 50.31 |      | 70.15 | 69.59 | 4.67 |
| qwen3.6:27b-mtp-q8_0-no_think                                                                    |          |   53.3 |     11 |    179 |     27 |    8 |  256 | 58.75 |      | 53.9 | 47.48 | 0.56 |
| ling-3.0-flash-no_think                                                                          |          |   51.9 |        |     21 |  124.0 |   16 |  256 | 56.97 |      | 54.42 | 44.1 | 2.08 |
| qwen3.6:35b-a3b-mtp-q8_0-no_think                                                                |          |   50.5 |     34 |    131 |     35 |    8 |  256 | 57.11 |      | 53.55 | 34.55 | 0.94 |
| qwen3.7-flash-no_think                                                                           |          |   49.4 |        |        |        |   16 | 1000 | 55.33 |      | 54.29 | 33.93 | 0.56 |
| qwen3.8:27b-mtp-q4_K_M-no_think                                                                  |    20.25 |   49.2 |      9 |    243 |   27.0 |    4 |  256 | 62.04 | 52.91 | 49.23 | 33.46 | 0.87 |
| frob/qwen3.5-instruct:35b                                                                        |          |   49.0 |     45 |    187 |   35.0 |    4 |  256 | 55.6 |      | 48.26 | 35.49 | 7.17 |
| hf.co/InternScience/Agents-A1-Q4_K_M-GGUF:Q4_K_M-no_think                                        |          |   49.0 |     46 |    187 |   35.0 |    4 |  256 | 55.03 |      | 57.46 | 25.76 | 3.81 |
| qwen3-coder-next:Q4_K_M                                                                          |          |   48.9 |     33 |     82 |   79.7 |    4 |  256 | 54.49 |      | 42.84 | 47.33 | 8.38 |
| qwen3.6:35b-a3b-q4_K_M-no_think                                                                  |          |   48.5 |     44 |    185 |   35.0 |    4 |  256 | 50.6 |      | 57.61 | 43.65 | 1.32 |
| qwen3.6:27b-q4_K_M-no_think                                                                      |    20.25 |   47.9 |     12 |    236 |   27.0 |    4 |  256 | 56.21 |      | 46.65 | 29.68 | 0.28 |
| qwen3.6:27b-q8_0-no_think                                                                        |          |   46.6 |     10 |    157 |   27.0 |    8 |  256 | 52.3 |      | 45.14 | 40.3 | 1.02 |
| frob/qwen3.5-instruct:122b                                                                       |          |   45.3 |        |     50 |  122.0 |    4 |  256 | 47.61 |      | 49.93 | 40.42 | 10.24 |
| qwen3-next:80b-a3b-instruct-q4_K_M                                                               |          |   45.3 |     28 |     76 |   79.7 |    4 |  256 | 48.41 |      | 50.71 | 32.66 | 16.0 |
| gemma4:12b-it-qat-no_think                                                                       |          |   44.7 |     24 |        |        |      |      | 47.01 |      | 45.74 | 48.03 | 3.72 |
| qwen3.6:35b-a3b-q8_0-no_think                                                                    |          |   42.9 |     36 |    111 |   35.0 |    8 |  256 | 44.64 |      | 49.94 | 40.93 | 0.56 |
| hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q8_K_XL-no_think                                               |          |   42.4 |      9 |    143 |   27.0 |    8 |  256 | 47.48 |      | 44.39 | 32.49 | 0.56 |
| qwen3.8:27b-mtp-q8_0-no_think                                                                    |          |   41.5 |      9 |    140 |   27.0 |    8 |  256 | 46.53 | 40.86 | 50.48 | 37.13 | 0.56 |
| frob/qwen3.5-instruct:27b                                                                        |    20.25 |   41.3 |     10 |    204 |   27.0 |    4 |  256 | 48.5 |      | 38.95 | 26.39 | 2.69 |
| qwen3:235b-a22b-instruct-2507-q4_K_M                                                             |          |   39.2 |        |     22 |  235.1 |    4 |  256 | 43.09 |      | 41.18 | 28.46 | 10.53 |
| qwen3.8:27b-mlx-no_think                                                                         |    20.25 |   37.4 |     10 |    185 |   27.0 |    4 |  256 | 42.82 | 41.52 | 42.79 | 26.03 | 0.56 |
| qwen3-vl:235b-a22b-instruct-q4_K_M                                                               |          |   37.4 |        |     21 |  235.7 |    4 |  256 | 36.44 |      | 47.94 | 34.77 | 11.66 |
| hf.co/inclusionAI/Ling-flash-2.0-GGUF:Q4_K_M                                                     |          |   36.9 |        |     48 |    103 |    4 |  128 | 42.38 |      | 34.36 | 23.3 | 13.74 |
| gpt-5.6-luna-no_think                                                                            |          |   30.8 |        |        |        |   16 | 1024 | 30.45 | 36.33 | 36.52 | 27.37 | 0.56 |
| hf.co/InternScience/Agents-A1-4B-Q8_0-GGUF:Q8_0-no_think                                         |     4.40 |   28.8 |     30 |    655 |      4 |    8 |  256 | 36.22 |      | 26.96 | 5.98 | 5.65 |
| frob/deepseek-v4-flash-0731:284b-a13b-ud-iq2_m-no_think                                          |          |   26.7 |        |      5 |    284 |    2 |      | 31.34 |      |      |      |      |
| frob/qwen3.5-instruct:9b                                                                         |          |   25.4 |     18 |    376 |      9 |    4 |  256 | 32.51 |      | 17.72 | 13.29 | 1.45 |
| qwen3-vl:32b-instruct-q4_K_M                                                                     |          |   23.4 |        |     93 |   33.4 |    4 |  256 | 27.78 |      | 21.15 | 13.91 | 3.19 |
| hf.co/unsloth/Qwen3.5-9B-MTP-GGUF:UD-Q4_K_XL-no_think                                            |          |   23.2 |     16 |    344 |    9.0 |    4 |  256 | 26.67 |      | 28.27 | 8.34 | 0.91 |
| hf.co/mradermacher/Ling-mini-2.0-i1-GGUF:Q4_K_M                                                  |          |   23.2 |        |    193 |     16 |    4 |  128 | 29.58 |      | 20.74 | 6.35 | 0.39 |
| hf.co/mradermacher/Ling-mini-2.0-GGUF:Q4_K_M                                                     |          |   22.7 |        |    189 |     16 |    4 |  128 | 26.89 |      | 19.74 | 15.66 | 1.91 |
| frob/kat-coder-v2.5-dev:35b-a3b-q4_K_M-no_think                                                  |          |   22.5 |        |     86 |   35.0 |    4 |  256 | 25.9 |      | 22.4 | 15.41 | 0.56 |
| hf.co/cturan/IQuest-Coder-V1-40B-Instruct-GGUF:Q4_K_M                                            |          |   22.5 |        |     75 |   39.8 |    4 |  128 | 26.12 |      | 19.65 | 17.81 | 1.83 |
| hf.co/mradermacher/OmniCoder-9B-i1-GGUF:Q4_K_M                                                   |          |   21.4 |        |    317 |      9 |    4 |  256 | 25.28 |      | 21.23 | 11.73 | 0.71 |
| nemotron-3.5-lightning-no_think                                                                  |          |   20.7 |        |     34 |     30 |   16 | 1024 | 23.62 |      | 21.6 | 13.53 | 0.81 |
| ornith-1.5:35b-no_think                                                                          |          |   19.0 |     17 |     72 |     35 |    4 |  256 | 22.51 |      | 19.26 | 9.76 | 0.56 |
| qwen3-vl:30b-a3b-instruct-q8_0                                                                   |          |   18.2 |        |     53 |   31.1 |    8 |  256 | 18.64 |      | 20.51 | 18.53 | 2.98 |
| qwen3-vl:30b-a3b-instruct-q4_K_M                                                                 |          |   18.2 |        |     78 |   31.1 |    4 |  128 | 18.95 |      | 21.38 | 16.01 | 1.38 |
| qwen3:30b-a3b-instruct-2507-q4_K_M                                                               |          |   17.4 |        |     76 |   30.5 |    4 |  256 | 16.93 |      | 23.76 | 16.1 | 1.89 |
| hf.co/InternScience/Agents-A1-4B-Q4_K_M-GGUF:Q4_K_M-no_think                                     |     3.00 |   17.4 |     19 |    581 |      4 |    4 |  256 | 22.82 |      | 13.79 | 4.52 | 0.65 |
| hf.co/mradermacher/SERA-32B-GGUF:Q4_K_M                                                          |          |   17.4 |        |     72 |   32.0 |    4 |   32 | 18.68 |      | 21.48 | 11.48 | 1.09 |
| qwen3-coder:30b-a3b-q4_K_M                                                                       |          |   16.9 |        |     74 |   30.5 |    4 |  256 | 19.51 |      | 13.41 | 14.03 | 5.46 |
| qwen/qwen3-vl-30b                                                                                |          |   16.9 |        |     72 |   31.1 |    4 |  128 | 18.98 |      | 19.02 | 9.83 | 1.88 |
| hf.co/mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-GGUF:Q4_K_M                   |          |   16.1 |        |     70 |   30.5 |    4 |  160 | 17.56 |      | 18.06 | 10.43 |  4.4 |
| hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-1M-GGUF:Q4_K_M                                        |          |   14.3 |        |     63 |   30.5 |    4 |  256 | 14.02 |      | 17.25 | 12.92 | 8.11 |
| hf.co/unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL-no_think                                            |     3.00 |   13.9 |     15 |    465 |    4.0 |    4 |   32 | 19.7 |      | 6.79 | 3.41 |  0.3 |
| qwen2.5vl:32b-q4_K_M                                                                             |          |   13.8 |        |     55 |   33.5 |    4 |  128 | 15.56 |      | 11.71 | 13.44 | 0.82 |
| qwen3:30b-a3b-q4_K_M-no_think                                                                    |          |   13.7 |        |     60 |   30.5 |    4 |   40 | 14.5 |      | 15.85 | 10.06 | 4.36 |
| hf.co/owao/Nanbeige4.2-3B-GGUF:Q4_K_M-no_think                                                   |     2.25 |   13.4 |      8 |    597 |      3 |    4 |      | 17.78 |      | 10.91 |  2.3 | 0.28 |
| olmo-3.1:32b-instruct-q4_K_M                                                                     |          |   12.9 |        |     53 |   32.2 |    4 |  128 | 17.37 |      | 6.19 | 6.68 | 1.11 |
| devstral-2:123b-instruct-2512-q4_K_M                                                             |          |   12.7 |        |     14 |  125.0 |    4 |  256 | 13.9 |      | 13.36 | 9.61 | 3.49 |
| defyma85/bonsai-27b-q1_0:latest-no_think                                                         |          |   12.7 |        |     24 |     27 |    1 |  256 | 17.37 |      |  7.1 | 4.56 | 0.09 |
| laguna-xs-2.1:Q4_K_M-no_think                                                                    |          |   10.4 |        |        |        |    4 |  256 | 11.8 |      | 11.81 | 5.74 | 0.28 |
| qwen2.5-coder:32b-instruct-q4_K_M                                                                |          |   10.2 |        |     42 |   32.8 |    4 |   32 | 11.6 |      | 11.5 | 4.69 | 2.53 |
| hf.co/janhq/Jan-v3-4B-base-instruct-gguf:Q4_K_M                                                  |          |   10.2 |     10 |    339 |      4 |    4 |  256 | 13.51 |      | 5.06 | 6.05 | 0.56 |
| hf.co/bartowski/internlm_JanusCoder-14B-GGUF:Q4_K_M                                              |          |   9.90 |        |     89 |   14.8 |    4 |   40 | 11.89 |      | 6.45 | 9.47 | 0.58 |
| qwen3.5:4b-q4_K_M-no_think                                                                       |          |   9.86 |     11 |    329 |      4 |    4 |  256 | 14.08 |      | 4.58 | 1.74 | 0.79 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                                                      |          |   9.69 |        |     18 |   72.7 |    4 |  128 | 11.13 |      | 10.62 | 5.03 | 0.77 |
| qwen2.5:72b-instruct-q4_K_M                                                                      |          |   9.65 |        |     18 |   72.7 |    4 |  128 | 11.5 |      | 8.83 | 5.27 | 1.69 |
| frob/qwen3.5-instruct:4b                                                                         |          |   9.59 |     10 |    320 |      4 |    4 |  256 | 11.23 |      | 6.84 | 9.14 | 1.52 |
| ministral-3:14b-instruct-2512-q4_K_M                                                             |          |   9.57 |        |     92 |   13.9 |    4 |  256 | 11.11 |      | 8.43 | 7.35 | 1.09 |
| qwen2.5vl:72b-q4_K_M                                                                             |          |   9.54 |        |     17 |   73.4 |    4 |  128 | 10.11 |      | 10.98 | 7.64 | 1.67 |
| laguna-s-2.1:q4_K_M-no_think                                                                     |          |   9.39 |        |        |        |    4 | 1024 | 9.52 |      | 13.02 | 6.98 |  0.0 |
| qwen3:4b-instruct-2507-q4_K_M                                                                    |          |   8.72 |      9 |    291 |    4.0 |    4 |  256 | 10.14 | 10.92 | 6.54 | 7.88 |  1.1 |
| hf.co/bartowski/ibm-granite_granite-4.1-30b-GGUF:q4_K_M                                          |          |   8.28 |        |    138 |    8.0 |    4 |  128 | 9.78 |      | 8.13 | 4.45 | 0.74 |
| bartowski/FutureMa_Eva-4B-GGUF:Q4_K_M                                                            |          |   8.26 |        |    275 |      4 |    4 |  256 | 10.86 |      | 5.05 | 3.98 | 0.69 |
| hf.co/vanta-research/apollo-astralis-8b:Q4_K_M                                                   |          |   8.24 |        |    134 |   8.19 |    4 |   32 | 8.36 |      | 12.08 | 4.45 | 1.38 |
| qwen3-vl:4b-instruct-q4_K_M                                                                      |          |   8.20 |        |    249 |    4.4 |    4 |  256 | 10.08 |      |  6.6 | 4.88 | 0.52 |
| devstral-small-2:24b-instruct-2512-q4_K_M                                                        |          |   8.14 |        |     45 |   24.0 |    4 |  128 | 9.87 |      | 7.26 | 3.88 | 1.55 |
| hf.co/tiiuae/Falcon-H1-34B-Instruct-GGUF:Q4_K_M                                                  |          |   8.00 |        |     32 |   33.6 |    4 |  256 | 7.87 |      | 9.73 | 8.81 | 0.57 |
| qwen2.5:32b-instruct-q4_K_M                                                                      |          |   7.97 |        |     32 |   32.8 |    4 |   32 | 9.74 |      | 6.08 |  5.6 | 0.35 |
| qwen3-vl:8b-instruct-q4_K_M                                                                      |          |   7.84 |        |    119 |    8.8 |    4 |  256 | 8.39 |      | 7.02 | 9.34 | 0.46 |
| qwen3:14b-q4_K_M-no_think                                                                        |          |   7.73 |        |     70 |   14.8 |    4 |   40 | 8.19 |      | 10.15 | 4.16 |  1.6 |
| phi4:14b-q4_K_M                                                                                  |          |   7.70 |      3 |     70 |   14.7 |    4 |   16 | 8.92 |      | 8.42 | 3.49 | 0.98 |
| hf.co/ProCreations/grug-27b-mtp-gguf:Q4_K_M-no_think                                             |          |   7.66 |        |        |        |    4 |      | 8.91 |      | 7.16 | 5.39 | 0.56 |
| qwen3-vl-8b-instruct-mlx                                                                         |          |   7.53 |        |    114 |    8.8 |    4 |  256 | 8.23 |      | 9.48 | 4.07 | 0.54 |
| ornith:9b-q4_K_M-no_think                                                                        |          |   7.53 |        |        |        |    4 |      | 9.07 |      | 7.48 | 3.08 | 0.73 |
| granite4:small-h                                                                                 |          |   7.31 |        |     30 |   32.2 |    4 |  131 | 8.34 |      | 7.04 | 5.54 | 0.54 |
| hf.co/kai-os/Grug-12B-GGUF:Q4_K_M-no_think                                                       |          |   7.28 |        |        |        |    4 |      | 6.46 |      | 11.57 | 7.33 | 0.21 |
| hf.co/bartowski/NousResearch_Hermes-4.3-36B-GGUF:Q4_K_M                                          |          |   6.91 |        |     25 |   36.2 |    4 |  128 | 8.48 |      | 5.36 | 4.15 | 1.07 |
| hf.co/speakleash/Bielik-11B-v3.0-Instruct-GGUF:Q4_K_M                                            |          |   6.74 |        |     80 |   11.2 |    4 |  128 | 8.57 |      | 4.95 |  3.5 | 0.25 |
| hf.co/mradermacher/Qwen2.5-VL-32B-Instruct-abliterated-GGUF:Q4_K_M                               |          |   6.69 |        |     27 |   32.8 |    4 |   32 |  7.6 |      | 6.33 | 5.52 | 0.32 |
| hf.co/bartowski/ibm-granite_granite-4.1-8b-GGUF:q4_K_M                                           |          |   6.55 |        |    109 |    8.0 |    4 |  128 | 9.02 |      | 1.97 | 4.25 | 0.65 |
| hf.co/LGAI-EXAONE/EXAONE-4.0-32B-GGUF:Q4_K_M                                                     |          |   6.37 |        |     27 |   32.0 |    4 |      | 8.54 |      | 4.39 | 1.57 |  0.5 |
| qwen2.5-coder:14b-instruct-q4_K_M                                                                |          |   6.22 |        |     56 |   14.8 |    4 |  128 | 6.35 |      | 8.46 | 4.08 | 1.15 |
| ornith-1.5:9b-no_think                                                                           |          |   5.93 |      4 |     88 |    9.0 |    4 |  256 | 7.02 |      | 5.31 | 3.72 | 0.87 |
| ling-3.0-tiny-no_think                                                                           |          |   5.86 |        |     37 |    7.9 |   16 |  256 |  5.6 |      | 9.32 | 4.14 |  0.0 |
| yi-coder:9b-chat-q4_K_M                                                                          |          |   5.72 |        |     87 |    8.8 |    4 |  128 |  7.2 |      | 5.39 | 1.51 | 0.22 |
| llama3.2-vision:90b-instruct-q4_K_M                                                              |          |   5.69 |        |      9 |   87.7 |    4 |  128 | 6.71 |      | 4.34 | 4.43 | 1.61 |
| qwen3:8b-q4_K_M-no_think                                                                         |          |   5.66 |        |     92 |    8.2 |    4 |  128 | 5.34 |      | 8.65 |  4.2 | 1.26 |
| rnj-1:8b-instruct-q4_K_M                                                                         |          |   5.65 |        |     91 |    8.3 |    4 |  256 | 6.87 |      | 4.87 | 2.94 | 0.96 |
| hf.co/mradermacher/AesCoder-4B-GGUF:Q4_K_M                                                       |          |   5.47 |        |    165 |   4.41 |    4 |      | 6.93 |      | 3.39 | 3.79 | 0.38 |
| qwen3-vl-4b-instruct-mlx                                                                         |          |   5.45 |        |     91 |    8.0 |    4 |  256 | 7.64 |      | 1.83 | 2.71 | 0.39 |
| ministral-3:8b-instruct-2512-q4_K_M                                                              |          |   5.38 |        |     81 |    8.9 |    4 |  256 | 5.67 |      | 6.97 | 3.43 | 0.58 |
| gemma3:27b                                                                                       |          |   5.33 |      1 |     26 |   27.4 |    4 |  128 | 6.11 |      | 4.74 | 4.54 | 0.36 |
| hf.co/ProCreations/grug-35b-mtp-gguf:Q4_K_M-no_think                                             |          |   5.22 |        |        |        |    4 |      | 5.57 |      |  5.3 | 5.35 | 0.29 |
| hf.co/bartowski/internlm_JanusCoder-8B-GGUF:Q4_K_M                                               |          |   5.19 |        |     85 |   8.19 |    4 |      | 5.97 |      |  6.7 | 1.07 | 0.58 |
| llama3.3:70b-instruct-q4_K_M                                                                     |          |   5.05 |      0 |     10 |   70.6 |    4 |  128 | 5.26 |      | 5.04 | 5.19 |  1.8 |
| hf.co/mradermacher/Josiefied-Qwen3-4B-Instruct-2507-abliterated-v1-GGUF:Q4_K_M                   |          |   5.02 |        |    166 |   4.02 |    4 |      | 5.97 |      | 4.24 | 3.42 | 0.66 |
| hf.co/unsloth/Qwen3.8-27B-GGUF:UD-IQ1_M-no_think                                                 |          |   4.95 |      1 |        |        |      |      | 6.61 |      | 2.96 | 2.08 |  0.2 |
| hf.co/tiiuae/Falcon-H1-7B-Instruct-GGUF:Q4_K_M                                                   |          |   4.89 |        |     86 |   7.59 |    4 |      | 6.23 |      | 3.45 | 2.55 |  0.4 |
| hf.co/bartowski/google_medgemma-27b-it-GGUF:Q4_K_M                                               |          |   4.86 |        |     24 |   27.0 |    4 |    8 | 6.03 |      | 4.08 | 2.46 | 0.11 |
| hf.co/mradermacher/Ling-lite-1.5-GGUF:Q4_K_M                                                     |          |   4.62 |        |     37 |   16.8 |    4 |      | 4.99 |      | 5.13 | 3.71 | 0.44 |
| hf.co/mradermacher/medgemma-27b-text-it-GGUF:Q4_K_M                                              |          |   4.39 |        |     22 |   27.0 |    4 |      | 4.96 |      | 4.12 | 3.67 | 0.47 |
| hf.co/arcee-ai/Trinity-Mini-GGUF:Q4_K_M                                                          |          |   4.31 |        |     22 |   26.1 |    4 |  128 | 4.33 |      |  3.4 | 5.56 | 3.46 |
| hf.co/mistralai/Devstral-Small-2507_gguf:Q4_K_M                                                  |          |   4.31 |        |     24 |   23.6 |    4 |  128 | 5.32 |      | 3.03 | 2.99 | 0.46 |
| lfm2:24b-q4_K_M                                                                                  |          |   4.27 |        |     24 |   24.0 |    4 |  128 | 5.39 |      | 3.56 | 1.73 | 0.21 |
| hf.co/bartowski/ai9stars_G9v3-3B-GGUF:Q4_K_M-no_think                                            |     2.25 |   4.25 |      5 |    189 |      3 |    4 |      |  5.4 |      | 2.71 |      |      |
| hf.co/LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF:Q4_K_M                                                    |     0.96 |   4.25 |      8 |    442 |   1.28 |    4 |   64 | 5.49 |      | 4.35 | 0.01 |  0.0 |
| hf.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF:Q4_K_M                        |          |   4.18 |        |     24 |   23.6 |    4 |  128 | 4.39 |      | 4.76 | 3.46 | 1.08 |
| hf.co/mradermacher/Qwen3-4b-tcomanr-merge-v2.5-GGUF:Q4_K_M                                       |          |   4.10 |        |    136 |   4.02 |    4 |   32 | 4.27 |      | 3.91 | 3.84 | 2.72 |
| qwen2.5:14b-instruct-q4_K_M                                                                      |          |   4.08 |        |     37 |   14.8 |    4 |   32 | 4.34 |      | 5.73 | 1.81 | 0.41 |
| hf.co/mradermacher/Olmo-3-32B-Think-GGUF:Q4_K_M                                                  |          |   4.03 |        |     17 |   32.0 |    4 |  128 | 3.99 |      | 4.84 | 3.78 | 1.56 |
| ministral-3:3b-instruct-2512-q4_K_M                                                              |          |   3.67 |        |    129 |    3.8 |    4 |  128 |  4.9 |      | 2.22 | 1.54 |  0.1 |
| hf.co/bartowski/ai21labs_AI21-Jamba2-Mini-GGUF:Q4_K_M                                            |          |   3.65 |        |      9 |     52 |    4 |  256 | 5.31 |      | 1.42 | 0.62 | 0.29 |
| hf.co/mradermacher/Olmo-3-7B-Think-GGUF:Q4_K_M                                                   |          |   3.61 |        |     69 |    7.0 |    4 |    2 | 5.53 |      | 0.53 | 0.32 | 0.98 |
| hf.co/bartowski/THUDM_GLM-4-9B-0414-GGUF:Q4_K_M                                                  |          |   3.46 |        |     49 |    9.4 |    4 |   32 | 4.48 |      | 2.82 |  1.0 | 0.16 |
| hf.co/unsloth/GLM-4.6V-Flash-GGUF:Q4_K_M                                                         |          |   3.44 |        |     49 |    9.4 |    4 |  128 | 4.61 |      | 1.78 | 1.44 | 0.84 |
| hf.co/mradermacher/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v1-GGUF:Q4_K_M                  |          |   3.33 |        |    110 |   4.02 |    4 |      | 3.94 |      |  3.1 | 1.78 | 0.74 |
| hf.co/bartowski/cognitivecomputations_Dolphin-Mistral-24B-Venice-Edition-GGUF:Q4_K_M             |          |   3.27 |        |     18 |   24.0 |    4 |   32 | 4.29 |      | 1.68 | 1.91 | 0.64 |
| olmo-3:7b-instruct-q4_K_M                                                                        |          |   3.11 |        |     57 |    7.3 |    4 |   64 | 4.69 |      | 0.49 | 0.72 | 0.52 |
| magistral:24b-small-2506-q4_K_M                                                                  |          |   3.10 |        |     17 |     24 |    4 |   32 | 4.38 |      | 1.51 | 0.59 | 0.42 |
| gemma3:12b                                                                                       |          |   3.10 |      2 |     34 |   12.2 |    4 |  128 | 3.21 |      | 2.79 | 3.92 | 0.69 |
| qwen2.5-coder:7b-instruct-q4_K_M                                                                 |          |   3.09 |        |     54 |    7.6 |    4 |   32 | 3.69 |      | 2.84 | 1.81 | 0.13 |
| hf.co/LGAI-EXAONE/EXAONE-3.5-32B-Instruct-GGUF:Q4_K_M                                            |          |   2.98 |        |     12 |   32.0 |    4 |  256 | 3.08 |      |  4.3 | 1.46 | 0.42 |
| hf.co/mradermacher/Qwen2.5-Coder-7B-Instruct-abliterated-GGUF:Q4_K_M                             |          |   2.92 |        |     51 |   7.62 |    4 |  128 | 3.33 |      | 3.58 |  1.1 | 0.23 |
| hf.co/bartowski/ibm-granite_granite-4.1-3b-GGUF:q4_K_M                                           |          |   2.79 |        |     91 |    4.1 |    4 |  128 | 3.38 |      | 2.44 | 1.44 | 0.45 |
| hf.co/tiiuae/Falcon-H1-3B-Instruct-GGUF:Q4_K_M                                                   |          |   2.71 |        |    115 |   3.15 |    4 |      | 3.56 |      | 1.48 | 1.45 | 0.45 |
| qwen2.5:7b-instruct-q4_K_M                                                                       |          |   2.65 |        |     47 |    7.6 |    4 |  128 | 2.97 |      | 3.12 | 1.42 | 0.24 |
| hf.co/jamesburton/Phi-4-reasoning-vision-15B-GGUF:latest                                         |          |   2.59 |        |     23 |     15 |    4 |      | 3.79 |      | 0.54 |  1.1 | 0.09 |
| hf.co/tiiuae/Falcon-H1-1.5B-Deep-Instruct-GGUF:Q4_K_M                                            |          |   2.58 |        |    222 |   1.55 |    4 |      | 3.77 |      | 0.45 | 1.25 | 0.09 |
| qwen2.5-coder:3b-instruct-q4_K_M                                                                 |          |   2.55 |        |    110 |    3.1 |    4 |   32 | 3.32 |      | 2.04 | 0.63 | 0.29 |
| hf.co/mradermacher/Qwen2.5-7B-Instruct-abliterated-GGUF:Q4_K_M                                   |          |   2.55 |        |     45 |   7.62 |    4 |  128 | 3.14 |      | 2.42 | 0.62 | 0.76 |
| hf.co/mradermacher/Strand-Rust-Coder-14B-v1-GGUF:Q4_K_M                                          |          |   2.46 |        |     23 |     14 |    4 |      | 2.47 |      | 2.89 | 2.38 | 0.69 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                                                 |          |   2.41 |        |     37 |    8.8 |    4 |   32 | 3.07 |      | 1.96 |  1.0 | 0.01 |
| hf.co/bartowski/nvidia_Nemotron-3-Nano-4B-GGUF:Q4_K_M                                            |          |   2.37 |        |     11 |   30.0 |    4 |  256 | 2.95 |      | 1.51 | 1.49 | 0.81 |
| hf.co/mradermacher/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2-GGUF:Q4_K_M                  |          |   2.36 |        |     78 |   4.02 |    4 |      | 3.15 |      | 1.72 | 0.58 | 0.09 |
| hf.co/janhq/Jan-v1-edge-gguf:Q4_K_M                                                              |          |   2.31 |        |    179 |   1.72 |    4 |      | 3.03 |      | 1.92 | 0.12 | 0.73 |
| granite4:tiny-h                                                                                  |          |   2.30 |        |     45 |    6.9 |    4 | 1024 | 2.63 |      | 2.69 | 1.03 | 0.19 |
| hf.co/tiiuae/Falcon-H1-1.5B-Instruct-GGUF:Q4_K_M                                                 |          |   2.23 |        |    192 |   1.55 |    4 |      | 3.36 |      |  0.7 | 0.18 | 0.01 |
| hf.co/mradermacher/Qwen2.5-Coder-3B-Instruct-abliterated-GGUF:Q4_K_M                             |          |   2.18 |        |     94 |   3.09 |    4 |   64 | 2.55 |      | 2.37 | 1.07 |  0.0 |
| granite4:micro                                                                                   |          |   2.04 |        |     80 |    3.4 |    4 |  128 | 2.78 |      | 1.21 | 0.57 |  0.2 |
| hf.co/bartowski/allura-forge_Llama-3.3-8B-Instruct-GGUF:Q4_K_M                                   |          |   2.04 |        |     34 |   8.03 |    4 |    8 | 2.78 |      | 1.03 | 0.77 |  0.3 |
| hf.co/gabriellarson/Moonlight-16B-A3B-Instruct-GGUF:Q4_K_M                                       |          |   2.02 |        |     17 |   16.0 |    4 |    8 | 2.95 |      | 0.68 | 0.44 | 0.14 |
| hf.co/mradermacher/Ling-Coder-lite-GGUF:Q4_K_M                                                   |          |   1.98 |        |     16 |   16.8 |    4 |      | 2.59 |      | 1.32 | 0.68 | 0.51 |
| qwen3:1.7b-q4_K_M-no_think                                                                       |          |   1.86 |      3 |    124 |    2.0 |    4 |   32 | 2.26 | 0.58 | 3.93 | 1.03 | 0.44 |
| hf.co/mradermacher/Kimi-VL-A3B-Instruct-GGUF:Q4_K_M                                              |          |   1.86 |        |     15 |   16.0 |    4 |  256 | 2.26 |      | 0.97 | 0.68 | 2.78 |
| llama3.2-vision:11b-instruct-q4_K_M                                                              |          |   1.73 |        |     24 |    9.8 |    4 |  128 |  1.9 |      | 2.14 | 0.68 | 0.62 |
| hf.co/ai-sage/GigaChat3.1-10B-A1.8B-GGUF:Q4_K_M                                                  |          |   1.72 |        |     23 |     10 |    4 |      | 2.31 |      | 1.11 | 0.43 | 0.29 |
| granite4:3b                                                                                      |          |   1.69 |      2 |     66 |    3.4 |    4 |      | 3.06 | 1.37 | 1.09 | 0.57 |  0.2 |
| hf.co/mradermacher/Olmo-3-7B-Instruct-GGUF:Q4_K_M                                                |          |   1.61 |        |     31 |      7 |    4 |    2 | 2.25 |      | 0.31 |  1.1 | 0.32 |
| hf.co/mradermacher/atom-v1-preview-12b-GGUF:Q4_K_M                                               |          |   1.59 |        |     18 |   11.8 |    4 |      | 2.05 |      | 1.32 | 0.53 |  0.0 |
| hf.co/mradermacher/qwen2.5-.5b-abliterated-GGUF:Q4_K_M                                           |     0.47 |   1.59 |      5 |    336 |   0.63 |    4 |      | 2.51 |      | 0.09 | 0.09 | 0.23 |
| hf.co/bartowski/internlm_JanusCoderV-7B-GGUF:Q4_K_M                                              |          |   1.54 |        |     27 |   7.62 |    4 |      | 1.93 |      | 1.62 | 0.16 | 0.17 |
| granite4:3b-h                                                                                    |          |   1.51 |        |     63 |    3.2 |    4 |  131 | 1.79 |      |  1.7 | 0.45 | 0.17 |
| granite4:micro-h                                                                                 |          |   1.50 |        |     62 |    3.2 |    4 | 1024 | 1.82 |      | 1.55 | 0.45 | 0.15 |
| hf.co/shb777/Llama-3.3-8B-Instruct-128K-GGUF:Q4_K_M                                              |          |   1.49 |        |     25 |   8.03 |    4 |  128 | 1.54 |      |  1.9 | 1.02 | 0.37 |
| qwen2.5vl:7b-q4_K_M                                                                              |          |   1.49 |        |     24 |    8.3 |    4 |  128 |  1.7 |      | 0.69 |  2.2 | 0.15 |
| qwen2.5:3b-instruct-q4_K_M                                                                       |          |   1.41 |        |     61 |    3.1 |    4 |  128 | 2.02 |      | 0.66 | 0.23 | 0.08 |
| hf.co/mradermacher/Qwen2.5-VL-7B-Instruct-abliterated-GGUF:Q4_K_M                                |          |   1.35 |        |     24 |   7.62 |    4 |   32 | 1.73 |      | 1.23 | 0.27 | 0.02 |
| granite4:1b-bf16                                                                                 |          |   1.31 |        |     66 |      1 |   16 |  128 | 1.81 |      | 0.78 | 0.28 | 0.08 |
| granite3.3:8b                                                                                    |          |   1.30 |        |     22 |    8.0 |    4 |  128 | 1.88 |      | 0.63 | 0.09 |  0.1 |
| hf.co/mradermacher/Qwen2.5-7B-Instruct-abliterated-v3-GGUF:Q4_K_M                                |          |   1.26 |        |     22 |   7.62 |    4 |  128 | 1.22 |      | 2.14 | 0.61 | 0.06 |
| hf.co/mradermacher/Qwen2.5-3B-Instruct-abliterated-GGUF:Q4_K_M                                   |          |   1.25 |        |     49 |    3.4 |    4 |   64 | 1.73 |      | 0.77 | 0.25 |  0.0 |
| hf.co/mradermacher/olmOCR-7B-0825-GGUF:Q4_K_M                                                    |          |   1.19 |        |     21 |   7.62 |    4 |  128 | 1.72 |      | 0.36 | 0.41 | 0.02 |
| hf.co/SicariusSicariiStuff/Assistant_Pepe_8B_GGUF:Q4_K_M                                         |          |   1.18 |        |     20 |    8.0 |    4 |      | 1.65 |      | 0.58 | 0.22 |  0.3 |
| hf.co/mradermacher/AI21-Jamba-Mini-1.5-GGUF:Q4_K_M                                               |          |   1.15 |        |      3 |     52 |    4 |  256 | 1.36 |      |  1.2 | 0.44 | 0.16 |
| gemma3n:e4b                                                                                      |          |   1.12 |        |     22 |    6.9 |    4 |   32 | 1.32 |      | 0.92 | 0.92 |  0.0 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                                               |          |   1.10 |        |     98 |    1.5 |    4 |   32 | 1.46 |      | 0.85 | 0.25 |  0.0 |
| hf.co/mradermacher/wraith-8b-GGUF:Q4_K_M                                                         |          |   1.09 |        |     18 |   8.03 |    4 |      | 1.35 |      | 0.91 |  0.6 | 0.02 |
| yi-coder:1.5b-chat-q4_K_M                                                                        |          |   1.09 |        |     97 |    1.5 |    4 |  128 | 1.53 |      | 0.66 | 0.08 | 0.13 |
| hf.co/bartowski/allenai_olmOCR-2-7B-1025-GGUF:Q4_K_M                                             |          |   1.09 |        |     19 |   7.62 |    4 |    2 | 1.44 |      | 0.75 |  0.3 | 0.21 |
| hf.co/allenai/OLMo-2-0325-32B-Instruct-GGUF:Q4_0                                                 |          |   1.07 |        |      4 |   32.2 |    4 |    4 | 1.68 |      | 0.06 | 0.11 | 0.09 |
| granite4:1b-h-q8_0                                                                               |          |   1.07 |        |     65 |    1.5 |    8 |  128 | 1.53 |      | 0.35 | 0.38 | 0.06 |
| gemma3n:e2b                                                                                      |          |   1.06 |        |     31 |    4.5 |    4 |    8 |  1.4 |      | 0.95 | 0.01 | 0.05 |
| qwen3:0.6b-q4_K_M-no_think                                                                       |          |   1.03 |        |    184 |   0.75 |    4 |   32 |  1.3 |      | 0.73 | 0.36 |  0.6 |
| hf.co/DevQuasar/inference-net.Schematron-8B-GGUF:Q4_K_M                                          |          |   0.99 |        |     16 |   8.03 |    4 |      | 1.16 |      | 1.01 | 0.27 | 0.55 |
| hf.co/bartowski/utter-project_EuroLLM-22B-Instruct-2512-GGUF:Q4_K_M                              |          |   0.98 |        |      6 |   22.6 |    4 |      |  1.5 |      | 0.12 | 0.23 | 0.01 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q4_K_M                                                             |          |   0.97 |        |     50 |   2.57 |    4 |   32 | 0.98 |      | 1.39 | 0.52 | 0.28 |
| hf.co/bartowski/ai21labs_AI21-Jamba2-3B-GGUF:Q4_K_M                                              |          |   0.94 |        |     42 |    3.0 |    4 |  256 | 1.35 |      | 0.21 | 0.28 | 0.48 |
| hf.co/mradermacher/Qwen2.5-Coder-1.5B-Instruct-abliterated-GGUF:Q4_K_M                           |          |   0.91 |        |     68 |   1.78 |    4 |  128 | 1.06 |      | 1.17 | 0.14 | 0.09 |
| qwen3-vl:2b-instruct-q4_K_M                                                                      |          |   0.82 |        |     52 |    2.1 |    4 |  256 | 1.07 |      | 0.59 | 0.29 | 0.09 |
| hf.co/unsloth/medgemma-4b-it-GGUF:Q4_K_M                                                         |          |   0.80 |        |     27 |   3.88 |    4 |  128 | 1.14 |      | 0.28 | 0.16 | 0.28 |
| hf.co/DavidAU/Llama-3.2-8X3B-MOE-Dark-Champion-Instruct-uncensored-abliterated-18.4B-GGUF:Q4_K_M |          |   0.76 |        |      6 |   18.4 |    4 |      | 1.05 |      |  0.3 |  0.3 | 0.28 |
| hf.co/bartowski/microsoft_Fara-7B-GGUF:Q4_K_M                                                    |          |   0.76 |        |     13 |   7.62 |    4 |   32 | 0.55 |      | 1.85 | 0.13 | 0.45 |
| hf.co/mradermacher/Lucy-128k-GGUF:Q4_K_M                                                         |          |   0.75 |        |     58 |   1.72 |    4 |      | 0.76 |      | 1.23 | 0.05 | 0.47 |
| gemma3:4b                                                                                        |          |   0.72 |      1 |     22 |    4.3 |    4 |  128 | 1.03 |      | 0.35 | 0.15 |  0.0 |
| llama3.2:3b                                                                                      |          |   0.72 |      1 |     30 |    3.2 |    4 |  128 |  1.3 | 0.84 | 0.27 | 0.05 |  0.0 |
| hf.co/tiiuae/Falcon-H1-0.5B-Instruct-GGUF:Q4_K_M                                                 |     0.39 |   0.71 |      1 |    181 |  0.521 |    4 |      | 1.08 |      | 0.21 | 0.02 |  0.0 |
| qwen2.5vl:3b-q4_K_M                                                                              |          |   0.65 |        |     23 |    3.8 |    4 |  128 | 0.82 |      | 0.71 | 0.03 |  0.0 |
| qwen2.5:1.5b-instruct-q4_K_M                                                                     |          |   0.62 |        |     55 |    1.5 |    4 |  128 | 0.92 |      |  0.2 | 0.03 | 0.09 |
| bartowski/LiquidAI_LFM2.5-1.2B-Instruct-GGUF:Q4_K_M                                              |          |   0.61 |        |     68 |    1.2 |    4 |   32 | 0.92 |      | 0.15 | 0.09 |  0.0 |
| hf.co/vanta-research/atom-v1-preview-4b:latest                                                   |          |   0.57 |        |     20 |   3.88 |    4 |      | 0.72 |      | 0.52 | 0.19 |  0.0 |
| phi4-mini:3.8b-q4_K_M                                                                            |          |   0.56 |        |     20 |    3.8 |    4 |  128 | 0.66 |      | 0.27 | 0.78 |  0.0 |
| hf.co/mradermacher/Arch-Router-1.5B-GGUF:Q4_K_M                                                  |          |   0.52 |        |     45 |   1.54 |    4 |      | 0.73 |      | 0.32 | 0.08 |  0.0 |
| granite3.3:2b                                                                                    |          |   0.49 |        |     33 |    2.0 |    4 |  128 | 0.67 |      |  0.2 | 0.26 |  0.1 |
| hf.co/mradermacher/Qwen2.5-1.5B-Instruct-abliterated-GGUF:Q4_K_M                                 |          |   0.49 |        |     43 |   1.54 |    4 |  128 | 0.35 |      | 0.67 | 0.15 | 1.85 |
| hf.co/mradermacher/scout-4b-GGUF:Q4_K_M                                                          |          |   0.49 |        |     17 |   3.88 |    4 |      | 0.77 |      | 0.04 | 0.03 |  0.0 |
| hf.co/mradermacher/UserLM-8b-GGUF:Q4_K_M                                                         |          |   0.48 |        |      8 |      8 |    4 |      | 0.73 |      | 0.05 | 0.12 |  0.1 |
| hf.co/mradermacher/AI21-Jamba-Mini-1.7-GGUF:Q4_K_M                                               |          |   0.48 |        |      1 |     52 |    4 |  256 | 0.61 |      |  0.3 |  0.3 | 0.06 |
| hf.co/allenai/OLMo-2-1124-7B-Instruct-GGUF:Q4_K_M                                                |          |   0.46 |        |      8 |    7.3 |    4 |    2 | 0.69 |      |  0.1 | 0.08 | 0.09 |
| hf.co/arcee-ai/Trinity-Nano-Preview-GGUF:Q4_K_M                                                  |          |   0.42 |        |     15 |    3.8 |    4 |  128 | 0.39 |      | 0.29 | 0.18 | 1.46 |
| hf.co/DevQuasar/inference-net.Schematron-3B-GGUF:Q4_K_M                                          |          |   0.40 |        |     17 |   3.21 |    4 |      | 0.42 |      | 0.34 | 0.32 | 0.48 |
| minicpm-v4.5:q4_K_M                                                                              |          |   0.37 |        |      5 |    9.0 |    4 |      | 0.55 |      | 0.12 | 0.05 |  0.0 |
| qwen3.5:2b-q4_K_M-no_think                                                                       |          |   0.35 |        |      1 |   35.0 |    4 |  256 | 0.48 |      | 0.01 | 0.29 | 0.28 |
| hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M                                              |          |   0.33 |        |      6 |   6.92 |    4 |    2 | 0.53 |      | 0.03 | 0.01 |  0.0 |
| hf.co/mradermacher/Qwen2.5-VL-3B-Instruct-abliterated-GGUF:Q4_K_M                                |          |   0.31 |        |     13 |   3.09 |    4 |   64 | 0.48 |      | 0.07 | 0.01 |  0.0 |
| hf.co/Goekdeniz-Guelmez/Josiefied-Qwen2.5-1.5B-Instruct-abliterated-v2-gguf:Q4_K_M               |          |   0.30 |        |     26 |   1.54 |    4 |      | 0.44 |      | 0.09 | 0.01 | 0.09 |
| hf.co/QuantFactory/EuroLLM-9B-Instruct-GGUF:Q4_K_M                                               |          |   0.27 |        |      4 |   9.15 |    4 |      | 0.42 |      | 0.04 | 0.01 |  0.0 |
| hf.co/LiquidAI/LFM2-1.2B-GGUF:Q4_K_M                                                             |          |   0.25 |        |     28 |   1.17 |    4 |   32 |  0.4 |      | 0.01 | 0.01 |  0.0 |
| hf.co/Goekdeniz-Guelmez/Josiefied-Qwen2.5-1.5B-Instruct-abliterated-v3-gguf:Q4_K_M               |          |   0.25 |        |     21 |   1.54 |    4 |      | 0.38 |      | 0.06 | 0.01 |  0.0 |
| phi3:3.8b                                                                                        |          |   0.23 |      0 |      8 |    3.8 |    4 |  128 |  0.1 | 0.62 | 0.09 | 0.07 |  0.0 |
| hf.co/mradermacher/occiglot-7b-eu5-instruct-GGUF:Q4_K_M                                          |          |   0.21 |        |      4 |   7.24 |    4 |      | 0.23 |      |  0.0 | 0.02 | 0.95 |
| hf.co/mradermacher/Qwen2.5-VL-instruct-3B-Geo-GGUF:Q4_K_M                                        |          |   0.20 |        |      9 |   3.09 |    4 |   64 | 0.26 |      | 0.07 | 0.13 |  0.1 |
| hf.co/unsloth/Qwen3.5-0.8B-MTP-GGUF:UD-Q4_K_XL-no_think                                          |          |   0.19 |      0 |      3 |    8.0 |    4 |   32 | 0.21 |      | 0.02 | 0.01 | 0.89 |
| hf.co/mradermacher/Ling-lite-GGUF:Q4_K_M                                                         |          |   0.16 |        |      1 |   16.8 |    4 |      | 0.21 |      | 0.01 | 0.11 | 0.27 |
| hf.co/mradermacher/Qwen2.5-Coder-0.5B-Instruct-abliterated-GGUF:Q4_K_M                           |     0.37 |   0.16 |        |     44 |  0.494 |    4 |  128 | 0.05 |      | 0.02 | 0.95 |  0.0 |
| hf.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF:Q4_K_M                                                  |          |   0.16 |        |     18 |    1.2 |    4 |   32 | 0.23 |      | 0.03 | 0.09 |  0.0 |
| hf.co/arcee-ai/AFM-4.5B-GGUF:Q4_K_M                                                              |          |   0.16 |        |      5 |   4.62 |    4 |   64 | 0.24 |      | 0.04 | 0.01 |  0.0 |
| hf.co/mradermacher/AI21-Jamba-Mini-1.6-GGUF:Q4_K_M                                               |          |   0.15 |        |      0 |     52 |    4 |  256 | 0.12 |      | 0.31 | 0.01 |  0.2 |
| llama3.2:1b                                                                                      |          |   0.14 |      0 |     11 |    1.2 |    8 |  128 | 0.22 |      | 0.03 |  0.0 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                                               |          |   0.10 |        |     27 |    0.5 |    4 |   32 | 0.11 |      |  0.1 | 0.09 |  0.0 |
| granite4:350m-bf16                                                                               |          |   0.09 |        |     13 |   0.35 |   16 |      | 0.12 |      | 0.03 | 0.09 |  0.0 |
| hf.co/LiquidAI/LFM2-350M-GGUF:Q4_K_M                                                             |     0.27 |   0.09 |        |     35 |  0.354 |    4 |   32 | 0.12 |      |  0.0 | 0.09 | 0.09 |
| hf.co/mradermacher/EuroLLM-1.7B-Instruct-GGUF:Q4_K_M                                             |          |   0.09 |        |      7 |   1.66 |    4 |  128 | 0.09 |      | 0.09 | 0.09 | 0.09 |
| granite4:350m-h-q8_0                                                                             |          |   0.07 |        |     18 |   0.35 |    8 |  131 |  0.1 |      |  0.0 |  0.0 | 0.09 |
| qwen3.5:0.8b-q8_0-no_think                                                                       |          |   0.06 |        |      1 |    8.0 |    8 |   32 | 0.03 |      | 0.14 | 0.09 | 0.09 |
| qwen2.5:0.5b-instruct-q4_K_M                                                                     |          |   0.06 |        |     17 |    0.5 |    4 |  128 | 0.06 |      |  0.1 |  0.0 | 0.09 |
| gemma3:270m                                                                                      |          |   0.06 |        |     19 |   0.27 |    8 |   32 |  0.0 |      | 0.09 | 0.28 |  0.0 |
| gemma3:1b                                                                                        |          |   0.06 |        |      7 |    1.0 |    4 |   32 | 0.08 |      | 0.03 |  0.0 |  0.0 |
| smollm2:360m-instruct-q4_K_M                                                                     |          |   0.05 |        |     20 |  0.362 |    4 |      | 0.03 |      | 0.09 | 0.09 | 0.09 |
| hf.co/LiquidAI/LFM2-700M-GGUF:Q4_K_M                                                             |          |   0.04 |        |      7 |    0.7 |    4 |   32 | 0.03 |      |  0.0 | 0.09 | 0.09 |
| hf.co/allenai/OLMo-2-0425-1B-Instruct-GGUF:Q4_K_M                                                |          |   0.04 |        |      3 |   1.48 |    4 |    4 | 0.03 |      | 0.09 |  0.0 |  0.0 |
| hf.co/LiquidAI/LFM2.5-350M-GGUF:Q4_K_M                                                           |          |   0.03 |        |      0 |   24.0 |    4 |  128 |  0.0 |      | 0.09 | 0.09 |  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                                                   |     0.15 |   0.02 |        |     15 |  0.135 |    8 |    2 |  0.0 |      |  0.0 | 0.17 |  0.0 |

### Thinking
| Model                                                                                            | Best<br/>Model<br/>for<br/>Size (GB) | PE-200-<br/>Score | Performance-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | JavaScript | Java | Rust | Clojure |
| :----------------------------------------------------------------------------------------------- | -----------------------------------: | ----------------: | ---------------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---------: | ---: | ---: | ------: |
| deepseek-v4-flash-0731-think                                                                     |          |  114.4 |        |        |        |    4 | 1024 | 121.26 |      | 121.45 | 112.66 |  7.6 |
| ox-alpha-think                                                                                   |          |  102.7 |        |        |        |   16 | 1024 | 105.8 | 109.32 | 114.52 | 110.15 | 10.31 |
| ling-3.0-flash-think                                                                             |      248 |   81.6 |        |     33 |  124.0 |   16 |  256 | 87.1 |      | 83.59 | 84.02 | 1.51 |
| qwen3.7-flash-think                                                                              |          |   75.6 |        |        |        |   16 | 1000 | 84.46 |      | 81.52 | 55.27 | 0.57 |
| qwen3.6:27b-mtp-q8_0-think                                                                       |    29.70 |   75.2 |     16 |    253 |     27 |    8 |  256 | 80.43 |      | 78.23 | 65.65 | 20.66 |
| qwen3.6:35b-a3b-mtp-q8_0-think                                                                   |          |   67.5 |     45 |    175 |     35 |    8 |  256 | 73.1 |      | 76.02 | 51.37 | 7.09 |
| gemma4:31b-it-qat-think                                                                          |    23.02 |   67.2 |        |    292 |   30.7 |    4 |  256 | 74.06 |      | 73.28 | 50.91 |  3.6 |
| frob/qwen-agentworld:35b-a3b-ud-q8_K_XL-think                                                    |          |   65.7 |        |    171 |     35 |    8 |  256 | 68.1 |      | 68.67 | 65.4 | 21.05 |
| gemma4:31b-it-q8_0-think                                                                         |          |   64.6 |        |    191 |   30.7 |    8 |  256 | 71.92 |      | 63.29 | 51.47 | 12.46 |
| gemma4:31b-mxfp8-think                                                                           |          |   62.6 |        |    185 |   30.7 |    8 |  256 | 68.0 |      | 64.77 | 55.03 | 8.09 |
| gemma4:31b-it-q4_K_M-think                                                                       |    23.02 |   61.4 |        |    267 |   30.7 |    4 |  256 | 64.0 |      | 65.1 | 62.3 | 11.08 |
| qwen3.5:27b-nvfp4-think                                                                          |    20.25 |   58.8 |        |    290 |   27.0 |    4 |  256 | 66.05 |      | 61.25 | 42.64 | 4.29 |
| hf.co/InternScience/Agents-A1-Q8_0-GGUF:Q8_0-think                                               |          |   58.6 |     50 |    152 |   35.0 |    8 |  256 | 67.1 |      | 55.83 | 44.84 | 3.61 |
| gemma4:31b-nvfp4-think                                                                           |          |   58.6 |        |    255 |   30.7 |    4 |  256 | 62.19 |      | 65.01 | 51.65 |  7.4 |
| gemma4:26b-a4b-it-q8_0-think                                                                     |          |   58.3 |        |    210 |   25.2 |    8 |  256 | 62.19 |      | 56.38 | 62.99 | 6.42 |
| gemma4:26b-a4b-it-qat-think                                                                      |    18.90 |   58.3 |        |    308 |   25.2 |    4 |  256 | 61.24 |      | 65.28 | 56.07 | 1.45 |
| hf.co/s-batman/Agents-A1-NVFP4-MTP-GGUF:latest-think                                             |          |   57.6 |        |    219 |   35.0 |    4 |  256 | 67.84 |      | 60.79 | 26.25 | 3.36 |
| hf.co/inclusionAI/Ring-flash-2.0-GGUF:Q4_K_M                                                     |          |   55.2 |        |     71 |    103 |    4 |  128 | 57.25 |      | 58.6 | 41.79 | 40.64 |
| qwen3.5:35b-a3b-q4_K_M-think                                                                     |          |   54.9 |        |    209 |   35.0 |    4 |  256 | 68.4 |      | 39.13 | 33.71 | 8.01 |
| gemma4:12b-it-qat-think                                                                          |     9.00 |   54.3 |     29 |    603 |   12.0 |    4 |  256 | 65.84 |      | 43.59 | 37.86 | 1.09 |
| gemma4:26b-mxfp8-think                                                                           |          |   54.0 |        |    195 |   25.2 |    8 |  256 | 57.19 |      | 58.67 | 51.61 | 3.13 |
| qwen3.5:35b-a3b-mxfp8-think                                                                      |          |   53.4 |        |    139 |   35.0 |    8 |  256 | 60.31 |      | 51.69 | 42.46 | 5.17 |
| gpt-oss-20b-think                                                                                |          |   52.5 |        |    131 |   20.0 |   16 |  128 | 50.63 |      | 66.92 | 59.34 | 0.77 |
| qwen3.6:27b-q8_0-think                                                                           |          |   50.7 |     11 |    171 |   27.0 |    8 |  256 | 52.58 |      | 56.67 | 45.94 | 14.41 |
| qwen3.6:35b-a3b-coding-mxfp8-think                                                               |          |   50.3 |        |    131 |   35.0 |    8 |  256 | 54.97 |      | 50.45 | 44.75 | 6.75 |
| qwen3.5:35b-a3b-coding-mxfp8-think                                                               |          |   49.8 |        |    129 |   35.0 |    8 |  256 | 55.85 |      | 50.17 | 39.47 | 2.83 |
| qwen3.6:35b-a3b-mxfp8-think                                                                      |          |   49.8 |        |    129 |   35.0 |    8 |  256 | 55.47 |      | 52.89 | 33.7 | 9.65 |
| qwen3.6:35b-a3b-nvfp4-think                                                                      |          |   48.6 |        |    185 |   35.0 |    4 |  256 | 52.06 |      | 57.27 | 34.35 |  7.9 |
| qwen3.5:35b-a3b-coding-nvfp4-think                                                               |          |   48.6 |        |    185 |     35 |    4 |  256 | 58.53 |      | 39.28 | 33.06 | 4.72 |
| qwen3.6:27b-bf16-think                                                                           |          |   48.2 |        |     89 |   27.0 |   16 |  256 | 48.34 |      | 58.27 | 46.8 | 8.87 |
| qwen3.6:35b-a3b-coding-nvfp4-think                                                               |          |   47.8 |        |    182 |   35.0 |    4 |  256 | 55.2 |      | 45.44 | 31.44 | 8.67 |
| nemotron-cascade-2:30b-a3b-q4_K_M                                                                |          |   47.4 |        |    200 |   31.6 |    4 |  256 | 56.59 |      | 39.19 | 31.05 | 9.01 |
| qwen3.5:35b-a3b-q8_0-think                                                                       |          |   46.7 |        |    121 |   35.0 |    8 |  256 | 48.73 |      | 55.77 | 37.59 | 8.33 |
| qwen3:30b-a3b-thinking-2507-q4_K_M                                                               |          |   46.3 |        |    202 |   30.5 |    4 |  128 | 47.67 |      | 56.83 | 31.3 | 22.16 |
| nemotron-3-nano:30b-a3b-q4_K_M                                                                   |          |   45.7 |        |    193 |   31.6 |    4 | 1024 | 48.01 |      | 57.0 | 29.47 | 13.21 |
| qwen3.6:35b-a3b-q8_0-think                                                                       |          |   45.7 |     38 |    119 |   35.0 |    8 |  256 | 48.59 |      | 48.94 | 39.76 | 10.75 |
| qwen3-next:80b-a3b-thinking-q4_K_M                                                               |          |   44.8 |        |     75 |   79.7 |    4 |  256 | 45.31 |      | 53.11 | 39.97 | 15.62 |
| qwen3.5:35b-a3b-nvfp4-think                                                                      |          |   44.6 |        |    170 |     35 |    4 |  256 | 48.34 |      | 49.56 | 33.42 | 8.22 |
| qwen3.5:27b-q4_K_M-think                                                                         |          |   43.7 |        |    216 |   27.0 |    4 |  256 | 45.09 |      | 55.69 | 32.6 | 7.21 |
| qwen3.5:27b-mxfp8-think                                                                          |          |   42.7 |        |    144 |   27.0 |    8 |  256 | 46.06 |      | 45.84 | 38.21 | 1.89 |
| gemma4:26b-nvfp4-think                                                                           |          |   42.7 |        |    154 |   25.2 |    8 |  256 | 43.5 |      | 51.38 | 39.34 | 6.18 |
| nemotron-3-super:120b-a12b-q4_K_M-think                                                          |          |   42.0 |        |     47 |    120 |    4 | 1000 | 46.35 |      | 46.37 | 28.73 | 5.82 |
| gemma4:12b-it-q8_0-think                                                                         |          |   41.0 |        |    311 |   12.0 |    8 |  256 | 39.08 |      | 50.66 | 49.66 |      |
| qwen3.6:27b-q4_K_M-think                                                                         |          |   39.6 |     10 |    196 |   27.0 |    4 |  256 | 39.23 |      | 44.53 | 42.88 | 13.14 |
| qwen3.5:27b-q8_0-think                                                                           |          |   37.9 |      8 |    128 |   27.0 |    8 |  256 | 40.4 |      | 40.97 | 35.03 | 3.14 |
| hf.co/bartowski/nvidia_Nemotron-Cascade-8B-Thinking-GGUF:Q4_K_M                                  |     6.14 |   37.7 |        |    614 |   8.19 |    4 |  128 | 45.65 |      | 39.25 | 13.4 | 0.45 |
| hf.co/mradermacher/Ring-mini-2.0-GGUF:Q4_K_M                                                     |          |   36.7 |        |    306 |     16 |    4 |  128 | 37.07 |      | 46.09 | 31.0 | 8.01 |
| hf.co/deepreinforce-ai/Ornith-1.0-35B-GGUF:Q4_K_M-think                                          |          |   35.7 |        |    136 |     35 |    4 |      | 40.17 |      | 36.88 | 23.56 | 7.71 |
| hf.co/bartowski/nvidia_Nemotron-Cascade-14B-Thinking-GGUF:Q4_K_M                                 |          |   33.6 |        |    302 |   14.8 |    4 |      | 39.78 |      | 32.01 | 19.42 | 1.67 |
| gemma4:e4b-it-q8_0-think                                                                         |          |   33.2 |        |    378 |    8.0 |    8 |  256 | 33.67 |      | 37.05 | 38.07 | 0.66 |
| olmo-3.1:32b-think-q4_K_M                                                                        |          |   33.0 |        |    136 |   32.2 |    4 |   64 | 36.34 |      | 40.86 | 15.51 | 5.65 |
| hf.co/bartowski/nvidia_Nemotron-Cascade-8B-GGUF:Q4_K_M                                           |     6.14 |   32.9 |        |    535 |   8.19 |    4 |  128 | 40.79 |      | 31.35 | 11.2 | 0.69 |
| north-mini-code-1.0:q4_K_M-think                                                                 |          |   32.8 |        |    146 |   30.0 |    4 |  500 | 38.64 |      | 28.13 | 20.61 | 9.78 |
| qwen3.6:27b-nvfp4-think                                                                          |          |   29.2 |        |    144 |   27.0 |    4 |  256 | 27.55 |      | 40.01 | 29.17 | 6.32 |
| hf.co/mradermacher/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-i1-GGUF:Q4_K_M-think          |          |   28.4 |        |    135 |     28 |    4 |  256 | 28.18 |      | 32.16 | 30.87 | 7.68 |
| hf.co/bartowski/NousResearch_NousCoder-14B-GGUF:Q4_K_M                                           |          |   28.2 |        |    254 |   14.8 |    4 |      | 33.87 |      | 20.18 | 23.3 | 3.09 |
| qwen3.5:9b-mxfp8-think                                                                           |          |   27.9 |        |    281 |    9.0 |    8 |  256 | 30.42 |      | 30.57 | 21.49 | 2.63 |
| hf.co/bartowski/nvidia_Orchestrator-8B-GGUF:Q4_K_M                                               |     6.14 |   27.5 |        |    448 |   8.19 |    4 |  128 | 33.75 |      | 25.36 | 11.03 | 3.39 |
| gemma4:e4b-it-q4_K_M-think                                                                       |     6.00 |   27.0 |        |    451 |    8.0 |    4 |  256 | 28.2 |      | 35.65 | 18.99 | 0.65 |
| nemotron3:33b-q4_K_M-think                                                                       |          |   26.3 |        |    106 |     33 |    4 |      | 29.0 |      | 29.54 | 15.0 | 9.23 |
| hf.co/ijohn07/QED-Nano-Q4_K_M-GGUF:Q4_K_M                                                        |     3.00 |   25.5 |        |    852 |      4 |    4 |      | 30.11 |      | 31.38 | 3.66 | 4.11 |
| hf.co/mradermacher/Qwen3-30B-A3B-YOYO-V2-Claude-4.6-Opus-High-INSTRUCT-GGUF:Q4_K_M               |          |   25.1 |        |    112 |     30 |    4 |  256 | 26.09 |      | 27.4 | 22.85 | 8.38 |
| hf.co/janhq/Jan-v1-4B-GGUF:Q4_K_M                                                                |          |   24.8 |        |    823 |   4.02 |    4 |      | 31.03 |      | 21.99 | 8.96 |  2.1 |
| gpt-oss:120b                                                                                     |          |   24.5 |        |     28 |  116.8 |    4 |  128 | 23.7 |      | 23.82 | 25.17 | 27.33 |
| hf.co/janhq/Jan-v1-2509-gguf:Q4_K_M                                                              |          |   23.5 |        |    781 |   4.02 |    4 |      | 29.27 |      | 23.63 | 5.84 |  0.6 |
| olmo-3:32b-think-q4_K_M                                                                          |          |   23.5 |        |     97 |   32.2 |    4 |   64 | 26.44 |      | 25.49 | 16.25 | 0.08 |
| hf.co/bartowski/PrimeIntellect_INTELLECT-3-GGUF:Q2_K                                             |          |   23.4 |        |     11 |  107.0 |    2 |  128 | 24.59 |      | 23.94 | 21.76 | 8.19 |
| olmo-3:7b-think-q4_K_M                                                                           |          |   22.7 |        |    415 |    7.3 |    4 |   64 | 31.93 |      | 12.21 | 4.34 | 1.21 |
| hf.co/mradermacher/Nanbeige4.1-3B-GGUF:Q4_K_M                                                    |     2.25 |   21.9 |        |    972 |      3 |    4 |      | 29.47 |      | 13.83 | 6.77 |  1.4 |
| hf.co/mradermacher/DASD-30B-A3B-Thinking-Preview-GGUF:Q4_K_M                                     |          |   21.5 |        |     96 |     30 |    4 |  128 | 22.85 |      | 18.36 | 20.31 | 16.56 |
| hf.co/tiiuae/Falcon-H1R-7B-GGUF:Q4_K_M                                                           |          |   21.4 |        |    377 |   7.59 |    4 |      | 26.08 |      | 13.07 | 17.14 | 7.79 |
| hf.co/bartowski/cerebras_GLM-4.5-Air-REAP-82B-A12B-GGUF:Q4_0                                     |          |   21.2 |        |     33 |   85.0 |    4 |      | 23.88 |      | 19.77 | 15.73 | 7.57 |
| qwen3.5:9b-q4_K_M-think                                                                          |          |   21.2 |     15 |    314 |    9.0 |    4 |  256 | 25.67 |      | 19.64 | 10.59 | 0.89 |
| gemma4:e4b-mxfp8-think                                                                           |          |   20.7 |        |    235 |    8.0 |    8 |  256 | 23.16 |      | 20.54 | 17.31 | 0.64 |
| gemma4:e4b-nvfp4-think                                                                           |          |   20.0 |        |    333 |    8.0 |    4 |  256 | 19.7 |      | 27.1 | 17.96 | 0.72 |
| hf.co/AaryanK/MiniMax-M2.1-GGUF:Q2_K                                                             |          |   19.9 |        |      4 |  229.0 |    2 |  200 | 22.83 |      | 20.51 | 11.72 | 2.71 |
| hf.co/mradermacher/apollo-astralis-4b-GGUF:Q4_K_M                                                |          |   19.9 |        |    659 |   4.02 |    4 |      | 24.22 |      | 19.35 | 6.47 | 3.75 |
| gemma4:12b-mlx-think                                                                             |          |   19.1 |        |    212 |   12.0 |    4 |  256 | 22.41 |      |      |      |      |
| hf.co/TeichAI/Qwen3-14B-Claude-4.5-Opus-High-Reasoning-Distill-GGUF:Q4_K_M                       |          |   18.3 |        |    174 |   14.0 |    4 |      | 22.09 |      | 20.54 | 4.02 | 1.22 |
| gemma4:31b-coding-mtp-bf16-think                                                                 |          |   17.7 |        |     28 |   31.0 |   16 |      | 20.69 |      |      |      |      |
| gemma4:e2b-it-q8_0-think                                                                         |          |   17.6 |        |    313 |    5.1 |    8 |  256 | 18.76 |      | 19.68 | 15.36 | 0.67 |
| qwen3:4b-thinking-2507-q4_K_M                                                                    |          |   17.5 |        |    582 |    4.0 |    4 |   32 | 20.88 |      | 16.63 | 7.49 | 4.63 |
| gpt-oss:20b                                                                                      |          |   16.6 |        |     72 |   20.9 |    8 |  128 | 16.51 |      | 16.85 | 17.86 | 10.99 |
| qwen3-vl:8b-thinking-q4_K_M                                                                      |          |   16.6 |        |    252 |    8.8 |    4 |  256 | 17.68 |      | 17.45 | 14.18 | 5.49 |
| hf.co/mradermacher/MiroThinker-v1.0-30B-GGUF:Q4_K_M                                              |          |   16.4 |        |     71 |   30.5 |    4 |      | 19.25 |      | 14.9 |  9.4 | 4.27 |
| hf.co/mradermacher/FrogMini-14B-2510-GGUF:Q4_K_M                                                 |          |   16.0 |        |    152 |     14 |    4 |      | 16.38 |      | 26.28 | 3.51 | 3.16 |
| qwen3-vl:4b-thinking-q4_K_M                                                                      |          |   15.3 |        |    463 |    4.4 |    4 |  256 | 17.87 |      | 13.81 | 8.84 | 5.31 |
| hf.co/t-tech/T-pro-it-2.1-GGUF:Q4_K_M                                                            |          |   15.2 |        |     62 |   32.8 |    4 |      | 17.56 |      | 14.77 | 7.87 | 5.48 |
| qwen3.5:9b-nvfp4-think                                                                           |          |   14.2 |        |    211 |    9.0 |    4 |  256 | 12.42 |      | 26.32 | 9.44 | 1.27 |
| gemma4:e2b-mxfp8-think                                                                           |          |   13.4 |        |    238 |    5.1 |    8 |  256 | 13.32 |      | 17.86 | 11.75 | 0.48 |
| hf.co/mradermacher/Qwen3.5-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled-i1-GGUF:Q4_K_M-think      |          |   13.2 |        |     49 |     36 |    4 |  256 | 14.22 |      | 13.16 | 13.15 | 1.57 |
| hf.co/bartowski/AGI-0_Art-0-8B-GGUF:Q4_K_M                                                       |          |   12.5 |        |    203 |   8.19 |    4 |   40 | 13.08 |      | 15.02 | 9.78 | 2.08 |
| hf.co/InternScience/Agents-A1-4B-Q4_K_M-GGUF:Q4_K_M-think                                        |          |   11.7 |     13 |    391 |      4 |    4 |  256 | 12.47 |      | 16.45 | 5.52 | 0.46 |
| qwen3.5:4b-mxfp8-think                                                                           |          |   11.5 |        |    262 |      4 |    8 |  256 | 14.85 |      | 8.26 | 5.26 | 0.86 |
| glm-4.7-flash:Q4_K_M                                                                             |          |   10.5 |        |     45 |     31 |    4 |  198 | 11.83 |      | 10.13 |  7.7 | 2.27 |
| hf.co/mradermacher/Tess-4-9B-GGUF:Q4_K_M-think                                                   |          |   10.5 |        |    155 |    9.0 |    4 |      | 13.17 |      | 6.18 | 6.41 | 4.33 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                                                   |          |   10.2 |        |     42 |   32.8 |    4 |   32 | 10.02 |      | 15.13 | 6.72 | 2.06 |
| hf.co/mradermacher/DASD-4B-Thinking-GGUF:Q4_K_M                                                  |          |   10.0 |        |    334 |      4 |    4 |      | 10.73 |      | 9.72 | 9.18 | 3.87 |
| hf.co/LiquidAI/LFM2.5-8B-A1B-GGUF:q4_K_M-think                                                   |          |   9.68 |        |    152 |   8.47 |    4 |    8 | 11.92 |      |  7.1 | 3.97 | 6.06 |
| nemotron-3-nano:30b-a3b-q4_K_M-think                                                             |          |   9.58 |        |     43 |   30.0 |    4 |  256 | 11.05 |      | 10.86 | 4.23 | 0.71 |
| lfm2.5:8b-a1b-q4_K_M-think                                                                       |          |   9.43 |     18 |    157 |    8.0 |    4 |    8 | 13.19 |      | 3.18 | 3.71 | 2.89 |
| qwen3.5:4b-q4_K_M-think                                                                          |          |   9.17 |     10 |    306 |      4 |    4 |  256 | 10.54 |      | 9.12 | 6.11 | 0.76 |
| hf.co/mradermacher/SERA-8B-GGUF:Q4_K_M                                                           |          |   8.87 |        |    148 |      8 |    4 |      | 10.07 |      | 8.64 | 6.85 |  0.6 |
| gemma4:e2b-it-q4_K_M-think                                                                       |          |   8.49 |        |    222 |    5.1 |    4 |  256 | 9.08 |      | 7.99 |  9.0 | 1.72 |
| hf.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF:q4_K_M-think                                  |          |   8.18 |        |    121 |      9 |    4 | 1024 | 10.13 |      | 8.62 | 1.24 |      |
| gemma4:e2b-nvfp4-think                                                                           |          |   8.10 |        |    212 |    5.1 |    4 |  256 | 10.85 |      | 4.73 | 3.41 | 0.51 |
| hf.co/mradermacher/Kimi-VL-A3B-Thinking-2506-GGUF:Q4_K_M                                         |          |   8.09 |        |     67 |   16.0 |    4 |  128 | 9.27 |      | 6.38 | 7.86 | 1.07 |
| hf.co/LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M-think                                                     |          |   7.94 |        |    176 |    6.0 |    4 |   32 | 11.48 |      | 4.15 | 0.26 | 0.29 |
| ornith:9b-q4_K_M-think                                                                           |          |   7.53 |        |    111 |      9 |    4 |      | 7.91 |      | 11.94 | 1.18 | 1.77 |
| hf.co/unsloth/Qwen3.5-9B-MTP-GGUF:UD-Q4_K_XL-think                                               |          |   7.24 |      5 |    107 |    9.0 |    4 |  256 | 8.88 |      | 6.37 | 3.55 | 0.52 |
| hf.co/mradermacher/VibeThinker-1.5B-GGUF:Q4_K_M                                                  |     1.33 |   6.55 |        |    491 |   1.78 |    4 |      | 9.38 |      | 1.51 | 1.97 |  3.3 |
| nemotron-cascade-2:30b-a3b-q4_K_M-think                                                          |          |   6.24 |        |     28 |   30.0 |    4 |  256 | 7.28 |      | 6.33 | 3.53 |  0.5 |
| hf.co/mradermacher/MiroThinker-v1.0-8B-GGUF:Q4_K_M                                               |          |   5.99 |        |     97 |   8.19 |    4 |      | 6.82 |      | 6.08 | 3.77 | 1.14 |
| hf.co/t-tech/T-lite-it-2.1-GGUF:Q4_K_M                                                           |          |   5.76 |        |     94 |   8.19 |    4 |      | 6.84 |      | 5.82 | 2.41 | 1.11 |
| hf.co/unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL-think                                               |          |   5.28 |      6 |    176 |    4.0 |    4 |  256 | 6.42 |      | 5.04 | 2.42 |  0.0 |
| hf.co/mradermacher/MiroThinker-v1.0-72B-GGUF:Q4_K_M                                              |          |   4.51 |        |      8 |   72.7 |    4 |      |  5.1 |      | 3.57 | 4.42 | 1.04 |
| hf.co/bartowski/ai21labs_AI21-Jamba-Reasoning-3B-GGUF:Q4_K_M                                     |          |   3.17 |        |    141 |    3.0 |    4 |  256 | 4.28 |      |  1.3 |  1.9 | 0.36 |
| nemotron-3-nano:4b-q8_0-think                                                                    |          |   2.80 |        |      8 |   30.0 |    8 |  256 |  3.5 |      | 2.25 | 1.08 | 0.76 |
| hf.co/mradermacher/SmolLM3-3B-gabliterated-GGUF:Q4_K_M                                           |          |   1.55 |        |     67 |   3.08 |    4 |      | 2.31 |      | 0.37 | 0.36 | 0.12 |
| qwen3-vl:2b-thinking-q4_K_M                                                                      |          |   1.55 |        |     98 |    2.1 |    4 |  256 | 1.49 |      | 2.25 | 1.14 | 0.42 |
| lfm2.5-thinking:1.2b-q4_K_M                                                                      |     0.90 |   1.52 |        |    168 |    1.2 |    4 |   32 | 1.83 |      | 1.74 | 0.09 | 0.47 |
| hf.co/unsloth/SmolLM3-3B-GGUF:Q4_K_M                                                             |          |   1.29 |        |     56 |   3.08 |    4 |      | 1.65 |      | 1.16 | 0.31 | 0.09 |
| openbmb/minicpm5:q8_0-think                                                                      |          |   1.12 |        |    102 |    1.0 |    8 |      | 1.71 |      | 0.36 | 0.01 |  0.0 |
| hf.co/unsloth/SmolLM3-3B-128K-GGUF:UD-Q4_K_XL-think                                              |          |   0.92 |        |     41 |      3 |    4 |  128 | 1.08 |      |      |      |      |
| hf.co/Luminia/MiniCPM5-1B-Agent-GGUF:Q8_0-think                                                  |          |   0.55 |        |     50 |    1.0 |    8 |      | 0.26 |      | 1.69 | 0.31 | 0.14 |
| qwen3.5:0.8b-q8_0-think                                                                          |     0.60 |   0.55 |        |     91 |    0.8 |    4 |  256 | 0.53 |      | 0.17 | 0.52 | 1.77 |
| hf.co/mradermacher/MiniCPM-V-4.6-GGUF:Q4_K_M-think                                               |          |   0.36 |        |        |        |    4 |      | 0.22 |      | 0.62 |  0.7 | 0.09 |
| phi4-mini-reasoning:3.8b-q4_K_M                                                                  |          |   0.34 |        |     12 |    3.8 |    4 |  128 | 0.55 |      |  0.0 |  0.0 |  0.0 |
| openbmb/minicpm5:q4_K_M-think                                                                    |          |   0.33 |        |     44 |    1.0 |    4 |      | 0.47 |      | 0.19 | 0.01 |  0.0 |
| minicpm-v4.6:q8_0-think                                                                          |          |   0.29 |        |     26 |    1.0 |    8 |      |  0.4 |      | 0.15 | 0.08 |  0.0 |
| hf.co/openbmb/MiniCPM5-1B-GGUF:Q4_K_M-think                                                      |          |   0.20 |      0 |     27 |      1 |    4 |      | 0.24 |      |      |      |      |
| hf.co/PleIAs/Baguettotron-GGUF:Q4_K_M                                                            |     0.24 |   0.03 |        |     12 |  0.321 |    4 |      |  0.0 |      | 0.09 | 0.09 |  0.0 |

## Archived Outdated PE-Bench-100
The following Benchmark result ("PE-Bench-Python-100", "PE-Bench-Java-100", "PE-Bench-Rust-100", "PE-Bench-Clojure-100") is an archive of a retired computation process that does not only compute only 100 problems for each language (the best models saturated those already) but also it used different prompt templates, so the benchmark values cannot be compared with the PE-Bench-200:

| Model                                                                                            | Best<br/>Model<br/>for<br/>Size (GB) | PE-100-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | Java | Rust | Clojure |
| :----------------------------------------------------------------------------------------------- | -----------------------------------: | ----------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---: | ---: | ------: |
| Grok-4-Fast                                                                                      |          |  22.54 |        |        |   16 | 2000 | 22.44 | 25.47 | 21.44 | 16.38 |
| o4-mini-2025-04-16                                                                               |          |  21.34 |        |        |   16 |  200 | 22.71 | 21.88 | 21.59 | 13.71 |
| gpt-4.1-2025-04-14                                                                               |          |  19.84 |        |        |   16 | 1024 | 22.41 | 20.88 | 17.0 | 12.08 |
| gpt-4.1-mini-2025-04-14                                                                          |          |  18.05 |        |        |   16 | 1024 | 18.34 | 20.53 | 18.99 | 7.56 |
| qwen3-coder:480b-a35b-q4_K_M                                                                     |      360 |  17.57 |      5 |  480.2 |    4 |  256 | 20.69 | 18.91 | 14.88 |  6.5 |
| DeepSeek-V3-0324                                                                                 |          |  17.06 |      1 |  671.0 |   16 |  128 | 20.08 | 18.63 | 14.91 | 4.62 |
| DeepSeek-V3                                                                                      |          |  16.11 |      1 |  671.0 |   16 |  128 | 20.01 | 16.95 | 12.16 | 5.92 |
| deepseek-v3.1:671b                                                                               |          |  15.27 |      3 |  671.0 |    4 |  160 | 19.25 | 14.73 | 12.78 | 5.93 |
| qwen3:235b-a22b-instruct-2507-q4_K_M                                                             |      176 |  15.26 |      9 |  235.1 |    4 |  256 | 18.66 | 17.64 | 10.32 | 4.38 |
| GPT-4o                                                                                           |          |  14.72 |        |        |   16 |  128 | 17.05 | 13.87 | 14.57 | 8.24 |
| mlx-community/Qwen3-Next-80B-A3B-Instruct-8bit                                                   |    87.67 |  14.46 |     16 |   79.7 |    8 |  256 | 18.85 | 15.27 | 9.92 | 3.51 |
| gpt-4-turbo-2024-04-09                                                                           |          |  13.86 |        |        |   16 |  128 | 16.87 | 15.82 | 10.12 | 3.45 |
| qwen3-coder:30b-a3b-q4_K_M                                                                       |    22.88 |  11.69 |     51 |   30.5 |    4 |  256 | 14.3 | 12.72 | 9.61 | 2.34 |
| GPT-o1-Mini                                                                                      |          |  11.32 |        |        |   16 |   32 | 17.44 |      |      |      |
| qwen3:30b-a3b-instruct-2507-q8_0                                                                 |          |  11.19 |     33 |   30.5 |    8 |  256 | 14.29 | 11.13 | 9.15 | 3.04 |
| athene-v2:72b-q8_0                                                                               |          |  10.97 |     14 |   72.7 |    8 |  128 | 16.22 | 10.15 | 5.55 | 3.32 |
| qwen3:30b-a3b-instruct-2507-q4_K_M                                                               |    22.88 |  10.78 |     47 |   30.5 |    4 |  256 | 13.95 | 10.58 | 8.42 | 3.39 |
| qwen3:235b-a22b-q4_K_M-no_think                                                                  |          |  10.76 |      6 |  235.1 |    4 |  128 | 13.27 | 15.17 | 3.33 | 2.35 |
| qwen3-coder:30b-a3b-q8_0                                                                         |          |  10.73 |     32 |   30.5 |    8 |  256 | 13.94 | 11.51 | 6.22 | 4.62 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                                                      |          |  10.60 |     19 |   72.7 |    4 |  128 | 14.49 | 10.56 | 6.33 | 3.74 |
| athene-v2:72b-q4_K_M                                                                             |          |  10.48 |     19 |   72.7 |    4 |  128 | 14.07 | 11.19 | 6.55 | 1.83 |
| llama4:17b-maverick-128e-instruct-q4_K_M                                                         |          |  10.38 |      3 |  401.6 |    4 | 1024 | 11.3 | 11.44 | 9.93 | 4.39 |
| gpt-4.1-nano-2025-04-14                                                                          |          |  10.35 |        |        |   16 | 1024 | 13.79 | 10.36 | 7.83 |  1.6 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                                                   |          |  10.33 |     42 |   32.8 |    4 |   32 | 12.72 | 11.67 | 7.25 | 2.89 |
| GPT-o1-Preview                                                                                   |          |  10.29 |      2 |  300.0 |   16 |   32 | 15.86 |      |      |      |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q8_0                                                     |          |  10.28 |     28 |   32.8 |    8 |   32 | 12.76 | 10.75 | 8.04 | 3.43 |
| qwen2.5:72b-instruct-q4_K_M                                                                      |          |   9.78 |     18 |   72.7 |    4 |  128 | 14.02 |  9.1 | 5.97 | 2.46 |
| qwen2.5:72b-instruct-q8_0                                                                        |          |   9.77 |     12 |   72.7 |    8 |  128 | 12.98 | 10.5 | 5.41 | 3.49 |
| qwen2.5-coder:32b-instruct-q4_K_M                                                                |          |   9.77 |     40 |   32.8 |    4 |   32 | 14.05 | 8.82 | 6.41 |  2.2 |
| hf.co/bartowski/Dracarys2-72B-Instruct-GGUF:Q4_K_M                                               |          |   9.74 |     18 |   72.7 |    4 |  128 | 13.45 | 8.54 | 7.34 | 3.35 |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M                                  |          |   9.69 |     18 |   72.7 |    4 |  128 | 13.92 | 8.65 | 6.11 | 3.07 |
| hf.co/bartowski/THUDM_GLM-4-32B-0414-GGUF:Q4_K_M                                                 |          |   9.64 |     39 |   32.6 |    4 |   32 | 13.9 | 10.14 | 4.82 | 0.75 |
| hf.co/bartowski/Sky-T1-32B-Flash-GGUF:Q4_K_M                                                     |          |   9.62 |     39 |   32.8 |    4 |   32 | 12.04 | 10.75 | 6.64 |  2.5 |
| hf.co/mradermacher/Bespoke-Stratos-32B-GGUF:Q4_K_M                                               |          |   9.61 |     39 |   32.8 |    4 |   32 | 12.37 |  9.9 | 7.58 | 1.78 |
| qwen2.5-coder:32b-instruct-q8_0                                                                  |          |   9.38 |     26 |   32.8 |    8 |   32 | 11.94 | 9.94 | 6.69 |  2.8 |
| qwen2.5:32b-instruct-q4_K_M                                                                      |          |   9.17 |     37 |   32.8 |    4 |   32 | 12.34 | 9.26 | 6.13 | 2.25 |
| mlx-community/Qwen3-Next-80B-A3B-Thinking-4bit                                                   |          |   9.13 |     15 |     80 |    4 |  256 | 9.72 | 11.69 | 6.94 | 3.43 |
| qwen2.5vl:32b-q4_K_M                                                                             |          |   8.95 |     36 |   33.5 |    4 |  128 | 13.02 | 7.74 | 6.01 | 2.18 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0                                 |          |   8.66 |     24 |   32.8 |    8 |   32 | 11.58 | 8.69 | 6.27 | 1.62 |
| qwen2.5:32b-instruct-q8_0                                                                        |          |   8.44 |     23 |   32.8 |    8 |   32 | 9.73 | 10.22 | 5.91 | 2.98 |
| GPT-4o-Mini                                                                                      |          |   8.00 |        |        |   16 |  128 | 11.39 | 7.36 | 5.19 | 1.93 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M                               |          |   7.95 |     32 |   32.8 |    4 |   32 | 9.55 |  9.3 | 5.71 | 1.94 |
| cogito:32b-v1-preview-qwen-q4_K_M                                                                |          |   7.83 |     32 |   32.8 |    4 |  128 | 11.32 | 7.12 | 5.26 | 1.19 |
| qwen3:32b-q4_K_M-no_think                                                                        |          |   7.67 |     31 |   32.8 |    4 |   40 | 10.25 | 8.94 | 3.93 | 1.07 |
| GPT-3.5-Turbo                                                                                    |          |   7.47 |      2 |  175.0 |   16 |   16 | 10.1 | 7.28 |  6.0 |  0.5 |
| yi-coder:9b-chat-q8_0                                                                            |     9.68 |   7.37 |     76 |    8.8 |    8 |  128 | 11.08 | 6.77 | 4.32 | 0.47 |
| deepseek-coder:33b-instruct-q4_K_M                                                               |          |   7.34 |     30 |   33.0 |    4 |   16 | 9.55 | 10.72 |  0.0 | 3.03 |
| qwen2.5vl:72b-q4_K_M                                                                             |          |   7.31 |     13 |   73.4 |    4 |  128 | 7.57 |  9.3 | 6.09 |  2.7 |
| llama3.3:70b-instruct-q8_0                                                                       |          |   7.17 |      9 |   70.6 |    8 |  128 | 8.93 | 8.06 | 4.29 | 3.17 |
| qwen2.5-coder:14b-instruct-q8_0                                                                  |          |   7.09 |     44 |   14.8 |    8 |  128 |  9.7 | 7.35 | 4.55 | 0.95 |
| hf.co/bartowski/Qwen_Qwen3-30B-A3B-GGUF:Q4_K_M-think                                             |          |   7.08 |     31 |   30.5 |    4 |   40 | 8.49 | 8.09 |  4.5 | 3.61 |
| qwen3:14b-q4_K_M-no_think                                                                        |          |   6.97 |     63 |   14.8 |    4 |   40 | 10.94 | 6.37 | 2.99 | 0.86 |
| hf.co/bartowski/AGI-0_Art-0-8B-GGUF:Q4_K_M                                                       |     6.14 |   6.96 |    113 |   8.19 |    4 |   40 | 9.22 | 6.61 | 4.45 | 3.95 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q8_0                                                   |          |   6.81 |     42 |   14.7 |    8 |   16 | 10.06 | 6.67 | 3.68 | 0.52 |
| qwen3:30b-a3b-q4_K_M-no_think                                                                    |          |   6.81 |     30 |   30.5 |    4 |   40 | 8.22 | 8.01 | 5.11 | 0.97 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q4_K_M                                                 |          |   6.72 |     61 |   14.7 |    4 |   16 | 9.26 |  6.8 | 4.42 | 0.89 |
| qwen2.5-coder:14b-instruct-q4_K_M                                                                |          |   6.68 |     60 |   14.8 |    4 |  128 | 8.65 | 7.28 | 4.62 | 1.13 |
| phi4:14b-q4_K_M                                                                                  |          |   6.64 |     60 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| phi4:latest                                                                                      |          |   6.64 |     60 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| deepseek-coder:33b-instruct-q8_0                                                                 |          |   6.58 |     18 |   33.0 |    8 |   16 | 8.35 | 10.2 |  0.0 | 1.82 |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M                               |          |   6.49 |     12 |   70.6 |    4 |  128 |  9.1 |  5.9 | 4.69 | 1.37 |
| hf.co/mradermacher/Seed-Coder-8B-Instruct-GGUF:Q4_K_M                                            |          |   6.39 |    103 |   8.25 |    4 |   32 | 9.16 | 6.07 | 3.52 | 2.02 |
| phi4-reasoning:14b-q4_K_M                                                                        |          |   6.36 |     58 |   14.7 |    4 |   32 | 6.73 | 7.73 |  5.2 | 3.05 |
| mistral-large:123b-instruct-2407-q4_K_M                                                          |          |   6.34 |      7 |  122.6 |    4 |  128 | 8.27 | 6.61 | 4.44 | 1.61 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-30B-A3B-GGUF:Q4_K_M                                        |          |   6.22 |     27 |   30.5 |    4 |   40 | 10.14 | 4.75 | 3.54 | 0.33 |
| hf.co/mradermacher/KAT-Dev-GGUF:Q4_K_M                                                           |          |   6.22 |     25 |   32.8 |    4 |      | 9.67 |  6.7 |  1.1 |      |
| qwen3:14b-q4_K_M-think                                                                           |          |   6.20 |     56 |   14.8 |    4 |   40 | 7.16 |  7.5 | 4.66 | 1.51 |
| vanilj/Phi-4:Q8_0                                                                                |          |   6.13 |     38 |   14.7 |    8 |   16 | 9.06 | 5.73 | 3.52 | 0.84 |
| hf.co/gaianet/Seed-Coder-8B-Instruct-GGUF:Q4_K_M                                                 |     6.00 |   6.10 |    102 |      8 |    4 |   32 |  9.0 | 4.99 | 4.09 | 1.81 |
| cogito:70b-v1-preview-llama-q4_K_M                                                               |          |   6.05 |     11 |   70.6 |    4 |  128 |  7.7 | 7.26 | 3.54 | 0.86 |
| qwen3:30b-a3b-q4_K_M-think                                                                       |          |   5.98 |     26 |   30.5 |    4 |   40 |  8.3 | 5.59 | 4.32 | 1.17 |
| yi-coder:9b-chat-q4_K_M                                                                          |          |   5.97 |     91 |    8.8 |    4 |  128 | 7.44 | 6.04 | 5.76 | 0.34 |
| qwq:32b-preview-q8_0                                                                             |          |   5.97 |     17 |   32.8 |    8 |   32 | 10.15 | 3.11 | 3.88 | 1.97 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                                                        |          |   5.83 |     11 |   70.6 |    4 |  128 | 8.07 | 6.49 | 2.59 | 1.36 |
| llama3.1:70b-instruct-q8_0                                                                       |          |   5.81 |      7 |   70.6 |    8 |  128 | 8.19 | 5.36 |  3.8 |  1.7 |
| hf.co/bartowski/deepcogito_cogito-v2-preview-llama-70B-GGUF:Q4_K_M                               |          |   5.78 |     11 |   70.6 |    4 |  128 | 7.49 | 5.65 |  4.5 | 1.92 |
| llama4:16x17b                                                                                    |          |   5.76 |      7 |  108.6 |    4 | 10000 | 9.13 | 4.78 | 2.89 | 0.93 |
| qwen2.5:14b-instruct-q8_0                                                                        |          |   5.75 |     35 |   14.8 |    8 |   32 | 8.59 | 4.14 | 4.55 | 1.61 |
| cogito:14b-v1-preview-qwen-q4_K_M                                                                |          |   5.70 |     51 |   14.8 |    4 |  128 |  7.9 | 5.89 | 3.41 | 0.91 |
| qwen2.5:14b-instruct-q4_K_M                                                                      |          |   5.63 |     51 |   14.8 |    4 |   32 | 8.44 | 5.08 | 3.44 | 0.43 |
| llama3.1:70b-instruct-q4_K_M                                                                     |          |   5.62 |     11 |   70.6 |    4 |  128 | 8.77 | 4.98 | 2.77 |  0.6 |
| llama3.3:70b-instruct-q4_K_M                                                                     |          |   5.60 |     11 |   70.6 |    4 |  128 | 7.26 | 5.25 | 4.49 | 2.21 |
| falcon3:10b-instruct-q8_0                                                                        |          |   5.48 |     48 |   10.3 |    8 |   32 | 8.15 | 5.14 | 2.71 | 1.39 |
| hf.co/bartowski/smirki_UIGEN-T1.1-Qwen-14B-GGUF:Q4_K_M                                           |          |   5.46 |     49 |   14.8 |    4 |   32 | 7.27 |  5.2 | 4.41 | 1.14 |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S                                            |          |   5.43 |      9 |   78.0 |    4 |   32 | 7.04 | 6.05 |  3.6 | 0.74 |
| hf.co/Tesslate/Tessa-Rust-T1-7B-Q8_0-GGUF:Q8_0                                                   |          |   5.37 |     64 |   7.62 |    8 |   32 | 7.04 |  5.0 | 4.84 | 0.86 |
| qwen3:32b-q4_K_M-think                                                                           |          |   5.31 |     22 |   32.8 |    4 |   40 | 5.78 | 6.75 | 4.78 | 0.19 |
| qwen3:8b-q4_K_M-think                                                                            |          |   5.30 |     86 |    8.2 |    4 |  128 | 5.69 | 6.48 | 4.77 | 1.27 |
| tulu3:70b-q8_0                                                                                   |          |   5.25 |      7 |   70.6 |    8 |  128 | 7.73 | 4.61 | 3.09 | 1.59 |
| qwen2-math:72b-instruct-q8_0                                                                     |          |   5.25 |      7 |   72.7 |    8 |    4 | 6.49 | 6.67 | 2.61 |  1.3 |
| tulu3:70b-q4_K_M                                                                                 |          |   5.21 |     10 |   70.6 |    4 |  128 | 7.31 | 4.68 | 3.35 | 2.15 |
| hf.co/unsloth/Magistral-Small-2509-GGUF:Q4_K_M                                                   |          |   5.18 |     29 |   23.6 |    4 |   40 | 7.14 | 5.08 | 3.36 | 1.32 |
| qwen3:4b-q4_K_M-think                                                                            |     3.00 |   5.18 |    173 |    4.0 |    4 |   32 | 7.89 | 4.61 | 2.73 | 0.91 |
| aravhawk/llama4:scout-q4_K_M                                                                     |          |   5.17 |      6 |  107.8 |    4 | 10240 | 6.78 | 5.64 | 3.55 | 0.59 |
| granite4:small-h                                                                                 |          |   5.15 |     21 |   32.2 |    4 |  131 | 7.67 | 4.59 | 2.97 | 1.13 |
| hf.co/ozone-ai/0x-lite-Q4_K_M-GGUF:latest                                                        |          |   5.14 |     46 |   14.8 |    4 |   32 | 7.66 | 4.52 | 3.32 | 0.56 |
| command-a:111b-03-2025-q4_K_M                                                                    |          |   5.06 |      6 |  111.1 |    4 |  256 | 6.33 | 5.17 | 4.21 | 1.32 |
| goekdenizguelmez/JOSIEFIED-Qwen3:8b-q4_k_m-think                                                 |          |   5.04 |     82 |    8.2 |    4 |   40 | 5.77 | 6.22 | 3.49 | 1.65 |
| devstral:24b-small-2505-q4_K_M                                                                   |          |   5.02 |     28 |   24.0 |    4 |  128 | 6.77 | 5.47 | 2.96 | 0.82 |
| qwen3:4b-instruct-2507-q4_K_M                                                                    |     3.00 |   5.01 |    167 |    4.0 |    4 |  256 | 8.07 |  4.5 | 2.01 | 0.26 |
| hf.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF:Q4_K_M                        |          |   4.96 |     28 |   23.6 |    4 |  128 | 6.79 | 5.19 | 3.05 | 0.79 |
| hf.co/bartowski/NousResearch_Hermes-4-14B-GGUF:Q4_K_M                                            |          |   4.94 |     45 |   14.8 |    4 |   40 | 6.81 | 4.01 | 4.69 | 0.78 |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                                              |          |   4.94 |     44 |   14.8 |    4 |  986 | 7.75 | 4.02 | 2.74 | 0.81 |
| falcon3:10b-instruct-q4_K_M                                                                      |          |   4.88 |     63 |   10.3 |    4 |   32 | 6.62 | 5.77 | 2.19 |  0.6 |
| hf.co/mradermacher/K2-Think-GGUF:Q4_K_M                                                          |          |   4.85 |     20 |   32.8 |    4 |  128 | 4.83 | 4.98 | 6.42 | 1.36 |
| hf.co/bartowski/Goekdeniz-Guelmez_Josiefied-Qwen3-8B-abliterated-v1-GGUF:Q4_K_M-no_think         |          |   4.83 |     79 |    8.2 |    4 |  128 | 7.25 | 4.93 | 2.05 | 0.44 |
| nemotron:70b-instruct-q4_K_M                                                                     |          |   4.78 |      9 |   70.6 |    4 |  128 | 5.78 | 5.13 | 4.22 | 0.83 |
| hf.co/bartowski/mistralai_Mistral-Small-3.1-24B-Instruct-2503-GGUF:Q4_K_M                        |          |   4.70 |     27 |   23.6 |    4 |  128 | 6.79 | 4.05 | 3.38 | 0.95 |
| qwen2.5-coder:7b-instruct-q8_0                                                                   |          |   4.69 |     56 |    7.6 |    8 |  128 | 6.37 |  4.4 | 3.78 | 0.63 |
| qwen3:8b-q4_K_M-no_think                                                                         |          |   4.68 |     76 |    8.2 |    4 |  128 | 6.98 | 4.84 | 1.92 | 0.51 |
| hf.co/bartowski/Qwen2.5-Math-72B-Instruct-GGUF:Q4_K_M                                            |          |   4.59 |      8 |   72.7 |    4 |    4 | 6.67 | 4.53 | 2.39 | 0.89 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-14B-GGUF:Q4_K_M                                            |          |   4.57 |     41 |   14.8 |    4 |   40 | 7.22 | 4.19 | 1.59 | 1.08 |
| llama3.2-vision:90b-instruct-q4_K_M                                                              |          |   4.50 |      7 |   87.7 |    4 |  128 | 5.61 | 4.79 | 3.78 | 0.65 |
| nemotron:70b-instruct-q8_0                                                                       |          |   4.50 |      6 |   70.6 |    8 |  128 | 6.31 | 4.05 | 3.23 | 1.13 |
| mistral-small3.2:24b-instruct-2506-q4_K_M                                                        |          |   4.49 |     25 |   24.0 |    4 |  128 | 5.73 | 4.74 | 3.38 | 1.02 |
| hf.co/mistralai/Devstral-Small-2507_gguf:Q4_K_M                                                  |          |   4.46 |     25 |   23.6 |    4 |  128 | 6.24 | 4.41 | 2.69 | 1.03 |
| qwen2.5:7b-instruct-q8_0                                                                         |          |   4.34 |     52 |    7.6 |    8 |  128 | 7.47 |  3.6 | 1.13 | 0.51 |
| falcon3:7b-instruct-q8_0                                                                         |          |   4.34 |     53 |    7.5 |    8 |   32 | 6.76 | 3.91 | 2.16 | 0.36 |
| hf.co/Tesslate/UIGEN-T2-7B-Q8_0-GGUF:Q8_0                                                        |          |   4.34 |     52 |   7.62 |    8 |   32 | 5.73 | 3.99 | 3.99 | 0.52 |
| hf.co/mradermacher/Viper-Coder-Hybrid-v1.3-GGUF:Q4_K_M                                           |          |   4.32 |     39 |   14.8 |    4 |  128 | 6.44 | 4.45 | 1.83 | 0.46 |
| hf.co/smirki/UIGEN-T1.1-Qwen-7B-Q4_K_M-GGUF:latest                                               |          |   4.29 |     75 |   7.62 |    4 |   32 | 6.06 | 4.53 | 2.08 | 0.88 |
| qwen2.5:7b-instruct-q4_K_M                                                                       |          |   4.22 |     74 |    7.6 |    4 |  128 |  7.5 | 2.67 | 1.86 | 0.49 |
| mistral-small3.1:24b-instruct-2503-q4_K_M                                                        |          |   4.15 |     23 |   24.0 |    4 |  128 | 5.31 | 4.38 | 3.07 |  1.0 |
| hf.co/Tesslate/Synthia-S1-27b-Q4_K_M-GGUF:Q4_K_M                                                 |          |   4.07 |     20 |   27.0 |    4 |  128 | 6.78 | 2.21 | 3.19 | 0.53 |
| hf.co/bartowski/WhiteRabbitNeo_WhiteRabbitNeo-V3-7B-GGUF:Q4_K_M                                  |          |   4.06 |     71 |   7.62 |    4 |   32 | 6.43 | 3.36 | 2.01 |  0.8 |
| hf.co/mradermacher/Sky-T1-mini-GGUF:Q4_K_M                                                       |          |   4.01 |     70 |   7.62 |    4 |  128 | 7.05 | 3.68 | 0.15 | 0.55 |
| mistral-small:24b-instruct-2501-q4_K_M                                                           |          |   3.98 |     22 |   23.6 |    4 |   32 | 6.32 | 2.89 | 2.47 | 0.93 |
| qwen2.5-coder:7b-instruct-q4_K_M                                                                 |          |   3.98 |     70 |    7.6 |    4 |   32 | 4.76 |  4.7 | 2.87 | 0.87 |
| hf.co/bartowski/Tesslate_Tessa-Rust-T1-7B-GGUF:Q4_K_M                                            |          |   3.94 |     69 |   7.62 |    4 |   32 | 6.14 |  3.2 | 2.28 | 0.73 |
| llama4:17b-scout-16e-instruct-q4_K_M                                                             |          |   3.93 |      5 |    109 |    4 | 10240 | 6.07 | 3.16 | 1.99 | 1.58 |
| hf.co/bartowski/open-thoughts_OpenThinker-32B-GGUF:Q4_K_M                                        |          |   3.90 |     16 |   32.8 |    4 |   32 |  4.2 | 4.22 | 3.28 | 2.95 |
| goekdenizguelmez/JOSIEFIED-Qwen3:8b-q4_k_m-no_think                                              |          |   3.83 |     62 |    8.2 |    4 |   40 | 6.13 |  3.3 | 1.55 | 0.83 |
| hf.co/mradermacher/Hermes-4-70B-GGUF:Q4_K_M                                                      |          |   3.76 |      7 |   70.6 |    4 |  128 | 4.95 | 4.07 | 2.21 | 1.15 |
| phi4-reasoning:14b-plus-q4_K_M                                                                   |          |   3.74 |     34 |   14.7 |    4 |   32 | 5.67 | 2.48 |  2.3 | 2.71 |
| gemma3:27b                                                                                       |          |   3.73 |     18 |   27.4 |    4 |  128 | 7.15 | 0.14 |  3.8 | 0.64 |
| hf.co/bartowski/HelpingAI_Helpingai3-raw-GGUF:Q4_K_M                                             |          |   3.70 |     48 |   10.3 |    4 |   32 | 5.88 | 3.82 | 0.92 | 0.13 |
| hf.co/bartowski/baidu_ERNIE-4.5-21B-A3B-PT-GGUF:Q4_K_M                                           |          |   3.67 |     22 |   21.8 |    4 |  128 | 5.51 | 3.42 | 2.08 | 0.28 |
| qwen3:4b-q4_K_M-no_think                                                                         |     3.00 |   3.67 |    122 |    4.0 |    4 |   32 | 5.44 | 3.72 | 1.71 | 0.38 |
| gemma2:27b-instruct-q8_0                                                                         |          |   3.65 |     12 |   27.2 |    8 |    8 | 5.18 |  3.3 | 2.47 | 0.98 |
| hf.co/bartowski/microsoft_Phi-4-reasoning-plus-GGUF:Q4_K_M                                       |          |   3.63 |     33 |   14.7 |    4 |   32 | 4.36 | 4.76 | 1.93 | 0.72 |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                                                           |          |   3.58 |      7 |   70.6 |    4 |    8 | 6.98 | 1.99 | 0.76 | 0.36 |
| hf.co/bartowski/andrewzh_Absolute_Zero_Reasoner-Coder-7b-GGUF:Q4_K_M                             |          |   3.58 |     63 |   7.62 |    4 |   32 | 5.53 | 2.99 | 2.08 | 0.52 |
| hf.co/mradermacher/Viper-Coder-HybridMini-v1.3-GGUF:Q4_K_M                                       |          |   3.55 |     62 |   7.62 |    4 |   32 | 5.18 | 3.51 | 1.99 | 0.24 |
| hf.co/lmstudio-community/INTELLECT-2-GGUF:Q4_K_M                                                 |          |   3.52 |     14 |   32.8 |    4 |      | 4.21 | 5.02 |      |      |
| deepseek-coder:6.7b-instruct-q8_0                                                                |          |   3.52 |     46 |    7.0 |    8 |   16 | 5.37 | 3.68 | 0.94 | 0.79 |
| granite4:tiny-h                                                                                  |          |   3.48 |     67 |    6.9 |    4 | 1024 | 5.33 | 3.74 | 1.03 |  0.2 |
| hf.co/bartowski/cognitivecomputations_Dolphin-Mistral-24B-Venice-Edition-GGUF:Q4_K_M             |          |   3.43 |     19 |   24.0 |    4 |   32 | 4.78 |  3.2 | 2.18 | 1.21 |
| hf.co/mradermacher/HelpingAI-3-GGUF:Q4_K_M                                                       |          |   3.38 |     44 |   10.3 |    4 |   32 |  5.8 | 2.82 | 1.09 |  0.0 |
| hf.co/katanemo/Arch-Function-7B.gguf:Q4_K_M                                                      |          |   3.34 |     59 |   7.62 |    4 |   32 | 4.63 | 3.99 | 1.17 | 0.61 |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                                                         |          |   3.34 |     34 |   8.83 |    8 |    4 | 6.54 | 2.11 |  0.4 | 0.09 |
| hf.co/lmstudio-community/Mistral-Small-24B-Instruct-2501-GGUF:Q4_K_M                             |          |   3.33 |     19 |   23.6 |    4 |   32 | 5.21 | 2.86 | 1.54 | 0.79 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                                                 |          |   3.30 |     50 |    8.8 |    4 |   32 | 4.92 | 3.64 | 1.18 | 0.06 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-8B-GGUF:Q4_K_M                                             |          |   3.22 |     52 |   8.19 |    4 |   32 | 5.69 | 2.38 |  1.0 | 0.25 |
| opencoder:8b-instruct-q8_0                                                                       |          |   3.21 |     37 |    7.8 |    8 |    8 | 4.63 | 3.22 | 1.62 | 0.72 |
| hf.co/mradermacher/Fathom-R1-14B-GGUF:Q4_K_M                                                     |          |   3.21 |     29 |   14.8 |    4 |  128 | 4.65 | 3.32 | 1.57 | 0.38 |
| hf.co/mradermacher/Bespoke-Stratos-7B-GGUF:Q4_K_M                                                |          |   3.16 |     55 |   7.62 |    4 |   32 | 4.72 | 2.67 | 2.26 | 0.23 |
| hf.co/bartowski/simplescaling_s1-32B-GGUF:Q4_K_M                                                 |          |   3.11 |     13 |   32.8 |    4 |   32 | 4.33 | 2.29 | 2.78 |  1.4 |
| gemma3:12b                                                                                       |          |   3.11 |     34 |   12.2 |    4 |  128 | 5.31 |  0.9 |  3.3 |  0.6 |
| hf.co/bartowski/THUDM_GLM-4-9B-0414-GGUF:Q4_K_M                                                  |          |   3.11 |     44 |    9.4 |    4 |   32 | 4.87 |  3.0 | 1.18 | 0.23 |
| qwen2.5-coder:3b-instruct-q4_K_M                                                                 |     2.33 |   3.05 |    131 |    3.1 |    4 |   32 | 4.98 | 2.51 | 1.53 | 0.03 |
| exaone3.5:32b-instruct-q8_0                                                                      |          |   3.05 |      9 |   32.0 |    8 |   32 | 3.96 | 3.82 | 1.38 | 0.47 |
| deepseek-r1:32b-qwen-distill-q4_K_M                                                              |          |   3.00 |     12 |   32.8 |    4 |  128 | 4.51 | 2.91 | 1.44 | 0.32 |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                                               |          |   2.97 |     52 |   7.62 |    4 |  128 | 6.55 |  0.0 | 1.63 | 0.24 |
| hf.co/bartowski/google_gemma-3-27b-it-qat-GGUF:Q4_0                                              |          |   2.93 |     14 |   27.0 |    4 |  128 | 5.12 | 0.25 | 3.96 | 0.16 |
| hf.co/mradermacher/medgemma-27b-text-it-GGUF:Q4_K_M                                              |          |   2.84 |     14 |   27.0 |    4 |      | 5.41 |  0.0 | 3.22 | 0.31 |
| goekdenizguelmez/JOSIEFIED-Qwen3:4b-q4_0-no_think                                                |          |   2.78 |     93 |    4.0 |    4 |   32 | 4.59 | 2.33 | 1.19 | 0.03 |
| hf.co/bartowski/all-hands_openhands-lm-32b-v0.1-GGUF:Q4_K_M                                      |          |   2.72 |     11 |   32.8 |    4 |  128 | 3.28 | 4.55 | 0.14 |  0.2 |
| hf.co/mradermacher/MiniCPM4-8B-GGUF:Q4_K_M                                                       |          |   2.65 |     43 |   8.19 |    4 |   32 | 4.14 | 2.38 | 1.36 | 0.05 |
| yi:34b-chat-v1.5-q4_K_M                                                                          |          |   2.63 |     10 |   34.0 |    4 |    4 | 4.25 | 2.63 | 0.58 | 0.24 |
| qwen2.5-coder:3b-instruct-q8_0                                                                   |          |   2.62 |     77 |    3.1 |    8 |   32 |  4.2 | 2.15 |  1.4 |  0.2 |
| hf.co/bartowski/Skywork_Skywork-OR1-7B-GGUF:Q4_K_M                                               |          |   2.56 |     49 |      7 |    4 |  128 | 3.72 |  2.6 |      |      |
| hf.co/bartowski/google_gemma-3-12b-it-qat-GGUF:Q4_0                                              |          |   2.55 |     29 |   11.8 |    4 |  128 | 4.64 | 0.68 | 2.42 | 0.08 |
| yi:9b-chat-v1.5-q4_K_M                                                                           |          |   2.54 |     38 |    9.0 |    4 |    4 | 4.04 | 2.71 | 0.39 | 0.33 |
| hf.co/bartowski/soob3123_GrayLine-Qwen3-8B-GGUF:Q4_K_M-no_think                                  |          |   2.48 |     40 |   8.19 |    4 |      | 3.82 | 2.19 | 1.03 | 0.91 |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                                                        |          |   2.45 |      6 |   34.4 |    8 |    4 | 4.61 | 1.49 | 0.72 | 0.16 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-4B-GGUF:Q4_K_M                                             |          |   2.33 |     70 |   4.41 |    4 |   32 | 2.75 | 3.43 | 0.83 | 0.34 |
| exaone3.5:7.8b-instruct-q8_0                                                                     |          |   2.28 |     27 |    7.8 |    8 |   32 | 3.76 | 2.26 | 0.17 | 0.68 |
| qwen3:235b-a22b-q4_K_M-think                                                                     |          |   2.28 |      1 |  235.1 |    4 |  128 | 2.86 | 2.27 | 2.17 | 0.25 |
| qwen:110b-chat-v1.5-q4_K_M                                                                       |          |   2.25 |      3 |  111.0 |    4 |   32 | 3.63 | 1.84 | 0.76 | 0.92 |
| phi3:14b-medium-128k-instruct-q8_0                                                               |          |   2.24 |     15 |   14.0 |    8 |  128 | 4.21 | 1.55 | 0.42 | 0.04 |
| hf.co/bartowski/THUDM_GLM-Z1-32B-0414-GGUF:Q4_K_M                                                |          |   2.24 |      9 |   32.6 |    4 |   32 | 3.13 | 1.58 |  2.0 |  1.1 |
| mlx-community/Ring-mini-2.0-4bit                                                                 |          |   2.20 |     18 |   16.0 |    4 |   32 | 2.42 | 2.69 | 1.72 | 0.76 |
| granite4:micro                                                                                   |          |   2.17 |     85 |    3.4 |    4 |  128 | 3.53 | 1.77 | 1.09 | 0.04 |
| hf.co/jedisct1/MiMo-7B-RL-GGUF:Q4_K_M                                                            |          |   2.10 |     40 |      7 |    4 |   32 | 3.74 | 1.94 | 0.13 |  0.0 |
| qwen2.5vl:7b-q4_K_M                                                                              |          |   2.09 |     34 |    8.3 |    4 |  128 | 3.48 | 1.64 | 0.97 | 0.13 |
| llama3.1:8b-instruct-q8_0                                                                        |          |   2.03 |     23 |    8.0 |    8 |  128 | 3.26 | 1.78 | 0.94 | 0.09 |
| qwq:32b-q4_K_M                                                                                   |          |   2.02 |      8 |   32.8 |    4 |  128 | 2.51 | 1.75 | 1.32 | 2.25 |
| tulu3:8b-q8_0                                                                                    |          |   2.01 |     23 |    8.0 |    8 |  128 | 3.91 | 1.06 | 0.42 | 0.49 |
| granite4:micro-h                                                                                 |          |   2.01 |     84 |    3.2 |    4 | 1024 | 3.27 | 1.79 | 0.77 | 0.14 |
| qwen3:1.7b-q4_K_M-think                                                                          |     1.50 |   1.97 |    131 |    2.0 |    4 |   32 | 3.97 | 0.94 | 0.48 | 0.04 |
| hf.co/bartowski/andrewzh_Absolute_Zero_Reasoner-Coder-3b-GGUF:Q4_K_M                             |          |   1.97 |     85 |   3.09 |    4 |   32 | 3.75 | 0.86 | 0.86 | 0.36 |
| hf.co/bartowski/open-r1_OlympicCoder-7B-GGUF:Q4_K_M                                              |          |   1.93 |     37 |    7.0 |    4 |   32 | 2.43 | 2.86 | 0.31 | 0.33 |
| hf.co/bartowski/Alibaba-NLP_Tongyi-DeepResearch-30B-A3B-GGUF:Q4_K_M                              |          |   1.91 |      8 |   30.5 |    4 |  128 | 2.47 | 2.55 | 0.74 | 0.04 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                                                         |          |   1.87 |     28 |   6.06 |    8 |    4 | 3.92 | 0.92 | 0.13 |  0.0 |
| hf.co/mradermacher/olmOCR-7B-0725-GGUF:Q4_K_M                                                    |          |   1.81 |     32 |   7.62 |    4 |  128 | 3.66 | 0.65 | 0.74 | 0.03 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                                                       |          |   1.81 |     40 |   6.06 |    4 |    4 | 3.71 | 0.87 | 0.32 |  0.0 |
| deepseek-llm:67b-chat-q4_K_M                                                                     |          |   1.79 |      4 |   67.0 |    4 |    4 | 2.94 | 1.63 |  0.5 | 0.23 |
| hf.co/katanemo/Arch-Function-3B.gguf:Q4_K_M                                                      |          |   1.76 |     76 |   3.09 |    4 |   32 | 2.81 | 1.55 | 0.66 | 0.43 |
| qwen2.5:3b-instruct-q4_K_M                                                                       |          |   1.70 |     73 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.56 | 0.05 |
| deepseek-r1:70b-llama-distill-q4_K_M                                                             |          |   1.69 |      3 |   70.6 |    4 |  128 | 2.17 | 2.49 | 0.19 | 0.41 |
| deepseek-r1:14b-qwen-distill-q4_K_M                                                              |          |   1.69 |     15 |   14.8 |    4 |  128 |  2.6 | 1.02 | 1.19 | 1.04 |
| qwen2.5:3b                                                                                       |          |   1.67 |     72 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.42 | 0.05 |
| llama3.2-vision:11b-instruct-q4_K_M                                                              |          |   1.67 |     23 |    9.8 |    4 |  128 | 3.13 | 1.21 | 0.21 | 0.11 |
| hf.co/mradermacher/Kimi-VL-A3B-Thinking-2506-GGUF:Q4_K_M                                         |          |   1.66 |     14 |   16.0 |    4 |  128 | 2.35 | 1.27 | 1.43 | 0.53 |
| yi-coder:1.5b-chat-q4_K_M                                                                        |     1.12 |   1.65 |    146 |    1.5 |    4 |  128 | 3.49 | 0.61 | 0.34 |  0.0 |
| gemma2:9b-instruct-q8_0                                                                          |          |   1.63 |     16 |    9.2 |    8 |    8 | 2.46 | 1.55 | 0.86 | 0.12 |
| granite3.1-dense:8b-instruct-q8_0                                                                |          |   1.59 |     18 |    8.2 |    8 |  128 | 2.73 | 1.55 | 0.16 | 0.03 |
| hf.co/katanemo/Arch-Function-1.5B.gguf:Q4_K_M                                                    |          |   1.56 |    135 |   1.54 |    4 |   32 | 2.44 |  1.6 | 0.53 | 0.02 |
| granite3.2:8b-instruct-q4_K_M                                                                    |          |   1.50 |     24 |    8.2 |    4 |  128 | 2.53 | 1.43 |  0.3 |  0.0 |
| codegemma:7b-instruct-v1.1-q4_K_M                                                                |          |   1.46 |     22 |    9.0 |    4 |    8 | 2.21 | 1.49 | 0.66 | 0.01 |
| hf.co/mradermacher/olmOCR-7B-0825-GGUF:Q4_K_M                                                    |          |   1.46 |     26 |   7.62 |    4 |  128 | 2.65 | 0.99 | 0.36 | 0.33 |
| exaone3.5:2.4b-instruct-q8_0                                                                     |          |   1.45 |     49 |    2.7 |    8 |   32 | 2.73 | 0.94 | 0.28 | 0.15 |
| deepseek-r1:7b-qwen-distill-q4_K_M                                                               |          |   1.43 |     25 |    7.6 |    4 |  128 | 2.64 |  1.1 |  0.0 | 0.46 |
| qwen2.5:3b-instruct-q8_0                                                                         |          |   1.43 |     42 |    3.1 |    8 |  128 | 2.87 | 0.59 | 0.44 | 0.18 |
| opencoder:1.5b-instruct-q8_0                                                                     |          |   1.42 |     68 |    1.9 |    8 |    4 |  2.2 | 1.47 |  0.5 |  0.0 |
| yi-coder:1.5b-chat-q8_0                                                                          |          |   1.36 |     83 |    1.5 |    8 |  128 | 2.32 | 1.17 | 0.42 |  0.0 |
| cogito:8b-v1-preview-llama-q4_K_M                                                                |          |   1.34 |     22 |      8 |    4 |  128 | 2.32 | 1.02 | 0.54 |  0.0 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                                               |     1.12 |   1.31 |    116 |    1.5 |    4 |   32 | 2.26 |  0.8 |  0.8 | 0.03 |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                                                |          |   1.30 |      4 |   46.7 |    4 |   32 |  2.0 | 1.24 | 0.62 |  0.0 |
| qwen2-math:7b-instruct-q8_0                                                                      |          |   1.28 |     15 |    7.6 |    8 |    4 | 2.49 | 0.95 | 0.02 |  0.0 |
| dolphin3:8b-llama3.1-q8_0                                                                        |          |   1.27 |     14 |    8.0 |    8 |  128 |  2.3 | 0.89 | 0.26 | 0.31 |
| goekdenizguelmez/JOSIEFIED-Qwen3:1.7b-q4_0-think                                                 |          |   1.25 |     84 |    2.0 |    4 |   32 |  2.1 | 1.26 | 0.18 |  0.0 |
| hf.co/mradermacher/MiniCPM4.1-8B-GGUF:Q4_K_M                                                     |          |   1.25 |     20 |   8.19 |    4 |   64 | 1.56 | 1.46 | 0.79 | 0.33 |
| qwen2.5-coder:1.5b-instruct-q8_0                                                                 |          |   1.22 |     74 |    1.5 |    8 |   32 | 2.04 |  0.9 | 0.66 | 0.03 |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0                                  |          |   1.21 |     14 |   8.03 |    8 |  128 | 2.29 | 0.47 | 0.58 | 0.37 |
| codegemma:7b-instruct-q8_0                                                                       |          |   1.19 |     12 |    9.0 |    8 |    8 | 1.84 | 1.27 | 0.39 |  0.0 |
| gemma3:4b                                                                                        |          |   1.17 |     36 |    4.3 |    4 |  128 | 2.09 | 0.61 | 0.77 |  0.0 |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                                                 |          |   1.16 |     13 |    8.0 |    8 |    8 | 1.51 | 1.65 |  0.3 | 0.03 |
| hf.co/mradermacher/HelpingAI-15B-GGUF:Q4_K_M                                                     |          |   1.16 |     10 |   15.3 |    4 |    4 | 2.42 | 0.64 |  0.0 |  0.0 |
| falcon3:3b-instruct-q8_0                                                                         |          |   1.16 |     33 |    3.2 |    8 |   32 | 1.89 | 1.09 | 0.36 | 0.04 |
| hf.co/TheDrummer/Rivermind-12B-v1-GGUF:Q4_K_M                                                    |          |   1.14 |     12 |   12.2 |    4 |   32 | 1.72 | 1.08 | 0.61 | 0.08 |
| qwen2.5:1.5b-instruct-q8_0                                                                       |          |   1.14 |     69 |    1.5 |    8 |  128 | 2.07 | 0.82 | 0.29 | 0.06 |
| deepseek-r1:8b-llama-distill-q4_K_M                                                              |          |   1.12 |     19 |    8.0 |    4 |  128 | 1.46 | 1.25 | 0.45 | 0.67 |
| hf.co/bartowski/THUDM_GLM-Z1-9B-0414-GGUF:Q4_K_M                                                 |          |   1.08 |     15 |    9.4 |    4 |   32 | 0.99 | 1.74 | 0.57 | 0.51 |
| qwen2.5vl:3b-q4_K_M                                                                              |          |   1.07 |     38 |    3.8 |    4 |  128 | 1.88 | 0.61 | 0.69 | 0.01 |
| hf.co/bartowski/nvidia_Llama-3.1-Nemotron-Nano-4B-v1.1-GGUF:Q4_K_M                               |          |   1.07 |     32 |   4.51 |    4 |  128 | 2.59 |  0.1 | 0.03 |  0.0 |
| granite3.3:2b                                                                                    |          |   1.04 |     69 |    2.0 |    4 |  128 | 2.19 | 0.54 | 0.02 |  0.0 |
| openchat:7b-v3.5-q8_0                                                                            |          |   1.02 |     13 |    7.0 |    8 |    8 | 1.62 | 1.21 | 0.06 |  0.0 |
| hf.co/bartowski/Zyphra_ZR1-1.5B-GGUF:Q4_K_M                                                      |     1.12 |   1.02 |     90 |    1.5 |    4 |  128 | 1.64 | 0.34 | 1.04 | 0.51 |
| granite3.3:8b                                                                                    |          |   0.98 |     16 |    8.0 |    4 |  128 | 1.67 | 0.78 | 0.25 | 0.27 |
| gemma3n:e2b                                                                                      |          |   0.97 |     29 |    4.5 |    4 |    8 | 2.21 | 0.23 | 0.11 |  0.0 |
| codellama:34b-instruct-q4_K_M                                                                    |          |   0.93 |      4 |   34.0 |    4 |   16 | 1.29 | 0.99 | 0.56 | 0.04 |
| gemma3n:e4b                                                                                      |          |   0.92 |     18 |    6.9 |    4 |   32 | 2.04 |  0.0 |  0.5 |  0.0 |
| exaone-deep:7.8b-q4_K_M                                                                          |          |   0.90 |     15 |    7.8 |    4 |   32 | 1.83 |  0.4 | 0.24 |  0.0 |
| qwen:32b-chat-v1.5-q4_K_M                                                                        |          |   0.90 |      4 |   33.0 |    4 |   32 | 1.54 | 0.81 | 0.13 | 0.12 |
| yi:6b-chat-v1.5-q4_K_M                                                                           |          |   0.89 |     20 |    6.0 |    4 |    4 | 0.79 | 1.48 | 0.62 | 0.01 |
| qwen2.5:1.5b-instruct-q4_K_M                                                                     |     1.12 |   0.88 |     79 |    1.5 |    4 |  128 | 1.94 | 0.26 | 0.15 |  0.0 |
| hf.co/bartowski/open-r1_OlympicCoder-32B-GGUF:Q4_K_M                                             |          |   0.88 |      4 |   32.8 |    4 |   32 | 1.54 | 0.32 | 0.58 | 0.53 |
| hf.co/allenai/OLMo-2-0325-32B-Instruct-GGUF:Q4_0                                                 |          |   0.86 |      4 |   32.2 |    4 |    4 | 1.32 | 0.77 | 0.51 |  0.0 |
| deepcoder:1.5b-preview-q4_K_M                                                                    |     1.12 |   0.82 |     73 |    1.5 |    4 |  128 | 1.93 | 0.15 |  0.0 | 0.08 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-2B-GGUF:Q4_K_M                                             |          |   0.82 |     54 |   2.03 |    4 |   40 | 1.54 | 0.57 | 0.12 | 0.12 |
| mixtral:8x7b-instruct-v0.1-q8_0                                                                  |          |   0.82 |      2 |   46.7 |    8 |   32 | 1.44 | 0.65 | 0.23 |  0.0 |
| hf.co/bartowski/google_gemma-3-4b-it-qat-GGUF:Q4_0                                               |          |   0.81 |     28 |   3.88 |    4 |  128 | 1.74 | 0.35 | 0.03 | 0.03 |
| hf.co/mradermacher/HelpingAI-9B-GGUF:Q4_K_M                                                      |          |   0.78 |     12 |   8.83 |    4 |    4 | 1.64 | 0.41 |  0.0 |  0.0 |
| qwen3:1.7b-q4_K_M-no_think                                                                       |          |   0.77 |     51 |    2.0 |    4 |   32 | 1.08 | 0.99 | 0.18 |  0.0 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q4_K_M                                                             |          |   0.76 |     39 |   2.57 |    4 |   32 | 1.86 | 0.04 |  0.0 |  0.0 |
| hf.co/bartowski/OpenThinker-7B-GGUF:Q4_K_M                                                       |          |   0.75 |     13 |   7.62 |    4 |   32 | 0.88 | 0.77 | 0.53 | 0.62 |
| exaone-deep:32b-q4_K_M                                                                           |          |   0.70 |      3 |   32.0 |    4 |   32 | 0.93 | 0.66 | 0.36 | 0.53 |
| command-r7b:7b-12-2024-q4_K_M                                                                    |          |   0.68 |     11 |    8.0 |    4 |  128 | 1.54 | 0.03 | 0.26 | 0.04 |
| goekdenizguelmez/JOSIEFIED-Qwen3:4b-q4_0-think                                                   |          |   0.68 |     23 |    4.0 |    4 |   40 | 0.97 | 0.84 | 0.18 |  0.0 |
| llama3.2:3b                                                                                      |          |   0.66 |     28 |    3.2 |    4 |  128 | 1.42 | 0.18 | 0.21 |  0.0 |
| olmo2:13b-1124-instruct-q4_K_M                                                                   |          |   0.66 |      6 |   13.7 |    4 |    4 | 1.59 | 0.06 | 0.01 | 0.03 |
| internlm2:7b-chat-v2.5-q4_K_M                                                                    |          |   0.66 |     11 |    7.7 |    4 |   32 |  1.1 | 0.41 | 0.47 |  0.0 |
| goekdenizguelmez/JOSIEFIED-Qwen3:1.7b-q4_0-no_think                                              |          |   0.64 |     43 |    2.0 |    4 |   32 | 1.42 | 0.25 | 0.01 |  0.0 |
| hf.co/bartowski/agentica-org_DeepScaleR-1.5B-Preview-GGUF:Q4_K_M                                 |          |   0.64 |     48 |   1.78 |    4 |  128 | 1.28 |  0.4 | 0.03 | 0.05 |
| qwen:72b-chat-v1.5-q4_K_M                                                                        |          |   0.64 |      1 |   72.0 |    4 |   32 | 0.94 | 0.78 | 0.13 |  0.0 |
| olmo2:7b-1124-instruct-q4_K_M                                                                    |          |   0.60 |     11 |    7.3 |    4 |    4 | 1.42 | 0.08 | 0.02 |  0.0 |
| hf.co/mradermacher/GLM-4.5-Air-GGUF:Q2_K                                                         |          |   0.59 |      0 |  110.0 |    2 |  128 | 0.64 | 0.35 | 0.93 | 0.42 |
| qwen2.5:0.5b-instruct-q8_0                                                                       |     0.55 |   0.57 |    104 |    0.5 |    8 |  128 | 1.33 |  0.0 | 0.21 |  0.0 |
| deepcoder:14b-preview-q4_K_M                                                                     |          |   0.57 |      5 |   14.8 |    4 |  128 | 1.03 | 0.33 | 0.28 |  0.0 |
| hf.co/mradermacher/Seed-Coder-8B-Reasoning-GGUF:Q4_K_M                                           |          |   0.54 |      9 |   8.25 |    4 |      | 1.06 | 0.38 |  0.0 | 0.03 |
| internlm2:1.8b-chat-v2.5-q4_K_M                                                                  |          |   0.51 |     36 |    1.9 |    4 |   32 | 1.24 | 0.06 |  0.0 |  0.0 |
| hf.co/bartowski/nvidia_Llama-3_3-Nemotron-Super-49B-v1_5-GGUF:Q4_K_M                             |          |   0.51 |      1 |   49.9 |    4 |  128 | 0.79 |      |      |      |
| granite3.1-dense:2b-instruct-q8_0                                                                |          |   0.50 |     18 |    2.5 |    8 |  128 | 1.07 | 0.11 |  0.2 |  0.0 |
| llama3.2:latest                                                                                  |          |   0.49 |     20 |   3.21 |    4 |  128 | 0.99 | 0.18 | 0.21 |  0.0 |
| exaone-deep:2.4b-q4_K_M                                                                          |          |   0.48 |     24 |    2.7 |    4 |   32 | 0.88 | 0.32 | 0.04 | 0.28 |
| codellama:13b-instruct-q4_K_M                                                                    |          |   0.48 |      5 |   13.0 |    4 |   16 | 0.52 | 0.84 | 0.05 | 0.08 |
| hf.co/openbmb/MiniCPM-o-2_6-gguf:Q4_K_M                                                          |          |   0.48 |      8 |   7.61 |    4 |   32 | 1.03 | 0.19 | 0.04 |  0.0 |
| hf.co/trillionlabs/Trillion-7B-preview-GGUF:Q4_K_M                                               |          |   0.47 |      8 |   7.53 |    4 |    4 | 0.98 | 0.09 | 0.21 | 0.11 |
| smallthinker:3b-preview-q4_K_M                                                                   |          |   0.47 |     18 |    3.4 |    4 |  128 | 0.98 | 0.25 |  0.0 |  0.0 |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                                                             |          |   0.46 |     34 |    1.8 |    4 |  128 | 0.87 | 0.24 | 0.03 | 0.37 |
| cogito:3b-v1-preview-llama-q4_K_M                                                                |          |   0.46 |     19 |   3.21 |    4 |  128 | 0.94 | 0.25 | 0.04 | 0.03 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q8_0                                                               |          |   0.46 |     16 |   2.57 |    8 |   32 | 0.94 | 0.24 | 0.04 |  0.0 |
| hf.co/TheBloke/Yi-34B-Chat-GGUF:Q4_K_M                                                           |          |   0.44 |      2 |   34.4 |    4 |    4 | 0.67 | 0.56 | 0.03 |  0.0 |
| granite3.2:2b-instruct-q4_K_M                                                                    |          |   0.42 |     23 |    2.5 |    4 |  128 | 0.85 | 0.16 | 0.15 | 0.05 |
| mistral:7b-instruct-q4_K_M                                                                       |          |   0.41 |      8 |    7.0 |    4 |   32 | 0.48 | 0.71 | 0.04 |  0.0 |
| smallthinker:3b-preview-q8_0                                                                     |          |   0.41 |     11 |    3.4 |    8 |  128 | 0.81 | 0.19 | 0.03 | 0.19 |
| phi:2.7b-chat-v2-q4_K_M                                                                          |          |   0.39 |     17 |    3.0 |    4 |    2 | 0.91 | 0.07 |  0.0 |  0.0 |
| vicuna:33b-q4_K_M                                                                                |          |   0.38 |      2 |   30.0 |    4 |    2 |  0.9 | 0.06 |  0.0 |  0.0 |
| granite3.1-moe:3b-instruct-q8_0                                                                  |          |   0.35 |     10 |    3.3 |    8 |  128 |  0.8 | 0.03 | 0.11 | 0.03 |
| qwen3:0.6b-q4_K_M-think                                                                          |          |   0.28 |     50 | 0.75163 |    4 |   32 | 0.53 |  0.0 | 0.36 |  0.0 |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                                                        |          |   0.27 |      3 |   7.62 |    8 |  128 | 0.27 | 0.54 |  0.0 |  0.0 |
| qwen2-math:1.5b-instruct-q8_0                                                                    |          |   0.27 |     16 |    1.5 |    8 |    4 | 0.65 | 0.03 |  0.0 |  0.0 |
| gemma2:2b-instruct-q8_0                                                                          |          |   0.23 |      8 |    2.6 |    8 |    8 | 0.39 | 0.22 | 0.03 |  0.0 |
| qwen3:0.6b-q4_K_M-no_think                                                                       |          |   0.22 |     39 |   0.75 |    4 |   32 | 0.48 |  0.1 |  0.0 |  0.0 |
| hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M                                              |          |   0.22 |      4 |   6.92 |    4 |    2 | 0.51 | 0.04 | 0.01 |  0.0 |
| openbmb/minicpm-v4:4b                                                                            |          |   0.21 |      8 |    3.6 |    4 |   32 | 0.52 |  0.0 | 0.01 |  0.0 |
| goekdenizguelmez/JOSIEFIED-Qwen3:0.6b-q4_0-think                                                 |          |   0.21 |     37 | 0.75163 |    4 |   40 | 0.49 | 0.04 |  0.0 |  0.0 |
| codellama:7b-instruct-q4_K_M                                                                     |          |   0.21 |      4 |    7.0 |    4 |   16 | 0.33 | 0.03 | 0.33 | 0.01 |
| deepseek-llm:7b-chat-q8_0                                                                        |          |   0.20 |      3 |    7.0 |    8 |    4 | 0.46 | 0.06 |  0.0 |  0.0 |
| hf.co/QuantFactory/HelpingAI-3B-coder-GGUF:Q4_K_M                                                |          |   0.20 |      8 |   3.48 |    4 |  128 | 0.31 | 0.22 |  0.0 |  0.1 |
| goekdenizguelmez/JOSIEFIED-Qwen3:0.6b-q4_0-no_think                                              |          |   0.20 |     35 | 0.75163 |    4 |   40 | 0.49 |  0.0 | 0.01 |  0.0 |
| llama3.2:1b-instruct-q4_K_M                                                                      |          |   0.18 |     14 |    1.2 |    8 |  128 | 0.41 | 0.06 |  0.0 |  0.0 |
| hf.co/mradermacher/Qwen3-0.6B-Code-Expert-GGUF:Q4_K_M-no_think                                   |     0.45 |   0.18 |     39 |  0.596 |    4 |   40 | 0.44 |  0.0 |  0.0 |  0.0 |
| phi3:3.8b                                                                                        |          |   0.17 |      6 |    3.8 |    4 |  128 | 0.39 | 0.04 | 0.03 |  0.0 |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                                                |          |   0.16 |      0 |   72.7 |    4 |   32 | 0.31 |  0.0 | 0.08 | 0.16 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-1B-GGUF:Q4_K_M                                             |          |   0.15 |     27 |  0.752 |    4 |   40 | 0.36 | 0.03 | 0.01 |  0.0 |
| gemma3:1b                                                                                        |          |   0.15 |     20 |    1.0 |    4 |   32 | 0.13 | 0.33 |  0.0 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                                               |     0.38 |   0.15 |     40 |    0.5 |    4 |   32 | 0.36 | 0.01 | 0.01 |  0.0 |
| qwen2.5:0.5b-instruct-q4_K_M                                                                     |     0.38 |   0.15 |     39 |    0.5 |    4 |  128 | 0.36 |  0.0 | 0.01 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q8_0                                                                 |          |   0.14 |     26 |    0.5 |    8 |   32 | 0.33 | 0.01 | 0.03 |  0.0 |
| llama2:70b-chat-q4_K_M                                                                           |          |   0.14 |      0 |   69.0 |    4 |    4 | 0.31 | 0.03 | 0.01 | 0.03 |
| llama3.2:1b-instruct-q8_0                                                                        |          |   0.13 |     10 |    1.2 |    8 |  128 | 0.28 | 0.06 |  0.0 |  0.0 |
| hf.co/mradermacher/MediPhi-Instruct-GGUF:Q4_K_M                                                  |          |   0.13 |      4 |   3.82 |    4 |  128 | 0.31 | 0.01 |  0.0 |  0.0 |
| hf.co/bartowski/google_gemma-3-1b-it-qat-GGUF:Q4_0                                               |          |   0.12 |     17 |    1.0 |    4 |   32 | 0.29 | 0.03 |  0.0 |  0.0 |
| falcon:7b-instruct-q4_0                                                                          |          |   0.11 |      2 |    7.0 |    4 |    2 | 0.28 |  0.0 |  0.0 |  0.0 |
| falcon:40b-instruct-q4_0                                                                         |          |   0.11 |      0 |   40.0 |    4 |    2 | 0.07 |  0.0 | 0.42 |  0.0 |
| hf.co/LiquidAI/LFM2-1.2B-GGUF:Q4_K_M                                                             |          |   0.11 |     12 |   1.17 |    4 |   32 | 0.25 | 0.03 |  0.0 |  0.0 |
| phi4-mini:3.8b-q4_K_M                                                                            |          |   0.11 |      4 |    3.8 |    4 |  128 | 0.23 | 0.04 | 0.01 |  0.0 |
| falcon3:1b-instruct-q8_0                                                                         |          |   0.10 |      5 |    1.7 |    8 |    8 | 0.25 |  0.0 |  0.0 |  0.0 |
| hf.co/mradermacher/MiniCPM4-0.5B-GGUF:Q4_K_M                                                     |     0.33 |   0.10 |     30 |  0.434 |    4 |      | 0.23 | 0.02 |  0.0 |  0.0 |
| granite3.1-moe:1b-instruct-q8_0                                                                  |          |   0.10 |      7 |    1.3 |    8 |  128 | 0.24 |  0.0 |  0.0 |  0.0 |
| qwen:14b-chat-v1.5-q4_K_M                                                                        |          |   0.08 |      1 |   14.0 |    4 |   32 | 0.15 |  0.0 | 0.08 |  0.0 |
| hf.co/bartowski/burtenshaw_GemmaCoder3-12B-GGUF:Q4_K_M                                           |          |   0.06 |      1 |   11.8 |    4 |  128 | 0.04 | 0.14 | 0.03 |  0.0 |
| qwen:1.8b-chat-v1.5-q4_K_M                                                                       |          |   0.06 |      4 |    2.0 |    4 |   32 |  0.0 |  0.0 |  0.0 | 0.62 |
| hf.co/LiquidAI/LFM2-350M-GGUF:Q4_K_M                                                             |     0.27 |   0.06 |     21 |  0.354 |    4 |   32 | 0.14 |  0.0 |  0.0 |  0.0 |
| hf.co/mradermacher/MiMo-VL-7B-RL-GGUF:Q4_K_M-no_think                                            |          |   0.06 |      1 |   7.62 |    4 |  128 | 0.14 |  0.0 |  0.0 |  0.0 |
| hf.co/sizzlebop/Holo1-7B-Q4_K_M-GGUF                                                             |          |   0.05 |      1 |    7.0 |    4 |  128 | 0.13 |  0.0 |  0.0 |  0.0 |
| vicuna:13b-q4_K_M                                                                                |          |   0.04 |      0 |   13.0 |    4 |    2 | 0.09 | 0.01 |  0.0 |  0.0 |
| granite3.2-vision:2b-q4_K_M                                                                      |          |   0.04 |      2 |    2.5 |    4 |   16 | 0.07 | 0.03 |  0.0 |  0.0 |
| vicuna:13b-v1.5-16k-q4_K_M                                                                       |          |   0.03 |      0 |   13.0 |    4 |    2 | 0.06 | 0.03 |  0.0 |  0.0 |
| qwen2:0.5b-instruct-q8_0                                                                         |          |   0.03 |      5 |  0.494 |    8 |   32 | 0.07 |  0.0 |  0.0 |  0.0 |
| starcoder2:3b                                                                                    |          |   0.03 |      1 |    3.0 |    4 |   16 | 0.07 |  0.0 |  0.0 |  0.0 |
| llama2:13b-chat-q4_K_M                                                                           |          |   0.03 |      0 |   13.0 |    4 |    4 | 0.06 | 0.01 |  0.0 |  0.0 |
| hf.co/mradermacher/Holo1-3B-GGUF:Q4_K_M                                                          |          |   0.03 |      1 |   3.09 |    4 |  128 | 0.06 |  0.0 |  0.0 | 0.03 |
| vicuna:7b-v1.5-16k-q4_K_M                                                                        |          |   0.01 |      0 |    7.0 |    4 |    4 | 0.03 |  0.0 |  0.0 |  0.0 |
| qwen:7b-chat-v1.5-q4_K_M                                                                         |          |   0.01 |      0 |    8.0 |    4 |   32 | 0.02 |  0.0 |  0.0 | 0.03 |
| deepseek-coder:1.3b-instruct-q8_0                                                                |          |   0.01 |      1 |    1.0 |    8 |   16 |  0.0 | 0.02 |  0.0 |  0.0 |
| gemma3:270m                                                                                      |          |   0.00 |      1 |   0.27 |    8 |   32 | 0.01 |  0.0 |  0.0 |  0.0 |
| hf.co/allenai/OLMo-2-0425-1B-Instruct-GGUF:Q4_K_M                                                |          |   0.00 |      0 |   1.48 |    4 |    4 | 0.01 |  0.0 |  0.0 |  0.0 |
| llama2:7b-chat-q4_K_M                                                                            |          |   0.00 |      0 |    7.0 |    4 |    4 | 0.01 |  0.0 |  0.0 |  0.0 |
| deepseek-r1:8b-0528-qwen3-q4_K_M                                                                 |          |   0.00 |      0 |    8.2 |    4 |  160 | 0.01 |  0.0 |  0.0 |  0.0 |
| phi4-mini-reasoning:3.8b-q4_K_M                                                                  |          |   0.00 |      0 |    3.8 |    4 |  128 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                                                   |     0.15 |   0.00 |      0 |  0.135 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:1.7b-instruct-v0.2-q8_0                                                                   |          |   0.00 |      0 |    1.7 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:360m-instruct-v0.2-q8_0                                                                   |          |   0.00 |      0 |   0.36 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:0.5b-chat-v1.5-q4_K_M                                                                       |          |   0.00 |      0 |   0.62 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:4b-chat-v1.5-q4_K_M                                                                         |          |   0.00 |      0 |    4.0 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| codegemma:2b-code-v1.1-q4_K_M                                                                    |          |   0.00 |      0 |    3.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |
| vicuna:7b-q4_K_M                                                                                 |          |   0.00 |      0 |    7.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |

This shows that even very small models like the llama3.2 model has a two-fold super-human performance at solving those problems.

## Motivation

Solving specific tasks by coding programs requires a high degree of accuracy and efficiency.
Challenging problems, such as those presented by Project Euler, test whether a person (or an AI system) can comprehend complex
problems and translate that understanding into effective solutions. 

Because the Project Euler has statistics about the number of solved problems we have the ability to compute the likelihod for
a human to solve the problem. The given counts of course also reflect several other causes for not solving the problem (not enough
interest, not enough time, not visible at the time the contestant has subscribed to the project) which cannot be easily integrated into
our measurement method; however Project Euler started 2015 with more than 160 problems so it is feasable to select only the first 100
problems for the PE-Bench-Python-100 benchmark.

## Scoring Method

We create the benchmark with the following concept:
- We have a fixed number of `participants = 1325386` and a number of participants who solved each problem `solved_by`
- Each Problem has a specific likelihood to be solved, which is `percentage_solved = solved_by / participants` (must be multiplied with 100 to get the percentage number)
- Each Problem gets a number of points assigned that a participants gets as score, which is `points = participants / solved_by`

So this leads to the effect, that an average person can solve each problem with an performance indicator of `1` (percentage_solved * points).
Therefore the average number of points for solving 100 problems is also `1`. This gives us a nice baseline for human performance.

### Data Sources

The data is scraped from the Project Euler web page and from other sources:

```
python3 problems_scraper.py
```

This loads all problems from https://projecteuler.net/ and stores them intoo the `problems` folder.

```
python3 solutions_scraper.py
```

This loads all solutions from https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md
and combines them with the number of solutions that users have submitted from https://projecteuler.net/archives
The result is stored in `solutions.json`. There also the data is enrichted with `percentage_solved` and `points`.

### Score Computation

The canonical combined score uses these language weights:

```text
(5 * Python + 4 * JavaScript + 3 * Java + 2 * Rust + Clojure) / 15
```

Python is the estimation baseline when a model has not yet been tested in every language. For each batch size and non-Python language, the benchmark calculates the median observed `language score / Python score` ratio from models having both real results. The median prevents an isolated extreme ratio from distorting estimates. A missing result is estimated as `language coefficient * model Python score`, then multiplied by its normal language weight. Estimates are computed only while ranking and publishing; they are never stored as results in `benchmark.json`.

During coefficient bootstrapping, a language without a paired calibration result is excluded from both the numerator and denominator instead of being treated as a zero. Estimation activates as soon as one valid pair exists. Standard and tool-mode coefficients are calculated independently, but tool-mode results are currently excluded from publishing.

### Performance Score

The Performance Score combines the PE-200 coding score with measured inference throughput. Throughput is measured locally with Ollama on an Apple M1 Mac Studio (`Mac13,1` or `Mac13,2`), as enforced by `performance.py`. Prompt processing is included at one percent of its measured rate because prompt ingestion is typically much faster than output generation:

```text
effective tokens/second = output tokens/second + prompt tokens/second / 100

Performance Score = PE-200 Score * effective tokens/second / 100
```

For example, a PE-200 Score of `40` and an effective throughput of `25` tokens per second produce a Performance Score of `10`. Throughput and Performance Scores measured on different hardware are not directly comparable. The score is only calculated for PE-Bench-200 and remains blank when either the output-token or prompt-token throughput measurement is unavailable.

If we ask a LLM to solve 100 problems, add the achieved points for each correctly solved problem and divide it by 100, we get the performance
number for that LLM which compares to human performance by that average number. A performance value of `2` would mean "two-fold super-human performance".
In our test, small models like "llama3.2" already have that super-human performance.
A performance number over 1 indicates a super-human performance. It turns out that almost all LLMs have super-human performance.

The score used for the benchmark is computed in three steps:

#### Inference

For a given model and a given programming language, we loop over all (or 1..100) problems within the `problems` directory and perform the following task:
- load the problem description, i.e. from `problems/0001.txt`
- insert the problem description into a prompt template, i.e. from `templates/template_python.md`
- sending the resulting prompt to the selected LLM model using an api call to the openai-api `/v1/chat/completions` endpoint
- storing the answer from the model into `solutions/<model_name>/<language>/0001.md

This results in 100 answer files. This can be done calling

```
python3 inference.py --model <model_name>
```

Without `--language`, the pipeline tests `python,javascript,java,rust,clojure` in that order. JavaScript prompts use `templates/template_javascript.md`.

#### Code Extraction

Code is embedded into code blocks of the answer of the llm. We want to extract this in such a way, that a code interpreter can execute the file
directly. This is done with the script

```
python3 codeextraction.py --model <model_name>
```

#### Code Execution and Evaluation

Finally the code is executed within a protected environment. This is done with

```
python3 execute.py --model <model_name>
```

Each language is executed by its protected execution framework. JavaScript runs as self-contained ECMAScript in an isolated Node context with filesystem, network, subprocess, worker, external-package, and dynamic-code access disabled. The resulting output is truncated to its last line. That line is compared
to the actual solution from the `solutions.json` file. The process does the code execution for all 100 problem solutions and adds up all the
points for the corresponding problem. This sum is divided by 100 and is the final score for the model.

## Installation

The JavaScript execution framework requires a recent Node.js installation whose `node --help` output includes both `--permission` and `--allow-net`. The runner fails closed when these permission features are unavailable. Node must be available on `PATH`; no npm packages are required.

As a preparation step for the tests, we must download the test cases from project euler with this script:
```
python3 problems_scraper.py
```

All over 900 tests are then stored in the `problems` folder. For our 100-bench-series, we use only the first 100.


## Inference Engine set-up

We give here a very short instruction on how to set-up llama.cpp or ollama. You can also of course use LMstudio,
vllm or any other engine that supports the openai api

### llama.cpp

Llama.cpp has lots of tools, one of them is a openai-api compatible server, simply called "server".
You can install it with:
```
curl -LsSf https://llama.app/install.sh | sh
```
Follow the instructions given by the installer to make llama-server available in the future sessions.
The server application then can be started with i.e.
```
llama-server -hf Jackrong/Qwopus3.6-27B-v2-GGUF:Q4_K_M
```
This starts a chat interface at http://localhost:8080
This server has Model Management, that means you can dynamically
load more models into its own model store, like
```
curl -X POST http://localhost:8080/models/load -H "Content-Type: application/json" -d '{"model": "my-model.gguf"}'
```
or delete a model with
```
curl -X POST http://localhost:8080/models/unload -H "Content-Type: application/json" -d '{"model": "my-model.gguf"}'
```
The model storage location is system-specific, you probably find it in `~/.cache/huggingface/`.


### Ollama

Ollama comes easy-to-install with a desktop application which itself installs a command-line applications `ollama`.
You then have commands like:
```
ollama ls
ollama ps
ollama run <model-name>
ollama pull <model-name>
ollama rm <model-name>
```

Ollama may be easy to use, but it sometimes takes a long time until they support the latest model architectures.
They also apply download limitations, so you will not be able to load as many models as you want.

## Test Preparation
To run a test (i.e. for the model `athene-v2:72b-q8_0`), the following command sequence is required:

```
python3 inference.py --language python --model athene-v2:72b-q8_0
python3 codeextraction.py --language python --model athene-v2:72b-q8_0
python3 execute.py --language python --model athene-v2:72b-q8_0
```

However, it is not convenient to do so, instead you can also call

```
python3 test.py --language python --model athene-v2:72b-q8_0
```

That computes all steps and updates the solutions.json file. 

You can also call

```
python3 test.py --language python --allmodels --skip_existing
```

which loads the list of models from the openai api and iterates over all available models.
This will take some time, if you have a large model collection, maybe this takes
longer than a week.


## License

This work (code and benchmark results) is licensed by Michael Christen under the
Apache License Version 2.0, January 2004
