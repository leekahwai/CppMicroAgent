# 🧠 C++ Micro Agent - AI-Enhanced Unit Test Generation

An intelligent AI-powered tool that automatically generates comprehensive unit tests for C++ projects with automated coverage analysis and intelligent test improvement capabilities.

## 🚀 Key Features

- **🤖 AI-Enhanced Test Generation**: Optionally uses Ollama/LLM for context-aware, intelligent test generation with proper initialization and threading support
- **⚡ Fast Template-Based Generation**: Works perfectly without AI using proven template-based test generation (~30 seconds)
- **📊 Comprehensive Coverage Analysis**: Detailed line, function, and branch coverage analysis with lcov/gcov integration
- **🎯 Multiple Test Projects**: Pre-configured support for SampleApp, TinyXML2, Ninja, Catch2, and more
- **📈 Rich HTML Reports**: Interactive coverage reports with color-coded source highlighting
- **🔧 Zero Configuration**: Auto-detects Ollama, GoogleTest, and compiler tools - works out of the box
- **🚀 Quick Start Menu**: Interactive script guides you through test generation and analysis

## 🛠️ Prerequisites

### Required (Linux):
```bash
# Install essential build tools
sudo apt update
sudo apt install -y gcc g++ cmake lcov gcov build-essential python3

# That's all you need to get started!
```

### Optional - AI-Enhanced Mode:
```bash
# Install Ollama for intelligent test generation (optional)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a recommended model
ollama pull qwen2.5:0.5b        # Fast, lightweight (recommended)
# OR
ollama pull llama3.2:latest     # Larger, higher quality

# Run quick_start.sh with --ollama flag to use AI mode
./quick_start.sh --ollama
```

**Note**: The tool works perfectly fine without Ollama using template-based test generation. Ollama is only needed for Option 3 (AI-Powered Test Improver) and enhanced test generation.

## 🚀 Quick Start

### Interactive Menu (Recommended)

The easiest way to use C++ Micro Agent is through the interactive quick start script:

```bash
./quick_start.sh
```

**Available Options:**
1. **Generate Unit Tests** (~30 seconds)
   - Automatically generates unit tests for your C++ project
   - Uses enhanced generators for TinyXML2 (78.3% function coverage)
   - Uses ultimate generator for other projects (65%+ function coverage target)
   - No AI/Ollama required - works with template-based generation

2. **Full Coverage Analysis** (~1-2 minutes)
   - Analyzes tests generated from Option 1
   - Compiles tests with coverage instrumentation
   - Generates detailed HTML and text reports
   - No AI/Ollama required

3. **AI-Powered Test Improver** (~3-5 minutes)
   - **Requires Ollama with qwen3-coder:480b model**
   - Analyzes your code patterns with AI
   - Suggests C++ parser improvements
   - Generates optimized test strategies
   - Provides actionable recommendations

4. **Select Project**
   - Switch between available test projects:
     - SampleApp (default multi-threaded application)
     - TinyXML2 (XML library)
     - Ninja (build system)
     - Catch2, fmt, spdlog, nlohmann-json libraries

5. **Exit**

### Your First Run

```bash
# Step 1: Run the quick start script
./quick_start.sh

# Step 2: Select Option 1 to generate unit tests
# Wait ~30 seconds for test generation and compilation

# Step 3: Select Option 2 for full coverage analysis
# Wait ~1-2 minutes for test execution and report generation

# Step 4: View the interactive HTML coverage report
open output/UnitTestCoverage/lcov_html/index.html
# Or check the text summary:
cat coverage_report.txt
```

### Using AI-Enhanced Mode (Optional)

```bash
# Option A: Use --ollama flag (for Option 1 only)
./quick_start.sh --ollama

# Option B: Use Option 3 from the menu
./quick_start.sh
# Then select: 3. AI-Powered Test Improver
```

## 📊 How It Works

### Option 1: Generate Unit Tests

