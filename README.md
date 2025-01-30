# Project Euler LLM Benchmark

To identify the performance of Large Language Models to solve problems with domain-specific knowledge (here: programming)
we created a benchmark using the Project Euler series of challenging mathematical/computer programming problems.
Because we want to apply LLMs for coding with specific programming languages, we also want to measure how good
a LLM is at coding with that given programming language.

## Super-Human Performance
AI systems have domain-specific super-human perforances: chess-AI can compete against the best humans since 1997 where
a chess system "Deep Blue" defeated the world champion Garry Kasparov. Since then the best chess programs are super-human
and the same holds for most other games including Go, defeated by AlphaGo in 2016. So in domain-specific fields, AI programs
have super-human performance and with the "Project Euler LLM Benchmark" we want to measure how strongly LLM models have
super-human performances in the domain of coding or "being a programmer". See "Motivation" chapter below how we measure this.

## Results
The computed Benchmark ("PE-Bench-Python-100", "PE-Bench-Java-100", "PE-Bench-Rust-100", "PE-Bench-Clojure-100")  is the super-human performance factor to code in Python/Java/Rust/Clojure.
The "Economic Score" is the average performance per bytes of model size (times 100). Results are:

| Model                                                              | Best<br/>Model<br/>for<br/>Size (GB) | Eco-<br/>Score | Size<br/>(*10^9 Params) | Quantization<br/>(Bits) | Context Length<br/>(K) | PE-Bench-Python-100 | PE-Bench-Java-100 | PE-Bench-Rust-100 | PE-Bench-Clojure-100 |
| :----------------------------------------------------------------- | -----------------------------------: | -------------: | ----------------------: | ----------------------: | ---------------------: | ------------------: | ----------------: | ----------------: | -------------------: |
| DeepSeek-V3                                                        |                              1342.00 |              1 |                   671.0 |                      16 |                     64 |               15.58 |             16.95 |             12.16 |                 5.92 |
| GPT-4o                                                             |                                      |                |                         |                      16 |                    128 |               15.05 |             13.87 |             14.57 |                 8.24 |
| GPT-o1-Mini                                                        |                                      |                |                         |                      16 |                        |                11.3 |                   |                   |                      |
| GPT-o1-Preview                                                     |                                      |                |                         |                      16 |                        |                10.9 |                   |                   |                      |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                        |                                36.35 |             26 |                    72.7 |                       4 |                    128 |               12.51 |             10.56 |              6.33 |                 3.74 |
| athene-v2:latest                                                   |                                36.35 |             25 |                    72.7 |                       4 |                    128 |               12.36 |             11.14 |              6.55 |                 1.62 |
| athene-v2:72b-q8_0                                                 |                                      |             13 |                    72.7 |                       8 |                    128 |                12.7 |             10.15 |              5.55 |                 3.32 |
| qwen2.5:72b-instruct-q4_K_M                                        |                                36.35 |             24 |                    72.7 |                       4 |                    128 |               13.35 |               9.1 |              5.97 |                 2.46 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                     |                                16.40 |             54 |                    32.8 |                       4 |                     32 |                9.85 |             11.67 |              7.25 |                 2.89 |
| qwen2.5:72b-instruct-q8_0                                          |                                      |             12 |                    72.7 |                       8 |                    128 |               11.01 |              10.5 |              5.41 |                 3.49 |
| qwen2.5-coder:32b-instruct-q8_0                                    |                                      |             26 |                    32.8 |                       8 |                     32 |               11.23 |              9.94 |              6.69 |                  2.8 |
| qwen2.5:32b-instruct-q4_K_M                                        |                                16.40 |             50 |                    32.8 |                       4 |                     32 |               10.96 |              9.26 |              6.13 |                 2.25 |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M    |                                      |             22 |                    72.7 |                       4 |                    128 |                10.9 |              8.65 |              6.11 |                 3.07 |
| qwen2.5:32b-instruct-q8_0                                          |                                      |             24 |                    32.8 |                       8 |                     32 |                9.25 |             10.22 |              5.91 |                 2.98 |
| qwen2.5-coder:32b-instruct-q4_K_M                                  |                                16.40 |             48 |                    32.8 |                       4 |                     32 |               10.46 |              8.82 |              6.41 |                  2.2 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0   |                                      |             24 |                    32.8 |                       8 |                     32 |               10.54 |              8.69 |              6.27 |                 1.62 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M |                                16.40 |             45 |                    32.8 |                       4 |                     32 |                9.02 |               9.3 |              5.71 |                 1.94 |
| GPT-4o-Mini                                                        |                                      |                |                         |                      16 |                    128 |               10.71 |              7.36 |              5.19 |                 1.93 |
| deepseek-coder:33b-instruct-q4_K_M                                 |                                      |             40 |                    33.0 |                       4 |                     16 |                7.79 |             10.72 |               0.0 |                 3.03 |
| qwen2.5-coder:14b-instruct-q8_0                                    |                                14.80 |             45 |                    14.8 |                       8 |                    128 |                 9.7 |              7.35 |              4.55 |                 0.95 |
| GPT-3.5-Turbo                                                      |                                      |              2 |                   175.0 |                      16 |                     16 |                9.02 |              7.28 |               6.0 |                  0.5 |
| llama3.3:70b-instruct-q8_0                                         |                                      |              9 |                    70.6 |                       8 |                    128 |                6.46 |              8.06 |              4.29 |                 3.17 |
| phi4:14b                                                           |                                 7.35 |             82 |                    14.7 |                       4 |                     16 |                9.26 |              6.91 |              3.14 |                 0.84 |
| phi4:latest                                                        |                                 7.35 |             82 |                    14.7 |                       4 |                     16 |                9.26 |              6.91 |              3.14 |                 0.84 |
| qwen2.5-coder:14b-instruct-q4_K_M                                  |                                      |             82 |                    14.8 |                       4 |                    128 |                7.98 |              7.28 |              4.62 |                 1.13 |
| yi-coder:9b-chat-q8_0                                              |                                      |             67 |                     8.8 |                       8 |                    128 |                8.57 |              6.77 |              4.32 |                 0.47 |
| phi4:14b-q8_0                                                      |                                      |             40 |                    14.7 |                       8 |                     16 |                9.64 |              5.29 |              4.52 |                 0.97 |
| deepseek-coder:33b-instruct-q8_0                                   |                                      |             17 |                    33.0 |                       8 |                     16 |                6.11 |              10.2 |               0.0 |                 1.82 |
| vanilj/Phi-4:Q8_0                                                  |                                      |             36 |                    14.7 |                       8 |                     16 |                7.81 |              5.73 |              3.52 |                 0.84 |
| qwen2.5:14b-instruct-q8_0                                          |                                      |             35 |                    14.8 |                       8 |                     32 |                8.11 |              4.14 |              4.55 |                 1.61 |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M |                                      |             14 |                    70.6 |                       4 |                    128 |                6.12 |               5.9 |              4.69 |                 1.37 |
| qwen2.5:14b-instruct-q4_K_M                                        |                                      |             68 |                    14.8 |                       4 |                     32 |                7.99 |              5.08 |              3.44 |                 0.43 |
| yi-coder:9b-chat-q4_K_M                                            |                                 4.40 |            113 |                     8.8 |                       4 |                    128 |                5.87 |              6.04 |              5.76 |                 0.34 |
| llama3.1:70b-instruct-q8_0                                         |                                      |              7 |                    70.6 |                       8 |                    128 |                 6.6 |              5.36 |               3.8 |                  1.7 |
| falcon3:10b-instruct-q8_0                                          |                                      |             47 |                    10.3 |                       8 |                     32 |                7.42 |              5.14 |              2.71 |                 1.39 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                          |                                      |             14 |                    70.6 |                       4 |                    128 |                6.14 |              6.49 |              2.59 |                 1.36 |
| llama3.3:70b-instruct-q4_K_M                                       |                                      |             14 |                    70.6 |                       4 |                    128 |                5.95 |              5.25 |              4.49 |                 2.21 |
| tulu3:70b-q4_K_M                                                   |                                      |             14 |                    70.6 |                       4 |                    128 |                 7.0 |              4.68 |              3.35 |                 2.15 |
| tulu3:70b-q8_0                                                     |                                      |              7 |                    70.6 |                       8 |                    128 |                7.34 |              4.61 |              3.09 |                 1.59 |
| qwen2-math:72b-instruct-q8_0                                       |                                      |              7 |                    72.7 |                       8 |                      4 |                5.64 |              6.67 |              2.61 |                  1.3 |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S              |                                      |             12 |                    78.0 |                       4 |                     32 |                6.01 |              6.05 |               3.6 |                 0.74 |
| falcon3:10b-instruct-q4_K_M                                        |                                      |             87 |                    10.3 |                       4 |                     32 |                6.31 |              5.77 |              2.19 |                  0.6 |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                |                                      |             61 |                    14.8 |                       4 |                    986 |                7.64 |              4.02 |              2.74 |                 0.81 |
| nemotron:70b-instruct-q4_K_M                                       |                                      |             13 |                    70.6 |                       4 |                    128 |                5.72 |              5.13 |              4.22 |                 0.83 |
| qwen2.5-coder:7b-instruct-q8_0                                     |                                      |             56 |                     7.6 |                       8 |                    128 |                6.13 |               4.4 |              3.78 |                 0.63 |
| llama3.1:70b-instruct-q4_K_M                                       |                                      |             12 |                    70.6 |                       4 |                    128 |                5.94 |              4.98 |              2.77 |                  0.6 |
| nemotron:70b-instruct-q8_0                                         |                                      |              6 |                    70.6 |                       8 |                    128 |                6.01 |              4.05 |              3.23 |                 1.13 |
| qwen2.5:7b-instruct-q8_0                                           |                                      |             47 |                     7.6 |                       8 |                    128 |                 6.4 |               3.6 |              1.13 |                 0.51 |
| falcon3:7b-instruct-q8_0                                           |                                      |             48 |                     7.5 |                       8 |                     32 |                5.57 |              3.91 |              2.16 |                 0.36 |
| qwen2.5:7b-instruct-q4_K_M                                         |                                 3.80 |             93 |                     7.6 |                       4 |                    128 |                6.81 |              2.67 |              1.86 |                 0.49 |
| gemma2:27b-instruct-q8_0                                           |                                      |             13 |                    27.2 |                       8 |                      8 |                5.18 |               3.3 |              2.47 |                 0.98 |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                             |                                      |              9 |                    70.6 |                       4 |                      8 |                6.81 |              1.99 |              0.76 |                 0.36 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                   |                                      |             68 |                     8.8 |                       4 |                     32 |                4.67 |              3.64 |              1.18 |                 0.06 |
| opencoder:8b-instruct-q8_0                                         |                                      |             38 |                     7.8 |                       8 |                      8 |                4.53 |              3.22 |              1.62 |                 0.72 |
| qwq:32b-preview-q8_0                                               |                                      |              9 |                    32.8 |                       8 |                     32 |                4.89 |              2.94 |              1.39 |                 0.54 |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                           |                                      |             32 |                    8.83 |                       8 |                      4 |                6.16 |              2.11 |               0.4 |                 0.09 |
| deepseek-r1:32b-qwen-distill-q4_K_M                                |                                      |             17 |                    32.8 |                       4 |                    128 |                4.51 |              2.91 |              1.44 |                 0.32 |
| deepseek-coder:6.7b-instruct-q8_0                                  |                                      |             37 |                     7.0 |                       8 |                     16 |                3.31 |              3.68 |              0.94 |                 0.79 |
| exaone3.5:32b-instruct-q8_0                                        |                                      |              8 |                    32.0 |                       8 |                     32 |                2.96 |              3.82 |              1.38 |                 0.47 |
| qwen2.5-coder:3b-instruct-q4_K_M                                   |                                 1.55 |            165 |                     3.1 |                       4 |                     32 |                4.39 |              2.51 |              1.53 |                 0.03 |
| qwen2.5-coder:3b-instruct-q8_0                                     |                                      |             78 |                     3.1 |                       8 |                     32 |                4.32 |              2.15 |               1.4 |                  0.2 |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                 |                                      |             63 |                    7.62 |                       4 |                    128 |                6.27 |               0.0 |              1.63 |                 0.24 |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                          |                                      |              6 |                    34.4 |                       8 |                      4 |                4.36 |              1.49 |              0.72 |                 0.16 |
| exaone3.5:7.8b-instruct-q8_0                                       |                                      |             27 |                     7.8 |                       8 |                     32 |                3.55 |              2.26 |              0.17 |                 0.68 |
| llama3.1:8b-instruct-q8_0                                          |                                      |             23 |                     8.0 |                       8 |                    128 |                3.32 |              1.78 |              0.94 |                 0.09 |
| phi3:14b-medium-128k-instruct-q8_0                                 |                                      |             13 |                    14.0 |                       8 |                    128 |                3.59 |              1.55 |              0.42 |                 0.04 |
| tulu3:8b-q8_0                                                      |                                      |             21 |                     8.0 |                       8 |                    128 |                3.64 |              1.06 |              0.42 |                 0.49 |
| deepseek-r1:70b-llama-distill-q4_K_M                               |                                      |              4 |                    70.6 |                       4 |                    128 |                1.81 |              2.49 |              0.19 |                 0.41 |
| deepseek-llm:67b-chat-q4_K_M                                       |                                      |              5 |                    67.0 |                       4 |                      4 |                2.59 |              1.63 |               0.5 |                 0.23 |
| gemma2:9b-instruct-q8_0                                            |                                      |             16 |                     9.2 |                       8 |                      8 |                2.46 |              1.55 |              0.86 |                 0.12 |
| deepseek-r1:14b-qwen-distill-q4_K_M                                |                                      |             20 |                    14.8 |                       4 |                    128 |                2.36 |              1.02 |              1.19 |                 1.02 |
| granite3.1-dense:8b-instruct-q8_0                                  |                                      |             18 |                     8.2 |                       8 |                    128 |                 2.8 |              1.55 |              0.16 |                 0.03 |
| qwen2.5:3b-instruct-q4_K_M                                         |                                 1.55 |             95 |                     3.1 |                       4 |                    128 |                2.75 |              1.35 |              0.56 |                 0.05 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                         |                                      |             48 |                    6.06 |                       4 |                      4 |                3.35 |              0.87 |              0.32 |                  0.0 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                           |                                      |             24 |                    6.06 |                       8 |                      4 |                3.39 |              0.92 |              0.13 |                  0.0 |
| yi-coder:1.5b-chat-q4_K_M                                          |                                 0.75 |            185 |                     1.5 |                       4 |                    128 |                3.39 |              0.61 |              0.34 |                  0.0 |
| opencoder:1.5b-instruct-q8_0                                       |                                      |             69 |                     1.9 |                       8 |                      4 |                 2.2 |              1.47 |               0.5 |                  0.0 |
| qwen2.5:3b-instruct-q8_0                                           |                                      |             41 |                     3.1 |                       8 |                    128 |                2.87 |              0.59 |              0.44 |                 0.18 |
| exaone3.5:2.4b-instruct-q8_0                                       |                                      |             45 |                     2.7 |                       8 |                     32 |                2.53 |              0.94 |              0.28 |                 0.15 |
| yi-coder:1.5b-chat-q8_0                                            |                                      |             82 |                     1.5 |                       8 |                    128 |                 2.3 |              1.17 |              0.42 |                  0.0 |
| deepseek-r1:7b-qwen-distill-q4_K_M                                 |                                      |             32 |                     7.6 |                       4 |                    128 |                2.36 |              1.08 |               0.0 |                 0.46 |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                  |                                      |              5 |                    46.7 |                       4 |                     32 |                 2.0 |              1.24 |              0.62 |                  0.0 |
| dolphin3:8b-llama3.1-q8_0                                          |                                      |             14 |                     8.0 |                       8 |                    128 |                 2.3 |              0.89 |              0.26 |                 0.31 |
| qwen2-math:7b-instruct-q8_0                                        |                                      |             15 |                     7.6 |                       8 |                      4 |                2.49 |              0.95 |              0.02 |                  0.0 |
| codegemma:7b-instruct-q8_0                                         |                                      |             12 |                     9.0 |                       8 |                      8 |                1.81 |              1.27 |              0.39 |                  0.0 |
| deepseek-r1:8b-llama-distill-q4_K_M                                |                                      |             27 |                     8.0 |                       4 |                    128 |                1.46 |              1.25 |              0.45 |                 0.67 |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0    |                                      |             13 |                    8.03 |                       8 |                    128 |                2.29 |              0.47 |              0.58 |                 0.37 |
| qwen2.5-coder:1.5b-instruct-q8_0                                   |                                      |             71 |                     1.5 |                       8 |                     32 |                1.95 |               0.9 |              0.66 |                 0.03 |
| falcon3:3b-instruct-q8_0                                           |                                      |             33 |                     3.2 |                       8 |                     32 |                1.89 |              1.09 |              0.36 |                 0.04 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                 |                                 0.75 |            132 |                     1.5 |                       4 |                     32 |                1.76 |               0.8 |               0.8 |                 0.03 |
| qwen2.5:1.5b-instruct-q8_0                                         |                                      |             66 |                     1.5 |                       8 |                    128 |                1.98 |              0.82 |              0.29 |                 0.06 |
| openchat:7b-v3.5-q8_0                                              |                                      |             14 |                     7.0 |                       8 |                      8 |                1.62 |              1.21 |              0.06 |                  0.0 |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                   |                                      |             12 |                     8.0 |                       8 |                      8 |                1.04 |              1.65 |               0.3 |                 0.03 |
| llama3.2:latest                                                    |                                      |             50 |                    3.21 |                       4 |                    128 |                2.14 |              0.18 |              0.21 |                  0.0 |
| mixtral:8x7b-instruct-v0.1-q8_0                                    |                                      |              2 |                    46.7 |                       8 |                     32 |                1.44 |              0.65 |              0.23 |                  0.0 |
| qwen2.5:1.5b-instruct-q4_K_M                                       |                                 0.75 |             92 |                     1.5 |                       4 |                    128 |                1.73 |              0.26 |              0.15 |                  0.0 |
| command-r7b:7b-12-2024-q4_K_M                                      |                                      |             14 |                     8.0 |                       4 |                    128 |                1.54 |              0.03 |              0.26 |                 0.04 |
| olmo2:13b-1124-instruct-q4_K_M                                     |                                      |              7 |                    13.7 |                       4 |                      4 |                1.38 |              0.06 |              0.01 |                 0.03 |
| olmo2:7b-1124-instruct-q4_K_M                                      |                                      |             12 |                     7.3 |                       4 |                      4 |                1.21 |              0.08 |              0.02 |                  0.0 |
| granite3.1-dense:2b-instruct-q8_0                                  |                                      |             17 |                     2.5 |                       8 |                    128 |                1.07 |              0.11 |               0.2 |                  0.0 |
| qwen2.5:0.5b-instruct-q8_0                                         |                                 0.50 |             74 |                     0.5 |                       8 |                    128 |                1.01 |               0.0 |              0.21 |                  0.0 |
| smallthinker:3b-preview-q8_0                                       |                                      |              9 |                     3.4 |                       8 |                    128 |                 0.6 |              0.19 |              0.03 |                 0.19 |
| granite3.1-moe:3b-instruct-q8_0                                    |                                      |              9 |                     3.3 |                       8 |                    128 |                0.78 |              0.03 |              0.11 |                 0.03 |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                          |                                      |              3 |                    7.62 |                       8 |                    128 |                0.23 |              0.54 |               0.0 |                  0.0 |
| qwen2-math:1.5b-instruct-q8_0                                      |                                      |             14 |                     1.5 |                       8 |                      4 |                0.61 |              0.03 |               0.0 |                  0.0 |
| gemma2:2b-instruct-q8_0                                            |                                      |              8 |                     2.6 |                       8 |                      8 |                0.39 |              0.22 |              0.03 |                  0.0 |
| deepseek-llm:7b-chat-q8_0                                          |                                      |              2 |                     7.0 |                       8 |                      4 |                0.46 |              0.06 |               0.0 |                  0.0 |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                               |                                      |             19 |                     1.8 |                       4 |                    128 |                0.42 |               0.1 |               0.0 |                  0.0 |
| smallthinker:3b-preview-q4_K_M                                     |                                      |              9 |                     3.4 |                       4 |                    128 |                0.22 |              0.25 |               0.0 |                  0.0 |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                  |                                      |              0 |                    72.7 |                       4 |                     32 |                0.28 |               0.0 |              0.08 |                 0.16 |
| llama3.2:1b-instruct-q8_0                                          |                                      |              8 |                     1.2 |                       8 |                    128 |                0.23 |              0.06 |               0.0 |                  0.0 |
| qwen2.5:0.5b-instruct-q4_K_M                                       |                                 0.25 |             34 |                     0.5 |                       4 |                    128 |                0.25 |               0.0 |              0.01 |                  0.0 |
| falcon3:1b-instruct-q8_0                                           |                                      |              5 |                     1.7 |                       8 |                      8 |                0.25 |               0.0 |               0.0 |                  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                 |                                 0.25 |             33 |                     0.5 |                       4 |                     32 |                0.23 |              0.01 |              0.01 |                  0.0 |
| granite3.1-moe:1b-instruct-q8_0                                    |                                      |              6 |                     1.3 |                       8 |                    128 |                0.24 |               0.0 |               0.0 |                  0.0 |
| qwen2.5-coder:0.5b-instruct-q8_0                                   |                                      |             10 |                     0.5 |                       8 |                     32 |                0.13 |              0.01 |              0.03 |                  0.0 |
| qwen2:0.5b-instruct-q8_0                                           |                                      |              0 |                  494.03 |                       8 |                     32 |                0.07 |               0.0 |               0.0 |                  0.0 |
| deepseek-coder:1.3b-instruct-q8_0                                  |                                      |              1 |                     1.0 |                       8 |                     16 |                 0.0 |              0.02 |               0.0 |                  0.0 |
| starcoder2:3b                                                      |                                      |              0 |                     3.0 |                       4 |                     16 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| smollm:1.7b-instruct-v0.2-q8_0                                     |                                      |              0 |                     1.7 |                       8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                     |                                 0.14 |              0 |                   0.135 |                       8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| smollm:360m-instruct-v0.2-q8_0                                     |                                      |              0 |                    0.36 |                       8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |

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

