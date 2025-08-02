#!/bin/bash
# Test script to run the installer and capture output

echo "Starting CCDK i124q Advanced Installer Test..."
echo "============================================="
echo ""

# Run the installer with automatic mode to see the flow
bash install-advanced.sh --auto

echo ""
echo "============================================="
echo "Test completed!"