The test generator automatically:
1. **Discovers Source Files**: Scans your project for .h and .cpp files
2. **Parses C++ Code**: Extracts classes, methods, and function signatures
3. **Detects Project Type**: Uses specialized generators for known projects (TinyXML2, etc.)
4. **Generates Mock Headers**: Creates necessary mock files for dependencies
5. **Creates Unit Tests**: Generates comprehensive test files for each method
6. **Compiles Tests**: Builds all tests using g++ with GoogleTest
7. **Reports Results**: Shows pass/fail statistics and compilation status

**Special Project Handling:**
- **TinyXML2**: Uses enhanced generator achieving 78.3% function coverage (317/405 functions)
- **Other Projects**: Uses ultimate generator targeting 65%+ function coverage with all strategies

**Test Generation Strategies:**
- Basic value testing (boundary values, null checks)
- Return type validation
- Exception safety testing
- Threading-aware test generation
- Proper initialization/cleanup handling

### Option 2: Full Coverage Analysis

The coverage analyzer:
1. **Compiles with Instrumentation**: Rebuilds tests with gcov coverage flags
2. **Executes All Tests**: Runs each test binary and collects coverage data
3. **Processes Coverage Data**: Uses lcov to aggregate .gcda coverage files
4. **Generates Reports**: Creates both HTML (interactive) and text (summary) reports
5. **Highlights Coverage**: Color-codes source files showing covered/uncovered lines

**Coverage Metrics:**
- **Line Coverage**: Percentage of source lines executed
- **Function Coverage**: Percentage of functions called at least once
- **Branch Coverage**: Percentage of conditional branches taken

### Option 3: AI-Powered Test Improver (Advanced)

The AI improver uses Qwen AI to:
1. **Analyze Code Patterns**: Examines your project's specific code structure
2. **Identify Gaps**: Detects areas where the C++ parser could be enhanced
3. **Generate Strategies**: Creates project-specific test improvement recommendations
4. **Provide Guidance**: Offers actionable suggestions for better coverage

**Requirements:**
- Ollama must be installed and running
- qwen3-coder:480b model (or qwen2.5-coder:7b as alternative)
- 3-5 minutes processing time

### Option 4: Select Project

Allows switching between test projects:
- `TestProjects/SampleApp/SampleApp` - Default multi-threaded application
- `TestProjects/tinyxml2` - TinyXML2 XML library
- `TestProjects/ninja` - Ninja build system
- `TestProjects/catch2-library` - Catch2 testing framework
- `TestProjects/fmt-library` - fmt formatting library
- `TestProjects/spdlog-library` - spdlog logging library
- `TestProjects/nlohmann-json` - nlohmann JSON library

Updates `CppMicroAgent.cfg` with the selected project path.

## 📁 Project Structure

```
CppMicroAgent/
├── quick_start.sh              # 🎯 MAIN ENTRY POINT (interactive menu)
├── install.sh                  # Installation and setup script
├── CppMicroAgent.cfg           # Configuration file (project settings)
├── README.md                   # This file
│
├── src/                        # Core Python modules
│   ├── quick_test_generator/   # Fast test generation (Option 1)
│   │   ├── generate_and_build_tests.py    # Main test generator
│   │   ├── ollama_test_improver.py        # AI test improver (Option 3)
│   │   └── ollama_test_fixer.py           # AI test fixer
│   │
│   ├── run_coverage_analysis.py           # Coverage analyzer (Option 2)
│   ├── ultimate_test_generator.py         # Ultimate test generation strategy
│   ├── enhanced_tinyxml2_test_generator.py # TinyXML2 specialized generator
│   ├── ConfigReader.py         # Configuration reader
│   ├── OllamaClient.py         # Ollama/LLM integration
│   └── ...                     # Other utilities
│
├── TestProjects/               # Sample and test projects
│   ├── SampleApp/             # Default multi-threaded application
│   ├── tinyxml2/              # TinyXML2 XML library
│   ├── ninja/                 # Ninja build system
│   ├── catch2-library/        # Catch2 testing framework
│   ├── fmt-library/           # fmt formatting library
│   ├── spdlog-library/        # spdlog logging library
│   └── nlohmann-json/         # nlohmann JSON library
│
├── output/                     # Generated outputs
│   ├── ConsolidatedTests/     # Option 1: Generated tests
│   │   ├── mocks/            # Mock headers
│   │   ├── tests/            # Test source files
│   │   ├── bin/              # Compiled test executables
│   │   └── test_metadata.json # Test catalog
│   │
│   ├── UnitTestCoverage/      # Option 2: Coverage reports
│   │   ├── coverage.info     # Raw coverage data
│   │   ├── coverage_report.txt # Text summary (copied to root)
│   │   └── lcov_html/        # HTML reports
│   │
│   └── OllamaImprovements/    # Option 3: AI recommendations
│       ├── parser_improvements.md
│       └── test_strategies.md
│
├── googletest-1.16.0/         # GoogleTest framework (included)
├── run_tinyxml2_enhanced_tests.sh  # TinyXML2 test runner
└── coverage_report.txt        # Latest coverage summary (quick access)
```

