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

| Model                                                                     | Best<br/>Model<br/>for<br/>Size (GB) | PE-100-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | Java | Rust | Clojure |
| :------------------------------------------------------------------------ | -----------------------------------: | ----------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---: | ---: | ------: |
| o4-mini-2025-04-16                                                        |     9999 |  21.34 |        |        |   16 |  200 | 22.71 | 21.88 | 21.59 | 13.71 |
| gpt-4.1-2025-04-14                                                        |     9999 |  19.84 |        |        |   16 | 1024 | 22.41 | 20.88 | 17.0 | 12.08 |
| gpt-4.1-mini-2025-04-14                                                   |     9999 |  18.05 |        |        |   16 | 1024 | 18.34 | 20.53 | 18.99 | 7.56 |
| DeepSeek-V3-0324                                                          |     1342 |  17.06 |      1 |  671.0 |   16 |  128 | 20.08 | 18.63 | 14.91 | 4.62 |
| DeepSeek-V3                                                               |     1342 |  16.11 |      1 |  671.0 |   16 |  128 | 20.01 | 16.95 | 12.16 | 5.92 |
| GPT-4o                                                                    |          |  14.72 |        |        |   16 |  128 | 17.05 | 13.87 | 14.57 | 8.24 |
| GPT-o1-Mini                                                               |          |  11.36 |        |        |   16 |   32 | 17.44 |      |      |      |
| athene-v2:72b-q8_0                                                        |    72.70 |  10.97 |     15 |   72.7 |    8 |  128 | 16.22 | 10.15 | 5.55 | 3.32 |
| qwen3:235b-a22b-q4_K_M-no_think                                           |          |  10.76 |      9 |  235.1 |    4 |  128 | 13.27 | 15.17 | 3.33 | 2.35 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                               |    36.35 |  10.60 |     29 |   72.7 |    4 |  128 | 14.49 | 10.56 | 6.33 | 3.74 |
| athene-v2:72b-q4_K_M                                                      |    36.35 |  10.48 |     29 |   72.7 |    4 |  128 | 14.07 | 11.19 | 6.55 | 1.83 |
| athene-v2:latest                                                          |    36.35 |  10.44 |     29 |   72.7 |    4 |  128 | 14.07 | 11.14 | 6.55 | 1.62 |
| gpt-4.1-nano-2025-04-14                                                   |          |  10.35 |        |        |   16 | 1024 | 13.79 | 10.36 | 7.83 |  1.6 |
| GPT-o1-Preview                                                            |          |  10.33 |      2 |  300.0 |   16 |   32 | 15.86 |      |      |      |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                            |    16.40 |  10.33 |     63 |   32.8 |    4 |   32 | 12.72 | 11.67 | 7.25 | 2.89 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q8_0                              |          |  10.28 |     31 |   32.8 |    8 |   32 | 12.76 | 10.75 | 8.04 | 3.43 |
| qwen2.5:72b-instruct-q4_K_M                                               |          |   9.78 |     27 |   72.7 |    4 |  128 | 14.02 |  9.1 | 5.97 | 2.46 |
| qwen2.5:72b-instruct-q8_0                                                 |          |   9.77 |     13 |   72.7 |    8 |  128 | 12.98 | 10.5 | 5.41 | 3.49 |
| qwen2.5-coder:32b-instruct-q4_K_M                                         |    16.40 |   9.77 |     60 |   32.8 |    4 |   32 | 14.05 | 8.82 | 6.41 |  2.2 |
| hf.co/bartowski/Dracarys2-72B-Instruct-GGUF:Q4_K_M                        |          |   9.74 |     27 |   72.7 |    4 |  128 | 13.45 | 8.54 | 7.34 | 3.35 |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M           |          |   9.69 |     27 |   72.7 |    4 |  128 | 13.92 | 8.65 | 6.11 | 3.07 |
| hf.co/bartowski/THUDM_GLM-4-32B-0414-GGUF:Q4_K_M                          |    16.30 |   9.64 |     59 |   32.6 |    4 |   32 | 13.9 | 10.14 | 4.82 | 0.75 |
| hf.co/bartowski/Sky-T1-32B-Flash-GGUF:Q4_K_M                              |          |   9.62 |     59 |   32.8 |    4 |   32 | 12.04 | 10.75 | 6.64 |  2.5 |
| hf.co/mradermacher/Bespoke-Stratos-32B-GGUF:Q4_K_M                        |          |   9.61 |     59 |   32.8 |    4 |   32 | 12.37 |  9.9 | 7.58 | 1.78 |
| qwen2.5-coder:32b-instruct-q8_0                                           |          |   9.38 |     29 |   32.8 |    8 |   32 | 11.94 | 9.94 | 6.69 |  2.8 |
| qwen2.5:32b-instruct-q4_K_M                                               |          |   9.17 |     56 |   32.8 |    4 |   32 | 12.34 | 9.26 | 6.13 | 2.25 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0          |          |   8.66 |     26 |   32.8 |    8 |   32 | 11.58 | 8.69 | 6.27 | 1.62 |
| qwen2.5:32b-instruct-q8_0                                                 |          |   8.44 |     26 |   32.8 |    8 |   32 | 9.73 | 10.22 | 5.91 | 2.98 |
| GPT-4o-Mini                                                               |          |   8.00 |        |        |   16 |  128 | 11.39 | 7.36 | 5.19 | 1.93 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M        |          |   7.95 |     48 |   32.8 |    4 |   32 | 9.55 |  9.3 | 5.71 | 1.94 |
| cogito:32b-v1-preview-qwen-q4_K_M                                         |          |   7.83 |     48 |   32.8 |    4 |      | 11.32 | 7.12 | 5.26 | 1.19 |
| qwen3:32b-q4_K_M-no_think                                                 |          |   7.67 |     47 |   32.8 |    4 |  128 | 10.25 | 8.94 | 3.93 | 1.07 |
| GPT-3.5-Turbo                                                             |          |   7.47 |      2 |  175.0 |   16 |   16 | 10.1 | 7.28 |  6.0 |  0.5 |
| yi-coder:9b-chat-q8_0                                                     |     8.80 |   7.37 |     84 |    8.8 |    8 |  128 | 11.08 | 6.77 | 4.32 | 0.47 |
| deepseek-coder:33b-instruct-q4_K_M                                        |          |   7.34 |     44 |   33.0 |    4 |   16 | 9.55 | 10.72 |  0.0 | 3.03 |
| llama3.3:70b-instruct-q8_0                                                |          |   7.17 |     10 |   70.6 |    8 |  128 | 8.93 | 8.06 | 4.29 | 3.17 |
| qwen2.5-coder:14b-instruct-q8_0                                           |          |   7.09 |     48 |   14.8 |    8 |  128 |  9.7 | 7.35 | 4.55 | 0.95 |
| qwen3:14b-q4_K_M-no_think                                                 |     7.40 |   6.97 |     94 |   14.8 |    4 |      | 10.94 | 6.37 | 2.99 | 0.86 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q8_0                            |          |   6.81 |     46 |   14.7 |    8 |   16 | 10.06 | 6.67 | 3.68 | 0.52 |
| qwen3:30b-a3b-q4_K_M-no_think                                             |          |   6.81 |     45 |   30.5 |    4 |  128 | 8.22 | 8.01 | 5.11 | 0.97 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q4_K_M                          |     7.35 |   6.72 |     91 |   14.7 |    4 |   16 | 9.26 |  6.8 | 4.42 | 0.89 |
| qwen2.5-coder:14b-instruct-q4_K_M                                         |          |   6.68 |     90 |   14.8 |    4 |  128 | 8.65 | 7.28 | 4.62 | 1.13 |
| phi4:14b-q8_0                                                             |          |   6.68 |     45 |   14.7 |    8 |   16 | 10.23 | 5.29 | 4.52 | 0.97 |
| phi4:14b                                                                  |     7.35 |   6.64 |     90 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| phi4:latest                                                               |     7.35 |   6.64 |     90 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| deepseek-coder:33b-instruct-q8_0                                          |          |   6.58 |     20 |   33.0 |    8 |   16 | 8.35 | 10.2 |  0.0 | 1.82 |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M        |          |   6.49 |     18 |   70.6 |    4 |  128 |  9.1 |  5.9 | 4.69 | 1.37 |
| phi4-reasoning:14b-q4_K_M                                                 |     7.35 |   6.36 |     86 |   14.7 |    4 |   32 | 6.73 | 7.73 |  5.2 | 3.05 |
| mistral-large:123b-instruct-2407-q4_K_M                                   |          |   6.34 |     10 |  122.6 |    4 |  128 | 8.27 | 6.61 | 4.44 | 1.61 |
| qwen3:14b-q4_K_M-think                                                    |          |   6.20 |     84 |   14.8 |    4 |      | 7.16 |  7.5 | 4.66 | 1.51 |
| vanilj/Phi-4:Q8_0                                                         |          |   6.13 |     42 |   14.7 |    8 |   16 | 9.06 | 5.73 | 3.52 | 0.84 |
| cogito:70b-v1-preview-llama-q4_K_M                                        |          |   6.05 |     17 |   70.6 |    4 |  128 |  7.7 | 7.26 | 3.54 | 0.86 |
| qwen3:30b-a3b-q4_K_M-think                                                |          |   5.98 |     39 |   30.5 |    4 |      |  8.3 | 5.59 | 4.32 | 1.17 |
| yi-coder:9b-chat-q4_K_M                                                   |     4.40 |   5.97 |    136 |    8.8 |    4 |  128 | 7.44 | 6.04 | 5.76 | 0.34 |
| qwq:32b-preview-q8_0                                                      |          |   5.97 |     18 |   32.8 |    8 |   32 | 10.15 | 3.11 | 3.88 | 1.97 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                                 |          |   5.83 |     17 |   70.6 |    4 |  128 | 8.07 | 6.49 | 2.59 | 1.36 |
| llama3.1:70b-instruct-q8_0                                                |          |   5.81 |      8 |   70.6 |    8 |  128 | 8.19 | 5.36 |  3.8 |  1.7 |
| qwen2.5:14b-instruct-q8_0                                                 |          |   5.75 |     39 |   14.8 |    8 |   32 | 8.59 | 4.14 | 4.55 | 1.61 |
| cogito:14b-v1-preview-qwen-q4_K_M                                         |          |   5.70 |     77 |   14.8 |    4 |  128 |  7.9 | 5.89 | 3.41 | 0.91 |
| qwen2.5:14b-instruct-q4_K_M                                               |          |   5.63 |     76 |   14.8 |    4 |   32 | 8.44 | 5.08 | 3.44 | 0.43 |
| llama3.1:70b-instruct-q4_K_M                                              |          |   5.62 |     16 |   70.6 |    4 |  128 | 8.77 | 4.98 | 2.77 |  0.6 |
| llama3.3:70b-instruct-q4_K_M                                              |          |   5.60 |     16 |   70.6 |    4 |  128 | 7.26 | 5.25 | 4.49 | 2.21 |
| falcon3:10b-instruct-q8_0                                                 |          |   5.48 |     53 |   10.3 |    8 |   32 | 8.15 | 5.14 | 2.71 | 1.39 |
| hf.co/bartowski/smirki_UIGEN-T1.1-Qwen-14B-GGUF:Q4_K_M                    |          |   5.46 |     74 |   14.8 |    4 |   32 | 7.27 |  5.2 | 4.41 | 1.14 |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S                     |          |   5.43 |     14 |   78.0 |    4 |   32 | 7.04 | 6.05 |  3.6 | 0.74 |
| hf.co/Tesslate/Tessa-Rust-T1-7B-Q8_0-GGUF:Q8_0                            |          |   5.37 |     70 |   7.62 |    8 |   32 | 7.04 |  5.0 | 4.84 | 0.86 |
| qwen3:32b-q4_K_M-think                                                    |          |   5.31 |     32 |   32.8 |    4 |      | 5.78 | 6.75 | 4.78 | 0.19 |
| qwen3:8b-q4_K_M-think                                                     |     4.10 |   5.30 |    129 |    8.2 |    4 |      | 5.69 | 6.48 | 4.77 | 1.27 |
| tulu3:70b-q8_0                                                            |          |   5.25 |      7 |   70.6 |    8 |  128 | 7.73 | 4.61 | 3.09 | 1.59 |
| qwen2-math:72b-instruct-q8_0                                              |          |   5.25 |      7 |   72.7 |    8 |    4 | 6.49 | 6.67 | 2.61 |  1.3 |
| tulu3:70b-q4_K_M                                                          |          |   5.21 |     15 |   70.6 |    4 |  128 | 7.31 | 4.68 | 3.35 | 2.15 |
| qwen3:4b-q4_K_M-think                                                     |     2.00 |   5.18 |    259 |    4.0 |    4 |      | 7.89 | 4.61 | 2.73 | 0.91 |
| aravhawk/llama4:scout-q4_K_M                                              |          |   5.17 |     10 |  107.8 |    4 |      | 6.78 | 5.64 | 3.55 | 0.59 |
| hf.co/ozone-ai/0x-lite-Q4_K_M-GGUF:latest                                 |          |   5.14 |     69 |   14.8 |    4 |   32 | 7.66 | 4.52 | 3.32 | 0.56 |
| command-a:111b-03-2025-q4_K_M                                             |          |   5.06 |      9 |  111.1 |    4 |  256 | 6.33 | 5.17 | 4.21 | 1.32 |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                       |          |   4.94 |     67 |   14.8 |    4 |  986 | 7.75 | 4.02 | 2.74 | 0.81 |
| falcon3:10b-instruct-q4_K_M                                               |          |   4.88 |     95 |   10.3 |    4 |   32 | 6.62 | 5.77 | 2.19 |  0.6 |
| nemotron:70b-instruct-q4_K_M                                              |          |   4.78 |     14 |   70.6 |    4 |  128 | 5.78 | 5.13 | 4.22 | 0.83 |
| hf.co/bartowski/mistralai_Mistral-Small-3.1-24B-Instruct-2503-GGUF:Q4_K_M |          |   4.70 |     40 |   23.6 |    4 |  128 | 6.79 | 4.05 | 3.38 | 0.95 |
| qwen2.5-coder:7b-instruct-q8_0                                            |          |   4.69 |     62 |    7.6 |    8 |  128 | 6.37 |  4.4 | 3.78 | 0.63 |
| qwen3:8b-q4_K_M-no_think                                                  |          |   4.68 |    114 |    8.2 |    4 |  128 | 6.98 | 4.84 | 1.92 | 0.51 |
| hf.co/bartowski/Qwen2.5-Math-72B-Instruct-GGUF:Q4_K_M                     |          |   4.59 |     13 |   72.7 |    4 |    4 | 6.67 | 4.53 | 2.39 | 0.89 |
| llama3.2-vision:90b-instruct-q4_K_M                                       |          |   4.50 |     10 |   87.7 |    4 |      | 5.61 | 4.79 | 3.78 | 0.65 |
| nemotron:70b-instruct-q8_0                                                |          |   4.50 |      6 |   70.6 |    8 |  128 | 6.31 | 4.05 | 3.23 | 1.13 |
| qwen2.5:7b-instruct-q8_0                                                  |          |   4.34 |     57 |    7.6 |    8 |  128 | 7.47 |  3.6 | 1.13 | 0.51 |
| falcon3:7b-instruct-q8_0                                                  |          |   4.34 |     58 |    7.5 |    8 |   32 | 6.76 | 3.91 | 2.16 | 0.36 |
| hf.co/Tesslate/UIGEN-T2-7B-Q8_0-GGUF:Q8_0                                 |          |   4.34 |     57 |   7.62 |    8 |   32 | 5.73 | 3.99 | 3.99 | 0.52 |
| hf.co/mradermacher/Viper-Coder-Hybrid-v1.3-GGUF:Q4_K_M                    |          |   4.32 |     58 |   14.8 |    4 |  128 | 6.44 | 4.45 | 1.83 | 0.46 |
| hf.co/smirki/UIGEN-T1.1-Qwen-7B-Q4_K_M-GGUF:latest                        |          |   4.29 |    113 |   7.62 |    4 |   32 | 6.06 | 4.53 | 2.08 | 0.88 |
| qwen2.5:7b-instruct-q4_K_M                                                |          |   4.22 |    111 |    7.6 |    4 |  128 |  7.5 | 2.67 | 1.86 | 0.49 |
| mistral-small3.1:24b-instruct-2503-q4_K_M                                 |          |   4.15 |     35 |   24.0 |    4 |  128 | 5.31 | 4.38 | 3.07 |  1.0 |
| hf.co/Tesslate/Synthia-S1-27b-Q4_K_M-GGUF:Q4_K_M                          |          |   4.07 |     30 |   27.0 |    4 |  128 | 6.78 | 2.21 | 3.19 | 0.53 |
| hf.co/mradermacher/Sky-T1-mini-GGUF:Q4_K_M                                |          |   4.01 |    105 |   7.62 |    4 |  128 | 7.05 | 3.68 | 0.15 | 0.55 |
| mistral-small:24b-instruct-2501-q4_K_M                                    |          |   3.98 |     34 |   23.6 |    4 |   32 | 6.32 | 2.89 | 2.47 | 0.93 |
| qwen2.5-coder:7b-instruct-q4_K_M                                          |          |   3.98 |    105 |    7.6 |    4 |   32 | 4.76 |  4.7 | 2.87 | 0.87 |
| hf.co/bartowski/Tesslate_Tessa-Rust-T1-7B-GGUF:Q4_K_M                     |          |   3.94 |    104 |   7.62 |    4 |   32 | 6.14 |  3.2 | 2.28 | 0.73 |
| hf.co/bartowski/open-thoughts_OpenThinker-32B-GGUF:Q4_K_M                 |          |   3.90 |     24 |   32.8 |    4 |   32 |  4.2 | 4.22 | 3.28 | 2.95 |
| phi4-reasoning:14b-plus-q4_K_M                                            |          |   3.74 |     51 |   14.7 |    4 |   32 | 5.67 | 2.48 |  2.3 | 2.71 |
| gemma3:27b                                                                |          |   3.73 |     27 |   27.4 |    4 |  128 | 7.15 | 0.14 |  3.8 | 0.64 |
| hf.co/bartowski/HelpingAI_Helpingai3-raw-GGUF:Q4_K_M                      |          |   3.70 |     72 |   10.3 |    4 |   32 | 5.88 | 3.82 | 0.92 | 0.13 |
| qwen3:4b-q4_K_M-no_think                                                  |     2.00 |   3.67 |    184 |    4.0 |    4 |   32 | 5.44 | 3.72 | 1.71 | 0.38 |
| gemma2:27b-instruct-q8_0                                                  |          |   3.65 |     13 |   27.2 |    8 |    8 | 5.18 |  3.3 | 2.47 | 0.98 |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                                    |          |   3.58 |     10 |   70.6 |    4 |    8 | 6.98 | 1.99 | 0.76 | 0.36 |
| hf.co/mradermacher/Viper-Coder-HybridMini-v1.3-GGUF:Q4_K_M                |          |   3.55 |     93 |   7.62 |    4 |   32 | 5.18 | 3.51 | 1.99 | 0.24 |
| deepseek-coder:6.7b-instruct-q8_0                                         |          |   3.52 |     50 |    7.0 |    8 |   16 | 5.37 | 3.68 | 0.94 | 0.79 |
| hf.co/mradermacher/HelpingAI-3-GGUF:Q4_K_M                                |          |   3.38 |     66 |   10.3 |    4 |   32 |  5.8 | 2.82 | 1.09 |  0.0 |
| hf.co/katanemo/Arch-Function-7B.gguf:Q4_K_M                               |          |   3.34 |     88 |   7.62 |    4 |   32 | 4.63 | 3.99 | 1.17 | 0.61 |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                                  |          |   3.34 |     38 |   8.83 |    8 |    4 | 6.54 | 2.11 |  0.4 | 0.09 |
| hf.co/lmstudio-community/Mistral-Small-24B-Instruct-2501-GGUF:Q4_K_M      |          |   3.33 |     28 |   23.6 |    4 |   32 | 5.21 | 2.86 | 1.54 | 0.79 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                          |          |   3.30 |     75 |    8.8 |    4 |   32 | 4.92 | 3.64 | 1.18 | 0.06 |
| opencoder:8b-instruct-q8_0                                                |          |   3.21 |     41 |    7.8 |    8 |    8 | 4.63 | 3.22 | 1.62 | 0.72 |
| hf.co/mradermacher/Bespoke-Stratos-7B-GGUF:Q4_K_M                         |          |   3.16 |     83 |   7.62 |    4 |   32 | 4.72 | 2.67 | 2.26 | 0.23 |
| hf.co/bartowski/simplescaling_s1-32B-GGUF:Q4_K_M                          |          |   3.11 |     19 |   32.8 |    4 |   32 | 4.33 | 2.29 | 2.78 |  1.4 |
| gemma3:12b                                                                |          |   3.11 |     51 |   12.2 |    4 |  128 | 5.31 |  0.9 |  3.3 |  0.6 |
| hf.co/bartowski/THUDM_GLM-4-9B-0414-GGUF:Q4_K_M                           |          |   3.11 |     66 |    9.4 |    4 |   32 | 4.87 |  3.0 | 1.18 | 0.23 |
| qwen2.5-coder:3b-instruct-q4_K_M                                          |     1.55 |   3.05 |    197 |    3.1 |    4 |   32 | 4.98 | 2.51 | 1.53 | 0.03 |
| exaone3.5:32b-instruct-q8_0                                               |          |   3.05 |     10 |   32.0 |    8 |   32 | 3.96 | 3.82 | 1.38 | 0.47 |
| deepseek-r1:32b-qwen-distill-q4_K_M                                       |          |   3.00 |     18 |   32.8 |    4 |  128 | 4.51 | 2.91 | 1.44 | 0.32 |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                        |          |   2.97 |     78 |   7.62 |    4 |  128 | 6.55 |  0.0 | 1.63 | 0.24 |
| hf.co/bartowski/google_gemma-3-27b-it-qat-GGUF:Q4_0                       |          |   2.93 |     22 |   27.0 |    4 |  128 | 5.12 | 0.25 | 3.96 | 0.16 |
| hf.co/bartowski/all-hands_openhands-lm-32b-v0.1-GGUF:Q4_K_M               |          |   2.72 |     17 |   32.8 |    4 |  128 | 3.28 | 4.55 | 0.14 |  0.2 |
| yi:34b-chat-v1.5-q4_K_M                                                   |          |   2.63 |     15 |   34.0 |    4 |    4 | 4.25 | 2.63 | 0.58 | 0.24 |
| qwen2.5-coder:3b-instruct-q8_0                                            |          |   2.62 |     85 |    3.1 |    8 |   32 |  4.2 | 2.15 |  1.4 |  0.2 |
| hf.co/bartowski/google_gemma-3-12b-it-qat-GGUF:Q4_0                       |          |   2.55 |     43 |   11.8 |    4 |  128 | 4.64 | 0.68 | 2.42 | 0.08 |
| yi:9b-chat-v1.5-q4_K_M                                                    |          |   2.54 |     56 |    9.0 |    4 |    4 | 4.04 | 2.71 | 0.39 | 0.33 |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                                 |          |   2.45 |      7 |   34.4 |    8 |    4 | 4.61 | 1.49 | 0.72 | 0.16 |
| exaone3.5:7.8b-instruct-q8_0                                              |          |   2.28 |     29 |    7.8 |    8 |   32 | 3.76 | 2.26 | 0.17 | 0.68 |
| qwen3:235b-a22b-q4_K_M-think                                              |          |   2.28 |      2 |  235.1 |    4 |  128 | 2.86 | 2.27 | 2.17 | 0.25 |
| qwen:110b-chat-v1.5-q4_K_M                                                |          |   2.25 |      4 |  111.0 |    4 |   32 | 3.63 | 1.84 | 0.76 | 0.92 |
| phi3:14b-medium-128k-instruct-q8_0                                        |          |   2.24 |     16 |   14.0 |    8 |  128 | 4.21 | 1.55 | 0.42 | 0.04 |
| hf.co/bartowski/THUDM_GLM-Z1-32B-0414-GGUF:Q4_K_M                         |          |   2.24 |     14 |   32.6 |    4 |   32 | 3.13 | 1.58 |  2.0 |  1.1 |
| llama3.1:8b-instruct-q8_0                                                 |          |   2.03 |     25 |    8.0 |    8 |  128 | 3.26 | 1.78 | 0.94 | 0.09 |
| qwq:32b-q4_K_M                                                            |          |   2.02 |     12 |   32.8 |    4 |  128 | 2.51 | 1.75 | 1.32 | 2.25 |
| tulu3:8b-q8_0                                                             |          |   2.01 |     25 |    8.0 |    8 |  128 | 3.91 | 1.06 | 0.42 | 0.49 |
| qwen3:1.7b-q4_K_M-think                                                   |     1.00 |   1.97 |    197 |    2.0 |    4 |   32 | 3.97 | 0.94 | 0.48 | 0.04 |
| hf.co/bartowski/open-r1_OlympicCoder-7B-GGUF:Q4_K_M                       |          |   1.93 |     55 |    7.0 |    4 |   32 | 2.43 | 2.86 | 0.31 | 0.33 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                                  |          |   1.87 |     31 |   6.06 |    8 |    4 | 3.92 | 0.92 | 0.13 |  0.0 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                                |          |   1.81 |     60 |   6.06 |    4 |    4 | 3.71 | 0.87 | 0.32 |  0.0 |
| deepseek-llm:67b-chat-q4_K_M                                              |          |   1.79 |      5 |   67.0 |    4 |    4 | 2.94 | 1.63 |  0.5 | 0.23 |
| hf.co/katanemo/Arch-Function-3B.gguf:Q4_K_M                               |          |   1.76 |    114 |   3.09 |    4 |   32 | 2.81 | 1.55 | 0.66 | 0.43 |
| qwen2.5:3b-instruct-q4_K_M                                                |          |   1.70 |    110 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.56 | 0.05 |
| deepseek-r1:70b-llama-distill-q4_K_M                                      |          |   1.69 |      5 |   70.6 |    4 |  128 | 2.17 | 2.49 | 0.19 | 0.41 |
| deepseek-r1:14b-qwen-distill-q4_K_M                                       |          |   1.69 |     23 |   14.8 |    4 |  128 |  2.6 | 1.02 | 1.19 | 1.04 |
| qwen2.5:3b                                                                |          |   1.67 |    108 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.42 | 0.05 |
| llama3.2-vision:11b-instruct-q4_K_M                                       |          |   1.67 |     34 |    9.8 |    4 |      | 3.13 | 1.21 | 0.21 | 0.11 |
| yi-coder:1.5b-chat-q4_K_M                                                 |     0.75 |   1.65 |    220 |    1.5 |    4 |  128 | 3.49 | 0.61 | 0.34 |  0.0 |
| gemma2:9b-instruct-q8_0                                                   |          |   1.63 |     18 |    9.2 |    8 |    8 | 2.46 | 1.55 | 0.86 | 0.12 |
| granite3.1-dense:8b-instruct-q8_0                                         |          |   1.59 |     19 |    8.2 |    8 |  128 | 2.73 | 1.55 | 0.16 | 0.03 |
| hf.co/katanemo/Arch-Function-1.5B.gguf:Q4_K_M                             |          |   1.56 |    203 |   1.54 |    4 |   32 | 2.44 |  1.6 | 0.53 | 0.02 |
| granite3.2:8b-instruct-q4_K_M                                             |          |   1.50 |     37 |    8.2 |    4 |  128 | 2.53 | 1.43 |  0.3 |  0.0 |
| codegemma:7b-instruct-v1.1-q4_K_M                                         |          |   1.46 |     33 |    9.0 |    4 |    8 | 2.21 | 1.49 | 0.66 | 0.01 |
| exaone3.5:2.4b-instruct-q8_0                                              |          |   1.45 |     54 |    2.7 |    8 |   32 | 2.73 | 0.94 | 0.28 | 0.15 |
| deepseek-r1:7b-qwen-distill-q4_K_M                                        |          |   1.43 |     38 |    7.6 |    4 |  128 | 2.64 |  1.1 |  0.0 | 0.46 |
| qwen2.5:3b-instruct-q8_0                                                  |          |   1.43 |     46 |    3.1 |    8 |  128 | 2.87 | 0.59 | 0.44 | 0.18 |
| opencoder:1.5b-instruct-q8_0                                              |          |   1.42 |     75 |    1.9 |    8 |    4 |  2.2 | 1.47 |  0.5 |  0.0 |
| yi-coder:1.5b-chat-q8_0                                                   |          |   1.36 |     91 |    1.5 |    8 |  128 | 2.32 | 1.17 | 0.42 |  0.0 |
| cogito:8b-v1-preview-llama-q4_K_M                                         |          |   1.34 |     34 |      8 |    4 |  128 | 2.32 | 1.02 | 0.54 |  0.0 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                        |     0.75 |   1.31 |    174 |    1.5 |    4 |   32 | 2.26 |  0.8 |  0.8 | 0.03 |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                         |          |   1.30 |      6 |   46.7 |    4 |   32 |  2.0 | 1.24 | 0.62 |  0.0 |
| qwen2-math:7b-instruct-q8_0                                               |          |   1.28 |     17 |    7.6 |    8 |    4 | 2.49 | 0.95 | 0.02 |  0.0 |
| dolphin3:8b-llama3.1-q8_0                                                 |          |   1.27 |     16 |    8.0 |    8 |  128 |  2.3 | 0.89 | 0.26 | 0.31 |
| qwen2.5-coder:1.5b-instruct-q8_0                                          |          |   1.22 |     81 |    1.5 |    8 |   32 | 2.04 |  0.9 | 0.66 | 0.03 |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0           |          |   1.21 |     15 |   8.03 |    8 |  128 | 2.29 | 0.47 | 0.58 | 0.37 |
| codegemma:7b-instruct-q8_0                                                |          |   1.19 |     13 |    9.0 |    8 |    8 | 1.84 | 1.27 | 0.39 |  0.0 |
| gemma3:4b                                                                 |          |   1.17 |     55 |    4.3 |    4 |  128 | 2.09 | 0.61 | 0.77 |  0.0 |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                          |          |   1.16 |     15 |    8.0 |    8 |    8 | 1.51 | 1.65 |  0.3 | 0.03 |
| hf.co/mradermacher/HelpingAI-15B-GGUF:Q4_K_M                              |          |   1.16 |     15 |   15.3 |    4 |    4 | 2.42 | 0.64 |  0.0 |  0.0 |
| falcon3:3b-instruct-q8_0                                                  |          |   1.16 |     36 |    3.2 |    8 |   32 | 1.89 | 1.09 | 0.36 | 0.04 |
| qwen2.5:1.5b-instruct-q8_0                                                |          |   1.14 |     76 |    1.5 |    8 |  128 | 2.07 | 0.82 | 0.29 | 0.06 |
| deepseek-r1:8b-llama-distill-q4_K_M                                       |          |   1.12 |     28 |    8.0 |    4 |  128 | 1.46 | 1.25 | 0.45 | 0.67 |
| hf.co/bartowski/THUDM_GLM-Z1-9B-0414-GGUF:Q4_K_M                          |          |   1.08 |     23 |    9.4 |    4 |   32 | 0.99 | 1.74 | 0.57 | 0.51 |
| granite3.3:2b                                                             |          |   1.04 |    104 |    2.0 |    4 |  128 | 2.19 | 0.54 | 0.02 |  0.0 |
| openchat:7b-v3.5-q8_0                                                     |          |   1.02 |     15 |    7.0 |    8 |    8 | 1.62 | 1.21 | 0.06 |  0.0 |
| hf.co/bartowski/Zyphra_ZR1-1.5B-GGUF:Q4_K_M                               |     0.75 |   1.02 |    136 |    1.5 |    4 |  128 | 1.64 | 0.34 | 1.04 | 0.51 |
| granite3.3:8b                                                             |          |   0.98 |     24 |    8.0 |    4 |  128 | 1.67 | 0.78 | 0.25 | 0.27 |
| codellama:34b-instruct-q4_K_M                                             |          |   0.93 |      5 |   34.0 |    4 |   16 | 1.29 | 0.99 | 0.56 | 0.04 |
| exaone-deep:7.8b-q4_K_M                                                   |          |   0.90 |     23 |    7.8 |    4 |   32 | 1.83 |  0.4 | 0.24 |  0.0 |
| qwen:32b-chat-v1.5-q4_K_M                                                 |          |   0.90 |      5 |   33.0 |    4 |   32 | 1.54 | 0.81 | 0.13 | 0.12 |
| yi:6b-chat-v1.5-q4_K_M                                                    |          |   0.89 |     30 |    6.0 |    4 |    4 | 0.79 | 1.48 | 0.62 | 0.01 |
| qwen2.5:1.5b-instruct-q4_K_M                                              |     0.75 |   0.88 |    118 |    1.5 |    4 |  128 | 1.94 | 0.26 | 0.15 |  0.0 |
| hf.co/bartowski/open-r1_OlympicCoder-32B-GGUF:Q4_K_M                      |          |   0.88 |      5 |   32.8 |    4 |   32 | 1.54 | 0.32 | 0.58 | 0.53 |
| deepcoder:1.5b-preview-q4_K_M                                             |     0.75 |   0.82 |    110 |    1.5 |    4 |  128 | 1.93 | 0.15 |  0.0 | 0.08 |
| mixtral:8x7b-instruct-v0.1-q8_0                                           |          |   0.82 |      2 |   46.7 |    8 |   32 | 1.44 | 0.65 | 0.23 |  0.0 |
| hf.co/bartowski/google_gemma-3-4b-it-qat-GGUF:Q4_0                        |          |   0.81 |     42 |   3.88 |    4 |  128 | 1.74 | 0.35 | 0.03 | 0.03 |
| hf.co/mradermacher/HelpingAI-9B-GGUF:Q4_K_M                               |          |   0.78 |     18 |   8.83 |    4 |    4 | 1.64 | 0.41 |  0.0 |  0.0 |
| qwen3:1.7b-q4_K_M-no_think                                                |          |   0.77 |     76 |    2.0 |    4 |   32 | 1.08 | 0.99 | 0.18 |  0.0 |
| hf.co/bartowski/OpenThinker-7B-GGUF:Q4_K_M                                |          |   0.75 |     20 |   7.62 |    4 |   32 | 0.88 | 0.77 | 0.53 | 0.62 |
| exaone-deep:32b-q4_K_M                                                    |          |   0.70 |      4 |   32.0 |    4 |   32 | 0.93 | 0.66 | 0.36 | 0.53 |
| command-r7b:7b-12-2024-q4_K_M                                             |          |   0.68 |     17 |    8.0 |    4 |  128 | 1.54 | 0.03 | 0.26 | 0.04 |
| llama3.2:3b                                                               |          |   0.66 |     41 |    3.2 |    4 |  128 | 1.42 | 0.18 | 0.21 |  0.0 |
| olmo2:13b-1124-instruct-q4_K_M                                            |          |   0.66 |     10 |   13.7 |    4 |    4 | 1.59 | 0.06 | 0.01 | 0.03 |
| internlm2:7b-chat-v2.5-q4_K_M                                             |          |   0.66 |     17 |    7.7 |    4 |   32 |  1.1 | 0.41 | 0.47 |  0.0 |
| hf.co/bartowski/agentica-org_DeepScaleR-1.5B-Preview-GGUF:Q4_K_M          |          |   0.64 |     72 |   1.78 |    4 |  128 | 1.28 |  0.4 | 0.03 | 0.05 |
| qwen:72b-chat-v1.5-q4_K_M                                                 |          |   0.64 |      2 |   72.0 |    4 |   32 | 0.94 | 0.78 | 0.13 |  0.0 |
| olmo2:7b-1124-instruct-q4_K_M                                             |          |   0.60 |     16 |    7.3 |    4 |    4 | 1.42 | 0.08 | 0.02 |  0.0 |
| qwen2.5:0.5b-instruct-q8_0                                                |     0.50 |   0.57 |    115 |    0.5 |    8 |  128 | 1.33 |  0.0 | 0.21 |  0.0 |
| deepcoder:14b-preview-q4_K_M                                              |          |   0.57 |      8 |   14.8 |    4 |  128 | 1.03 | 0.33 | 0.28 |  0.0 |
| internlm2:1.8b-chat-v2.5-q4_K_M                                           |          |   0.51 |     54 |    1.9 |    4 |   32 | 1.24 | 0.06 |  0.0 |  0.0 |
| granite3.1-dense:2b-instruct-q8_0                                         |          |   0.50 |     20 |    2.5 |    8 |  128 | 1.07 | 0.11 |  0.2 |  0.0 |
| llama3.2:latest                                                           |          |   0.49 |     31 |   3.21 |    4 |  128 | 0.99 | 0.18 | 0.21 |  0.0 |
| exaone-deep:2.4b-q4_K_M                                                   |          |   0.48 |     36 |    2.7 |    4 |   32 | 0.88 | 0.32 | 0.04 | 0.28 |
| codellama:13b-instruct-q4_K_M                                             |          |   0.48 |      7 |   13.0 |    4 |   16 | 0.52 | 0.84 | 0.05 | 0.08 |
| hf.co/trillionlabs/Trillion-7B-preview-GGUF:Q4_K_M                        |          |   0.47 |     13 |   7.53 |    4 |    4 | 0.98 | 0.09 | 0.21 | 0.11 |
| smallthinker:3b-preview-q4_K_M                                            |          |   0.47 |     27 |    3.4 |    4 |  128 | 0.98 | 0.25 |  0.0 |  0.0 |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                                      |          |   0.46 |     51 |    1.8 |    4 |  128 | 0.87 | 0.24 | 0.03 | 0.37 |
| cogito:3b-v1-preview-llama-q4_K_M                                         |          |   0.46 |     29 |   3.21 |    4 |      | 0.94 | 0.25 | 0.04 | 0.03 |
| hf.co/TheBloke/Yi-34B-Chat-GGUF:Q4_K_M                                    |          |   0.44 |      3 |   34.4 |    4 |    4 | 0.67 | 0.56 | 0.03 |  0.0 |
| granite3.2:2b-instruct-q4_K_M                                             |          |   0.42 |     34 |    2.5 |    4 |  128 | 0.85 | 0.16 | 0.15 | 0.05 |
| mistral:7b-instruct-q4_K_M                                                |          |   0.41 |     12 |    7.0 |    4 |   32 | 0.48 | 0.71 | 0.04 |  0.0 |
| smallthinker:3b-preview-q8_0                                              |          |   0.41 |     12 |    3.4 |    8 |  128 | 0.81 | 0.19 | 0.03 | 0.19 |
| phi:2.7b-chat-v2-q4_K_M                                                   |          |   0.39 |     26 |    3.0 |    4 |    2 | 0.91 | 0.07 |  0.0 |  0.0 |
| vicuna:33b-q4_K_M                                                         |          |   0.38 |      3 |   30.0 |    4 |    2 |  0.9 | 0.06 |  0.0 |  0.0 |
| granite3.1-moe:3b-instruct-q8_0                                           |          |   0.35 |     11 |    3.3 |    8 |  128 |  0.8 | 0.03 | 0.11 | 0.03 |
| qwen3:0.6b-q4_K_M-think                                                   |          |   0.28 |      0 | 751.63 |    4 |   32 | 0.53 |  0.0 | 0.36 |  0.0 |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                                 |          |   0.27 |      4 |   7.62 |    8 |  128 | 0.27 | 0.54 |  0.0 |  0.0 |
| qwen2-math:1.5b-instruct-q8_0                                             |          |   0.27 |     18 |    1.5 |    8 |    4 | 0.65 | 0.03 |  0.0 |  0.0 |
| gemma2:2b-instruct-q8_0                                                   |          |   0.23 |      9 |    2.6 |    8 |    8 | 0.39 | 0.22 | 0.03 |  0.0 |
| qwen3:0.6b-q4_K_M-no_think                                                |          |   0.22 |      0 | 751.63 |    4 |   32 | 0.48 |  0.1 |  0.0 |  0.0 |
| codellama:7b-instruct-q4_K_M                                              |          |   0.21 |      6 |    7.0 |    4 |   16 | 0.33 | 0.03 | 0.33 | 0.01 |
| deepseek-llm:7b-chat-q8_0                                                 |          |   0.20 |      3 |    7.0 |    8 |    4 | 0.46 | 0.06 |  0.0 |  0.0 |
| hf.co/QuantFactory/HelpingAI-3B-coder-GGUF:Q4_K_M                         |          |   0.20 |     11 |   3.48 |    4 |  128 | 0.31 | 0.22 |  0.0 |  0.1 |
| llama3.2:1b                                                               |          |   0.18 |     15 |    1.2 |    8 |      | 0.41 | 0.06 |  0.0 |  0.0 |
| phi3:3.8b                                                                 |          |   0.17 |      9 |    3.8 |    4 |      | 0.39 | 0.04 | 0.03 |  0.0 |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                         |          |   0.16 |      0 |   72.7 |    4 |   32 | 0.31 |  0.0 | 0.08 | 0.16 |
| gemma3:1b                                                                 |     0.50 |   0.15 |     30 |    1.0 |    4 |   32 | 0.13 | 0.33 |  0.0 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                        |     0.25 |   0.15 |     60 |    0.5 |    4 |   32 | 0.36 | 0.01 | 0.01 |  0.0 |
| qwen2.5:0.5b-instruct-q4_K_M                                              |     0.25 |   0.15 |     58 |    0.5 |    4 |  128 | 0.36 |  0.0 | 0.01 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q8_0                                          |          |   0.14 |     28 |    0.5 |    8 |   32 | 0.33 | 0.01 | 0.03 |  0.0 |
| llama2:70b-chat-q4_K_M                                                    |          |   0.14 |      0 |   69.0 |    4 |    4 | 0.31 | 0.03 | 0.01 | 0.03 |
| llama3.2:1b-instruct-q8_0                                                 |          |   0.13 |     11 |    1.2 |    8 |  128 | 0.28 | 0.06 |  0.0 |  0.0 |
| hf.co/bartowski/google_gemma-3-1b-it-qat-GGUF:Q4_0                        |          |   0.12 |     25 |    1.0 |    4 |   32 | 0.29 | 0.03 |  0.0 |  0.0 |
| falcon:7b-instruct-q4_0                                                   |          |   0.11 |      3 |    7.0 |    4 |    2 | 0.28 |  0.0 |  0.0 |  0.0 |
| falcon:40b-instruct-q4_0                                                  |          |   0.11 |      1 |   40.0 |    4 |    2 | 0.07 |  0.0 | 0.42 |  0.0 |
| phi4-mini:3.8b-q4_K_M                                                     |          |   0.11 |      6 |    3.8 |    4 |  128 | 0.23 | 0.04 | 0.01 |  0.0 |
| falcon3:1b-instruct-q8_0                                                  |          |   0.10 |      6 |    1.7 |    8 |    8 | 0.25 |  0.0 |  0.0 |  0.0 |
| granite3.1-moe:1b-instruct-q8_0                                           |          |   0.10 |      7 |    1.3 |    8 |  128 | 0.24 |  0.0 |  0.0 |  0.0 |
| qwen:14b-chat-v1.5-q4_K_M                                                 |          |   0.08 |      1 |   14.0 |    4 |   32 | 0.15 |  0.0 | 0.08 |  0.0 |
| hf.co/bartowski/burtenshaw_GemmaCoder3-12B-GGUF:Q4_K_M                    |          |   0.06 |      1 |   11.8 |    4 |  128 | 0.04 | 0.14 | 0.03 |  0.0 |
| qwen:1.8b-chat-v1.5-q4_K_M                                                |          |   0.06 |      6 |    2.0 |    4 |   32 |  0.0 |  0.0 |  0.0 | 0.62 |
| vicuna:13b-q4_K_M                                                         |          |   0.04 |      1 |   13.0 |    4 |    2 | 0.09 | 0.01 |  0.0 |  0.0 |
| granite3.2-vision:2b-q4_K_M                                               |          |   0.04 |      3 |    2.5 |    4 |   16 | 0.07 | 0.03 |  0.0 |  0.0 |
| vicuna:13b-v1.5-16k-q4_K_M                                                |          |   0.03 |      1 |   13.0 |    4 |    2 | 0.06 | 0.03 |  0.0 |  0.0 |
| qwen2:0.5b-instruct-q8_0                                                  |          |   0.03 |      0 | 494.03 |    8 |   32 | 0.07 |  0.0 |  0.0 |  0.0 |
| starcoder2:3b                                                             |          |   0.03 |      2 |    3.0 |    4 |   16 | 0.07 |  0.0 |  0.0 |  0.0 |
| llama2:13b-chat-q4_K_M                                                    |          |   0.03 |      0 |   13.0 |    4 |    4 | 0.06 | 0.01 |  0.0 |  0.0 |
| vicuna:7b-v1.5-16k-q4_K_M                                                 |          |   0.01 |      0 |    7.0 |    4 |    4 | 0.03 |  0.0 |  0.0 |  0.0 |
| qwen:7b-chat-v1.5-q4_K_M                                                  |          |   0.01 |      0 |    8.0 |    4 |   32 | 0.02 |  0.0 |  0.0 | 0.03 |
| deepseek-coder:1.3b-instruct-q8_0                                         |          |   0.01 |      1 |    1.0 |    8 |   16 |  0.0 | 0.02 |  0.0 |  0.0 |
| llama2:7b-chat-q4_K_M                                                     |          |   0.00 |      0 |    7.0 |    4 |    4 | 0.01 |  0.0 |  0.0 |  0.0 |
| smollm:1.7b-instruct-v0.2-q8_0                                            |          |   0.00 |      0 |    1.7 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                            |     0.14 |   0.00 |      0 |  0.135 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:360m-instruct-v0.2-q8_0                                            |          |   0.00 |      0 |   0.36 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:0.5b-chat-v1.5-q4_K_M                                                |          |   0.00 |      0 |  620.0 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:4b-chat-v1.5-q4_K_M                                                  |          |   0.00 |      0 |    4.0 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| codegemma:2b-code-v1.1-q4_K_M                                             |          |   0.00 |      0 |    3.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |
| vicuna:7b-q4_K_M                                                          |          |   0.00 |      0 |    7.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |
| phi4-mini-reasoning:3.8b-q4_K_M                                           |          |   0.00 |      0 |    3.8 |    4 |  128 |  0.0 |  0.0 |  0.0 |  0.0 |

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
