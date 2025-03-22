# 🧠 LLM-Powered C++ Code Quality Assistant

This project leverages [Ollama](https://ollama.com) and Large Language Models (LLMs) to assist developers in C++ code generation and quality assurance. It uses intelligent, modular **state machines** to automate tasks such as unit test creation, static analysis, and fuzzing, aiming to streamline and strengthen your development workflow.

## 🚀 Key Features

- **LLM-based C++ Code Generation**  
  Automatically generate C++ functions and classes based on high-level descriptions or templates using powerful LLMs via Ollama.

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
- **LLVM/Clang tooling**: For coverage, static analysis, and instrumentation  
- **libFuzzer / AFL++**: Fuzzing support  

---

## 📦 Project Structure

