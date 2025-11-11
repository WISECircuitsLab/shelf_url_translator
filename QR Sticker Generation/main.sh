#!/bin/bash
# file: main.sh
# Author: Yash Patel
# Date: 2025-11-11
# Description: This script runs the QR code generation and subsequent PDF Generation Process.
# 
# USAGE: 
#   Run directly: ./main.sh
#   Do NOT use: source main.sh (this will terminate your shell on error)

# Detect if script is being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    SOURCED=false
else
    SOURCED=true
    echo "Warning: This script is being sourced. If errors occur, your shell may terminate."
    echo "Recommended usage: ./main.sh"
fi

# Set the Python environment path
export PYTHON_ENV=/home/yashp/dev/shelf_url_translator/.venv/bin/python

# Change to the parent directory where the scripts are located
cd /home/yashp/dev/shelf_url_translator/QR\ Sticker\ Generation

# Run QR code generation
echo "Generating QR codes..."
$PYTHON_ENV gen_qr_codes.py

# Check if QR code generation was successful
if [ $? -eq 0 ]; then
    echo "QR codes generated successfully."
    
    # Run PDF generation
    echo "Generating PDF..."
    $PYTHON_ENV gen_pdf.py
    
    if [ $? -eq 0 ]; then
        echo "PDF generated successfully."
        echo "Process completed! Check qr_codes.pdf"
    else
        echo "Error: PDF generation failed."
        if [ "$SOURCED" = false ]; then
            exit 1
        else
            return 1
        fi
    fi
else
    echo "Error: QR code generation failed."
    if [ "$SOURCED" = false ]; then
        exit 1
    else
        return 1
    fi
fi
