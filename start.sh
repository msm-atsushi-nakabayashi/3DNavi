#!/bin/bash

# 3DNavi Startup Script
echo "🚀 Starting 3DNavi Manufacturing Platform..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip and try again."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your Python environment."
        exit 1
    fi
else
    echo "⚠️  requirements.txt not found. Assuming dependencies are already installed."
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest test_main.py -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix the issues before starting the server."
    exit 1
fi

echo "✅ All tests passed!"

# Start the server
echo "🌐 Starting server on port 12000..."
echo "📱 Access the application at:"
echo "   Local: http://localhost:12000"
echo "   External: https://work-1-nqrqnrulfiwdqxwt.prod-runtime.all-hands.dev"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py