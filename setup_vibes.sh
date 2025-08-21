#!/bin/bash

# Setup script for Vibes Manager Python application
# This script installs dependencies and runs the vibes manager

echo "🎵 Setting up Vibes Manager..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if Cosmos DB emulator is running
echo "🔍 Checking if Cosmos DB emulator is running..."
if curl -k -s https://localhost:8081 > /dev/null 2>&1; then
    echo "✅ Cosmos DB emulator is running"
elif curl -s http://localhost:1234 > /dev/null 2>&1; then
    echo "✅ Cosmos DB emulator detected (Data Explorer available)"
else
    echo "⚠️  Cosmos DB emulator may not be running"
    echo "💡 Start it with: ./start-cosmos-emulator.sh"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Starting Vibes Manager..."
echo "================================"
python3 vibes_manager.py
