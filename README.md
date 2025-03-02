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

| Model                                                                | Best<br/>Model<br/>for<br/>Size (GB) | PE-<br/>Score<br/>(Superhuman<br/>Factor) | Memory-<br/>Score | Size<br/>(*10^9 Params) | Bits | Context Length<br/>(K) | PE-Bench-100 Details |
| :------------------------------------------------------------------- | -----------------------------------: | ----------------------------------------: | ----------------: | ----------------------: | ---: | ---------------------: | -------------------: |
| DeepSeek-V3                                                          |  1342.00 |  16.11 |      1 |  671.0 |   16 |   64 | `Python:  20.01`<br/>`Java:    16.95`<br/>`Rust:    12.16`<br/>`Clojure: 5.92` |
| GPT-4o                                                               |          |  14.72 |        |        |   16 |  128 | `Python:  17.05`<br/>`Java:    13.87`<br/>`Rust:    14.57`<br/>`Clojure: 8.24` |
| GPT-o1-Mini                                                          |          |  11.05 |        |        |   16 |      | `Python:  17.44`<br/>`Java:    `<br/>`Rust:    `<br/>`Clojure: ` |
| athene-v2:72b-q8_0                                                   |    72.70 |  10.97 |     15 |   72.7 |    8 |  128 | `Python:  16.22`<br/>`Java:    10.15`<br/>`Rust:    5.55`<br/>`Clojure: 3.32` |
| hf.co/bartowski/Athene-V2-Agent-GGUF:Q4_K_M                          |    36.35 |  10.60 |     29 |   72.7 |    4 |  128 | `Python:  14.49`<br/>`Java:    10.56`<br/>`Rust:    6.33`<br/>`Clojure: 3.74` |
| athene-v2:latest                                                     |    36.35 |  10.44 |     29 |   72.7 |    4 |  128 | `Python:  14.07`<br/>`Java:    11.14`<br/>`Rust:    6.55`<br/>`Clojure: 1.62` |
| hf.co/bartowski/Sky-T1-32B-Preview-GGUF:Q4_K_M                       |    16.40 |  10.33 |     63 |   32.8 |    4 |   32 | `Python:  12.72`<br/>`Java:    11.67`<br/>`Rust:    7.25`<br/>`Clojure: 2.89` |
| GPT-o1-Preview                                                       |          |  10.05 |        |        |   16 |      | `Python:  15.86`<br/>`Java:    `<br/>`Rust:    `<br/>`Clojure: ` |
| qwen2.5:72b-instruct-q4_K_M                                          |          |   9.78 |     27 |   72.7 |    4 |  128 | `Python:  14.02`<br/>`Java:    9.1`<br/>`Rust:    5.97`<br/>`Clojure: 2.46` |
| qwen2.5:72b-instruct-q8_0                                            |          |   9.77 |     13 |   72.7 |    8 |  128 | `Python:  12.98`<br/>`Java:    10.5`<br/>`Rust:    5.41`<br/>`Clojure: 3.49` |
| qwen2.5-coder:32b-instruct-q4_K_M                                    |    16.40 |   9.77 |     60 |   32.8 |    4 |   32 | `Python:  14.05`<br/>`Java:    8.82`<br/>`Rust:    6.41`<br/>`Clojure: 2.2` |
| hf.co/mradermacher/Qwen2.5-72B-Instruct-abliterated-GGUF:Q4_K_M      |          |   9.69 |     27 |   72.7 |    4 |  128 | `Python:  13.92`<br/>`Java:    8.65`<br/>`Rust:    6.11`<br/>`Clojure: 3.07` |
| hf.co/bartowski/Sky-T1-32B-Flash-GGUF:Q4_K_M                         |    16.40 |   9.62 |     59 |   32.8 |    4 |   32 | `Python:  12.04`<br/>`Java:    10.75`<br/>`Rust:    6.64`<br/>`Clojure: 2.5` |
| hf.co/mradermacher/Bespoke-Stratos-32B-GGUF:Q4_K_M                   |    16.40 |   9.61 |     59 |   32.8 |    4 |   32 | `Python:  12.37`<br/>`Java:    9.9`<br/>`Rust:    7.58`<br/>`Clojure: 1.78` |
| qwen2.5-coder:32b-instruct-q8_0                                      |          |   9.38 |     29 |   32.8 |    8 |   32 | `Python:  11.94`<br/>`Java:    9.94`<br/>`Rust:    6.69`<br/>`Clojure: 2.8` |
| qwen2.5:32b-instruct-q4_K_M                                          |    16.40 |   9.17 |     56 |   32.8 |    4 |   32 | `Python:  12.34`<br/>`Java:    9.26`<br/>`Rust:    6.13`<br/>`Clojure: 2.25` |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q8_0     |          |   8.66 |     26 |   32.8 |    8 |   32 | `Python:  11.58`<br/>`Java:    8.69`<br/>`Rust:    6.27`<br/>`Clojure: 1.62` |
| qwen2.5:32b-instruct-q8_0                                            |          |   8.44 |     26 |   32.8 |    8 |   32 | `Python:  9.73`<br/>`Java:    10.22`<br/>`Rust:    5.91`<br/>`Clojure: 2.98` |
| GPT-4o-Mini                                                          |          |   8.00 |        |        |   16 |  128 | `Python:  11.39`<br/>`Java:    7.36`<br/>`Rust:    5.19`<br/>`Clojure: 1.93` |
| hf.co/bartowski/Qwen2.5-Coder-32B-Instruct-abliterated-GGUF:Q4_K_M   |    16.40 |   7.95 |     48 |   32.8 |    4 |   32 | `Python:  9.55`<br/>`Java:    9.3`<br/>`Rust:    5.71`<br/>`Clojure: 1.94` |
| GPT-3.5-Turbo                                                        |          |   7.47 |      2 |  175.0 |   16 |   16 | `Python:  10.1`<br/>`Java:    7.28`<br/>`Rust:    6.0`<br/>`Clojure: 0.5` |
| yi-coder:9b-chat-q8_0                                                |     8.80 |   7.37 |     84 |    8.8 |    8 |  128 | `Python:  11.08`<br/>`Java:    6.77`<br/>`Rust:    4.32`<br/>`Clojure: 0.47` |
| deepseek-coder:33b-instruct-q4_K_M                                   |          |   7.34 |     44 |   33.0 |    4 |   16 | `Python:  9.55`<br/>`Java:    10.72`<br/>`Rust:    0.0`<br/>`Clojure: 3.03` |
| llama3.3:70b-instruct-q8_0                                           |          |   7.17 |     10 |   70.6 |    8 |  128 | `Python:  8.93`<br/>`Java:    8.06`<br/>`Rust:    4.29`<br/>`Clojure: 3.17` |
| qwen2.5-coder:14b-instruct-q8_0                                      |          |   7.09 |     48 |   14.8 |    8 |  128 | `Python:  9.7`<br/>`Java:    7.35`<br/>`Rust:    4.55`<br/>`Clojure: 0.95` |
| hf.co/mradermacher/phi-4-abliterated-GGUF:Q4_K_M                     |     7.35 |   6.72 |     91 |   14.7 |    4 |   16 | `Python:  9.26`<br/>`Java:    6.8`<br/>`Rust:    4.42`<br/>`Clojure: 0.89` |
| qwen2.5-coder:14b-instruct-q4_K_M                                    |          |   6.68 |     90 |   14.8 |    4 |  128 | `Python:  8.65`<br/>`Java:    7.28`<br/>`Rust:    4.62`<br/>`Clojure: 1.13` |
| phi4:14b-q8_0                                                        |          |   6.68 |     45 |   14.7 |    8 |   16 | `Python:  10.23`<br/>`Java:    5.29`<br/>`Rust:    4.52`<br/>`Clojure: 0.97` |
| phi4:14b                                                             |     7.35 |   6.64 |     90 |   14.7 |    4 |   16 | `Python:  9.64`<br/>`Java:    6.91`<br/>`Rust:    3.14`<br/>`Clojure: 0.84` |
| phi4:latest                                                          |     7.35 |   6.64 |     90 |   14.7 |    4 |   16 | `Python:  9.64`<br/>`Java:    6.91`<br/>`Rust:    3.14`<br/>`Clojure: 0.84` |
| deepseek-coder:33b-instruct-q8_0                                     |          |   6.58 |     20 |   33.0 |    8 |   16 | `Python:  8.35`<br/>`Java:    10.2`<br/>`Rust:    0.0`<br/>`Clojure: 1.82` |
| hf.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF:Q4_K_M   |          |   6.49 |     18 |   70.6 |    4 |  128 | `Python:  9.1`<br/>`Java:    5.9`<br/>`Rust:    4.69`<br/>`Clojure: 1.37` |
| mistral-large:123b-instruct-2407-q4_K_M                              |          |   6.34 |     10 |  122.6 |    4 |  128 | `Python:  8.27`<br/>`Java:    6.61`<br/>`Rust:    4.44`<br/>`Clojure: 1.61` |
| vanilj/Phi-4:Q8_0                                                    |          |   6.13 |     42 |   14.7 |    8 |   16 | `Python:  9.06`<br/>`Java:    5.73`<br/>`Rust:    3.52`<br/>`Clojure: 0.84` |
| yi-coder:9b-chat-q4_K_M                                              |     4.40 |   5.97 |    136 |    8.8 |    4 |  128 | `Python:  7.44`<br/>`Java:    6.04`<br/>`Rust:    5.76`<br/>`Clojure: 0.34` |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M                            |          |   5.83 |     17 |   70.6 |    4 |  128 | `Python:  8.07`<br/>`Java:    6.49`<br/>`Rust:    2.59`<br/>`Clojure: 1.36` |
| llama3.1:70b-instruct-q8_0                                           |          |   5.81 |      8 |   70.6 |    8 |  128 | `Python:  8.19`<br/>`Java:    5.36`<br/>`Rust:    3.8`<br/>`Clojure: 1.7` |
| qwen2.5:14b-instruct-q8_0                                            |          |   5.75 |     39 |   14.8 |    8 |   32 | `Python:  8.59`<br/>`Java:    4.14`<br/>`Rust:    4.55`<br/>`Clojure: 1.61` |
| qwen2.5:14b-instruct-q4_K_M                                          |          |   5.63 |     76 |   14.8 |    4 |   32 | `Python:  8.44`<br/>`Java:    5.08`<br/>`Rust:    3.44`<br/>`Clojure: 0.43` |
| llama3.1:70b-instruct-q4_K_M                                         |          |   5.62 |     16 |   70.6 |    4 |  128 | `Python:  8.77`<br/>`Java:    4.98`<br/>`Rust:    2.77`<br/>`Clojure: 0.6` |
| llama3.3:70b-instruct-q4_K_M                                         |          |   5.60 |     16 |   70.6 |    4 |  128 | `Python:  7.26`<br/>`Java:    5.25`<br/>`Rust:    4.49`<br/>`Clojure: 2.21` |
| falcon3:10b-instruct-q8_0                                            |          |   5.48 |     53 |   10.3 |    8 |   32 | `Python:  8.15`<br/>`Java:    5.14`<br/>`Rust:    2.71`<br/>`Clojure: 1.39` |
| hf.co/bartowski/smirki_UIGEN-T1.1-Qwen-14B-GGUF:Q4_K_M               |          |   5.46 |        |   14.8 |      |      | `Python:  7.27`<br/>`Java:    5.2`<br/>`Rust:    4.41`<br/>`Clojure: 1.14` |
| hf.co/mradermacher/calme-3.2-instruct-78b-GGUF:Q4_K_S                |          |   5.43 |     14 |   78.0 |    4 |   32 | `Python:  7.04`<br/>`Java:    6.05`<br/>`Rust:    3.6`<br/>`Clojure: 0.74` |
| tulu3:70b-q8_0                                                       |          |   5.25 |      7 |   70.6 |    8 |  128 | `Python:  7.73`<br/>`Java:    4.61`<br/>`Rust:    3.09`<br/>`Clojure: 1.59` |
| qwen2-math:72b-instruct-q8_0                                         |          |   5.25 |      7 |   72.7 |    8 |    4 | `Python:  6.49`<br/>`Java:    6.67`<br/>`Rust:    2.61`<br/>`Clojure: 1.3` |
| tulu3:70b-q4_K_M                                                     |          |   5.21 |     15 |   70.6 |    4 |  128 | `Python:  7.31`<br/>`Java:    4.68`<br/>`Rust:    3.35`<br/>`Clojure: 2.15` |
| hf.co/ozone-ai/0x-lite-Q4_K_M-GGUF:latest                            |          |   5.14 |     69 |   14.8 |    4 |   32 | `Python:  7.66`<br/>`Java:    4.52`<br/>`Rust:    3.32`<br/>`Clojure: 0.56` |
| qwq:32b-preview-q8_0                                                 |          |   5.09 |     16 |   32.8 |    8 |   32 | `Python:  9.68`<br/>`Java:    2.94`<br/>`Rust:    1.39`<br/>`Clojure: 0.54` |
| hf.co/bartowski/Qwen2.5-14B-Instruct-1M-GGUF:Q4_K_M                  |          |   4.94 |     67 |   14.8 |    4 |  986 | `Python:  7.75`<br/>`Java:    4.02`<br/>`Rust:    2.74`<br/>`Clojure: 0.81` |
| falcon3:10b-instruct-q4_K_M                                          |          |   4.88 |     95 |   10.3 |    4 |   32 | `Python:  6.62`<br/>`Java:    5.77`<br/>`Rust:    2.19`<br/>`Clojure: 0.6` |
| nemotron:70b-instruct-q4_K_M                                         |          |   4.78 |     14 |   70.6 |    4 |  128 | `Python:  5.78`<br/>`Java:    5.13`<br/>`Rust:    4.22`<br/>`Clojure: 0.83` |
| qwen2.5-coder:7b-instruct-q8_0                                       |          |   4.69 |     62 |    7.6 |    8 |  128 | `Python:  6.37`<br/>`Java:    4.4`<br/>`Rust:    3.78`<br/>`Clojure: 0.63` |
| nemotron:70b-instruct-q8_0                                           |          |   4.50 |      6 |   70.6 |    8 |  128 | `Python:  6.31`<br/>`Java:    4.05`<br/>`Rust:    3.23`<br/>`Clojure: 1.13` |
| qwen2.5:7b-instruct-q8_0                                             |          |   4.34 |     57 |    7.6 |    8 |  128 | `Python:  7.47`<br/>`Java:    3.6`<br/>`Rust:    1.13`<br/>`Clojure: 0.51` |
| falcon3:7b-instruct-q8_0                                             |          |   4.34 |     58 |    7.5 |    8 |   32 | `Python:  6.76`<br/>`Java:    3.91`<br/>`Rust:    2.16`<br/>`Clojure: 0.36` |
| hf.co/mradermacher/Viper-Coder-Hybrid-v1.3-GGUF:Q4_K_M               |          |   4.32 |     58 |   14.8 |    4 |  128 | `Python:  6.44`<br/>`Java:    4.45`<br/>`Rust:    1.83`<br/>`Clojure: 0.46` |
| hf.co/smirki/UIGEN-T1.1-Qwen-7B-Q4_K_M-GGUF:latest                   |          |   4.29 |        |   7.62 |      |      | `Python:  6.06`<br/>`Java:    4.53`<br/>`Rust:    2.08`<br/>`Clojure: 0.88` |
| qwen2.5:7b-instruct-q4_K_M                                           |     3.80 |   4.22 |    111 |    7.6 |    4 |  128 | `Python:  7.5`<br/>`Java:    2.67`<br/>`Rust:    1.86`<br/>`Clojure: 0.49` |
| mistral-small:24b-instruct-2501-q4_K_M                               |          |   3.98 |     34 |   23.6 |    4 |   32 | `Python:  6.32`<br/>`Java:    2.89`<br/>`Rust:    2.47`<br/>`Clojure: 0.93` |
| qwen2.5-coder:7b-instruct-q4_K_M                                     |     3.80 |   3.98 |    105 |    7.6 |    4 |   32 | `Python:  4.76`<br/>`Java:    4.7`<br/>`Rust:    2.87`<br/>`Clojure: 0.87` |
| hf.co/bartowski/open-thoughts_OpenThinker-32B-GGUF:Q4_K_M            |          |   3.89 |        |   32.8 |      |      | `Python:  4.2`<br/>`Java:    4.22`<br/>`Rust:    3.22`<br/>`Clojure: 2.95` |
| gemma2:27b-instruct-q8_0                                             |          |   3.65 |     13 |   27.2 |    8 |    8 | `Python:  5.18`<br/>`Java:    3.3`<br/>`Rust:    2.47`<br/>`Clojure: 0.98` |
| hf.co/bartowski/Athene-70B-GGUF:Q4_K_M                               |          |   3.58 |     10 |   70.6 |    4 |    8 | `Python:  6.98`<br/>`Java:    1.99`<br/>`Rust:    0.76`<br/>`Clojure: 0.36` |
| hf.co/mradermacher/Viper-Coder-HybridMini-v1.3-GGUF:Q4_K_M           |          |   3.55 |     93 |   7.62 |    4 |   32 | `Python:  5.18`<br/>`Java:    3.51`<br/>`Rust:    1.99`<br/>`Clojure: 0.24` |
| deepseek-coder:6.7b-instruct-q8_0                                    |          |   3.52 |     50 |    7.0 |    8 |   16 | `Python:  5.37`<br/>`Java:    3.68`<br/>`Rust:    0.94`<br/>`Clojure: 0.79` |
| hf.co/bartowski/Yi-1.5-9B-Chat-GGUF:Q8_0                             |          |   3.34 |     38 |   8.83 |    8 |    4 | `Python:  6.54`<br/>`Java:    2.11`<br/>`Rust:    0.4`<br/>`Clojure: 0.09` |
| hf.co/lmstudio-community/Mistral-Small-24B-Instruct-2501-GGUF:Q4_K_M |          |   3.33 |     28 |   23.6 |    4 |   32 | `Python:  5.21`<br/>`Java:    2.86`<br/>`Rust:    1.54`<br/>`Clojure: 0.79` |
| hf.co/internlm/internlm3-8b-instruct-gguf:Q4_K_M                     |          |   3.30 |     75 |    8.8 |    4 |   32 | `Python:  4.92`<br/>`Java:    3.64`<br/>`Rust:    1.18`<br/>`Clojure: 0.06` |
| opencoder:8b-instruct-q8_0                                           |          |   3.21 |     41 |    7.8 |    8 |    8 | `Python:  4.63`<br/>`Java:    3.22`<br/>`Rust:    1.62`<br/>`Clojure: 0.72` |
| hf.co/mradermacher/Bespoke-Stratos-7B-GGUF:Q4_K_M                    |          |   3.16 |     83 |   7.62 |    4 |   32 | `Python:  4.72`<br/>`Java:    2.67`<br/>`Rust:    2.26`<br/>`Clojure: 0.23` |
| hf.co/bartowski/simplescaling_s1-32B-GGUF:Q4_K_M                     |          |   3.11 |     19 |   32.8 |    4 |   32 | `Python:  4.33`<br/>`Java:    2.29`<br/>`Rust:    2.78`<br/>`Clojure: 1.4` |
| qwen2.5-coder:3b-instruct-q4_K_M                                     |     1.55 |   3.05 |    197 |    3.1 |    4 |   32 | `Python:  4.98`<br/>`Java:    2.51`<br/>`Rust:    1.53`<br/>`Clojure: 0.03` |
| exaone3.5:32b-instruct-q8_0                                          |          |   3.05 |     10 |   32.0 |    8 |   32 | `Python:  3.96`<br/>`Java:    3.82`<br/>`Rust:    1.38`<br/>`Clojure: 0.47` |
| deepseek-r1:32b-qwen-distill-q4_K_M                                  |          |   3.00 |     18 |   32.8 |    4 |  128 | `Python:  4.51`<br/>`Java:    2.91`<br/>`Rust:    1.44`<br/>`Clojure: 0.32` |
| hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:Q4_K_M                   |          |   2.97 |     78 |   7.62 |    4 |  128 | `Python:  6.55`<br/>`Java:    0.0`<br/>`Rust:    1.63`<br/>`Clojure: 0.24` |
| yi:34b-chat-v1.5-q4_K_M                                              |          |   2.65 |     16 |   34.0 |    4 |    4 | `Python:  4.25`<br/>`Java:    2.63`<br/>`Rust:    0.58`<br/>`Clojure: ` |
| qwen2.5-coder:3b-instruct-q8_0                                       |          |   2.62 |     85 |    3.1 |    8 |   32 | `Python:  4.2`<br/>`Java:    2.15`<br/>`Rust:    1.4`<br/>`Clojure: 0.2` |
| yi:9b-chat-v1.5-q4_K_M                                               |          |   2.54 |     56 |    9.0 |    4 |    4 | `Python:  4.04`<br/>`Java:    2.71`<br/>`Rust:    0.39`<br/>`Clojure: 0.33` |
| hf.co/bartowski/Yi-1.5-34B-Chat-GGUF:Q8_0                            |          |   2.45 |      7 |   34.4 |    8 |    4 | `Python:  4.61`<br/>`Java:    1.49`<br/>`Rust:    0.72`<br/>`Clojure: 0.16` |
| exaone3.5:7.8b-instruct-q8_0                                         |          |   2.28 |     29 |    7.8 |    8 |   32 | `Python:  3.76`<br/>`Java:    2.26`<br/>`Rust:    0.17`<br/>`Clojure: 0.68` |
| qwen:110b-chat-v1.5-q4_K_M                                           |          |   2.25 |      4 |  111.0 |    4 |   32 | `Python:  3.63`<br/>`Java:    1.84`<br/>`Rust:    0.76`<br/>`Clojure: 0.92` |
| phi3:14b-medium-128k-instruct-q8_0                                   |          |   2.24 |     16 |   14.0 |    8 |  128 | `Python:  4.21`<br/>`Java:    1.55`<br/>`Rust:    0.42`<br/>`Clojure: 0.04` |
| llama3.1:8b-instruct-q8_0                                            |          |   2.03 |     25 |    8.0 |    8 |  128 | `Python:  3.26`<br/>`Java:    1.78`<br/>`Rust:    0.94`<br/>`Clojure: 0.09` |
| tulu3:8b-q8_0                                                        |          |   2.01 |     25 |    8.0 |    8 |  128 | `Python:  3.91`<br/>`Java:    1.06`<br/>`Rust:    0.42`<br/>`Clojure: 0.49` |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q8_0                             |          |   1.87 |     31 |   6.06 |    8 |    4 | `Python:  3.92`<br/>`Java:    0.92`<br/>`Rust:    0.13`<br/>`Clojure: 0.0` |
| hf.co/bartowski/Yi-1.5-6B-Chat-GGUF:Q4_K_M                           |          |   1.81 |     60 |   6.06 |    4 |    4 | `Python:  3.71`<br/>`Java:    0.87`<br/>`Rust:    0.32`<br/>`Clojure: 0.0` |
| qwen2.5:3b                                                           |     1.55 |   1.80 |    116 |    3.1 |    4 |      | `Python:  2.95`<br/>`Java:    1.35`<br/>`Rust:    `<br/>`Clojure: ` |
| deepseek-llm:67b-chat-q4_K_M                                         |          |   1.79 |      5 |   67.0 |    4 |    4 | `Python:  2.94`<br/>`Java:    1.63`<br/>`Rust:    0.5`<br/>`Clojure: 0.23` |
| qwen2.5:3b-instruct-q4_K_M                                           |     1.55 |   1.70 |    110 |    3.1 |    4 |  128 | `Python:  2.95`<br/>`Java:    1.35`<br/>`Rust:    0.56`<br/>`Clojure: 0.05` |
| deepseek-r1:70b-llama-distill-q4_K_M                                 |          |   1.69 |      5 |   70.6 |    4 |  128 | `Python:  2.17`<br/>`Java:    2.49`<br/>`Rust:    0.19`<br/>`Clojure: 0.41` |
| deepseek-r1:14b-qwen-distill-q4_K_M                                  |          |   1.69 |     23 |   14.8 |    4 |  128 | `Python:  2.6`<br/>`Java:    1.02`<br/>`Rust:    1.19`<br/>`Clojure: 1.02` |
| yi-coder:1.5b-chat-q4_K_M                                            |     0.75 |   1.65 |    220 |    1.5 |    4 |  128 | `Python:  3.49`<br/>`Java:    0.61`<br/>`Rust:    0.34`<br/>`Clojure: 0.0` |
| gemma2:9b-instruct-q8_0                                              |          |   1.63 |     18 |    9.2 |    8 |    8 | `Python:  2.46`<br/>`Java:    1.55`<br/>`Rust:    0.86`<br/>`Clojure: 0.12` |
| granite3.1-dense:8b-instruct-q8_0                                    |          |   1.59 |     19 |    8.2 |    8 |  128 | `Python:  2.73`<br/>`Java:    1.55`<br/>`Rust:    0.16`<br/>`Clojure: 0.03` |
| granite3.2:8b-instruct-q4_K_M                                        |          |   1.50 |     37 |    8.2 |    4 |  128 | `Python:  2.53`<br/>`Java:    1.43`<br/>`Rust:    0.3`<br/>`Clojure: 0.0` |
| codegemma:7b-instruct-v1.1-q4_K_M                                    |          |   1.46 |     33 |    9.0 |    4 |      | `Python:  2.21`<br/>`Java:    1.49`<br/>`Rust:    0.66`<br/>`Clojure: 0.01` |
| exaone3.5:2.4b-instruct-q8_0                                         |          |   1.45 |     54 |    2.7 |    8 |   32 | `Python:  2.73`<br/>`Java:    0.94`<br/>`Rust:    0.28`<br/>`Clojure: 0.15` |
| qwen2.5:3b-instruct-q8_0                                             |          |   1.43 |     46 |    3.1 |    8 |  128 | `Python:  2.87`<br/>`Java:    0.59`<br/>`Rust:    0.44`<br/>`Clojure: 0.18` |
| deepseek-r1:7b-qwen-distill-q4_K_M                                   |          |   1.43 |     38 |    7.6 |    4 |  128 | `Python:  2.64`<br/>`Java:    1.08`<br/>`Rust:    0.0`<br/>`Clojure: 0.46` |
| opencoder:1.5b-instruct-q8_0                                         |          |   1.42 |     75 |    1.9 |    8 |    4 | `Python:  2.2`<br/>`Java:    1.47`<br/>`Rust:    0.5`<br/>`Clojure: 0.0` |
| yi-coder:1.5b-chat-q8_0                                              |          |   1.36 |     91 |    1.5 |    8 |  128 | `Python:  2.32`<br/>`Java:    1.17`<br/>`Rust:    0.42`<br/>`Clojure: 0.0` |
| qwen2.5-coder:1.5b-instruct-q4_K_M                                   |     0.75 |   1.31 |    174 |    1.5 |    4 |   32 | `Python:  2.26`<br/>`Java:    0.8`<br/>`Rust:    0.8`<br/>`Clojure: 0.03` |
| mixtral:8x7b-instruct-v0.1-q4_K_M                                    |          |   1.30 |      6 |   46.7 |    4 |   32 | `Python:  2.0`<br/>`Java:    1.24`<br/>`Rust:    0.62`<br/>`Clojure: 0.0` |
| qwen2-math:7b-instruct-q8_0                                          |          |   1.28 |     17 |    7.6 |    8 |    4 | `Python:  2.49`<br/>`Java:    0.95`<br/>`Rust:    0.02`<br/>`Clojure: 0.0` |
| dolphin3:8b-llama3.1-q8_0                                            |          |   1.27 |     16 |    8.0 |    8 |  128 | `Python:  2.3`<br/>`Java:    0.89`<br/>`Rust:    0.26`<br/>`Clojure: 0.31` |
| qwen2.5-coder:1.5b-instruct-q8_0                                     |          |   1.22 |     81 |    1.5 |    8 |   32 | `Python:  2.04`<br/>`Java:    0.9`<br/>`Rust:    0.66`<br/>`Clojure: 0.03` |
| hf.co/mradermacher/Dolphin3.0-Llama3.1-8B-abliterated-GGUF:Q8_0      |          |   1.21 |     15 |   8.03 |    8 |  128 | `Python:  2.29`<br/>`Java:    0.47`<br/>`Rust:    0.58`<br/>`Clojure: 0.37` |
| codegemma:7b-instruct-q8_0                                           |          |   1.19 |     13 |    9.0 |    8 |    8 | `Python:  1.84`<br/>`Java:    1.27`<br/>`Rust:    0.39`<br/>`Clojure: 0.0` |
| Bio-Medical-Llama-3-8B-GGUF:Q8_0                                     |          |   1.16 |     15 |    8.0 |    8 |    8 | `Python:  1.51`<br/>`Java:    1.65`<br/>`Rust:    0.3`<br/>`Clojure: 0.03` |
| falcon3:3b-instruct-q8_0                                             |          |   1.16 |     36 |    3.2 |    8 |   32 | `Python:  1.89`<br/>`Java:    1.09`<br/>`Rust:    0.36`<br/>`Clojure: 0.04` |
| qwen2.5:1.5b-instruct-q8_0                                           |          |   1.14 |     76 |    1.5 |    8 |  128 | `Python:  2.07`<br/>`Java:    0.82`<br/>`Rust:    0.29`<br/>`Clojure: 0.06` |
| deepseek-r1:8b-llama-distill-q4_K_M                                  |          |   1.12 |     28 |    8.0 |    4 |  128 | `Python:  1.46`<br/>`Java:    1.25`<br/>`Rust:    0.45`<br/>`Clojure: 0.67` |
| openchat:7b-v3.5-q8_0                                                |          |   1.02 |     15 |    7.0 |    8 |    8 | `Python:  1.62`<br/>`Java:    1.21`<br/>`Rust:    0.06`<br/>`Clojure: 0.0` |
| codellama:34b-instruct-q4_K_M                                        |          |   0.93 |      5 |   34.0 |    4 |   16 | `Python:  1.29`<br/>`Java:    0.99`<br/>`Rust:    0.56`<br/>`Clojure: 0.04` |
| qwen:32b-chat-v1.5-q4_K_M                                            |          |   0.90 |      5 |   33.0 |    4 |   32 | `Python:  1.54`<br/>`Java:    0.81`<br/>`Rust:    0.13`<br/>`Clojure: 0.12` |
| yi:6b-chat-v1.5-q4_K_M                                               |          |   0.89 |     30 |    6.0 |    4 |    4 | `Python:  0.79`<br/>`Java:    1.48`<br/>`Rust:    0.62`<br/>`Clojure: 0.01` |
| qwen2.5:1.5b-instruct-q4_K_M                                         |     0.75 |   0.88 |    118 |    1.5 |    4 |  128 | `Python:  1.94`<br/>`Java:    0.26`<br/>`Rust:    0.15`<br/>`Clojure: 0.0` |
| mixtral:8x7b-instruct-v0.1-q8_0                                      |          |   0.82 |      2 |   46.7 |    8 |   32 | `Python:  1.44`<br/>`Java:    0.65`<br/>`Rust:    0.23`<br/>`Clojure: 0.0` |
| hf.co/bartowski/OpenThinker-7B-GGUF:Q4_K_M                           |          |   0.75 |     20 |   7.62 |    4 |   32 | `Python:  0.88`<br/>`Java:    0.77`<br/>`Rust:    0.53`<br/>`Clojure: 0.62` |
| command-r7b:7b-12-2024-q4_K_M                                        |          |   0.68 |     17 |    8.0 |    4 |  128 | `Python:  1.54`<br/>`Java:    0.03`<br/>`Rust:    0.26`<br/>`Clojure: 0.04` |
| olmo2:13b-1124-instruct-q4_K_M                                       |          |   0.66 |     10 |   13.7 |    4 |    4 | `Python:  1.59`<br/>`Java:    0.06`<br/>`Rust:    0.01`<br/>`Clojure: 0.03` |
| hf.co/bartowski/agentica-org_DeepScaleR-1.5B-Preview-GGUF:Q4_K_M     |          |   0.64 |     72 |   1.78 |    4 |  128 | `Python:  1.28`<br/>`Java:    0.4`<br/>`Rust:    0.03`<br/>`Clojure: 0.05` |
| qwen:72b-chat-v1.5-q4_K_M                                            |          |   0.64 |      2 |   72.0 |    4 |   32 | `Python:  0.94`<br/>`Java:    0.78`<br/>`Rust:    0.13`<br/>`Clojure: 0.0` |
| olmo2:7b-1124-instruct-q4_K_M                                        |          |   0.60 |     16 |    7.3 |    4 |    4 | `Python:  1.42`<br/>`Java:    0.08`<br/>`Rust:    0.02`<br/>`Clojure: 0.0` |
| qwen2.5:0.5b-instruct-q8_0                                           |     0.50 |   0.57 |    115 |    0.5 |    8 |  128 | `Python:  1.33`<br/>`Java:    0.0`<br/>`Rust:    0.21`<br/>`Clojure: 0.0` |
| granite3.1-dense:2b-instruct-q8_0                                    |          |   0.50 |     20 |    2.5 |    8 |  128 | `Python:  1.07`<br/>`Java:    0.11`<br/>`Rust:    0.2`<br/>`Clojure: 0.0` |
| llama3.2:latest                                                      |          |   0.49 |     31 |   3.21 |    4 |  128 | `Python:  0.99`<br/>`Java:    0.18`<br/>`Rust:    0.21`<br/>`Clojure: 0.0` |
| codellama:13b-instruct-q4_K_M                                        |          |   0.48 |      7 |   13.0 |    4 |   16 | `Python:  0.52`<br/>`Java:    0.84`<br/>`Rust:    0.05`<br/>`Clojure: 0.08` |
| smallthinker:3b-preview-q4_K_M                                       |          |   0.47 |     27 |    3.4 |    4 |  128 | `Python:  0.98`<br/>`Java:    0.25`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| granite3.2:2b-instruct-q4_K_M                                        |          |   0.42 |     34 |    2.5 |    4 |  128 | `Python:  0.85`<br/>`Java:    0.16`<br/>`Rust:    0.15`<br/>`Clojure: 0.05` |
| mistral:7b-instruct-q4_K_M                                           |          |   0.41 |     12 |    7.0 |    4 |   32 | `Python:  0.48`<br/>`Java:    0.71`<br/>`Rust:    0.04`<br/>`Clojure: 0.0` |
| smallthinker:3b-preview-q8_0                                         |          |   0.41 |     12 |    3.4 |    8 |  128 | `Python:  0.81`<br/>`Java:    0.19`<br/>`Rust:    0.03`<br/>`Clojure: 0.19` |
| phi:2.7b-chat-v2-q4_K_M                                              |          |   0.39 |     26 |    3.0 |    4 |    2 | `Python:  0.91`<br/>`Java:    0.07`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| vicuna:33b-q4_K_M                                                    |          |   0.38 |      3 |   30.0 |    4 |    2 | `Python:  0.9`<br/>`Java:    0.06`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| granite3.1-moe:3b-instruct-q8_0                                      |          |   0.35 |     11 |    3.3 |    8 |  128 | `Python:  0.8`<br/>`Java:    0.03`<br/>`Rust:    0.11`<br/>`Clojure: 0.03` |
| hf.co/bartowski/UwU-7B-Instruct-GGUF:Q8_0                            |          |   0.27 |      4 |   7.62 |    8 |  128 | `Python:  0.27`<br/>`Java:    0.54`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| qwen2-math:1.5b-instruct-q8_0                                        |          |   0.27 |     18 |    1.5 |    8 |    4 | `Python:  0.65`<br/>`Java:    0.03`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| gemma2:2b-instruct-q8_0                                              |          |   0.23 |      9 |    2.6 |    8 |    8 | `Python:  0.39`<br/>`Java:    0.22`<br/>`Rust:    0.03`<br/>`Clojure: 0.0` |
| llama3.2:1b                                                          |          |   0.21 |     18 |    1.2 |    8 |      | `Python:  0.41`<br/>`Java:    0.06`<br/>`Rust:    `<br/>`Clojure: ` |
| deepseek-r1:1.5b-qwen-distill-q4_K_M                                 |          |   0.21 |     23 |    1.8 |    4 |  128 | `Python:  0.45`<br/>`Java:    0.1`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| codellama:7b-instruct-q4_K_M                                         |          |   0.21 |      6 |    7.0 |    4 |   16 | `Python:  0.33`<br/>`Java:    0.03`<br/>`Rust:    0.33`<br/>`Clojure: 0.01` |
| deepseek-llm:7b-chat-q8_0                                            |          |   0.20 |      3 |    7.0 |    8 |    4 | `Python:  0.46`<br/>`Java:    0.06`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| phi3:3.8b                                                            |          |   0.17 |      9 |    3.8 |    4 |      | `Python:  0.39`<br/>`Java:    0.04`<br/>`Rust:    0.03`<br/>`Clojure: 0.0` |
| hf.co/bartowski/Qwen2-VL-72B-Instruct-GGUF:Q4_K_M                    |          |   0.16 |      0 |   72.7 |    4 |   32 | `Python:  0.31`<br/>`Java:    0.0`<br/>`Rust:    0.08`<br/>`Clojure: 0.16` |
| qwen2.5-coder:0.5b-instruct-q4_K_M                                   |     0.25 |   0.15 |     60 |    0.5 |    4 |   32 | `Python:  0.36`<br/>`Java:    0.01`<br/>`Rust:    0.01`<br/>`Clojure: 0.0` |
| qwen2.5:0.5b-instruct-q4_K_M                                         |     0.25 |   0.15 |     58 |    0.5 |    4 |  128 | `Python:  0.36`<br/>`Java:    0.0`<br/>`Rust:    0.01`<br/>`Clojure: 0.0` |
| qwen2.5-coder:0.5b-instruct-q8_0                                     |          |   0.14 |     28 |    0.5 |    8 |   32 | `Python:  0.33`<br/>`Java:    0.01`<br/>`Rust:    0.03`<br/>`Clojure: 0.0` |
| llama2:70b-chat-q4_K_M                                               |          |   0.14 |      0 |   69.0 |    4 |    4 | `Python:  0.31`<br/>`Java:    0.03`<br/>`Rust:    0.01`<br/>`Clojure: 0.03` |
| llama3.2:1b-instruct-q8_0                                            |          |   0.13 |     11 |    1.2 |    8 |  128 | `Python:  0.28`<br/>`Java:    0.06`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| falcon:7b-instruct-q4_0                                              |          |   0.11 |      3 |    7.0 |    4 |    2 | `Python:  0.28`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| falcon:40b-instruct-q4_0                                             |          |   0.11 |      1 |   40.0 |    4 |    2 | `Python:  0.07`<br/>`Java:    0.0`<br/>`Rust:    0.42`<br/>`Clojure: 0.0` |
| phi4-mini:3.8b-q4_K_M                                                |          |   0.11 |      6 |    3.8 |    4 |  128 | `Python:  0.23`<br/>`Java:    0.04`<br/>`Rust:    0.01`<br/>`Clojure: 0.0` |
| falcon3:1b-instruct-q8_0                                             |          |   0.10 |      6 |    1.7 |    8 |    8 | `Python:  0.25`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| granite3.1-moe:1b-instruct-q8_0                                      |          |   0.10 |      7 |    1.3 |    8 |  128 | `Python:  0.24`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| qwen:1.8b-chat-v1.5-q4_K_M                                           |          |   0.06 |      6 |    2.0 |    4 |   32 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.62` |
| vicuna:13b-q4_K_M                                                    |          |   0.04 |      1 |   13.0 |    4 |    2 | `Python:  0.09`<br/>`Java:    0.01`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| granite3.2-vision:2b-q4_K_M                                          |          |   0.04 |      3 |    2.5 |    4 |   16 | `Python:  0.07`<br/>`Java:    0.03`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| vicuna:13b-v1.5-16k-q4_K_M                                           |          |   0.03 |      1 |   13.0 |    4 |    2 | `Python:  0.06`<br/>`Java:    0.03`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| qwen2:0.5b-instruct-q8_0                                             |          |   0.03 |      0 | 494.03 |    8 |   32 | `Python:  0.07`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| starcoder2:3b                                                        |          |   0.03 |      2 |    3.0 |    4 |   16 | `Python:  0.07`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| llama2:13b-chat-q4_K_M                                               |          |   0.03 |      0 |   13.0 |    4 |    4 | `Python:  0.06`<br/>`Java:    0.01`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| vicuna:7b-v1.5-16k-q4_K_M                                            |          |   0.01 |      0 |    7.0 |    4 |    4 | `Python:  0.03`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| deepseek-coder:1.3b-instruct-q8_0                                    |          |   0.01 |      1 |    1.0 |    8 |   16 | `Python:  0.0`<br/>`Java:    0.02`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| llama2:7b-chat-q4_K_M                                                |          |   0.00 |      0 |    7.0 |    4 |    4 | `Python:  0.01`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| smollm:1.7b-instruct-v0.2-q8_0                                       |          |   0.00 |      0 |    1.7 |    8 |    2 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| smollm:135m-instruct-v0.2-q8_0                                       |     0.14 |   0.00 |      0 |  0.135 |    8 |    2 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| smollm:360m-instruct-v0.2-q8_0                                       |          |   0.00 |      0 |   0.36 |    8 |    2 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| qwen:0.5b-chat-v1.5-q4_K_M                                           |          |   0.00 |      0 |  620.0 |    4 |   32 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| qwen:4b-chat-v1.5-q4_K_M                                             |          |   0.00 |      0 |    4.0 |    4 |   32 | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| codegemma:2b-code-v1.1-q4_K_M                                        |          |   0.00 |      0 |    3.0 |    4 |      | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |
| vicuna:7b-q4_K_M                                                     |          |   0.00 |      0 |    7.0 |    4 |      | `Python:  0.0`<br/>`Java:    0.0`<br/>`Rust:    0.0`<br/>`Clojure: 0.0` |

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