If we ask a LLM to solve 100 problems, add the achieved points for each correctly solved problem and divide it by 100, we get the performance
number for that LLM which compares to human performance by that average number. A performance value of `2` would mean "two-fold super-human performance".
In our test, small models like "llama3.2" already have that super-human performance.
A performance number over 1 indicates a super-human performance. It turns out that almost all LLMs have super-human performance.

The score used for the benchmark is computed in three steps:

#### Inference

For a given model and a given programming language, we loop over all (or 1..100) problems within the `problems` directory and perform the following task:
- load the problem description, i.e. from `problems/0001.txt`
- insert the problem description into a prompt template, i.e. from `templates/template_python.md`
- sending the resulting prompt to the selected LLM model using an api call to the ollama `/v1/chat/completions` endpoint
- storing the answer from the model into `solutions/<model_name>/<language>/0001.md

This results in 100 answer files. This can be done calling

```
python3 inference.py --model <model_name>
```

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

where the python code is executed within. The resulting output line is truncated, only the last line is used. That line is compared
to the actual solution from the `solutions.json` file. The process does the code execution for all 100 problem solutions and adds up all the
points for the corresponding problem. This sum is divided by 100 and is the final score for the model.

## Installation

As a preparation step for the tests, we must download the test cases from project euler with this script:
```
python3 problems_scraper.py
```

All over 900 tests are then stored in the `problems` folder. For our 100-bench-series, we use only the first 100.

## Test Preparation
To compute the benchmark, we use ollama as local inference engine.
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

which loads the list of models from ollama and iterates over all models stored with ollama.
This will take some time, if you have a large model collection in ollama maybe this takes
longer than a week.

## Contribution

My current set-up does not allow to run models greater than 128GB. Models greater than this size
had been tested using the API of the providing institution (i.e. OpenAI, DeepSeek). Other bigger models
cannot be tested on my hardware.

### Wanted

Please send me a pull request for the following cases:

- If you have better hardware and want to contribute your contribution is welcome. 
- The code runner for python, java, rust, clojure (see `execute.py`) can possibly be enhanced. That would cause better benchmark scorings for affected models. Please see if this can be enhanced.
- bugfixes (code and documentation)

## License

This work (code and benchmark results) is licensed by Michael Christen under the
Apache License Version 2.0, January 2004
