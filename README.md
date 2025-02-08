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

| Model                                                                | Best<br/>Model<br/>for<br/>Size (GB) | Eco-<br/>Score | Size<br/>(*10^9 Params) | Bits | Context Length<br/>(K) | PE-Bench-Python-100 | PE-Bench-Java-100 | PE-Bench-Rust-100 | PE-Bench-Clojure-100 |
| :------------------------------------------------------------------- | -----------------------------------: | -------------: | ----------------------: | ---: | ---------------------: | ------------------: | ----------------: | ----------------: | -------------------: |
| GPT-o1-Mini                                                          |                              9999.00 |                |                         |   16 |                        |               17.44 |                   |                   |                      |
| GPT-o1-Preview                                                       |                              9999.00 |                |                         |   16 |                        |               15.86 |                   |                   |                      |
| DeepSeek-V3                                                          |                              1342.00 |              1 |                   671.0 |   16 |                     64 |               20.01 |             16.95 |             12.16 |                 5.92 |
| GPT-4o                                                               |                                      |                |                         |   16 |                    128 |               17.05 |             13.87 |             14.57 |                 8.24 |
| athene-v2:72b-q8_0                                                   |                                72.70 |             14 |                    72.7 |    8 |                    128 |               16.22 |             10.15 |              5.55 |                 3.32 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                          |                                36.35 |             28 |                    72.7 |    4 |                    128 |               14.49 |             10.56 |              6.33 |                 3.74 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                       |                                16.40 |             60 |                    32.8 |    4 |                     32 |               12.72 |             11.67 |              7.25 |                 2.89 |
| athene-v2:latest                                                     |                                      |             27 |                    72.7 |    4 |                    128 |               14.07 |             11.14 |              6.55 |                 1.62 |
| qwen2.5:72b-instruct-q8_0                                            |                                      |             13 |                    72.7 |    8 |                    128 |               12.98 |              10.5 |              5.41 |                 3.49 |
| hf.co/bartowski/Sky-T1-32B-Flash-GGUF:Q4_K_M                         |                                16.40 |             56 |                    32.8 |    4 |                     32 |               12.04 |             10.75 |              6.64 |                  2.5 |
| qwen2.5:72b-instruct-q4_K_M                                          |                                      |             25 |                    72.7 |    4 |                    128 |               14.02 |               9.1 |              5.97 |                 2.46 |
| qwen2.5-coder:32b-instruct-q4_K_M                                    |                                16.40 |             55 |                    32.8 |    4 |                     32 |               14.05 |              8.82 |              6.41 |                  2.2 |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M      |                                      |             25 |                    72.7 |    4 |                    128 |               13.92 |              8.65 |              6.11 |                 3.07 |
| hf.co/mradermacher/Bespoke-Stratos-32B-GGUF:Q4_K_M                   |                                16.40 |             55 |                    32.8 |    4 |                     32 |               12.37 |               9.9 |              7.58 |                 1.78 |
| qwen2.5-coder:32b-instruct-q8_0                                      |                                      |             27 |                    32.8 |    8 |                     32 |               11.94 |              9.94 |              6.69 |                  2.8 |
| qwen2.5:32b-instruct-q4_K_M                                          |                                16.40 |             52 |                    32.8 |    4 |                     32 |               12.34 |              9.26 |              6.13 |                 2.25 |
| qwen2.5:32b-instruct-q8_0                                            |                                      |             25 |                    32.8 |    8 |                     32 |                9.73 |             10.22 |              5.91 |                 2.98 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0     |                                      |             25 |                    32.8 |    8 |                     32 |               11.58 |              8.69 |              6.27 |                 1.62 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M   |                                16.40 |             46 |                    32.8 |    4 |                     32 |                9.55 |               9.3 |              5.71 |                 1.94 |
| GPT-4o-Mini                                                          |                                      |                |                         |   16 |                    128 |               11.39 |              7.36 |              5.19 |                 1.93 |
| deepseek-coder:33b-instruct-q4_K_M                                   |                                      |             44 |                    33.0 |    4 |                     16 |                9.55 |             10.72 |               0.0 |                 3.03 |
| llama3.3:70b-instruct-q8_0                                           |                                      |             10 |                    70.6 |    8 |                    128 |                8.93 |              8.06 |              4.29 |                 3.17 |
| GPT-3.5-Turbo                                                        |                                      |              2 |                   175.0 |   16 |                     16 |                10.1 |              7.28 |               6.0 |                  0.5 |
| yi-coder:9b-chat-q8_0                                                |                                 8.80 |             77 |                     8.8 |    8 |                    128 |               11.08 |              6.77 |              4.32 |                 0.47 |
| qwen2.5-coder:14b-instruct-q8_0                                      |                                      |             45 |                    14.8 |    8 |                    128 |                 9.7 |              7.35 |              4.55 |                 0.95 |
| deepseek-coder:33b-instruct-q8_0                                     |                                      |             20 |                    33.0 |    8 |                     16 |                8.35 |              10.2 |               0.0 |                 1.82 |
| qwen2.5-coder:14b-instruct-q4_K_M                                    |                                 7.40 |             85 |                    14.8 |    4 |                    128 |                8.65 |              7.28 |              4.62 |                 1.13 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q4_K_M                     |                                 7.35 |             85 |                    14.7 |    4 |                     16 |                9.26 |               6.8 |              4.42 |                 0.89 |
| phi4:14b                                                             |                                 7.35 |             84 |                    14.7 |    4 |                     16 |                9.64 |              6.91 |              3.14 |                 0.84 |
| phi4:latest                                                          |                                 7.35 |             84 |                    14.7 |    4 |                     16 |                9.64 |              6.91 |              3.14 |                 0.84 |
| phi4:14b-q8_0                                                        |                                      |             41 |                    14.7 |    8 |                     16 |               10.23 |              5.29 |              4.52 |                 0.97 |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M   |                                      |             17 |                    70.6 |    4 |                    128 |                 9.1 |               5.9 |              4.69 |                 1.37 |
| vanilj/Phi-4:Q8_0                                                    |                                      |             38 |                    14.7 |    8 |                     16 |                9.06 |              5.73 |              3.52 |                 0.84 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                            |                                      |             16 |                    70.6 |    4 |                    128 |                8.07 |              6.49 |              2.59 |                 1.36 |
| yi-coder:9b-chat-q4_K_M                                              |                                 4.40 |            125 |                     8.8 |    4 |                    128 |                7.44 |              6.04 |              5.76 |                 0.34 |
| llama3.1:70b-instruct-q8_0                                           |                                      |              8 |                    70.6 |    8 |                    128 |                8.19 |              5.36 |               3.8 |                  1.7 |
| llama3.3:70b-instruct-q4_K_M                                         |                                      |             15 |                    70.6 |    4 |                    128 |                7.26 |              5.25 |              4.49 |                 2.21 |
| qwen2.5:14b-instruct-q8_0                                            |                                      |             36 |                    14.8 |    8 |                     32 |                8.59 |              4.14 |              4.55 |                 1.61 |
| qwen2.5:14b-instruct-q4_K_M                                          |                                      |             70 |                    14.8 |    4 |                     32 |                8.44 |              5.08 |              3.44 |                 0.43 |
| llama3.1:70b-instruct-q4_K_M                                         |                                      |             15 |                    70.6 |    4 |                    128 |                8.77 |              4.98 |              2.77 |                  0.6 |
| falcon3:10b-instruct-q8_0                                            |                                      |             50 |                    10.3 |    8 |                     32 |                8.15 |              5.14 |              2.71 |                 1.39 |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S                |                                      |             13 |                    78.0 |    4 |                     32 |                7.04 |              6.05 |               3.6 |                 0.74 |
| qwen2-math:72b-instruct-q8_0                                         |                                      |              7 |                    72.7 |    8 |                      4 |                6.49 |              6.67 |              2.61 |                  1.3 |
| tulu3:70b-q4_K_M                                                     |                                      |             14 |                    70.6 |    4 |                    128 |                7.31 |              4.68 |              3.35 |                 2.15 |
| tulu3:70b-q8_0                                                       |                                      |              7 |                    70.6 |    8 |                    128 |                7.73 |              4.61 |              3.09 |                 1.59 |
| falcon3:10b-instruct-q4_K_M                                          |                                      |             89 |                    10.3 |    4 |                     32 |                6.62 |              5.77 |              2.19 |                  0.6 |
| qwq:32b-preview-q8_0                                                 |                                      |             14 |                    32.8 |    8 |                     32 |                9.68 |              2.94 |              1.39 |                 0.54 |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                  |                                      |             61 |                    14.8 |    4 |                    986 |                7.75 |              4.02 |              2.74 |                 0.81 |
| nemotron:70b-instruct-q4_K_M                                         |                                      |             13 |                    70.6 |    4 |                    128 |                5.78 |              5.13 |              4.22 |                 0.83 |
| qwen2.5-coder:7b-instruct-q8_0                                       |                                      |             57 |                     7.6 |    8 |                    128 |                6.37 |               4.4 |              3.78 |                 0.63 |
| nemotron:70b-instruct-q8_0                                           |                                      |              6 |                    70.6 |    8 |                    128 |                6.31 |              4.05 |              3.23 |                 1.13 |
| falcon3:7b-instruct-q8_0                                             |                                      |             53 |                     7.5 |    8 |                     32 |                6.76 |              3.91 |              2.16 |                 0.36 |
| qwen2.5:7b-instruct-q8_0                                             |                                      |             52 |                     7.6 |    8 |                    128 |                7.47 |               3.6 |              1.13 |                 0.51 |
| qwen2.5:7b-instruct-q4_K_M                                           |                                 3.80 |            100 |                     7.6 |    4 |                    128 |                 7.5 |              2.67 |              1.86 |                 0.49 |
| qwen2.5-coder:7b-instruct-q4_K_M                                     |                                 3.80 |             99 |                     7.6 |    4 |                     32 |                4.76 |               4.7 |              2.87 |                 0.87 |
| mistral-small:24b-instruct-2501-q4_K_M                               |                                      |             31 |                    23.6 |    4 |                     32 |                6.32 |              2.89 |              2.47 |                 0.93 |
| gemma2:27b-instruct-q8_0                                             |                                      |             13 |                    27.2 |    8 |                      8 |                5.18 |               3.3 |              2.47 |                 0.98 |
| deepseek-coder:6.7b-instruct-q8_0                                    |                                      |             47 |                     7.0 |    8 |                     16 |                5.37 |              3.68 |              0.94 |                 0.79 |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                               |                                      |              9 |                    70.6 |    4 |                      8 |                6.98 |              1.99 |              0.76 |                 0.36 |
| hf.co/lmstudio-community/Mistral-Small-24B-Instruct-2501-GGUF:Q4_K_M |                                      |             26 |                    23.6 |    4 |                     32 |                5.21 |              2.86 |              1.54 |                 0.79 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                     |                                      |             70 |                     8.8 |    4 |                     32 |                4.92 |              3.64 |              1.18 |                 0.06 |
| opencoder:8b-instruct-q8_0                                           |                                      |             39 |                     7.8 |    8 |                      8 |                4.63 |              3.22 |              1.62 |                 0.72 |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                             |                                      |             34 |                    8.83 |    8 |                      4 |                6.54 |              2.11 |               0.4 |                 0.09 |
| hf.co/bartowski/simplescaling_s1-32B-GGUF:Q4_K_M                     |                                      |                |                    32.8 |      |                        |                4.33 |              2.29 |              2.78 |                  1.4 |
| exaone3.5:32b-instruct-q8_0                                          |                                      |              9 |                    32.0 |    8 |                     32 |                3.96 |              3.82 |              1.38 |                 0.47 |
| hf.co/mradermacher/Bespoke-Stratos-7B-GGUF:Q4_K_M                    |                                      |             76 |                    7.62 |    4 |                     32 |                4.72 |              2.67 |              2.26 |                 0.23 |
| yi:34b-chat-v1.5-q4_K_M                                              |                                      |             17 |                    34.0 |    4 |                      4 |                4.25 |              2.63 |              0.58 |                      |
| deepseek-r1:32b-qwen-distill-q4_K_M                                  |                                      |             17 |                    32.8 |    4 |                    128 |                4.51 |              2.91 |              1.44 |                 0.32 |
| qwen2.5-coder:3b-instruct-q4_K_M                                     |                                 1.55 |            178 |                     3.1 |    4 |                     32 |                4.98 |              2.51 |              1.53 |                 0.03 |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                   |                                      |             65 |                    7.62 |    4 |                    128 |                6.55 |               0.0 |              1.63 |                 0.24 |
| qwen2.5-coder:3b-instruct-q8_0                                       |                                      |             77 |                     3.1 |    8 |                     32 |                 4.2 |              2.15 |               1.4 |                  0.2 |
| yi:9b-chat-v1.5-q4_K_M                                               |                                      |             53 |                     9.0 |    4 |                      4 |                4.04 |              2.71 |              0.39 |                 0.33 |
| qwen:110b-chat-v1.5-q4_K_M                                           |                                      |              4 |                   111.0 |    4 |                        |                3.63 |              1.84 |              0.76 |                      |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                            |                                      |              6 |                    34.4 |    8 |                      4 |                4.61 |              1.49 |              0.72 |                 0.16 |
| exaone3.5:7.8b-instruct-q8_0                                         |                                      |             28 |                     7.8 |    8 |                     32 |                3.76 |              2.26 |              0.17 |                 0.68 |
| phi3:14b-medium-128k-instruct-q8_0                                   |                                      |             14 |                    14.0 |    8 |                    128 |                4.21 |              1.55 |              0.42 |                 0.04 |
| llama3.1:8b-instruct-q8_0                                            |                                      |             23 |                     8.0 |    8 |                    128 |                3.26 |              1.78 |              0.94 |                 0.09 |
| tulu3:8b-q8_0                                                        |                                      |             23 |                     8.0 |    8 |                    128 |                3.91 |              1.06 |              0.42 |                 0.49 |
| deepseek-r1:70b-llama-distill-q4_K_M                                 |                                      |              5 |                    70.6 |    4 |                    128 |                2.17 |              2.49 |              0.19 |                 0.41 |
| deepseek-llm:67b-chat-q4_K_M                                         |                                      |              5 |                    67.0 |    4 |                      4 |                2.94 |              1.63 |               0.5 |                 0.23 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                             |                                      |             27 |                    6.06 |    8 |                      4 |                3.92 |              0.92 |              0.13 |                  0.0 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                           |                                      |             52 |                    6.06 |    4 |                      4 |                3.71 |              0.87 |              0.32 |                  0.0 |
| deepseek-r1:14b-qwen-distill-q4_K_M                                  |                                      |             21 |                    14.8 |    4 |                    128 |                 2.6 |              1.02 |              1.19 |                 1.02 |
| qwen2.5:3b-instruct-q4_K_M                                           |                                 1.55 |             99 |                     3.1 |    4 |                    128 |                2.95 |              1.35 |              0.56 |                 0.05 |
| gemma2:9b-instruct-q8_0                                              |                                      |             16 |                     9.2 |    8 |                      8 |                2.46 |              1.55 |              0.86 |                 0.12 |
| granite3.1-dense:8b-instruct-q8_0                                    |                                      |             18 |                     8.2 |    8 |                    128 |                2.73 |              1.55 |              0.16 |                 0.03 |
| yi-coder:1.5b-chat-q4_K_M                                            |                                 0.75 |            190 |                     1.5 |    4 |                    128 |                3.49 |              0.61 |              0.34 |                  0.0 |
| codegemma:7b-instruct-v1.1-q4_K_M                                    |                                      |             30 |                     9.0 |    4 |                        |                2.21 |              1.49 |              0.66 |                 0.01 |
| deepseek-r1:7b-qwen-distill-q4_K_M                                   |                                      |             35 |                     7.6 |    4 |                    128 |                2.64 |              1.08 |               0.0 |                 0.46 |
| opencoder:1.5b-instruct-q8_0                                         |                                      |             69 |                     1.9 |    8 |                      4 |                 2.2 |              1.47 |               0.5 |                  0.0 |
| exaone3.5:2.4b-instruct-q8_0                                         |                                      |             48 |                     2.7 |    8 |                     32 |                2.73 |              0.94 |              0.28 |                 0.15 |
| qwen2.5:3b-instruct-q8_0                                             |                                      |             41 |                     3.1 |    8 |                    128 |                2.87 |              0.59 |              0.44 |                 0.18 |
| yi-coder:1.5b-chat-q8_0                                              |                                      |             82 |                     1.5 |    8 |                    128 |                2.32 |              1.17 |              0.42 |                  0.0 |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                    |                                      |              5 |                    46.7 |    4 |                     32 |                 2.0 |              1.24 |              0.62 |                  0.0 |
| dolphin3:8b-llama3.1-q8_0                                            |                                      |             14 |                     8.0 |    8 |                    128 |                 2.3 |              0.89 |              0.26 |                 0.31 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                   |                                 0.75 |            154 |                     1.5 |    4 |                     32 |                2.26 |               0.8 |               0.8 |                 0.03 |
| qwen2-math:7b-instruct-q8_0                                          |                                      |             15 |                     7.6 |    8 |                      4 |                2.49 |              0.95 |              0.02 |                  0.0 |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                     |                                      |             14 |                     8.0 |    8 |                      8 |                1.51 |              1.65 |               0.3 |                 0.03 |
| codegemma:7b-instruct-q8_0                                           |                                      |             12 |                     9.0 |    8 |                      8 |                1.84 |              1.27 |              0.39 |                  0.0 |
| qwen2.5-coder:1.5b-instruct-q8_0                                     |                                      |             73 |                     1.5 |    8 |                     32 |                2.04 |               0.9 |              0.66 |                 0.03 |
| deepseek-r1:8b-llama-distill-q4_K_M                                  |                                      |             27 |                     8.0 |    4 |                    128 |                1.46 |              1.25 |              0.45 |                 0.67 |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0      |                                      |             13 |                    8.03 |    8 |                    128 |                2.29 |              0.47 |              0.58 |                 0.37 |
| falcon3:3b-instruct-q8_0                                             |                                      |             33 |                     3.2 |    8 |                     32 |                1.89 |              1.09 |              0.36 |                 0.04 |
| qwen2.5:1.5b-instruct-q8_0                                           |                                      |             68 |                     1.5 |    8 |                    128 |                2.07 |              0.82 |              0.29 |                 0.06 |
| openchat:7b-v3.5-q8_0                                                |                                      |             14 |                     7.0 |    8 |                      8 |                1.62 |              1.21 |              0.06 |                  0.0 |
| yi:6b-chat-v1.5-q4_K_M                                               |                                      |             29 |                     6.0 |    4 |                      4 |                0.79 |              1.48 |              0.62 |                 0.01 |
| codellama:34b-instruct-q4_K_M                                        |                                      |              5 |                    34.0 |    4 |                        |                1.29 |              0.99 |              0.56 |                 0.04 |
| qwen:32b-chat-v1.5-q4_K_M                                            |                                      |              5 |                    33.0 |    4 |                        |                1.54 |              0.81 |              0.13 |                 0.12 |
| llama3.2:latest                                                      |                                      |             50 |                    3.21 |    4 |                    128 |                2.14 |              0.18 |              0.21 |                  0.0 |
| qwen2.5:1.5b-instruct-q4_K_M                                         |                                 0.75 |            101 |                     1.5 |    4 |                    128 |                1.94 |              0.26 |              0.15 |                  0.0 |
| hf.co/bartowski/OpenThinker-7B-GGUF:Q4_K_M                           |                                      |             19 |                    7.62 |    4 |                     32 |                0.88 |              0.77 |              0.53 |                 0.62 |
| mixtral:8x7b-instruct-v0.1-q8_0                                      |                                      |              2 |                    46.7 |    8 |                     32 |                1.44 |              0.65 |              0.23 |                  0.0 |
| qwen:72b-chat-v1.5-q4_K_M                                            |                                      |              2 |                    72.0 |    4 |                     32 |                0.94 |              0.78 |              0.13 |                  0.0 |
| command-r7b:7b-12-2024-q4_K_M                                        |                                      |             14 |                     8.0 |    4 |                    128 |                1.54 |              0.03 |              0.26 |                 0.04 |
| olmo2:13b-1124-instruct-q4_K_M                                       |                                      |              8 |                    13.7 |    4 |                      4 |                1.59 |              0.06 |              0.01 |                 0.03 |
| olmo2:7b-1124-instruct-q4_K_M                                        |                                      |             14 |                     7.3 |    4 |                      4 |                1.42 |              0.08 |              0.02 |                  0.0 |
| qwen2.5:0.5b-instruct-q8_0                                           |                                 0.50 |             96 |                     0.5 |    8 |                    128 |                1.33 |               0.0 |              0.21 |                  0.0 |
| codellama:13b-instruct-q4_K_M                                        |                                      |              7 |                    13.0 |    4 |                     16 |                0.52 |              0.84 |              0.05 |                 0.08 |
| granite3.1-dense:2b-instruct-q8_0                                    |                                      |             17 |                     2.5 |    8 |                    128 |                1.07 |              0.11 |               0.2 |                  0.0 |
| smallthinker:3b-preview-q4_K_M                                       |                                      |             24 |                     3.4 |    4 |                    128 |                0.98 |              0.25 |               0.0 |                  0.0 |
| mistral:7b-instruct-q4_K_M                                           |                                      |             12 |                     7.0 |    4 |                     32 |                0.48 |              0.71 |              0.04 |                  0.0 |
| smallthinker:3b-preview-q8_0                                         |                                      |             11 |                     3.4 |    8 |                    128 |                0.81 |              0.19 |              0.03 |                 0.19 |
| phi:2.7b-chat-v2-q4_K_M                                              |                                      |             22 |                     3.0 |    4 |                      2 |                0.91 |              0.07 |               0.0 |                  0.0 |
| vicuna:33b-q4_K_M                                                    |                                      |              2 |                    30.0 |    4 |                        |                 0.9 |              0.06 |               0.0 |                  0.0 |
| granite3.1-moe:3b-instruct-q8_0                                      |                                      |              9 |                     3.3 |    8 |                    128 |                 0.8 |              0.03 |              0.11 |                 0.03 |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                            |                                      |              4 |                    7.62 |    8 |                    128 |                0.27 |              0.54 |               0.0 |                  0.0 |
| qwen2-math:1.5b-instruct-q8_0                                        |                                      |             15 |                     1.5 |    8 |                      4 |                0.65 |              0.03 |               0.0 |                  0.0 |
| gemma2:2b-instruct-q8_0                                              |                                      |              8 |                     2.6 |    8 |                      8 |                0.39 |              0.22 |              0.03 |                  0.0 |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                                 |                                      |             20 |                     1.8 |    4 |                    128 |                0.45 |               0.1 |               0.0 |                  0.0 |
| codellama:7b-instruct-q4_K_M                                         |                                      |              5 |                     7.0 |    4 |                        |                0.33 |              0.03 |              0.33 |                 0.01 |
| deepseek-llm:7b-chat-q8_0                                            |                                      |              2 |                     7.0 |    8 |                      4 |                0.46 |              0.06 |               0.0 |                  0.0 |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                    |                                      |              0 |                    72.7 |    4 |                     32 |                0.31 |               0.0 |              0.08 |                 0.16 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                   |                                 0.25 |             50 |                     0.5 |    4 |                     32 |                0.36 |              0.01 |              0.01 |                  0.0 |
| qwen2.5:0.5b-instruct-q4_K_M                                         |                                 0.25 |             49 |                     0.5 |    4 |                    128 |                0.36 |               0.0 |              0.01 |                  0.0 |
| llama2:70b-chat-q4_K_M                                               |                                      |              0 |                    69.0 |    4 |                      4 |                0.31 |              0.03 |              0.01 |                 0.03 |
| llama3.2:1b-instruct-q8_0                                            |                                      |              9 |                     1.2 |    8 |                    128 |                0.28 |              0.06 |               0.0 |                  0.0 |
| qwen2.5-coder:0.5b-instruct-q8_0                                     |                                      |             22 |                     0.5 |    8 |                     32 |                0.31 |              0.01 |              0.03 |                  0.0 |
| qwen:1.8b-chat-v1.5-q4_K_M                                           |                                      |             10 |                     2.0 |    4 |                     32 |                 0.0 |               0.0 |               0.0 |                 0.62 |
| falcon:7b-instruct-q4_0                                              |                                      |              3 |                     7.0 |    4 |                      2 |                0.28 |               0.0 |               0.0 |                  0.0 |
| falcon:40b-instruct-q4_0                                             |                                      |              0 |                    40.0 |    4 |                        |                0.07 |               0.0 |              0.42 |                  0.0 |
| falcon3:1b-instruct-q8_0                                             |                                      |              5 |                     1.7 |    8 |                      8 |                0.25 |               0.0 |               0.0 |                  0.0 |
| granite3.1-moe:1b-instruct-q8_0                                      |                                      |              6 |                     1.3 |    8 |                    128 |                0.24 |               0.0 |               0.0 |                  0.0 |
| vicuna:13b-q4_K_M                                                    |                                      |              1 |                    13.0 |    4 |                        |                0.09 |              0.01 |               0.0 |                  0.0 |
| vicuna:13b-v1.5-16k-q4_K_M                                           |                                      |              0 |                    13.0 |    4 |                        |                0.06 |              0.03 |               0.0 |                  0.0 |
| qwen2:0.5b-instruct-q8_0                                             |                                      |              0 |                  494.03 |    8 |                     32 |                0.07 |               0.0 |               0.0 |                  0.0 |
| starcoder2:3b                                                        |                                      |              2 |                     3.0 |    4 |                     16 |                0.07 |               0.0 |               0.0 |                  0.0 |
| llama2:13b-chat-q4_K_M                                               |                                      |              0 |                    13.0 |    4 |                        |                0.06 |              0.01 |               0.0 |                  0.0 |
| vicuna:7b-v1.5-16k-q4_K_M                                            |                                      |              0 |                     7.0 |    4 |                        |                0.03 |               0.0 |               0.0 |                  0.0 |
| deepseek-coder:1.3b-instruct-q8_0                                    |                                      |              1 |                     1.0 |    8 |                     16 |                 0.0 |              0.02 |               0.0 |                  0.0 |
| llama2:7b-chat-q4_K_M                                                |                                      |              0 |                     7.0 |    4 |                        |                0.01 |               0.0 |               0.0 |                  0.0 |
| smollm:1.7b-instruct-v0.2-q8_0                                       |                                      |              0 |                     1.7 |    8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                       |                                 0.14 |              0 |                   0.135 |    8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| smollm:360m-instruct-v0.2-q8_0                                       |                                      |              0 |                    0.36 |    8 |                      2 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| qwen:0.5b-chat-v1.5-q4_K_M                                           |                                      |              0 |                   620.0 |    4 |                     32 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| qwen:4b-chat-v1.5-q4_K_M                                             |                                      |              0 |                     4.0 |    4 |                     32 |                 0.0 |               0.0 |               0.0 |                  0.0 |
| codegemma:2b-code-v1.1-q4_K_M                                        |                                      |              0 |                     3.0 |    4 |                        |                 0.0 |               0.0 |               0.0 |                  0.0 |
| vicuna:7b-q4_K_M                                                     |                                      |              0 |                     7.0 |    4 |                        |                 0.0 |               0.0 |               0.0 |                  0.0 |

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
