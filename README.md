# Project Euler LLM Benchmark

To identify the performance of Large Language Models to solve problems with domain-specific knowledge (here: programming)
we created a benchmark using the Project Euler series of challenging mathematical/computer programming problems.
Because we want to apply LLMs for coding with specific programming languages, we also want to measure how good
a LLM is at coding with that given programming language.

![Benchmark Results](benchmark.png)

## Super-Human Performance
AI systems have achieved domain-specific super-human performance. In 1997, IBM’s “Deep Blue” defeated world chess champion Garry Kasparov, marking the first time a machine outperformed the best human player. Since then, AI has surpassed human ability in many games, including Go, where AlphaGo triumphed in 2016.

While Deep Blue was “super-human” because it exceeded the best human, our goal is to define super-human performance relative to the average human score in the Project Euler test. This allows us to express an AI’s performance as a multiplier of human ability.

With the Project Euler LLM Benchmark, we aim to quantify how strongly LLMs demonstrate super-human capabilities in the domain of programming. See the Motivation chapter below for details on our measurement approach.

## Results for PE-Bench-200
The computed Benchmark ("PE-Bench-Python-200", "PE-Bench-Java-200", "PE-Bench-Rust-200", "PE-Bench-Clojure-200")  is the super-human performance factor to code in Python/Java/Rust/Clojure.
The "Economic Score" is the average performance per bytes of model size (times 100). Results are:

| Model                                                                                    | Best<br/>Model<br/>for<br/>Size (GB) | PE-200-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | Java | Rust | Clojure |
| :--------------------------------------------------------------------------------------- | -----------------------------------: | ----------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---: | ---: | ------: |
| qwen3:30b-a3b-thinking-2507-q4_K_M                                                       |    15.25 |  44.59 |    292 |   30.5 |    4 |      | 47.67 | 56.83 | 31.3 | 22.16 |
| mlx-community/Qwen3-Next-80B-A3B-Instruct-4bit                                           |          |  37.92 |     95 |   79.7 |    4 |  256 | 42.87 | 42.04 | 32.92 | 15.71 |
| qwen3-vl:235b-a22b-instruct-q4_K_M                                                       |          |  37.08 |     31 |  235.7 |    4 |  256 | 36.44 | 47.94 | 34.77 | 11.66 |
| qwen3:235b-a22b-instruct-2507-q4_K_M                                                     |          |  36.33 |     31 |  235.1 |    4 |  256 | 43.09 | 41.18 | 28.46 | 10.53 |
| hf.co/janhq/Jan-v1-4B-GGUF:Q4_K_M                                                        |     2.01 |  21.01 |   1045 |   4.02 |    4 |      | 31.03 | 21.99 | 8.96 |  2.1 |
| qwen3-vl:32b-instruct-q4_K_M                                                             |          |  20.56 |    123 |   33.4 |    4 |      | 27.78 | 21.15 | 13.91 | 3.19 |
| hf.co/janhq/Jan-v1-2509-gguf:Q4_K_M                                                      |     2.01 |  20.02 |    996 |   4.02 |    4 |      | 29.27 | 23.63 | 5.84 |  0.6 |
| hf.co/bartowski/cerebras_GLM-4.5-Air-REAP-82B-A12B-GGUF:Q4_0                             |          |  19.39 |     46 |   85.0 |    4 |      | 23.88 | 19.77 | 15.73 | 7.57 |
| qwen3-vl:30b-a3b-instruct-q8_0                                                           |          |  17.61 |     57 |   31.1 |    8 |      | 18.64 | 20.51 | 18.53 | 2.98 |
| qwen3-vl:30b-a3b-instruct-q4_K_M                                                         |          |  17.33 |    111 |   31.1 |    4 |  128 | 18.95 | 21.38 | 16.01 | 1.38 |
| qwen3:30b-a3b-instruct-2507-q4_K_M                                                       |          |  17.31 |    114 |   30.5 |    4 |  256 | 16.93 | 23.76 | 16.1 | 1.89 |
| hf.co/mradermacher/apollo-astralis-4b-GGUF:Q4_K_M                                        |     2.01 |  17.16 |    854 |   4.02 |    4 |      | 24.22 | 19.35 | 6.47 | 3.75 |
| qwen3-vl:8b-thinking-q4_K_M                                                              |          |  15.69 |    357 |    8.8 |    4 |      | 17.68 | 17.45 | 14.18 | 5.49 |
| qwen/qwen3-vl-30b                                                                        |          |  15.45 |     99 |   31.1 |    4 |  128 | 18.98 | 19.02 | 9.83 | 1.88 |
| qwen3:4b-thinking-2507-q4_K_M                                                            |     2.00 |  15.30 |    765 |    4.0 |    4 |      | 20.88 | 16.63 | 7.49 | 4.63 |
| qwen3-coder:30b-a3b-q4_K_M                                                               |          |  15.18 |    100 |   30.5 |    4 |  256 | 19.51 | 13.41 | 14.03 | 5.46 |
| hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M                                   |          |  14.72 |     97 |   30.5 |    4 |      | 20.06 | 11.05 | 14.18 | 5.42 |
| qwen3-vl:4b-thinking-q4_K_M                                                              |          |  13.59 |    618 |    4.4 |    4 |      | 17.87 | 13.81 | 8.84 | 5.31 |
| qwen3:30b-a3b-q4_K_M-no_think                                                            |          |  13.00 |     85 |   30.5 |    4 |   40 | 14.5 | 15.85 | 10.06 | 4.36 |
| qwen2.5vl:32b-q4_K_M                                                                     |          |  12.51 |     75 |   33.5 |    4 |  128 | 15.56 | 11.71 | 13.44 | 0.82 |
| hf.co/bartowski/AGI-0_Art-0-8B-GGUF:Q4_K_M                                               |          |  11.90 |    291 |   8.19 |    4 |   40 | 13.08 | 15.02 | 9.78 | 2.08 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                                           |          |  10.10 |     62 |   32.8 |    4 |   32 | 10.02 | 15.13 | 6.72 | 2.06 |
| qwen2.5-coder:32b-instruct-q4_K_M                                                        |          |   9.28 |     57 |   32.8 |    4 |   32 | 11.6 | 11.5 | 4.69 | 2.53 |
| qwen2.5vl:72b-q4_K_M                                                                     |          |   9.03 |     25 |   73.4 |    4 |  128 | 10.11 | 10.98 | 7.64 | 1.67 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                                              |          |   8.72 |     24 |   72.7 |    4 |  128 | 11.13 | 10.62 | 5.03 | 0.77 |
| hf.co/bartowski/internlm_JanusCoder-14B-GGUF:Q4_K_M                                      |          |   8.64 |    117 |   14.8 |    4 |      | 11.89 | 6.45 | 9.47 | 0.58 |
| qwen2.5:72b-instruct-q4_K_M                                                              |          |   8.47 |     23 |   72.7 |    4 |  128 | 11.5 | 8.83 | 5.27 | 1.69 |
| qwen3:4b-instruct-2507-q4_K_M                                                            |     2.00 |   7.70 |    385 |    4.0 |    4 |  256 | 10.14 | 6.54 | 7.88 |  1.1 |
| qwen3-vl:8b-instruct-q4_K_M                                                              |          |   7.38 |    168 |    8.8 |    4 |      | 8.39 | 7.02 | 9.34 | 0.46 |
| qwen3:14b-q4_K_M-no_think                                                                |          |   7.31 |     99 |   14.8 |    4 |   40 | 8.19 | 10.15 | 4.16 |  1.6 |
| qwen3-vl:4b-instruct-q4_K_M                                                              |          |   7.04 |    320 |    4.4 |    4 |      | 10.08 |  6.6 | 4.88 | 0.52 |
| qwen3-vl-8b-instruct-mlx                                                                 |          |   7.00 |    159 |    8.8 |    4 |  256 | 8.23 | 9.48 | 4.07 | 0.54 |
| phi4:14b-q4_K_M                                                                          |          |   6.89 |     94 |   14.7 |    4 |   16 | 8.92 | 8.42 | 3.49 | 0.98 |
| qwen2.5:32b-instruct-q4_K_M                                                              |          |   6.88 |     42 |   32.8 |    4 |   32 | 9.74 | 6.08 |  5.6 | 0.35 |
| granite4:small-h                                                                         |          |   6.61 |     41 |   32.2 |    4 |  131 | 8.34 | 7.04 | 5.54 | 0.54 |
| qwen2.5-coder:14b-instruct-q4_K_M                                                        |          |   6.01 |     81 |   14.8 |    4 |  128 | 6.35 | 8.46 | 4.08 | 1.15 |
| qwen3:8b-q4_K_M-no_think                                                                 |          |   5.70 |    139 |    8.2 |    4 |  128 | 5.34 | 8.65 |  4.2 | 1.26 |
| hf.co/LGAI-EXAONE/EXAONE-4.0-32B-GGUF:Q4_K_M                                             |          |   5.10 |     32 |   32.0 |    4 |      | 8.54 | 4.39 | 1.57 |  0.5 |
| llama3.2-vision:90b-instruct-q4_K_M                                                      |          |   5.03 |     11 |   87.7 |    4 |  128 | 6.71 | 4.34 | 4.43 | 1.61 |
| hf.co/mradermacher/VibeThinker-1.5B-GGUF:Q4_K_M                                          |     0.89 |   4.93 |    554 |   1.78 |    4 |      | 9.38 | 1.51 | 1.97 |  3.3 |
| llama3.3:70b-instruct-q4_K_M                                                             |          |   4.83 |     14 |   70.6 |    4 |  128 | 5.26 | 5.04 | 5.19 |  1.8 |
| yi-coder:9b-chat-q4_K_M                                                                  |          |   4.82 |    110 |    8.8 |    4 |  128 |  7.2 | 5.39 | 1.51 | 0.22 |
| gemma3:27b                                                                               |          |   4.81 |     35 |   27.4 |    4 |  128 | 6.11 | 4.74 | 4.54 | 0.36 |
| hf.co/bartowski/internlm_JanusCoder-8B-GGUF:Q4_K_M                                       |          |   4.67 |    114 |   8.19 |    4 |      | 5.97 |  6.7 | 1.07 | 0.58 |
| hf.co/mradermacher/AesCoder-4B-GGUF:Q4_K_M                                               |          |   4.58 |    208 |   4.41 |    4 |      | 6.93 | 3.39 | 3.79 | 0.38 |
| hf.co/mradermacher/Josiefied-Qwen3-4B-Instruct-2507-abliterated-v1-GGUF:Q4_K_M           |          |   4.41 |    219 |   4.02 |    4 |      | 5.97 | 4.24 | 3.42 | 0.66 |
| hf.co/mradermacher/Ling-lite-1.5-GGUF:Q4_K_M                                             |          |   4.32 |     51 |   16.8 |    4 |      | 4.99 | 5.13 | 3.71 | 0.44 |
| qwen3-vl-4b-instruct-mlx                                                                 |          |   4.19 |    105 |    8.0 |    4 |  256 | 7.64 | 1.83 | 2.71 | 0.39 |
| hf.co/bartowski/google_medgemma-27b-it-GGUF:Q4_K_M                                       |          |   4.14 |     31 |   27.0 |    4 |      | 6.03 | 4.08 | 2.46 | 0.11 |
| hf.co/mradermacher/MiroThinker-v1.0-72B-GGUF:Q4_K_M                                      |          |   4.10 |     11 |   72.7 |    4 |      |  5.1 | 3.57 | 4.42 | 1.04 |
| hf.co/mradermacher/medgemma-27b-text-it-GGUF:Q4_K_M                                      |          |   4.00 |     30 |   27.0 |    4 |      | 4.96 | 4.12 | 3.67 | 0.47 |
| hf.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF:Q4_K_M                |          |   3.98 |     34 |   23.6 |    4 |  128 | 4.39 | 4.76 | 3.46 | 1.08 |
| hf.co/mradermacher/Qwen3-4b-tcomanr-merge-v2.5-GGUF:Q4_K_M                               |          |   3.92 |    195 |   4.02 |    4 |      | 4.27 | 3.91 | 3.84 | 2.72 |
| hf.co/mistralai/Devstral-Small-2507_gguf:Q4_K_M                                          |          |   3.68 |     31 |   23.6 |    4 |  128 | 5.32 | 3.03 | 2.99 | 0.46 |
| hf.co/LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF:Q4_K_M                                            |     0.64 |   3.50 |    547 |   1.28 |    4 |      | 5.49 | 4.35 | 0.01 |  0.0 |
| gemma3:12b                                                                               |          |   2.97 |     49 |   12.2 |    4 |  128 | 3.21 | 2.79 | 3.92 | 0.69 |
| hf.co/LGAI-EXAONE/EXAONE-3.5-32B-Instruct-GGUF:Q4_K_M                                    |          |   2.86 |     18 |   32.0 |    4 |      | 3.08 |  4.3 | 1.46 | 0.42 |
| hf.co/bartowski/THUDM_GLM-4-9B-0414-GGUF:Q4_K_M                                          |          |   2.85 |     61 |    9.4 |    4 |   32 | 4.48 | 2.82 |  1.0 | 0.16 |
| qwen2.5-coder:7b-instruct-q4_K_M                                                         |          |   2.70 |     71 |    7.6 |    4 |   32 | 3.69 | 2.84 | 1.81 | 0.13 |
| hf.co/bartowski/cognitivecomputations_Dolphin-Mistral-24B-Venice-Edition-GGUF:Q4_K_M     |          |   2.67 |     22 |   24.0 |    4 |   32 | 4.29 | 1.68 | 1.91 | 0.64 |
| qwen2.5:7b-instruct-q4_K_M                                                               |          |   2.43 |     64 |    7.6 |    4 |  128 | 2.97 | 3.12 | 1.42 | 0.24 |
| qwen3:1.7b-q4_K_M-no_think                                                               |          |   2.33 |    233 |    2.0 |    4 |   32 | 2.26 | 3.93 | 1.03 | 0.44 |
| qwen2.5-coder:3b-instruct-q4_K_M                                                         |          |   2.09 |    135 |    3.1 |    4 |   32 | 3.32 | 2.04 | 0.63 | 0.29 |
| granite4:tiny-h                                                                          |          |   2.08 |     60 |    6.9 |    4 | 1024 | 2.63 | 2.69 | 1.03 | 0.19 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                                         |          |   2.02 |     46 |    8.8 |    4 |   32 | 3.07 | 1.96 |  1.0 | 0.01 |
| hf.co/mradermacher/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2-GGUF:Q4_K_M          |          |   1.90 |     95 |   4.02 |    4 |      | 3.15 | 1.72 | 0.58 | 0.09 |
| hf.co/janhq/Jan-v1-edge-gguf:Q4_K_M                                                      |          |   1.88 |    219 |   1.72 |    4 |      | 3.03 | 1.92 | 0.12 | 0.73 |
| granite4:3b                                                                              |          |   1.69 |     99 |    3.4 |    4 |      | 3.06 | 1.09 | 0.57 |  0.2 |
| hf.co/mradermacher/Ling-Coder-lite-GGUF:Q4_K_M                                           |          |   1.62 |     19 |   16.8 |    4 |      | 2.59 | 1.32 | 0.68 | 0.51 |
| granite4:micro                                                                           |          |   1.61 |     95 |    3.4 |    4 |  128 | 2.78 | 1.21 | 0.57 |  0.2 |
| llama3.2-vision:11b-instruct-q4_K_M                                                      |          |   1.60 |     33 |    9.8 |    4 |  128 |  1.9 | 2.14 | 0.68 | 0.62 |
| qwen3-vl:2b-thinking-q4_K_M                                                              |          |   1.54 |    147 |    2.1 |    4 |      | 1.49 | 2.25 | 1.14 | 0.42 |
| qwen3-vl-2b-instruct-mlx                                                                 |          |   1.40 |     70 |      2 |    8 |      | 2.25 | 1.22 |  0.6 | 0.09 |
| qwen2.5vl:7b-q4_K_M                                                                      |          |   1.34 |     32 |    8.3 |    4 |  128 |  1.7 | 0.69 |  2.2 | 0.15 |
| granite4:3b-h                                                                            |          |   1.33 |     83 |    3.2 |    4 |      | 1.79 |  1.7 | 0.45 | 0.17 |
| hf.co/bartowski/internlm_JanusCoderV-7B-GGUF:Q4_K_M                                      |          |   1.31 |     34 |   7.62 |    4 |      | 1.93 | 1.62 | 0.16 | 0.17 |
| granite4:micro-h                                                                         |          |   1.30 |     81 |    3.2 |    4 | 1024 | 1.82 | 1.55 | 0.45 | 0.15 |
| hf.co/mradermacher/Olmo-3-7B-Instruct-GGUF:Q4_K_M                                        |          |   1.24 |     36 |      7 |    4 |      | 2.25 | 0.31 |  1.1 | 0.32 |
| granite4:1b-bf16                                                                         |          |   1.19 |        |        |      |      | 1.81 |      | 0.28 | 0.08 |
| hf.co/bartowski/HuggingFaceTB_SmolLM3-3B-GGUF:Q4_K_M                                     |          |   1.06 |     69 |   3.08 |    4 |      | 1.47 | 1.41 | 0.18 | 0.09 |
| gemma3n:e4b                                                                              |          |   0.99 |     29 |    6.9 |    4 |   32 | 1.32 | 0.92 | 0.92 |  0.0 |
| granite3.3:8b                                                                            |          |   0.97 |     24 |    8.0 |    4 |  128 | 1.88 | 0.63 | 0.09 |  0.1 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q4_K_M                                                     |          |   0.94 |     73 |   2.57 |    4 |      | 0.98 | 1.39 | 0.52 | 0.28 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                                       |          |   0.89 |    119 |    1.5 |    4 |   32 | 1.46 | 0.85 | 0.25 |  0.0 |
| hf.co/bartowski/allenai_olmOCR-2-7B-1025-GGUF:Q4_K_M                                     |          |   0.88 |     23 |   7.62 |    4 |    2 | 1.44 | 0.75 |  0.3 | 0.21 |
| hf.co/mradermacher/olmOCR-7B-0825-GGUF:Q4_K_M                                            |          |   0.88 |     23 |   7.62 |    4 |  128 | 1.72 | 0.36 | 0.41 | 0.02 |
| hf.co/DevQuasar/inference-net.Schematron-8B-GGUF:Q4_K_M                                  |          |   0.88 |     22 |   8.03 |    4 |      | 1.16 | 1.01 | 0.27 | 0.55 |
| qwen3:0.6b-q4_K_M-no_think                                                               |     0.38 |   0.87 |    232 | 0.75163 |    4 |   32 |  1.3 | 0.73 | 0.36 |  0.6 |
| gemma3n:e2b                                                                              |          |   0.85 |     38 |    4.5 |    4 |    8 |  1.4 | 0.95 | 0.01 | 0.05 |
| yi-coder:1.5b-chat-q4_K_M                                                                |          |   0.84 |    112 |    1.5 |    4 |  128 | 1.53 | 0.66 | 0.08 | 0.13 |
| granite4:1b-h-q8_0                                                                       |          |   0.80 |     53 |    1.5 |    8 |      | 1.53 | 0.35 | 0.38 | 0.06 |
| hf.co/mradermacher/Lucy-128k-GGUF:Q4_K_M                                                 |          |   0.73 |     85 |   1.72 |    4 |      | 0.76 | 1.23 | 0.05 | 0.47 |
| hf.co/allenai/OLMo-2-0325-32B-Instruct-GGUF:Q4_0                                         |          |   0.72 |      4 |   32.2 |    4 |    4 | 1.68 | 0.06 | 0.11 | 0.09 |
| qwen3-vl:2b-instruct-q4_K_M                                                              |          |   0.72 |     68 |    2.1 |    4 |      | 1.07 | 0.59 |      | 0.09 |
| llama3.2:3b                                                                              |          |   0.61 |     38 |    3.2 |    4 |  128 |  1.3 | 0.27 | 0.05 |  0.0 |
| hf.co/unsloth/medgemma-4b-it-GGUF:Q4_K_M                                                 |          |   0.60 |     31 |   3.88 |    4 |      | 1.14 | 0.28 | 0.16 | 0.28 |
| gemma3:4b                                                                                |          |   0.55 |     25 |    4.3 |    4 |  128 | 1.03 | 0.35 | 0.15 |  0.0 |
| qwen2.5vl:3b-q4_K_M                                                                      |          |   0.55 |     29 |    3.8 |    4 |  128 | 0.82 | 0.71 | 0.03 |  0.0 |
| phi4-mini:3.8b-q4_K_M                                                                    |          |   0.50 |     26 |    3.8 |    4 |  128 | 0.66 | 0.27 | 0.78 |  0.0 |
| qwen2.5:1.5b-instruct-q4_K_M                                                             |          |   0.44 |     59 |    1.5 |    4 |  128 | 0.92 |  0.2 | 0.03 | 0.09 |
| hf.co/mradermacher/Arch-Router-1.5B-GGUF:Q4_K_M                                          |          |   0.40 |     52 |   1.54 |    4 |      | 0.73 | 0.32 | 0.08 |  0.0 |
| granite3.3:2b                                                                            |          |   0.39 |     39 |    2.0 |    4 |  128 | 0.67 |  0.2 | 0.26 |  0.1 |
| hf.co/DevQuasar/inference-net.Schematron-3B-GGUF:Q4_K_M                                  |          |   0.38 |     24 |   3.21 |    4 |      | 0.42 | 0.34 | 0.32 | 0.48 |
| hf.co/mradermacher/medgemma-4b-it-GGUF:Q4_K_M                                            |          |   0.35 |     18 |   3.88 |    4 |      | 0.64 | 0.07 | 0.37 |  0.0 |
| hf.co/mradermacher/UserLM-8b-GGUF:Q4_K_M                                                 |          |   0.34 |        |        |    4 |      | 0.73 | 0.05 | 0.12 |  0.1 |
| hf.co/allenai/OLMo-2-1124-7B-Instruct-GGUF:Q4_K_M                                        |          |   0.33 |      9 |    7.3 |    4 |      | 0.69 |  0.1 | 0.08 | 0.09 |
| hf.co/mradermacher/scout-4b-GGUF:Q4_K_M                                                  |          |   0.33 |     17 |   3.88 |    4 |      | 0.77 | 0.04 | 0.03 |  0.0 |
| hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M                                      |          |   0.22 |      6 |   6.92 |    4 |    2 | 0.53 | 0.03 | 0.01 |  0.0 |
| hf.co/mradermacher/occiglot-7b-eu5-instruct-GGUF:Q4_K_M                                  |          |   0.19 |      5 |   7.24 |    4 |      | 0.23 |  0.0 | 0.02 | 0.95 |
| hf.co/QuantFactory/EuroLLM-9B-Instruct-GGUF:Q4_K_M                                       |          |   0.18 |      4 |   9.15 |    4 |      | 0.42 | 0.04 | 0.01 |  0.0 |
| hf.co/LiquidAI/LFM2-1.2B-GGUF:Q4_K_M                                                     |          |   0.17 |     28 |   1.17 |    4 |      |  0.4 | 0.01 | 0.01 |  0.0 |
| hf.co/mradermacher/Ling-lite-GGUF:Q4_K_M                                                 |          |   0.14 |      2 |   16.8 |    4 |      | 0.21 | 0.01 | 0.11 | 0.27 |
| llama3.2:1b-instruct-q4_K_M                                                              |          |   0.10 |      8 |    1.2 |    8 |  128 | 0.22 | 0.03 |  0.0 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                                       |     0.25 |   0.09 |     37 |    0.5 |    4 |   32 | 0.11 |  0.1 | 0.09 |  0.0 |
| hf.co/mradermacher/EuroLLM-1.7B-Instruct-GGUF:Q4_K_M                                     |          |   0.09 |     11 |   1.66 |    4 |      | 0.09 | 0.09 | 0.09 | 0.09 |
| gemma3:270m                                                                              |          |   0.08 |     31 |   0.27 |    8 |   32 |  0.0 | 0.09 | 0.28 |  0.0 |
| phi3:3.8b                                                                                |          |   0.08 |      4 |    3.8 |    4 |  128 |  0.1 | 0.09 | 0.07 |  0.0 |
| granite4:350m-bf16                                                                       |          |   0.07 |     11 |   0.35 |   16 |      | 0.12 | 0.03 | 0.09 |  0.0 |
| hf.co/LiquidAI/LFM2-350M-GGUF:Q4_K_M                                                     |     0.18 |   0.07 |     42 |  0.354 |    4 |      | 0.12 |  0.0 | 0.09 | 0.09 |
| smollm2:360m-instruct-q4_K_M                                                             |          |   0.07 |      0 | 361.82 |    4 |      | 0.03 | 0.09 | 0.09 | 0.09 |
| qwen2.5:0.5b-instruct-q4_K_M                                                             |          |   0.06 |     25 |    0.5 |    4 |  128 | 0.06 |  0.1 |  0.0 | 0.09 |
| granite4:350m-h-q8_0                                                                     |          |   0.05 |     14 |   0.35 |    8 |      |  0.1 |  0.0 |  0.0 | 0.09 |
| gemma3:1b                                                                                |          |   0.04 |      8 |    1.0 |    4 |   32 | 0.08 | 0.03 |  0.0 |  0.0 |
| hf.co/LiquidAI/LFM2-700M-GGUF:Q4_K_M                                                     |          |   0.04 |        |        |    4 |      | 0.03 |  0.0 | 0.09 | 0.09 |
| hf.co/allenai/OLMo-2-0425-1B-Instruct-GGUF:Q4_K_M                                        |          |   0.04 |      5 |   1.48 |    4 |    4 | 0.03 | 0.09 |  0.0 |  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                                           |     0.14 |   0.03 |     25 |  0.135 |    8 |    2 |  0.0 |  0.0 | 0.17 |  0.0 |

