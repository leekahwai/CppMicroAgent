#!/bin/bash

# Installation script for CppMicroAgent dependencies
# This script installs lcov, ollama, and GitHub Copilot CLI

set -e  # Exit on error

echo "================================"
echo "CppMicroAgent Dependency Installer"
echo "================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    
    # Check if running in a Debian/Ubuntu environment
    if command -v apt-get &> /dev/null; then
        echo "Installing lcov using apt-get..."
        sudo apt-get update
        sudo apt-get install -y lcov
    elif command -v yum &> /dev/null; then
        echo "Installing lcov using yum..."
        sudo yum install -y lcov
    elif command -v dnf &> /dev/null; then
        echo "Installing lcov using dnf..."
        sudo dnf install -y lcov
    else
        echo "Warning: Could not detect package manager. Please install lcov manually."
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    
    if command -v brew &> /dev/null; then
        echo "Installing lcov using Homebrew..."
        brew install lcov
    else
        echo "Error: Homebrew not found. Please install Homebrew first: https://brew.sh"
        exit 1
    fi
else
    echo "Warning: Unsupported OS type: $OSTYPE"
    echo "Please install lcov manually for your system."
fi

echo ""
echo "Checking lcov installation..."
if command -v lcov &> /dev/null; then
    echo "✓ lcov installed successfully: $(lcov --version | head -n1)"
else
    echo "✗ lcov installation failed or not found in PATH"
fi

echo ""
echo "================================"
echo "Installing Ollama..."
echo "================================"
echo ""

# Install Ollama
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing Ollama for Linux..."
    curl -fsSL https://ollama.com/install.sh | sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing Ollama for macOS..."
    if command -v brew &> /dev/null; then
        brew install ollama
    else
        echo "Installing Ollama using curl..."
        curl -fsSL https://ollama.com/install.sh | sh
    fi
else
    echo "Warning: Unsupported OS for Ollama automatic installation."
    echo "Please install Ollama manually from https://ollama.com"
fi

echo ""
echo "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama installed successfully: $(ollama --version)"
    
    echo ""
    echo "Starting Ollama service..."
    # Start ollama in the background if not already running
    if ! pgrep -x "ollama" > /dev/null; then
        ollama serve > /dev/null 2>&1 &
        sleep 3
        echo "✓ Ollama service started"
    else
        echo "✓ Ollama service already running"
    fi
    
    echo ""
    echo "Downloading tinyllama model (small model for testing)..."
    ollama pull qwen2.5:0.5b
    echo "✓ qwen2.5:0.5b model downloaded successfully"
else
    echo "✗ Ollama installation failed or not found in PATH"
fi

echo ""
echo "================================"
echo "Installing npm packages..."
echo "================================"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Install GitHub Copilot CLI
echo "Installing @github/copilot globally..."
npm install -g @github/copilot

echo ""
echo "================================"
echo "Installation Summary"
echo "================================"
echo ""

# Verify installations
echo "Installed tools:"
echo ""

if command -v lcov &> /dev/null; then
    echo "✓ lcov: $(lcov --version | head -n1)"
else
    echo "✗ lcov: Not found"
fi

if command -v ollama &> /dev/null; then
    echo "✓ ollama: $(ollama --version)"
    echo "  Available models:"
    ollama list | head -n 5
else
    echo "✗ ollama: Not found"
fi

if npm list -g @github/copilot &> /dev/null; then
    echo "✓ @github/copilot: Installed"
else
    echo "✗ @github/copilot: Not found"
fi

echo ""
echo "Installation complete!"
