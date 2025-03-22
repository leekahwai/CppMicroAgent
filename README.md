# 🧠 LLM-Powered C++ Code Generation and Quality Assistant

This project leverages [Ollama](https://ollama.com) and Large Language Models (LLMs) to assist developers in on-premise/on-device C++ code generation and quality assurance for safety critical systems. It uses intelligent, modular **state machines** to automate tasks such as code generation, unit test creation, static analysis, and fuzzing, aiming to streamline and strengthen your development workflow.

## 🚀 Key Features

- **LLM-based C++ Code Generation**  
  Automatically generate C++ functions and classes based on high-level descriptions or templates using powerful LLMs via Ollama. State machine is used to iteratively generate and validate codes using prompt engineering to guide and reinforce code generation to hit an objective using coding metrics. (for instance generation of gtest codes to hit 80% coverage)

- **Unit Test Generation with Coverage Awareness**  
  Creates unit tests tailored to hit as many branches and edge cases as possible. Uses feedback loops to iteratively increase test coverage.

- **Static Analysis**  
  Integrates LLM-supported static code checks to identify potential issues in logic, performance, and code standards.

- **Fuzz Testing Automation**  
  Generate and manage fuzzers to detect unexpected behavior and edge-case bugs early in development.

- **State Machine-Driven Architecture**  
  Each task (e.g., test creation, coverage validation, fuzzing setup) is controlled by a dedicated state machine for flexibility, debuggability, and traceability.

---

## 🛠️ Tech Stack

- **Ollama**: Local LLM runtime for fast, customizable model inference  
- **Large Language Models**: (e.g., LLaMA, Mistral, or custom fine-tuned models)  
- **C++**: Target language for code generation and analysis  
- **Python**: Control logic and state machine orchestration  
- **MingW**: For C++ compilation  
- **libFuzzer / AFL++**: Fuzzing support  

---

## 📦 Installation Procedure
- **Microsoft Visual Studios 2022**: Install Microsoft Visual Studios 2022 Community or Professional from Microsoft. During installation, ensure that python development is selected.  
- **Ollama**: Install Ollama 0.6.0 and above 
- **Ollama Models**: Download models from selection here https://ollama.com/models (Select 3b models for on-device and <30b models for GPU resources of less than 24GB RAM)

It is recommended to use multi-agents mechanism using multiple small LLM models rather than single large LLM for speed and practicality on local devices.
This is a guide that we can use. 
Recommended on device GPU resources: 4GB GPU RAM for 3B models, 24GB GPU ram for 21B models
Recommended general NLP and verification states: Gemma3 models from Google
Recommended C++ coding: Qwen2.5-coder models from Alibaba
Recommended C++ gtest: llama3.2 models from Meta 


---

## 📦 Deployment Guide
- **Struture**: Solution file contains the python development code to generate C++ code. Open Visual Studios Solution by double clicking on the solution file
- **Execution**: Runs the solution. Type the following to run "Write me a C++ header class that does a simple mathematical division operation".

  * Status: The current project is now on compilation steps. 


