# 🧠 C++ Micro Agent - Advanced Coverage Improvement System

A powerful LLM-powered tool that automatically generates high-quality unit tests for C++ projects with intelligent coverage improvement and cross-platform support (Linux/Windows).

## 🚀 Key Features

- **🎯 Intelligent Unit Test Generation**: Automatically generates comprehensive unit tests using LLM guidance with iterative coverage improvement
- **📊 Advanced Coverage Analysis**: Detailed branch, line, and function coverage analysis with lcov/gcov integration
- **🔄 Iterative Improvement**: ML-enhanced coverage prediction with automatic test regeneration to achieve target coverage
- **🌐 Cross-Platform Support**: Works on both Linux and Windows with platform-specific compiler detection
- **📈 Comprehensive Reporting**: Generates detailed HTML and text coverage reports with improvement suggestions
- **🏗️ Multi-Project Analysis**: Batch analysis capabilities for multiple C++ projects

## 🛠️ Prerequisites

### For Linux:
```bash
# Install required tools
sudo apt update
sudo apt install -y gcc g++ cmake lcov gcov build-essential

# Install Python dependencies
pip install requests ollama
```

### For Windows:
- **Visual Studio 2022**: Community or Professional with C++ development tools
- **MinGW**: For GCC compilation (included in project)

### Ollama Setup:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download recommended models
ollama pull qwen2.5:0.5b        # For code generation
ollama pull llama3.2:latest     # For unit test generation
```

## 🚀 Quick Start

### 1. Basic Usage
```bash
# Interactive mode (recommended for first-time users)
python3 main.py

# Quick one-click analysis
python3 main.py --quick

# Multi-project batch analysis
python3 main.py --multi

# View existing reports
python3 main.py --reports
```

### 2. Configuration

Edit `CppMicroAgent.cfg` to customize settings:

```ini
[PROJECT_SETTINGS]
# Point to your CMake project directory
default_project_path=TestProjects/YourProject/build

[OUTPUT_SETTINGS]
# Coverage target percentage
coverage_target=85.0
# Maximum improvement iterations
max_iterations=5
```

### 3. Project Structure

Your C++ project should have:
```
YourProject/
├── CMakeLists.txt          # Main CMake file
├── src/                    # Source files
│   ├── main.cpp
│   └── your_code.cpp
└── include/                # Header files
    └── your_code.h
```

## 📁 Project Structure

```
CppMicroAgent/
├── main.py                 # Main entry point
├── CppMicroAgent.cfg      # Configuration file
├── README.md              # This file
├── src/                   # Core modules
│   ├── states_coverage/   # Coverage analysis state machine
│   ├── ConfigReader.py    # Configuration management
│   ├── OllamaClient.py    # LLM integration
│   └── ...               # Other core modules
├── TestProjects/          # Sample and test projects
│   ├── SampleApplication/ # Example C++ project
│   ├── nlohmann-json/     # JSON library example
│   └── ...               # Other test projects
└── output/                # Generated reports and results
    └── UnitTestCoverage/  # Coverage analysis results
```

## 🎯 Usage Examples

### Example 1: Analyze Sample Project
```bash
# Run on the included sample application
python3 main.py --quick
```

### Example 2: Analyze Your Own Project
```bash
# Edit configuration
nano CppMicroAgent.cfg

# Set your project path
default_project_path=path/to/your/cmake/project

# Run analysis
python3 main.py
# Choose option 1: Complete Coverage Analysis
```

### Example 3: Batch Analysis
```bash
# Analyze multiple projects in TestProjects/
python3 main.py --multi
```

## 📊 Understanding Results

After analysis, check the `output/` directory for:

- **📄 coverage_report.txt**: Detailed text report with coverage metrics
- **🌐 lcov_html/index.html**: Interactive HTML coverage report
- **🧪 unit_tests/**: Generated unit test files
- **📈 improvement_history.json**: Coverage improvement tracking

### Coverage Metrics Explained:
- **Line Coverage**: Percentage of source lines executed
- **Function Coverage**: Percentage of functions called
- **Branch Coverage**: Percentage of conditional branches taken

## 🔧 Advanced Configuration

### ML Enhancement Settings:
```ini
[ADVANCED_IMPROVEMENT_SETTINGS]
enable_ml_prediction=true          # Enable ML-enhanced coverage prediction
enable_branch_analysis=true        # Detailed branch coverage analysis
enable_boundary_testing=true       # Boundary value testing
improvement_confidence_threshold=0.7 # Confidence threshold for improvements
```

### Compiler Settings:
```ini
[OLLAMA_SETTINGS]
gcc_compiler=/usr/bin/g++          # Linux GCC path
gcov_tool=/usr/bin/gcov            # gcov tool path
lcov_tool=/usr/bin/lcov            # lcov tool path
```

## 🚨 Troubleshooting

### Common Issues:

1. **"CMakeLists.txt not found"**
   - Ensure your project path in config points to a directory containing CMakeLists.txt
   - Check the `default_project_path` setting in CppMicroAgent.cfg

2. **"Ollama connection failed"**
   - Verify Ollama is running: `ollama list`
   - Check if required models are installed: `ollama pull qwen2.5:0.5b`

3. **"No coverage data generated"**
   - Ensure gcc/g++ and gcov are installed
   - Verify your C++ project compiles successfully
   - Check if CMake is properly configured

4. **"Permission denied during compilation"**
   - On Windows: Run as Administrator
   - On Linux: Check file permissions and ensure gcc is accessible

### Getting Help:
```bash
# Show configuration
python3 main.py --config

# Check project structure
python3 main.py --reports
```

## 🏆 Expected Results

A successful run will achieve:
- ✅ 80%+ code coverage (configurable)
- ✅ Comprehensive unit tests for all functions
- ✅ Branch and edge case coverage
- ✅ Detailed HTML and text reports
- ✅ Iterative improvement tracking

## 🤝 Contributing

This tool is designed for safety-critical C++ development with emphasis on high code coverage and quality assurance through intelligent test generation.