## 🎯 Usage Examples

### Example 1: Quick Start (Default Project)
```bash
# Run the interactive menu
./quick_start.sh

# Follow the prompts:
# 1. Select Option 1 (Generate Unit Tests) - wait ~30 seconds
# 2. Select Option 2 (Full Coverage Analysis) - wait ~1-2 minutes
# 3. View results: open output/UnitTestCoverage/lcov_html/index.html
```

### Example 2: Switch to TinyXML2 Project
```bash
./quick_start.sh

# Select Option 4 (Select Project)
# Choose TinyXML2 from the list
# Then run Option 1 to generate tests (achieves 78.3% function coverage)
# Then run Option 2 to verify coverage
```

### Example 3: AI-Enhanced Test Improvement
```bash
# Ensure Ollama is installed and has qwen3-coder:480b model
ollama pull qwen3-coder:480b

# Run quick start and select Option 3
./quick_start.sh
# Select: 3. AI-Powered Test Improver

# Review AI recommendations in output/OllamaImprovements/
```

### Example 4: Use AI for Test Generation
```bash
# Ensure Ollama is installed with a model
ollama pull qwen2.5:0.5b

# Run quick start with --ollama flag
./quick_start.sh --ollama

# Select Option 1 (will use AI-enhanced generation)
```

## 📊 Understanding Results