## Archived Outdated PE-Bench-100
The following Benchmark result ("PE-Bench-Python-100", "PE-Bench-Java-100", "PE-Bench-Rust-100", "PE-Bench-Clojure-100") is an archive of a retired computation process that does not only compute only 100 problems for each language (the best models saturated those already) but also it used different prompt templates, so the benchmark values cannot be compared with the PE-Bench-200:

| Model                                                                                    | Best<br/>Model<br/>for<br/>Size (GB) | PE-100-<br/>Score | Mem-<br/>Score | Size<br/>*10^9 Params | Bits | Context Length<br/>(K) | Python | Java | Rust | Clojure |
| :--------------------------------------------------------------------------------------- | -----------------------------------: | ----------------: | -------------: | --------------------: | ---: | ---------------------: | -----: | ---: | ---: | ------: |
| Grok-4-Fast                                                                              |          |  22.54 |        |        |   16 | 2000 | 22.44 | 25.47 | 21.44 | 16.38 |
| o4-mini-2025-04-16                                                                       |          |  21.34 |        |        |   16 |  200 | 22.71 | 21.88 | 21.59 | 13.71 |
| gpt-4.1-2025-04-14                                                                       |          |  19.84 |        |        |   16 | 1024 | 22.41 | 20.88 | 17.0 | 12.08 |
| gpt-4.1-mini-2025-04-14                                                                  |          |  18.05 |        |        |   16 | 1024 | 18.34 | 20.53 | 18.99 | 7.56 |
| qwen3-coder:480b-a35b-q4_K_M                                                             |      240 |  17.57 |      7 |  480.2 |    4 |  256 | 20.69 | 18.91 | 14.88 |  6.5 |
| DeepSeek-V3-0324                                                                         |          |  17.06 |      1 |  671.0 |   16 |  128 | 20.08 | 18.63 | 14.91 | 4.62 |
| DeepSeek-V3                                                                              |          |  16.11 |      1 |  671.0 |   16 |  128 | 20.01 | 16.95 | 12.16 | 5.92 |
| deepseek-v3.1:671b                                                                       |          |  15.27 |      5 |  671.0 |    4 |  160 | 19.25 | 14.73 | 12.78 | 5.93 |
| qwen3:235b-a22b-instruct-2507-q4_K_M                                                     |      118 |  15.26 |     13 |  235.1 |    4 |  256 | 18.66 | 17.64 | 10.32 | 4.38 |
| GPT-4o                                                                                   |          |  14.72 |        |        |   16 |  128 | 17.05 | 13.87 | 14.57 | 8.24 |
| mlx-community/Qwen3-Next-80B-A3B-Instruct-8bit                                           |    79.70 |  14.46 |     18 |   79.7 |    8 |  256 | 18.85 | 15.27 | 9.92 | 3.51 |
| gpt-4-turbo-2024-04-09                                                                   |          |  13.86 |        |        |   16 |  128 | 16.87 | 15.82 | 10.12 | 3.45 |
| mlx-community/Qwen3-Next-80B-A3B-Instruct-4bit                                           |    39.85 |  13.13 |     33 |   79.7 |    4 |  256 | 16.04 | 14.51 | 9.55 | 4.47 |
| qwen3-coder:30b-a3b-q4_K_M                                                               |    15.25 |  11.69 |     77 |   30.5 |    4 |  256 | 14.3 | 12.72 | 9.61 | 2.34 |
| GPT-o1-Mini                                                                              |          |  11.32 |        |        |   16 |   32 | 17.44 |      |      |      |
| qwen3:30b-a3b-instruct-2507-q8_0                                                         |          |  11.19 |     37 |   30.5 |    8 |  256 | 14.29 | 11.13 | 9.15 | 3.04 |
| athene-v2:72b-q8_0                                                                       |          |  10.97 |     15 |   72.7 |    8 |  128 | 16.22 | 10.15 | 5.55 | 3.32 |
| qwen3:30b-a3b-instruct-2507-q4_K_M                                                       |    15.25 |  10.78 |     71 |   30.5 |    4 |  256 | 13.95 | 10.58 | 8.42 | 3.39 |
| qwen3:235b-a22b-q4_K_M-no_think                                                          |          |  10.76 |      9 |  235.1 |    4 |  128 | 13.27 | 15.17 | 3.33 | 2.35 |
| qwen3-coder:30b-a3b-q8_0                                                                 |          |  10.73 |     35 |   30.5 |    8 |  256 | 13.94 | 11.51 | 6.22 | 4.62 |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                                              |          |  10.60 |     29 |   72.7 |    4 |  128 | 14.49 | 10.56 | 6.33 | 3.74 |
| athene-v2:72b-q4_K_M                                                                     |          |  10.48 |     29 |   72.7 |    4 |  128 | 14.07 | 11.19 | 6.55 | 1.83 |
| llama4:17b-maverick-128e-instruct-q4_K_M                                                 |          |  10.38 |      5 |  401.6 |    4 | 1024 | 11.3 | 11.44 | 9.93 | 4.39 |
| gpt-4.1-nano-2025-04-14                                                                  |          |  10.35 |        |        |   16 | 1024 | 13.79 | 10.36 | 7.83 |  1.6 |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                                           |          |  10.33 |     63 |   32.8 |    4 |   32 | 12.72 | 11.67 | 7.25 | 2.89 |
| GPT-o1-Preview                                                                           |          |  10.30 |      2 |  300.0 |   16 |   32 | 15.86 |      |      |      |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q8_0                                             |          |  10.28 |     31 |   32.8 |    8 |   32 | 12.76 | 10.75 | 8.04 | 3.43 |
| qwen2.5:72b-instruct-q4_K_M                                                              |          |   9.78 |     27 |   72.7 |    4 |  128 | 14.02 |  9.1 | 5.97 | 2.46 |
| qwen2.5:72b-instruct-q8_0                                                                |          |   9.77 |     13 |   72.7 |    8 |  128 | 12.98 | 10.5 | 5.41 | 3.49 |
| qwen2.5-coder:32b-instruct-q4_K_M                                                        |          |   9.77 |     60 |   32.8 |    4 |   32 | 14.05 | 8.82 | 6.41 |  2.2 |
| hf.co/bartowski/Dracarys2-72B-Instruct-GGUF:Q4_K_M                                       |          |   9.74 |     27 |   72.7 |    4 |  128 | 13.45 | 8.54 | 7.34 | 3.35 |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M                          |          |   9.69 |     27 |   72.7 |    4 |  128 | 13.92 | 8.65 | 6.11 | 3.07 |
| hf.co/bartowski/THUDM_GLM-4-32B-0414-GGUF:Q4_K_M                                         |          |   9.64 |     59 |   32.6 |    4 |   32 | 13.9 | 10.14 | 4.82 | 0.75 |
| hf.co/bartowski/Sky-T1-32B-Flash-GGUF:Q4_K_M                                             |          |   9.62 |     59 |   32.8 |    4 |   32 | 12.04 | 10.75 | 6.64 |  2.5 |
| hf.co/mradermacher/Bespoke-Stratos-32B-GGUF:Q4_K_M                                       |          |   9.61 |     59 |   32.8 |    4 |   32 | 12.37 |  9.9 | 7.58 | 1.78 |
| qwen2.5-coder:32b-instruct-q8_0                                                          |          |   9.38 |     29 |   32.8 |    8 |   32 | 11.94 | 9.94 | 6.69 |  2.8 |
| qwen2.5:32b-instruct-q4_K_M                                                              |          |   9.17 |     56 |   32.8 |    4 |   32 | 12.34 | 9.26 | 6.13 | 2.25 |
| mlx-community/Qwen3-Next-80B-A3B-Thinking-4bit                                           |          |   9.13 |     23 |     80 |    4 |  256 | 9.72 | 11.69 | 6.94 | 3.43 |
| qwen2.5vl:32b-q4_K_M                                                                     |          |   8.95 |     53 |   33.5 |    4 |  128 | 13.02 | 7.74 | 6.01 | 2.18 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0                         |          |   8.66 |     26 |   32.8 |    8 |   32 | 11.58 | 8.69 | 6.27 | 1.62 |
| qwen2.5:32b-instruct-q8_0                                                                |          |   8.44 |     26 |   32.8 |    8 |   32 | 9.73 | 10.22 | 5.91 | 2.98 |
| GPT-4o-Mini                                                                              |          |   8.00 |        |        |   16 |  128 | 11.39 | 7.36 | 5.19 | 1.93 |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M                       |          |   7.95 |     48 |   32.8 |    4 |   32 | 9.55 |  9.3 | 5.71 | 1.94 |
| mlx-community/Ling-mini-2.0-4bit                                                         |     8.00 |   7.86 |     98 |   16.0 |    4 |   32 | 12.23 | 7.64 |  3.0 | 0.79 |
| cogito:32b-v1-preview-qwen-q4_K_M                                                        |          |   7.83 |     48 |   32.8 |    4 |  128 | 11.32 | 7.12 | 5.26 | 1.19 |
| qwen3:32b-q4_K_M-no_think                                                                |          |   7.67 |     47 |   32.8 |    4 |   40 | 10.25 | 8.94 | 3.93 | 1.07 |
| GPT-3.5-Turbo                                                                            |          |   7.47 |      2 |  175.0 |   16 |   16 | 10.1 | 7.28 |  6.0 |  0.5 |
| yi-coder:9b-chat-q8_0                                                                    |          |   7.37 |     84 |    8.8 |    8 |  128 | 11.08 | 6.77 | 4.32 | 0.47 |
| deepseek-coder:33b-instruct-q4_K_M                                                       |          |   7.34 |     44 |   33.0 |    4 |   16 | 9.55 | 10.72 |  0.0 | 3.03 |
| qwen2.5vl:72b-q4_K_M                                                                     |          |   7.31 |     20 |   73.4 |    4 |  128 | 7.57 |  9.3 | 6.09 |  2.7 |
| llama3.3:70b-instruct-q8_0                                                               |          |   7.17 |     10 |   70.6 |    8 |  128 | 8.93 | 8.06 | 4.29 | 3.17 |
| qwen2.5-coder:14b-instruct-q8_0                                                          |          |   7.09 |     48 |   14.8 |    8 |  128 |  9.7 | 7.35 | 4.55 | 0.95 |
| hf.co/bartowski/Qwen_Qwen3-30B-A3B-GGUF:Q4_K_M-think                                     |          |   7.08 |     46 |   30.5 |    4 |   40 | 8.49 | 8.09 |  4.5 | 3.61 |
| qwen3:14b-q4_K_M-no_think                                                                |     7.40 |   6.97 |     94 |   14.8 |    4 |   40 | 10.94 | 6.37 | 2.99 | 0.86 |
| hf.co/bartowski/AGI-0_Art-0-8B-GGUF:Q4_K_M                                               |     4.09 |   6.96 |    170 |   8.19 |    4 |   40 | 9.22 | 6.61 | 4.45 | 3.95 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q8_0                                           |          |   6.81 |     46 |   14.7 |    8 |   16 | 10.06 | 6.67 | 3.68 | 0.52 |
| qwen3:30b-a3b-q4_K_M-no_think                                                            |          |   6.81 |     45 |   30.5 |    4 |   40 | 8.22 | 8.01 | 5.11 | 0.97 |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q4_K_M                                         |          |   6.72 |     91 |   14.7 |    4 |   16 | 9.26 |  6.8 | 4.42 | 0.89 |
| qwen2.5-coder:14b-instruct-q4_K_M                                                        |          |   6.68 |     90 |   14.8 |    4 |  128 | 8.65 | 7.28 | 4.62 | 1.13 |
| phi4:14b-q4_K_M                                                                          |          |   6.64 |     90 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| phi4:latest                                                                              |          |   6.64 |     90 |   14.7 |    4 |   16 | 9.64 | 6.91 | 3.14 | 0.84 |
| deepseek-coder:33b-instruct-q8_0                                                         |          |   6.58 |     20 |   33.0 |    8 |   16 | 8.35 | 10.2 |  0.0 | 1.82 |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M                       |          |   6.49 |     18 |   70.6 |    4 |  128 |  9.1 |  5.9 | 4.69 | 1.37 |
| hf.co/mradermacher/Seed-Coder-8B-Instruct-GGUF:Q4_K_M                                    |          |   6.39 |    155 |   8.25 |    4 |   32 | 9.16 | 6.07 | 3.52 | 2.02 |
| phi4-reasoning:14b-q4_K_M                                                                |          |   6.36 |     86 |   14.7 |    4 |   32 | 6.73 | 7.73 |  5.2 | 3.05 |
| mistral-large:123b-instruct-2407-q4_K_M                                                  |          |   6.34 |     10 |  122.6 |    4 |  128 | 8.27 | 6.61 | 4.44 | 1.61 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-30B-A3B-GGUF:Q4_K_M                                |          |   6.22 |     41 |   30.5 |    4 |   40 | 10.14 | 4.75 | 3.54 | 0.33 |
| hf.co/mradermacher/KAT-Dev-GGUF:Q4_K_M                                                   |          |   6.22 |     38 |   32.8 |    4 |      | 9.67 |  6.7 |  1.1 |      |
| qwen3:14b-q4_K_M-think                                                                   |          |   6.20 |     84 |   14.8 |    4 |   40 | 7.16 |  7.5 | 4.66 | 1.51 |
| vanilj/Phi-4:Q8_0                                                                        |          |   6.13 |     42 |   14.7 |    8 |   16 | 9.06 | 5.73 | 3.52 | 0.84 |
| hf.co/gaianet/Seed-Coder-8B-Instruct-GGUF:Q4_K_M                                         |     4.00 |   6.10 |    152 |      8 |    4 |   32 |  9.0 | 4.99 | 4.09 | 1.81 |
| cogito:70b-v1-preview-llama-q4_K_M                                                       |          |   6.05 |     17 |   70.6 |    4 |  128 |  7.7 | 7.26 | 3.54 | 0.86 |
| qwen3:30b-a3b-q4_K_M-think                                                               |          |   5.98 |     39 |   30.5 |    4 |   40 |  8.3 | 5.59 | 4.32 | 1.17 |
| yi-coder:9b-chat-q4_K_M                                                                  |          |   5.97 |    136 |    8.8 |    4 |  128 | 7.44 | 6.04 | 5.76 | 0.34 |
| qwq:32b-preview-q8_0                                                                     |          |   5.97 |     18 |   32.8 |    8 |   32 | 10.15 | 3.11 | 3.88 | 1.97 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                                                |          |   5.83 |     17 |   70.6 |    4 |  128 | 8.07 | 6.49 | 2.59 | 1.36 |
| llama3.1:70b-instruct-q8_0                                                               |          |   5.81 |      8 |   70.6 |    8 |  128 | 8.19 | 5.36 |  3.8 |  1.7 |
| hf.co/bartowski/deepcogito_cogito-v2-preview-llama-70B-GGUF:Q4_K_M                       |          |   5.78 |     16 |   70.6 |    4 |  128 | 7.49 | 5.65 |  4.5 | 1.92 |
| llama4:16x17b                                                                            |          |   5.76 |     11 |  108.6 |    4 | 10000 | 9.13 | 4.78 | 2.89 | 0.93 |
| qwen2.5:14b-instruct-q8_0                                                                |          |   5.75 |     39 |   14.8 |    8 |   32 | 8.59 | 4.14 | 4.55 | 1.61 |
| cogito:14b-v1-preview-qwen-q4_K_M                                                        |          |   5.70 |     77 |   14.8 |    4 |  128 |  7.9 | 5.89 | 3.41 | 0.91 |
| qwen2.5:14b-instruct-q4_K_M                                                              |          |   5.63 |     76 |   14.8 |    4 |   32 | 8.44 | 5.08 | 3.44 | 0.43 |
| llama3.1:70b-instruct-q4_K_M                                                             |          |   5.62 |     16 |   70.6 |    4 |  128 | 8.77 | 4.98 | 2.77 |  0.6 |
| llama3.3:70b-instruct-q4_K_M                                                             |          |   5.60 |     16 |   70.6 |    4 |  128 | 7.26 | 5.25 | 4.49 | 2.21 |
| falcon3:10b-instruct-q8_0                                                                |          |   5.48 |     53 |   10.3 |    8 |   32 | 8.15 | 5.14 | 2.71 | 1.39 |
| hf.co/bartowski/smirki_UIGEN-T1.1-Qwen-14B-GGUF:Q4_K_M                                   |          |   5.46 |     74 |   14.8 |    4 |   32 | 7.27 |  5.2 | 4.41 | 1.14 |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S                                    |          |   5.43 |     14 |   78.0 |    4 |   32 | 7.04 | 6.05 |  3.6 | 0.74 |
| hf.co/Tesslate/Tessa-Rust-T1-7B-Q8_0-GGUF:Q8_0                                           |          |   5.37 |     70 |   7.62 |    8 |   32 | 7.04 |  5.0 | 4.84 | 0.86 |
| qwen3:32b-q4_K_M-think                                                                   |          |   5.31 |     32 |   32.8 |    4 |   40 | 5.78 | 6.75 | 4.78 | 0.19 |
| qwen3:8b-q4_K_M-think                                                                    |          |   5.30 |    129 |    8.2 |    4 |  128 | 5.69 | 6.48 | 4.77 | 1.27 |
| tulu3:70b-q8_0                                                                           |          |   5.25 |      7 |   70.6 |    8 |  128 | 7.73 | 4.61 | 3.09 | 1.59 |
| qwen2-math:72b-instruct-q8_0                                                             |          |   5.25 |      7 |   72.7 |    8 |    4 | 6.49 | 6.67 | 2.61 |  1.3 |
| tulu3:70b-q4_K_M                                                                         |          |   5.21 |     15 |   70.6 |    4 |  128 | 7.31 | 4.68 | 3.35 | 2.15 |
| hf.co/unsloth/Magistral-Small-2509-GGUF:Q4_K_M                                           |          |   5.18 |     44 |   23.6 |    4 |   40 | 7.14 | 5.08 | 3.36 | 1.32 |
| qwen3:4b-q4_K_M-think                                                                    |     2.00 |   5.18 |    259 |    4.0 |    4 |   32 | 7.89 | 4.61 | 2.73 | 0.91 |
| aravhawk/llama4:scout-q4_K_M                                                             |          |   5.17 |     10 |  107.8 |    4 | 10240 | 6.78 | 5.64 | 3.55 | 0.59 |
| granite4:small-h                                                                         |          |   5.15 |     32 |   32.2 |    4 |  131 | 7.67 | 4.59 | 2.97 | 1.13 |
| hf.co/ozone-ai/0x-lite-Q4_K_M-GGUF:latest                                                |          |   5.14 |     69 |   14.8 |    4 |   32 | 7.66 | 4.52 | 3.32 | 0.56 |
| command-a:111b-03-2025-q4_K_M                                                            |          |   5.06 |      9 |  111.1 |    4 |  256 | 6.33 | 5.17 | 4.21 | 1.32 |
| goekdenizguelmez/JOSIEFIED-Qwen3:8b-q4_k_m-think                                         |          |   5.04 |    123 |    8.2 |    4 |   40 | 5.77 | 6.22 | 3.49 | 1.65 |
| devstral:24b-small-2505-q4_K_M                                                           |          |   5.02 |     42 |   24.0 |    4 |  128 | 6.77 | 5.47 | 2.96 | 0.82 |
| qwen3:4b-instruct-2507-q4_K_M                                                            |     2.00 |   5.01 |    250 |    4.0 |    4 |  256 | 8.07 |  4.5 | 2.01 | 0.26 |
| hf.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF:Q4_K_M                |          |   4.96 |     42 |   23.6 |    4 |  128 | 6.79 | 5.19 | 3.05 | 0.79 |
| hf.co/bartowski/NousResearch_Hermes-4-14B-GGUF:Q4_K_M                                    |          |   4.94 |     67 |   14.8 |    4 |   40 | 6.81 | 4.01 | 4.69 | 0.78 |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                                      |          |   4.94 |     67 |   14.8 |    4 |  986 | 7.75 | 4.02 | 2.74 | 0.81 |
| falcon3:10b-instruct-q4_K_M                                                              |          |   4.88 |     95 |   10.3 |    4 |   32 | 6.62 | 5.77 | 2.19 |  0.6 |
| hf.co/mradermacher/K2-Think-GGUF:Q4_K_M                                                  |          |   4.85 |     30 |   32.8 |    4 |  128 | 4.83 | 4.98 | 6.42 | 1.36 |
| hf.co/bartowski/Goekdeniz-Guelmez_Josiefied-Qwen3-8B-abliterated-v1-GGUF:Q4_K_M-no_think |          |   4.83 |    118 |    8.2 |    4 |  128 | 7.25 | 4.93 | 2.05 | 0.44 |
| nemotron:70b-instruct-q4_K_M                                                             |          |   4.78 |     14 |   70.6 |    4 |  128 | 5.78 | 5.13 | 4.22 | 0.83 |
| hf.co/bartowski/mistralai_Mistral-Small-3.1-24B-Instruct-2503-GGUF:Q4_K_M                |          |   4.70 |     40 |   23.6 |    4 |  128 | 6.79 | 4.05 | 3.38 | 0.95 |
| qwen2.5-coder:7b-instruct-q8_0                                                           |          |   4.69 |     62 |    7.6 |    8 |  128 | 6.37 |  4.4 | 3.78 | 0.63 |
| qwen3:8b-q4_K_M-no_think                                                                 |          |   4.68 |    114 |    8.2 |    4 |  128 | 6.98 | 4.84 | 1.92 | 0.51 |
| hf.co/bartowski/Qwen2.5-Math-72B-Instruct-GGUF:Q4_K_M                                    |          |   4.59 |     13 |   72.7 |    4 |    4 | 6.67 | 4.53 | 2.39 | 0.89 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-14B-GGUF:Q4_K_M                                    |          |   4.57 |     62 |   14.8 |    4 |   40 | 7.22 | 4.19 | 1.59 | 1.08 |
| llama3.2-vision:90b-instruct-q4_K_M                                                      |          |   4.50 |     10 |   87.7 |    4 |  128 | 5.61 | 4.79 | 3.78 | 0.65 |
| nemotron:70b-instruct-q8_0                                                               |          |   4.50 |      6 |   70.6 |    8 |  128 | 6.31 | 4.05 | 3.23 | 1.13 |
| mistral-small3.2:24b-instruct-2506-q4_K_M                                                |          |   4.49 |     37 |   24.0 |    4 |  128 | 5.73 | 4.74 | 3.38 | 1.02 |
| hf.co/mistralai/Devstral-Small-2507_gguf:Q4_K_M                                          |          |   4.46 |     38 |   23.6 |    4 |  128 | 6.24 | 4.41 | 2.69 | 1.03 |
| qwen2.5:7b-instruct-q8_0                                                                 |          |   4.34 |     57 |    7.6 |    8 |  128 | 7.47 |  3.6 | 1.13 | 0.51 |
| falcon3:7b-instruct-q8_0                                                                 |          |   4.34 |     58 |    7.5 |    8 |   32 | 6.76 | 3.91 | 2.16 | 0.36 |
| hf.co/Tesslate/UIGEN-T2-7B-Q8_0-GGUF:Q8_0                                                |          |   4.34 |     57 |   7.62 |    8 |   32 | 5.73 | 3.99 | 3.99 | 0.52 |
| hf.co/mradermacher/Viper-Coder-Hybrid-v1.3-GGUF:Q4_K_M                                   |          |   4.32 |     58 |   14.8 |    4 |  128 | 6.44 | 4.45 | 1.83 | 0.46 |
| hf.co/smirki/UIGEN-T1.1-Qwen-7B-Q4_K_M-GGUF:latest                                       |          |   4.29 |    113 |   7.62 |    4 |   32 | 6.06 | 4.53 | 2.08 | 0.88 |
| qwen2.5:7b-instruct-q4_K_M                                                               |          |   4.22 |    111 |    7.6 |    4 |  128 |  7.5 | 2.67 | 1.86 | 0.49 |
| mistral-small3.1:24b-instruct-2503-q4_K_M                                                |          |   4.15 |     35 |   24.0 |    4 |  128 | 5.31 | 4.38 | 3.07 |  1.0 |
| hf.co/Tesslate/Synthia-S1-27b-Q4_K_M-GGUF:Q4_K_M                                         |          |   4.07 |     30 |   27.0 |    4 |  128 | 6.78 | 2.21 | 3.19 | 0.53 |
| hf.co/bartowski/WhiteRabbitNeo_WhiteRabbitNeo-V3-7B-GGUF:Q4_K_M                          |          |   4.06 |    107 |   7.62 |    4 |   32 | 6.43 | 3.36 | 2.01 |  0.8 |
| hf.co/mradermacher/Sky-T1-mini-GGUF:Q4_K_M                                               |          |   4.01 |    105 |   7.62 |    4 |  128 | 7.05 | 3.68 | 0.15 | 0.55 |
| mistral-small:24b-instruct-2501-q4_K_M                                                   |          |   3.98 |     34 |   23.6 |    4 |   32 | 6.32 | 2.89 | 2.47 | 0.93 |
| qwen2.5-coder:7b-instruct-q4_K_M                                                         |          |   3.98 |    105 |    7.6 |    4 |   32 | 4.76 |  4.7 | 2.87 | 0.87 |
| hf.co/bartowski/Tesslate_Tessa-Rust-T1-7B-GGUF:Q4_K_M                                    |          |   3.94 |    104 |   7.62 |    4 |   32 | 6.14 |  3.2 | 2.28 | 0.73 |
| llama4:17b-scout-16e-instruct-q4_K_M                                                     |          |   3.93 |      7 |    109 |    4 | 10240 | 6.07 | 3.16 | 1.99 | 1.58 |
| hf.co/bartowski/open-thoughts_OpenThinker-32B-GGUF:Q4_K_M                                |          |   3.90 |     24 |   32.8 |    4 |   32 |  4.2 | 4.22 | 3.28 | 2.95 |
| goekdenizguelmez/JOSIEFIED-Qwen3:8b-q4_k_m-no_think                                      |          |   3.83 |     94 |    8.2 |    4 |   40 | 6.13 |  3.3 | 1.55 | 0.83 |
| hf.co/mradermacher/Hermes-4-70B-GGUF:Q4_K_M                                              |          |   3.76 |     11 |   70.6 |    4 |  128 | 4.95 | 4.07 | 2.21 | 1.15 |
| phi4-reasoning:14b-plus-q4_K_M                                                           |          |   3.74 |     51 |   14.7 |    4 |   32 | 5.67 | 2.48 |  2.3 | 2.71 |
| gemma3:27b                                                                               |          |   3.73 |     27 |   27.4 |    4 |  128 | 7.15 | 0.14 |  3.8 | 0.64 |
| hf.co/bartowski/HelpingAI_Helpingai3-raw-GGUF:Q4_K_M                                     |          |   3.70 |     72 |   10.3 |    4 |   32 | 5.88 | 3.82 | 0.92 | 0.13 |
| hf.co/bartowski/baidu_ERNIE-4.5-21B-A3B-PT-GGUF:Q4_K_M                                   |          |   3.67 |     34 |   21.8 |    4 |  128 | 5.51 | 3.42 | 2.08 | 0.28 |
| qwen3:4b-q4_K_M-no_think                                                                 |     2.00 |   3.67 |    184 |    4.0 |    4 |   32 | 5.44 | 3.72 | 1.71 | 0.38 |
| gemma2:27b-instruct-q8_0                                                                 |          |   3.65 |     13 |   27.2 |    8 |    8 | 5.18 |  3.3 | 2.47 | 0.98 |
| hf.co/bartowski/microsoft_Phi-4-reasoning-plus-GGUF:Q4_K_M                               |          |   3.63 |     49 |   14.7 |    4 |   32 | 4.36 | 4.76 | 1.93 | 0.72 |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                                                   |          |   3.58 |     10 |   70.6 |    4 |    8 | 6.98 | 1.99 | 0.76 | 0.36 |
| hf.co/bartowski/andrewzh_Absolute_Zero_Reasoner-Coder-7b-GGUF:Q4_K_M                     |          |   3.58 |     94 |   7.62 |    4 |   32 | 5.53 | 2.99 | 2.08 | 0.52 |
| hf.co/mradermacher/Viper-Coder-HybridMini-v1.3-GGUF:Q4_K_M                               |          |   3.55 |     93 |   7.62 |    4 |   32 | 5.18 | 3.51 | 1.99 | 0.24 |
| hf.co/lmstudio-community/INTELLECT-2-GGUF:Q4_K_M                                         |          |   3.53 |     21 |   32.8 |    4 |      | 4.21 | 5.02 |      |      |
| deepseek-coder:6.7b-instruct-q8_0                                                        |          |   3.52 |     50 |    7.0 |    8 |   16 | 5.37 | 3.68 | 0.94 | 0.79 |
| granite4:tiny-h                                                                          |          |   3.48 |    101 |    6.9 |    4 | 1024 | 5.33 | 3.74 | 1.03 |  0.2 |
| hf.co/bartowski/cognitivecomputations_Dolphin-Mistral-24B-Venice-Edition-GGUF:Q4_K_M     |          |   3.43 |     29 |   24.0 |    4 |   32 | 4.78 |  3.2 | 2.18 | 1.21 |
| hf.co/mradermacher/HelpingAI-3-GGUF:Q4_K_M                                               |          |   3.38 |     66 |   10.3 |    4 |   32 |  5.8 | 2.82 | 1.09 |  0.0 |
| hf.co/katanemo/Arch-Function-7B.gguf:Q4_K_M                                              |          |   3.34 |     88 |   7.62 |    4 |   32 | 4.63 | 3.99 | 1.17 | 0.61 |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                                                 |          |   3.34 |     38 |   8.83 |    8 |    4 | 6.54 | 2.11 |  0.4 | 0.09 |
| hf.co/lmstudio-community/Mistral-Small-24B-Instruct-2501-GGUF:Q4_K_M                     |          |   3.33 |     28 |   23.6 |    4 |   32 | 5.21 | 2.86 | 1.54 | 0.79 |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                                         |          |   3.30 |     75 |    8.8 |    4 |   32 | 4.92 | 3.64 | 1.18 | 0.06 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-8B-GGUF:Q4_K_M                                     |          |   3.22 |     79 |   8.19 |    4 |   32 | 5.69 | 2.38 |  1.0 | 0.25 |
| opencoder:8b-instruct-q8_0                                                               |          |   3.21 |     41 |    7.8 |    8 |    8 | 4.63 | 3.22 | 1.62 | 0.72 |
| hf.co/mradermacher/Fathom-R1-14B-GGUF:Q4_K_M                                             |          |   3.21 |     43 |   14.8 |    4 |  128 | 4.65 | 3.32 | 1.57 | 0.38 |
| hf.co/mradermacher/Bespoke-Stratos-7B-GGUF:Q4_K_M                                        |          |   3.16 |     83 |   7.62 |    4 |   32 | 4.72 | 2.67 | 2.26 | 0.23 |
| hf.co/bartowski/simplescaling_s1-32B-GGUF:Q4_K_M                                         |          |   3.11 |     19 |   32.8 |    4 |   32 | 4.33 | 2.29 | 2.78 |  1.4 |
| gemma3:12b                                                                               |          |   3.11 |     51 |   12.2 |    4 |  128 | 5.31 |  0.9 |  3.3 |  0.6 |
| hf.co/bartowski/THUDM_GLM-4-9B-0414-GGUF:Q4_K_M                                          |          |   3.11 |     66 |    9.4 |    4 |   32 | 4.87 |  3.0 | 1.18 | 0.23 |
| qwen2.5-coder:3b-instruct-q4_K_M                                                         |     1.55 |   3.05 |    197 |    3.1 |    4 |   32 | 4.98 | 2.51 | 1.53 | 0.03 |
| exaone3.5:32b-instruct-q8_0                                                              |          |   3.05 |     10 |   32.0 |    8 |   32 | 3.96 | 3.82 | 1.38 | 0.47 |
| deepseek-r1:32b-qwen-distill-q4_K_M                                                      |          |   3.00 |     18 |   32.8 |    4 |  128 | 4.51 | 2.91 | 1.44 | 0.32 |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                                       |          |   2.97 |     78 |   7.62 |    4 |  128 | 6.55 |  0.0 | 1.63 | 0.24 |
| hf.co/bartowski/google_gemma-3-27b-it-qat-GGUF:Q4_0                                      |          |   2.93 |     22 |   27.0 |    4 |  128 | 5.12 | 0.25 | 3.96 | 0.16 |
| hf.co/mradermacher/medgemma-27b-text-it-GGUF:Q4_K_M                                      |          |   2.84 |     21 |   27.0 |    4 |      | 5.41 |  0.0 | 3.22 | 0.31 |
| goekdenizguelmez/JOSIEFIED-Qwen3:4b-q4_0-no_think                                        |          |   2.78 |    139 |    4.0 |    4 |   32 | 4.59 | 2.33 | 1.19 | 0.03 |
| hf.co/bartowski/all-hands_openhands-lm-32b-v0.1-GGUF:Q4_K_M                              |          |   2.72 |     17 |   32.8 |    4 |  128 | 3.28 | 4.55 | 0.14 |  0.2 |
| hf.co/mradermacher/MiniCPM4-8B-GGUF:Q4_K_M                                               |          |   2.65 |     65 |   8.19 |    4 |   32 | 4.14 | 2.38 | 1.36 | 0.05 |
| yi:34b-chat-v1.5-q4_K_M                                                                  |          |   2.63 |     15 |   34.0 |    4 |    4 | 4.25 | 2.63 | 0.58 | 0.24 |
| qwen2.5-coder:3b-instruct-q8_0                                                           |          |   2.62 |     85 |    3.1 |    8 |   32 |  4.2 | 2.15 |  1.4 |  0.2 |
| hf.co/bartowski/Skywork_Skywork-OR1-7B-GGUF:Q4_K_M                                       |          |   2.56 |     73 |      7 |    4 |  128 | 3.72 |  2.6 |      |      |
| hf.co/bartowski/google_gemma-3-12b-it-qat-GGUF:Q4_0                                      |          |   2.55 |     43 |   11.8 |    4 |  128 | 4.64 | 0.68 | 2.42 | 0.08 |
| yi:9b-chat-v1.5-q4_K_M                                                                   |          |   2.54 |     56 |    9.0 |    4 |    4 | 4.04 | 2.71 | 0.39 | 0.33 |
| hf.co/bartowski/soob3123_GrayLine-Qwen3-8B-GGUF:Q4_K_M-no_think                          |          |   2.48 |     61 |   8.19 |    4 |      | 3.82 | 2.19 | 1.03 | 0.91 |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                                                |          |   2.45 |      7 |   34.4 |    8 |    4 | 4.61 | 1.49 | 0.72 | 0.16 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-4B-GGUF:Q4_K_M                                     |          |   2.33 |    106 |   4.41 |    4 |   32 | 2.75 | 3.43 | 0.83 | 0.34 |
| exaone3.5:7.8b-instruct-q8_0                                                             |          |   2.28 |     29 |    7.8 |    8 |   32 | 3.76 | 2.26 | 0.17 | 0.68 |
| qwen3:235b-a22b-q4_K_M-think                                                             |          |   2.28 |      2 |  235.1 |    4 |  128 | 2.86 | 2.27 | 2.17 | 0.25 |
| qwen:110b-chat-v1.5-q4_K_M                                                               |          |   2.25 |      4 |  111.0 |    4 |   32 | 3.63 | 1.84 | 0.76 | 0.92 |
| phi3:14b-medium-128k-instruct-q8_0                                                       |          |   2.24 |     16 |   14.0 |    8 |  128 | 4.21 | 1.55 | 0.42 | 0.04 |
| hf.co/bartowski/THUDM_GLM-Z1-32B-0414-GGUF:Q4_K_M                                        |          |   2.24 |     14 |   32.6 |    4 |   32 | 3.13 | 1.58 |  2.0 |  1.1 |
| mlx-community/Ring-mini-2.0-4bit                                                         |          |   2.20 |     27 |   16.0 |    4 |   32 | 2.42 | 2.69 | 1.72 | 0.76 |
| granite4:micro                                                                           |          |   2.17 |    127 |    3.4 |    4 |  128 | 3.53 | 1.77 | 1.09 | 0.04 |
| hf.co/jedisct1/MiMo-7B-RL-GGUF:Q4_K_M                                                    |          |   2.10 |     60 |      7 |    4 |   32 | 3.74 | 1.94 | 0.13 |  0.0 |
| qwen2.5vl:7b-q4_K_M                                                                      |          |   2.09 |     50 |    8.3 |    4 |  128 | 3.48 | 1.64 | 0.97 | 0.13 |
| llama3.1:8b-instruct-q8_0                                                                |          |   2.03 |     25 |    8.0 |    8 |  128 | 3.26 | 1.78 | 0.94 | 0.09 |
| qwq:32b-q4_K_M                                                                           |          |   2.02 |     12 |   32.8 |    4 |  128 | 2.51 | 1.75 | 1.32 | 2.25 |
| tulu3:8b-q8_0                                                                            |          |   2.01 |     25 |    8.0 |    8 |  128 | 3.91 | 1.06 | 0.42 | 0.49 |
| granite4:micro-h                                                                         |          |   2.01 |    126 |    3.2 |    4 | 1024 | 3.27 | 1.79 | 0.77 | 0.14 |
| qwen3:1.7b-q4_K_M-think                                                                  |     1.00 |   1.97 |    197 |    2.0 |    4 |   32 | 3.97 | 0.94 | 0.48 | 0.04 |
| hf.co/bartowski/andrewzh_Absolute_Zero_Reasoner-Coder-3b-GGUF:Q4_K_M                     |          |   1.97 |    127 |   3.09 |    4 |   32 | 3.75 | 0.86 | 0.86 | 0.36 |
| hf.co/bartowski/open-r1_OlympicCoder-7B-GGUF:Q4_K_M                                      |          |   1.93 |     55 |    7.0 |    4 |   32 | 2.43 | 2.86 | 0.31 | 0.33 |
| hf.co/bartowski/Alibaba-NLP_Tongyi-DeepResearch-30B-A3B-GGUF:Q4_K_M                      |          |   1.91 |     12 |   30.5 |    4 |  128 | 2.47 | 2.55 | 0.74 | 0.04 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                                                 |          |   1.87 |     31 |   6.06 |    8 |    4 | 3.92 | 0.92 | 0.13 |  0.0 |
| hf.co/mradermacher/olmOCR-7B-0725-GGUF:Q4_K_M                                            |          |   1.81 |     48 |   7.62 |    4 |  128 | 3.66 | 0.65 | 0.74 | 0.03 |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                                               |          |   1.81 |     60 |   6.06 |    4 |    4 | 3.71 | 0.87 | 0.32 |  0.0 |
| deepseek-llm:67b-chat-q4_K_M                                                             |          |   1.79 |      5 |   67.0 |    4 |    4 | 2.94 | 1.63 |  0.5 | 0.23 |
| hf.co/katanemo/Arch-Function-3B.gguf:Q4_K_M                                              |          |   1.76 |    114 |   3.09 |    4 |   32 | 2.81 | 1.55 | 0.66 | 0.43 |
| qwen2.5:3b-instruct-q4_K_M                                                               |          |   1.70 |    110 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.56 | 0.05 |
| deepseek-r1:70b-llama-distill-q4_K_M                                                     |          |   1.69 |      5 |   70.6 |    4 |  128 | 2.17 | 2.49 | 0.19 | 0.41 |
| deepseek-r1:14b-qwen-distill-q4_K_M                                                      |          |   1.69 |     23 |   14.8 |    4 |  128 |  2.6 | 1.02 | 1.19 | 1.04 |
| qwen2.5:3b                                                                               |          |   1.67 |    108 |    3.1 |    4 |  128 | 2.95 | 1.35 | 0.42 | 0.05 |
| llama3.2-vision:11b-instruct-q4_K_M                                                      |          |   1.67 |     34 |    9.8 |    4 |  128 | 3.13 | 1.21 | 0.21 | 0.11 |
| hf.co/mradermacher/Kimi-VL-A3B-Thinking-2506-GGUF:Q4_K_M                                 |          |   1.66 |     21 |   16.0 |    4 |  128 | 2.35 | 1.27 | 1.43 | 0.53 |
| yi-coder:1.5b-chat-q4_K_M                                                                |     0.75 |   1.65 |    220 |    1.5 |    4 |  128 | 3.49 | 0.61 | 0.34 |  0.0 |
| gemma2:9b-instruct-q8_0                                                                  |          |   1.63 |     18 |    9.2 |    8 |    8 | 2.46 | 1.55 | 0.86 | 0.12 |
| granite3.1-dense:8b-instruct-q8_0                                                        |          |   1.59 |     19 |    8.2 |    8 |  128 | 2.73 | 1.55 | 0.16 | 0.03 |
| hf.co/katanemo/Arch-Function-1.5B.gguf:Q4_K_M                                            |          |   1.56 |    203 |   1.54 |    4 |   32 | 2.44 |  1.6 | 0.53 | 0.02 |
| granite3.2:8b-instruct-q4_K_M                                                            |          |   1.50 |     37 |    8.2 |    4 |  128 | 2.53 | 1.43 |  0.3 |  0.0 |
| codegemma:7b-instruct-v1.1-q4_K_M                                                        |          |   1.46 |     33 |    9.0 |    4 |    8 | 2.21 | 1.49 | 0.66 | 0.01 |
| hf.co/mradermacher/olmOCR-7B-0825-GGUF:Q4_K_M                                            |          |   1.46 |     38 |   7.62 |    4 |  128 | 2.65 | 0.99 | 0.36 | 0.33 |
| exaone3.5:2.4b-instruct-q8_0                                                             |          |   1.45 |     54 |    2.7 |    8 |   32 | 2.73 | 0.94 | 0.28 | 0.15 |
| deepseek-r1:7b-qwen-distill-q4_K_M                                                       |          |   1.43 |     38 |    7.6 |    4 |  128 | 2.64 |  1.1 |  0.0 | 0.46 |
| qwen2.5:3b-instruct-q8_0                                                                 |          |   1.43 |     46 |    3.1 |    8 |  128 | 2.87 | 0.59 | 0.44 | 0.18 |
| opencoder:1.5b-instruct-q8_0                                                             |          |   1.42 |     75 |    1.9 |    8 |    4 |  2.2 | 1.47 |  0.5 |  0.0 |
| yi-coder:1.5b-chat-q8_0                                                                  |          |   1.36 |     91 |    1.5 |    8 |  128 | 2.32 | 1.17 | 0.42 |  0.0 |
| cogito:8b-v1-preview-llama-q4_K_M                                                        |          |   1.34 |     34 |      8 |    4 |  128 | 2.32 | 1.02 | 0.54 |  0.0 |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                                       |     0.75 |   1.31 |    174 |    1.5 |    4 |   32 | 2.26 |  0.8 |  0.8 | 0.03 |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                                        |          |   1.30 |      6 |   46.7 |    4 |   32 |  2.0 | 1.24 | 0.62 |  0.0 |
| qwen2-math:7b-instruct-q8_0                                                              |          |   1.28 |     17 |    7.6 |    8 |    4 | 2.49 | 0.95 | 0.02 |  0.0 |
| dolphin3:8b-llama3.1-q8_0                                                                |          |   1.27 |     16 |    8.0 |    8 |  128 |  2.3 | 0.89 | 0.26 | 0.31 |
| goekdenizguelmez/JOSIEFIED-Qwen3:1.7b-q4_0-think                                         |          |   1.25 |    125 |    2.0 |    4 |   32 |  2.1 | 1.26 | 0.18 |  0.0 |
| hf.co/mradermacher/MiniCPM4.1-8B-GGUF:Q4_K_M                                             |          |   1.25 |     31 |   8.19 |    4 |   64 | 1.56 | 1.46 | 0.79 | 0.33 |
| qwen2.5-coder:1.5b-instruct-q8_0                                                         |          |   1.22 |     81 |    1.5 |    8 |   32 | 2.04 |  0.9 | 0.66 | 0.03 |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0                          |          |   1.21 |     15 |   8.03 |    8 |  128 | 2.29 | 0.47 | 0.58 | 0.37 |
| codegemma:7b-instruct-q8_0                                                               |          |   1.19 |     13 |    9.0 |    8 |    8 | 1.84 | 1.27 | 0.39 |  0.0 |
| gemma3:4b                                                                                |          |   1.17 |     55 |    4.3 |    4 |  128 | 2.09 | 0.61 | 0.77 |  0.0 |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                                         |          |   1.16 |     15 |    8.0 |    8 |    8 | 1.51 | 1.65 |  0.3 | 0.03 |
| hf.co/mradermacher/HelpingAI-15B-GGUF:Q4_K_M                                             |          |   1.16 |     15 |   15.3 |    4 |    4 | 2.42 | 0.64 |  0.0 |  0.0 |
| falcon3:3b-instruct-q8_0                                                                 |          |   1.16 |     36 |    3.2 |    8 |   32 | 1.89 | 1.09 | 0.36 | 0.04 |
| hf.co/TheDrummer/Rivermind-12B-v1-GGUF:Q4_K_M                                            |          |   1.14 |     19 |   12.2 |    4 |   32 | 1.72 | 1.08 | 0.61 | 0.08 |
| qwen2.5:1.5b-instruct-q8_0                                                               |          |   1.14 |     76 |    1.5 |    8 |  128 | 2.07 | 0.82 | 0.29 | 0.06 |
| deepseek-r1:8b-llama-distill-q4_K_M                                                      |          |   1.12 |     28 |    8.0 |    4 |  128 | 1.46 | 1.25 | 0.45 | 0.67 |
| hf.co/bartowski/THUDM_GLM-Z1-9B-0414-GGUF:Q4_K_M                                         |          |   1.08 |     23 |    9.4 |    4 |   32 | 0.99 | 1.74 | 0.57 | 0.51 |
| qwen2.5vl:3b-q4_K_M                                                                      |          |   1.07 |     57 |    3.8 |    4 |  128 | 1.88 | 0.61 | 0.69 | 0.01 |
| hf.co/bartowski/nvidia_Llama-3.1-Nemotron-Nano-4B-v1.1-GGUF:Q4_K_M                       |          |   1.07 |     48 |   4.51 |    4 |  128 | 2.59 |  0.1 | 0.03 |  0.0 |
| granite3.3:2b                                                                            |          |   1.04 |    104 |    2.0 |    4 |  128 | 2.19 | 0.54 | 0.02 |  0.0 |
| openchat:7b-v3.5-q8_0                                                                    |          |   1.02 |     15 |    7.0 |    8 |    8 | 1.62 | 1.21 | 0.06 |  0.0 |
| hf.co/bartowski/Zyphra_ZR1-1.5B-GGUF:Q4_K_M                                              |     0.75 |   1.02 |    136 |    1.5 |    4 |  128 | 1.64 | 0.34 | 1.04 | 0.51 |
| granite3.3:8b                                                                            |          |   0.98 |     24 |    8.0 |    4 |  128 | 1.67 | 0.78 | 0.25 | 0.27 |
| gemma3n:e2b                                                                              |          |   0.97 |     43 |    4.5 |    4 |    8 | 2.21 | 0.23 | 0.11 |  0.0 |
| codellama:34b-instruct-q4_K_M                                                            |          |   0.93 |      5 |   34.0 |    4 |   16 | 1.29 | 0.99 | 0.56 | 0.04 |
| gemma3n:e4b                                                                              |          |   0.92 |     27 |    6.9 |    4 |   32 | 2.04 |  0.0 |  0.5 |  0.0 |
| exaone-deep:7.8b-q4_K_M                                                                  |          |   0.90 |     23 |    7.8 |    4 |   32 | 1.83 |  0.4 | 0.24 |  0.0 |
| qwen:32b-chat-v1.5-q4_K_M                                                                |          |   0.90 |      5 |   33.0 |    4 |   32 | 1.54 | 0.81 | 0.13 | 0.12 |
| yi:6b-chat-v1.5-q4_K_M                                                                   |          |   0.89 |     30 |    6.0 |    4 |    4 | 0.79 | 1.48 | 0.62 | 0.01 |
| qwen2.5:1.5b-instruct-q4_K_M                                                             |     0.75 |   0.88 |    118 |    1.5 |    4 |  128 | 1.94 | 0.26 | 0.15 |  0.0 |
| hf.co/bartowski/open-r1_OlympicCoder-32B-GGUF:Q4_K_M                                     |          |   0.88 |      5 |   32.8 |    4 |   32 | 1.54 | 0.32 | 0.58 | 0.53 |
| hf.co/allenai/OLMo-2-0325-32B-Instruct-GGUF:Q4_0                                         |          |   0.86 |      5 |   32.2 |    4 |    4 | 1.32 | 0.77 | 0.51 |  0.0 |
| hf.co/mradermacher/medgemma-4b-it-GGUF:Q4_K_M                                            |          |   0.84 |     43 |   3.88 |    4 |      | 1.46 |  0.2 | 0.68 | 0.62 |
| deepcoder:1.5b-preview-q4_K_M                                                            |     0.75 |   0.82 |    110 |    1.5 |    4 |  128 | 1.93 | 0.15 |  0.0 | 0.08 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-2B-GGUF:Q4_K_M                                     |          |   0.82 |     81 |   2.03 |    4 |   40 | 1.54 | 0.57 | 0.12 | 0.12 |
| mixtral:8x7b-instruct-v0.1-q8_0                                                          |          |   0.82 |      2 |   46.7 |    8 |   32 | 1.44 | 0.65 | 0.23 |  0.0 |
| hf.co/bartowski/google_gemma-3-4b-it-qat-GGUF:Q4_0                                       |          |   0.81 |     42 |   3.88 |    4 |  128 | 1.74 | 0.35 | 0.03 | 0.03 |
| hf.co/mradermacher/HelpingAI-9B-GGUF:Q4_K_M                                              |          |   0.78 |     18 |   8.83 |    4 |    4 | 1.64 | 0.41 |  0.0 |  0.0 |
| qwen3:1.7b-q4_K_M-no_think                                                               |          |   0.77 |     76 |    2.0 |    4 |   32 | 1.08 | 0.99 | 0.18 |  0.0 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q4_K_M                                                     |          |   0.76 |     59 |   2.57 |    4 |      | 1.86 | 0.04 |  0.0 |  0.0 |
| hf.co/bartowski/OpenThinker-7B-GGUF:Q4_K_M                                               |          |   0.75 |     20 |   7.62 |    4 |   32 | 0.88 | 0.77 | 0.53 | 0.62 |
| exaone-deep:32b-q4_K_M                                                                   |          |   0.70 |      4 |   32.0 |    4 |   32 | 0.93 | 0.66 | 0.36 | 0.53 |
| command-r7b:7b-12-2024-q4_K_M                                                            |          |   0.68 |     17 |    8.0 |    4 |  128 | 1.54 | 0.03 | 0.26 | 0.04 |
| goekdenizguelmez/JOSIEFIED-Qwen3:4b-q4_0-think                                           |          |   0.68 |     34 |    4.0 |    4 |   40 | 0.97 | 0.84 | 0.18 |  0.0 |
| llama3.2:3b                                                                              |          |   0.66 |     41 |    3.2 |    4 |  128 | 1.42 | 0.18 | 0.21 |  0.0 |
| olmo2:13b-1124-instruct-q4_K_M                                                           |          |   0.66 |     10 |   13.7 |    4 |    4 | 1.59 | 0.06 | 0.01 | 0.03 |
| internlm2:7b-chat-v2.5-q4_K_M                                                            |          |   0.66 |     17 |    7.7 |    4 |   32 |  1.1 | 0.41 | 0.47 |  0.0 |
| goekdenizguelmez/JOSIEFIED-Qwen3:1.7b-q4_0-no_think                                      |          |   0.64 |     64 |    2.0 |    4 |   32 | 1.42 | 0.25 | 0.01 |  0.0 |
| hf.co/bartowski/agentica-org_DeepScaleR-1.5B-Preview-GGUF:Q4_K_M                         |          |   0.64 |     72 |   1.78 |    4 |  128 | 1.28 |  0.4 | 0.03 | 0.05 |
| qwen:72b-chat-v1.5-q4_K_M                                                                |          |   0.64 |      2 |   72.0 |    4 |   32 | 0.94 | 0.78 | 0.13 |  0.0 |
| olmo2:7b-1124-instruct-q4_K_M                                                            |          |   0.60 |     16 |    7.3 |    4 |    4 | 1.42 | 0.08 | 0.02 |  0.0 |
| hf.co/mradermacher/GLM-4.5-Air-GGUF:Q2_K                                                 |          |   0.59 |      2 |  110.0 |    2 |  128 | 0.64 | 0.35 | 0.93 | 0.42 |
| qwen2.5:0.5b-instruct-q8_0                                                               |     0.50 |   0.57 |    115 |    0.5 |    8 |  128 | 1.33 |  0.0 | 0.21 |  0.0 |
| deepcoder:14b-preview-q4_K_M                                                             |          |   0.57 |      8 |   14.8 |    4 |  128 | 1.03 | 0.33 | 0.28 |  0.0 |
| hf.co/mradermacher/Seed-Coder-8B-Reasoning-GGUF:Q4_K_M                                   |          |   0.54 |     13 |   8.25 |    4 |      | 1.06 | 0.38 |  0.0 | 0.03 |
| internlm2:1.8b-chat-v2.5-q4_K_M                                                          |          |   0.51 |     54 |    1.9 |    4 |   32 | 1.24 | 0.06 |  0.0 |  0.0 |
| hf.co/bartowski/nvidia_Llama-3_3-Nemotron-Super-49B-v1_5-GGUF:Q4_K_M                     |          |   0.51 |      2 |   49.9 |    4 |  128 | 0.79 |      |      |      |
| granite3.1-dense:2b-instruct-q8_0                                                        |          |   0.50 |     20 |    2.5 |    8 |  128 | 1.07 | 0.11 |  0.2 |  0.0 |
| llama3.2:latest                                                                          |          |   0.49 |     31 |   3.21 |    4 |  128 | 0.99 | 0.18 | 0.21 |  0.0 |
| exaone-deep:2.4b-q4_K_M                                                                  |          |   0.48 |     36 |    2.7 |    4 |   32 | 0.88 | 0.32 | 0.04 | 0.28 |
| codellama:13b-instruct-q4_K_M                                                            |          |   0.48 |      7 |   13.0 |    4 |   16 | 0.52 | 0.84 | 0.05 | 0.08 |
| hf.co/openbmb/MiniCPM-o-2_6-gguf:Q4_K_M                                                  |          |   0.48 |     13 |   7.61 |    4 |   32 | 1.03 | 0.19 | 0.04 |  0.0 |
| hf.co/trillionlabs/Trillion-7B-preview-GGUF:Q4_K_M                                       |          |   0.47 |     13 |   7.53 |    4 |    4 | 0.98 | 0.09 | 0.21 | 0.11 |
| smallthinker:3b-preview-q4_K_M                                                           |          |   0.47 |     27 |    3.4 |    4 |  128 | 0.98 | 0.25 |  0.0 |  0.0 |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                                                     |          |   0.46 |     51 |    1.8 |    4 |  128 | 0.87 | 0.24 | 0.03 | 0.37 |
| cogito:3b-v1-preview-llama-q4_K_M                                                        |          |   0.46 |     29 |   3.21 |    4 |  128 | 0.94 | 0.25 | 0.04 | 0.03 |
| hf.co/LiquidAI/LFM2-2.6B-GGUF:Q8_0                                                       |          |   0.46 |        |   2.57 |      |      | 0.94 | 0.24 | 0.04 |  0.0 |
| hf.co/TheBloke/Yi-34B-Chat-GGUF:Q4_K_M                                                   |          |   0.44 |      3 |   34.4 |    4 |    4 | 0.67 | 0.56 | 0.03 |  0.0 |
| granite3.2:2b-instruct-q4_K_M                                                            |          |   0.42 |     34 |    2.5 |    4 |  128 | 0.85 | 0.16 | 0.15 | 0.05 |
| mistral:7b-instruct-q4_K_M                                                               |          |   0.41 |     12 |    7.0 |    4 |   32 | 0.48 | 0.71 | 0.04 |  0.0 |
| smallthinker:3b-preview-q8_0                                                             |          |   0.41 |     12 |    3.4 |    8 |  128 | 0.81 | 0.19 | 0.03 | 0.19 |
| phi:2.7b-chat-v2-q4_K_M                                                                  |          |   0.39 |     26 |    3.0 |    4 |    2 | 0.91 | 0.07 |  0.0 |  0.0 |
| vicuna:33b-q4_K_M                                                                        |          |   0.38 |      3 |   30.0 |    4 |    2 |  0.9 | 0.06 |  0.0 |  0.0 |
| granite3.1-moe:3b-instruct-q8_0                                                          |          |   0.35 |     11 |    3.3 |    8 |  128 |  0.8 | 0.03 | 0.11 | 0.03 |
| qwen3:0.6b-q4_K_M-think                                                                  |     0.38 |   0.28 |     76 | 0.75163 |    4 |   32 | 0.53 |  0.0 | 0.36 |  0.0 |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                                                |          |   0.27 |      4 |   7.62 |    8 |  128 | 0.27 | 0.54 |  0.0 |  0.0 |
| qwen2-math:1.5b-instruct-q8_0                                                            |          |   0.27 |     18 |    1.5 |    8 |    4 | 0.65 | 0.03 |  0.0 |  0.0 |
| gemma2:2b-instruct-q8_0                                                                  |          |   0.23 |      9 |    2.6 |    8 |    8 | 0.39 | 0.22 | 0.03 |  0.0 |
| qwen3:0.6b-q4_K_M-no_think                                                               |     0.38 |   0.22 |     59 | 0.75163 |    4 |   32 | 0.48 |  0.1 |  0.0 |  0.0 |
| hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M                                      |          |   0.22 |      6 |   6.92 |    4 |    2 | 0.51 | 0.04 | 0.01 |  0.0 |
| openbmb/minicpm-v4:4b                                                                    |          |   0.21 |     12 |    3.6 |    4 |   32 | 0.52 |  0.0 | 0.01 |  0.0 |
| goekdenizguelmez/JOSIEFIED-Qwen3:0.6b-q4_0-think                                         |     0.38 |   0.21 |     55 | 0.75163 |    4 |   40 | 0.49 | 0.04 |  0.0 |  0.0 |
| codellama:7b-instruct-q4_K_M                                                             |          |   0.21 |      6 |    7.0 |    4 |   16 | 0.33 | 0.03 | 0.33 | 0.01 |
| deepseek-llm:7b-chat-q8_0                                                                |          |   0.20 |      3 |    7.0 |    8 |    4 | 0.46 | 0.06 |  0.0 |  0.0 |
| hf.co/QuantFactory/HelpingAI-3B-coder-GGUF:Q4_K_M                                        |          |   0.20 |     11 |   3.48 |    4 |  128 | 0.31 | 0.22 |  0.0 |  0.1 |
| goekdenizguelmez/JOSIEFIED-Qwen3:0.6b-q4_0-no_think                                      |     0.38 |   0.20 |     53 | 0.75163 |    4 |   40 | 0.49 |  0.0 | 0.01 |  0.0 |
| llama3.2:1b-instruct-q4_K_M                                                              |          |   0.18 |     15 |    1.2 |    8 |  128 | 0.41 | 0.06 |  0.0 |  0.0 |
| hf.co/mradermacher/Qwen3-0.6B-Code-Expert-GGUF:Q4_K_M-no_think                           |          |   0.18 |      0 |  596.0 |    4 |   40 | 0.44 |  0.0 |  0.0 |  0.0 |
| phi3:3.8b                                                                                |          |   0.17 |      9 |    3.8 |    4 |  128 | 0.39 | 0.04 | 0.03 |  0.0 |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                                        |          |   0.16 |      0 |   72.7 |    4 |   32 | 0.31 |  0.0 | 0.08 | 0.16 |
| hf.co/bartowski/OpenGVLab_InternVL3_5-1B-GGUF:Q4_K_M                                     |          |   0.15 |      0 |  752.0 |    4 |   40 | 0.36 | 0.03 | 0.01 |  0.0 |
| gemma3:1b                                                                                |          |   0.15 |     30 |    1.0 |    4 |   32 | 0.13 | 0.33 |  0.0 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                                       |     0.25 |   0.15 |     60 |    0.5 |    4 |   32 | 0.36 | 0.01 | 0.01 |  0.0 |
| qwen2.5:0.5b-instruct-q4_K_M                                                             |     0.25 |   0.15 |     58 |    0.5 |    4 |  128 | 0.36 |  0.0 | 0.01 |  0.0 |
| qwen2.5-coder:0.5b-instruct-q8_0                                                         |          |   0.14 |     28 |    0.5 |    8 |   32 | 0.33 | 0.01 | 0.03 |  0.0 |
| llama2:70b-chat-q4_K_M                                                                   |          |   0.14 |      0 |   69.0 |    4 |    4 | 0.31 | 0.03 | 0.01 | 0.03 |
| llama3.2:1b-instruct-q8_0                                                                |          |   0.13 |     11 |    1.2 |    8 |  128 | 0.28 | 0.06 |  0.0 |  0.0 |
| hf.co/mradermacher/MediPhi-Instruct-GGUF:Q4_K_M                                          |          |   0.13 |      7 |   3.82 |    4 |  128 | 0.31 | 0.01 |  0.0 |  0.0 |
| hf.co/bartowski/google_gemma-3-1b-it-qat-GGUF:Q4_0                                       |          |   0.12 |     25 |    1.0 |    4 |   32 | 0.29 | 0.03 |  0.0 |  0.0 |
| falcon:7b-instruct-q4_0                                                                  |          |   0.11 |      3 |    7.0 |    4 |    2 | 0.28 |  0.0 |  0.0 |  0.0 |
| falcon:40b-instruct-q4_0                                                                 |          |   0.11 |      1 |   40.0 |    4 |    2 | 0.07 |  0.0 | 0.42 |  0.0 |
| hf.co/LiquidAI/LFM2-1.2B-GGUF:Q4_K_M                                                     |          |   0.11 |     19 |   1.17 |    4 |      | 0.25 | 0.03 |  0.0 |  0.0 |
| phi4-mini:3.8b-q4_K_M                                                                    |          |   0.11 |      6 |    3.8 |    4 |  128 | 0.23 | 0.04 | 0.01 |  0.0 |
| falcon3:1b-instruct-q8_0                                                                 |          |   0.10 |      6 |    1.7 |    8 |    8 | 0.25 |  0.0 |  0.0 |  0.0 |
| hf.co/mradermacher/MiniCPM4-0.5B-GGUF:Q4_K_M                                             |          |   0.10 |      0 |  434.0 |    4 |      | 0.23 | 0.02 |  0.0 |  0.0 |
| granite3.1-moe:1b-instruct-q8_0                                                          |          |   0.10 |      7 |    1.3 |    8 |  128 | 0.24 |  0.0 |  0.0 |  0.0 |
| qwen:14b-chat-v1.5-q4_K_M                                                                |          |   0.08 |      1 |   14.0 |    4 |   32 | 0.15 |  0.0 | 0.08 |  0.0 |
| hf.co/bartowski/burtenshaw_GemmaCoder3-12B-GGUF:Q4_K_M                                   |          |   0.06 |      1 |   11.8 |    4 |  128 | 0.04 | 0.14 | 0.03 |  0.0 |
| qwen:1.8b-chat-v1.5-q4_K_M                                                               |          |   0.06 |      6 |    2.0 |    4 |   32 |  0.0 |  0.0 |  0.0 | 0.62 |
| hf.co/LiquidAI/LFM2-350M-GGUF:Q4_K_M                                                     |     0.18 |   0.06 |     32 |  0.354 |    4 |      | 0.14 |  0.0 |  0.0 |  0.0 |
| hf.co/mradermacher/MiMo-VL-7B-RL-GGUF:Q4_K_M-no_think                                    |          |   0.06 |      1 |   7.62 |    4 |  128 | 0.14 |  0.0 |  0.0 |  0.0 |
| hf.co/sizzlebop/Holo1-7B-Q4_K_M-GGUF                                                     |          |   0.05 |      1 |    7.0 |    4 |  128 | 0.13 |  0.0 |  0.0 |  0.0 |
| vicuna:13b-q4_K_M                                                                        |          |   0.04 |      1 |   13.0 |    4 |    2 | 0.09 | 0.01 |  0.0 |  0.0 |
| granite3.2-vision:2b-q4_K_M                                                              |          |   0.04 |      3 |    2.5 |    4 |   16 | 0.07 | 0.03 |  0.0 |  0.0 |
| vicuna:13b-v1.5-16k-q4_K_M                                                               |          |   0.03 |      1 |   13.0 |    4 |    2 | 0.06 | 0.03 |  0.0 |  0.0 |
| qwen2:0.5b-instruct-q8_0                                                                 |          |   0.03 |      0 | 494.03 |    8 |   32 | 0.07 |  0.0 |  0.0 |  0.0 |
| starcoder2:3b                                                                            |          |   0.03 |      2 |    3.0 |    4 |   16 | 0.07 |  0.0 |  0.0 |  0.0 |
| llama2:13b-chat-q4_K_M                                                                   |          |   0.03 |      0 |   13.0 |    4 |    4 | 0.06 | 0.01 |  0.0 |  0.0 |
| hf.co/mradermacher/Holo1-3B-GGUF:Q4_K_M                                                  |          |   0.03 |      2 |   3.09 |    4 |  128 | 0.06 |  0.0 |  0.0 | 0.03 |
| vicuna:7b-v1.5-16k-q4_K_M                                                                |          |   0.01 |      0 |    7.0 |    4 |    4 | 0.03 |  0.0 |  0.0 |  0.0 |
| qwen:7b-chat-v1.5-q4_K_M                                                                 |          |   0.01 |      0 |    8.0 |    4 |   32 | 0.02 |  0.0 |  0.0 | 0.03 |
| deepseek-coder:1.3b-instruct-q8_0                                                        |          |   0.01 |      1 |    1.0 |    8 |   16 |  0.0 | 0.02 |  0.0 |  0.0 |
| gemma3:270m                                                                              |          |   0.00 |      1 |   0.27 |    8 |   32 | 0.01 |  0.0 |  0.0 |  0.0 |
| hf.co/allenai/OLMo-2-0425-1B-Instruct-GGUF:Q4_K_M                                        |          |   0.00 |      1 |   1.48 |    4 |    4 | 0.01 |  0.0 |  0.0 |  0.0 |
| llama2:7b-chat-q4_K_M                                                                    |          |   0.00 |      0 |    7.0 |    4 |    4 | 0.01 |  0.0 |  0.0 |  0.0 |
| deepseek-r1:8b-0528-qwen3-q4_K_M                                                         |          |   0.00 |      0 |    8.2 |    4 |  160 | 0.01 |  0.0 |  0.0 |  0.0 |
| smollm:135m-instruct-v0.2-q8_0                                                           |     0.14 |   0.00 |      0 |  0.135 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:1.7b-instruct-v0.2-q8_0                                                           |          |   0.00 |      0 |    1.7 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| smollm:360m-instruct-v0.2-q8_0                                                           |          |   0.00 |      0 |   0.36 |    8 |    2 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:0.5b-chat-v1.5-q4_K_M                                                               |          |   0.00 |      0 |  620.0 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| qwen:4b-chat-v1.5-q4_K_M                                                                 |          |   0.00 |      0 |    4.0 |    4 |   32 |  0.0 |  0.0 |  0.0 |  0.0 |
| codegemma:2b-code-v1.1-q4_K_M                                                            |          |   0.00 |      0 |    3.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |
| vicuna:7b-q4_K_M                                                                         |          |   0.00 |      0 |    7.0 |    4 |      |  0.0 |  0.0 |  0.0 |  0.0 |
| phi4-mini-reasoning:3.8b-q4_K_M                                                          |          |   0.00 |      0 |    3.8 |    4 |  128 |  0.0 |  0.0 |  0.0 |  0.0 |

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
