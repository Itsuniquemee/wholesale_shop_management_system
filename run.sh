#!/bin/bash

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed. Please install it first."
    exit 1
fi

echo "Ensuring dependencies are installed..."
pip3 install -r requirements.txt

echo "Starting Wholesale Shop Management System..."
python3 main.py