### Option 1 Output (Generated Tests)
Located in `output/ConsolidatedTests/`:
- **test_metadata.json**: Catalog of all generated tests with metadata
- **tests/**: Individual test source files (e.g., `Program_init.cpp`)
- **bin/**: Compiled test executables ready to run
- **mocks/**: Mock header files for dependencies

### Option 2 Output (Coverage Reports)
Located in `output/UnitTestCoverage/`:
- **coverage_report.txt**: Detailed text summary (also copied to root directory)
- **lcov_html/index.html**: Interactive HTML report with color-coded coverage
- **coverage.info**: Raw coverage data in lcov format

**Also available**: `coverage_report.txt` in the project root for quick access

### Option 3 Output (AI Recommendations)
Located in `output/OllamaImprovements/`:
- **parser_improvements.md**: Suggested C++ parser enhancements
- **test_strategies.md**: Project-specific test generation strategies

### Coverage Metrics Explained

**Line Coverage**: Percentage of source code lines executed during test runs
- Green lines: Executed by tests
- Red lines: Not executed

**Function Coverage**: Percentage of functions called at least once
- Important for ensuring all APIs are tested

**Branch Coverage**: Percentage of conditional branches (if/else) taken
- Critical for logic correctness

### Visual HTML Report Features
Open `output/UnitTestCoverage/lcov_html/index.html` to see:
- **Summary Dashboard**: Overall project coverage metrics
- **File List**: Per-file coverage percentages
- **Source Code View**: Color-coded line-by-line coverage
- **Branch Details**: Which conditional branches were tested
- **Uncovered Code**: Highlighted areas needing attention

### Expected Coverage Results

**SampleApp Project**:
- ~60-75% line coverage (multi-threaded application)
- Tests for basic functionality pass consistently
- Some threading tests may be skipped for stability

**TinyXML2 Project** (with enhanced generator):
- 78.3% function coverage (317/405 functions)
- 72.3% line coverage (1323/1829 lines)
- 169 passing tests
- Comprehensive XML parsing and manipulation coverage

**Other Projects**:
- 65%+ function coverage target
- Varies based on project complexity
- Ultimate generator applies all strategies

## 🔧 Configuration

### CppMicroAgent.cfg

The configuration file controls key settings:

```ini
[OLLAMA_SETTINGS]
model_used=qwen2.5:0.5b          # Model for general use
unittest_model=qwen3-coder:480b   # Model for Option 3 (AI improver)
gcc_compiler=/usr/bin/g++         # C++ compiler path
gcov_tool=/usr/bin/gcov           # Coverage tool
lcov_tool=/usr/bin/lcov           # Report generator

[PROJECT_SETTINGS]
project_path=TestProjects/SampleApp/SampleApp  # Current project
# Available: SampleApp, tinyxml2, ninja, catch2-library, etc.

[OUTPUT_SETTINGS]
clean_output_before_run=true      # Clean before generation
output_directory=output           # Output location
coverage_target=80.0              # Target coverage %
max_iterations=3                  # Max improvement iterations
```

### Changing Projects

**Method 1: Use Option 4 in quick_start.sh** (Recommended)
```bash
./quick_start.sh
# Select: 4. Select Project
# Choose from the list
```

**Method 2: Edit CppMicroAgent.cfg directly**
```bash
nano CppMicroAgent.cfg
# Change project_path to desired project
```

### Available Test Projects

- `TestProjects/SampleApp/SampleApp` - Multi-threaded application (default)
- `TestProjects/tinyxml2` - XML parsing library (78.3% coverage achievable)
- `TestProjects/ninja` - Build system
- `TestProjects/catch2-library` - Testing framework
- `TestProjects/fmt-library` - Formatting library
- `TestProjects/spdlog-library` - Logging library
- `TestProjects/nlohmann-json` - JSON library

### Customizing for Your Project

To analyze your own C++ project:

1. Place your project in `TestProjects/YourProject/`
2. Ensure it has a standard structure:
   ```
   YourProject/
   ├── src/ or source files
   ├── inc/ or include/ (headers)
   └── (optional) common.h
   ```
3. Update `CppMicroAgent.cfg`:
   ```ini
   project_path=TestProjects/YourProject
   ```
4. Run `./quick_start.sh` and select Option 1

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "Prerequisites not found"
**Solution**:
```bash
# Install required tools
sudo apt update
sudo apt install -y gcc g++ cmake lcov gcov build-essential python3

# Verify installation
which g++ gcov lcov python3
```

#### 2. "Ollama not found" (for Option 3 or --ollama flag)
**Note**: Ollama is optional - the tool works perfectly without it!

**Solution** (if you want AI features):
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve

# Pull a model (in another terminal)
ollama pull qwen2.5:0.5b          # For general use
ollama pull qwen3-coder:480b      # For Option 3 (AI improver)
```

#### 3. "No tests found" when running Option 2
**Cause**: Option 1 must be run first

**Solution**:
```bash
./quick_start.sh
# Select Option 1 first, then Option 2
```

#### 4. "GoogleTest not found"
**Solution**:
```bash
# Check if GoogleTest libraries exist
ls googletest-1.16.0/build/lib/

# If missing, build GoogleTest
cd googletest-1.16.0
mkdir -p build && cd build
cmake ..
make
cd ../..
```

#### 5. Tests fail or timeout
**This is expected** for complex threading code:
- Some tests (InterfaceA, InterfaceB) are automatically skipped
- Tests with threading issues timeout after 10 seconds
- Coverage analysis works with passing tests only
- This does not affect overall functionality

**Check test results**:
```bash
# View test output
cat output/ConsolidatedTests/test_results.log

# Manually run a test
cd output/ConsolidatedTests/bin
./test_name
```

#### 6. "Permission denied" on quick_start.sh
**Solution**:
```bash
chmod +x quick_start.sh
./quick_start.sh
```

#### 7. Low coverage percentages
**Expected behavior**: Complex code may have lower coverage
- Multi-threaded code: 60-75% is typical
- Threading-heavy functions may not be fully testable
- Use Option 3 (AI improver) for suggestions

**Tips**:
- Try different test projects (TinyXML2 achieves 78.3%)
- Review HTML coverage report to identify gaps
- Check `coverage_report.txt` for per-file metrics

#### 8. Compilation errors during test generation
**Common causes**:
- Missing dependencies in project
- Complex template code
- Circular includes

**Solution**:
```bash
# Check compiler version
g++ --version  # Should be 5.0+

# View compilation errors
cat output/ConsolidatedTests/build.log
```

## 🏆 Expected Performance

### Timing Benchmarks

**Option 1: Generate Unit Tests**
- SampleApp: ~30 seconds
- TinyXML2: ~45 seconds (more comprehensive tests)
- Other projects: 30-60 seconds depending on size

**Option 2: Full Coverage Analysis**
- SampleApp: ~1-2 minutes
- TinyXML2: ~2-3 minutes
- Includes compilation, test execution, and report generation

**Option 3: AI-Powered Test Improver**
- Analysis time: 3-5 minutes
- Requires qwen3-coder:480b model
- Generates detailed recommendations

### Coverage Achievements

**SampleApp (Multi-threaded Application)**:
- Line Coverage: 60-75%
- Function Coverage: 65-80%
- ~50+ unit tests generated
- Threading tests handled gracefully

**TinyXML2 (with enhanced generator)**:
- Function Coverage: 78.3% (317/405 functions)
- Line Coverage: 72.3% (1323/1829 lines)
- 169 passing tests
- Comprehensive XML parsing coverage

**Ninja Build System**:
- Function Coverage: 65%+
- Complex build system logic tested
- Multiple compilation strategies covered

**Library Projects** (catch2, fmt, spdlog, nlohmann-json):
- Coverage varies by project complexity
- Header-only libraries supported
- Template-heavy code handled

### Test Generation Statistics

**Typical Output**:
- 40-150 tests generated per project
- 80-95% compilation success rate
- 70-85% tests passing
- Remaining tests timeout or skip (threading issues)

### Success Indicators

✅ **Successful Run**:
- Tests compile without major errors
- Most tests pass (70%+ pass rate)
- Coverage report generated
- HTML report viewable
- coverage_report.txt in root directory

⚠️ **Partial Success** (Still Useful):
- Some tests fail/timeout (normal for threading)
- Coverage still calculated from passing tests
- HTML report shows coverage gaps
- AI improver can suggest enhancements

❌ **Needs Attention**:
- No tests compile
- GoogleTest not found
- Project path incorrect
- Missing prerequisites

## 🎯 Quick Reference

### Essential Commands

```bash
# Main entry point (recommended)
./quick_start.sh                 # Interactive menu

# With AI enhancement
./quick_start.sh --ollama        # Use AI for test generation (Option 1)

# Direct script execution (advanced)
python3 src/quick_test_generator/generate_and_build_tests.py   # Option 1
python3 src/run_coverage_analysis.py                           # Option 2
python3 src/quick_test_generator/ollama_test_improver.py       # Option 3
```

### Quick Access Paths

```bash
# View generated tests
ls output/ConsolidatedTests/tests/

# View test executables  
ls output/ConsolidatedTests/bin/

# Quick coverage summary
cat coverage_report.txt

# Full coverage report (HTML)
open output/UnitTestCoverage/lcov_html/index.html

# AI recommendations
cat output/OllamaImprovements/*.md
```

### Typical Workflow

1. **Initial Setup** (one-time):
   ```bash
   # Install prerequisites
   sudo apt install -y gcc g++ cmake lcov gcov build-essential python3
   
   # Optional: Install Ollama for AI features
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull qwen2.5:0.5b
   ```

2. **Generate Tests**:
   ```bash
   ./quick_start.sh
   # Select: 1. Generate Unit Tests
   ```

3. **Analyze Coverage**:
   ```bash
   # In same quick_start.sh session
   # Select: 2. Full Coverage Analysis
   ```

4. **Review Results**:
   ```bash
   # View HTML report
   open output/UnitTestCoverage/lcov_html/index.html
   
   # Or quick text summary
   cat coverage_report.txt
   ```

5. **Iterate** (optional):
   ```bash
   # Use AI to get improvement suggestions
   ./quick_start.sh
   # Select: 3. AI-Powered Test Improver
   ```

### Configuration Quick Reference

```bash
# Change project
./quick_start.sh
# Select: 4. Select Project

# Or edit config directly
nano CppMicroAgent.cfg
# Change: project_path=TestProjects/YourProject

# Check current settings
cat CppMicroAgent.cfg
```

### Verification Commands

```bash
# Check prerequisites
which g++ gcov lcov python3 ollama

# Verify GoogleTest
ls googletest-1.16.0/build/lib/

# Check test generation output
ls -la output/ConsolidatedTests/

# Verify coverage was generated
ls -la output/UnitTestCoverage/
```

## 💡 Advanced Features

### Specialized Test Generators

The tool automatically selects the best generator for your project:

**Enhanced TinyXML2 Generator**:
- Specialized for TinyXML2 library
- Achieves 78.3% function coverage (317/405)
- 169 comprehensive tests
- Handles XML parsing edge cases

**Ultimate Test Generator**:
- Used for most projects
- Targets 65%+ function coverage
- Applies multiple strategies:
  - Boundary value testing
  - Return type validation
  - Exception safety testing
  - Threading-aware generation

**Generic Enhanced Generator**:
- Fallback for complex projects
- Template-based reliable generation
- Fast and consistent

### AI-Powered Features (Optional)

**With --ollama flag (Option 1)**:
- Context-aware test generation
- Proper initialization/cleanup handling
- Threading safety improvements
- Better edge case coverage

**Option 3: AI Test Improver**:
- Analyzes project-specific patterns
- Suggests parser enhancements
- Generates optimization strategies
- Provides actionable recommendations

### Threading Support

The tool handles multi-threaded code intelligently:
- Adds sleep delays for thread initialization
- Calls init() before tests
- Calls close() after tests
- Skips problematic threading tests
- Times out after 10 seconds

### Coverage Analysis Features

**Multiple Report Formats**:
- Interactive HTML with color coding
- Text summary for quick review
- Raw lcov data for integration
- Per-file detailed breakdowns

**Coverage Types**:
- Line coverage (execution)
- Function coverage (API testing)
- Branch coverage (logic paths)

## 🤝 Contributing

This tool is designed for:
- Safety-critical C++ development
- Automated testing and CI/CD integration
- Coverage analysis and quality assurance
- Research in automated test generation

**Key Design Principles**:
- Zero configuration for common cases
- Intelligent auto-detection of tools
- Graceful degradation without AI
- Comprehensive error handling
- Fast iteration cycles

## 📚 Additional Documentation

For more detailed information:
- **quick_start.sh**: See inline comments for option details
- **CppMicroAgent.cfg**: Configuration file with setting explanations
- **output/**: Generated reports with embedded documentation

## 🔗 Related Tools

This project includes:
- **GoogleTest 1.16.0**: C++ testing framework
- **lcov/gcov**: Coverage analysis tools
- **Ollama integration**: Optional AI enhancement

**Test Projects Included**:
- TinyXML2: XML parsing library
- Ninja: Build system
- Catch2: Testing framework
- fmt: Formatting library
- spdlog: Logging library
- nlohmann-json: JSON library

---

**Getting Started**: Run `./quick_start.sh` and select Option 1 to begin!

**Need Help?**: Check the Troubleshooting section or review test output in `output/ConsolidatedTests/`

**Quick Summary Access**: Latest coverage results are always in `coverage_report.txt` at the project root.