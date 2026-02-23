#!/bin/bash
# Artemis Environment Setup Script
# Author: Jerry Wayne Dawson Jr. | Nashville, TN

echo "🛰️  Artemis-Sovereign-Lattice: Initializing Environment..."

# Update and install Python/Git if missing
pkg update && pkg upgrade -y
pkg install python git -y

# Install Core Quantum and AI Frameworks
echo "⚛️  Installing Quantum and Neuromorphic dependencies..."
pip install --upgrade pip
pip install qiskit numpy strawberryfields

# Verify Installation
echo "✅ Environment Ready."
echo "🚀 To launch the 33F Sovereign Engine, run: python artemis_core_runtime.py"
