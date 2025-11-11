# QR Sticker Generation

A Python-based system for generating QR code labels for shelf management, formatted for Avery 1" x 2-5/8" label sheets.

## Overview

This system reads inventory data from a CSV file and generates professional-quality QR code labels that include:
- QR codes linking to the shelf URL translator
- Company logo
- WISE ID text labels
- Proper formatting for Avery label sheets

## Files

- `gen_qr_codes.py` - Generates clean QR code images from CSV data
- `gen_pdf.py` - Creates PDF labels with QR codes, logos, and text
- `main.sh` - Automation script to run the complete workflow

## Requirements

- Python 3.12+
- Virtual environment (`.venv`)
- Required packages: `qrcode[pil]`, `pylabels`, `reportlab`, `pandas`, `Pillow`

## Input Files

- `WISE Asset Matrix - Sheet1.csv` - Inventory data with columns:
  - `WISE_ID` - Asset identifier (e.g., WISE-01)
  - `Shelf_QR_ID` - Unique shelf identifier
  - `QR Code Printed` - Boolean flag (FALSE = needs printing)
- `logo.JPG` - Company logo image

## Usage

### Quick Start
```bash
./main.sh
```

### Manual Steps
```bash
# Generate QR codes
python gen_qr_codes.py

# Generate PDF labels
python gen_pdf.py
```

## Output

- `qr_codes/` - Directory containing individual QR code PNG files
- `qr_codes.pdf` - Print-ready PDF formatted for Avery 1" x 2-5/8" labels

## Configuration

Label dimensions and spacing can be easily customized in `gen_pdf.py`:

```python
# Label dimensions (currently Avery 1" x 2-5/8")
LABEL_WIDTH_MM = 66.675   # 2.625 inches
LABEL_HEIGHT_MM = 25.4    # 1 inch

# Spacing settings
LABEL_PADDING_PERCENT = 0.10    # 10% padding
QR_CODE_WIDTH_PERCENT = 0.70    # QR code takes 70% width
LOGO_SIZE_PERCENT = 0.80        # Logo max size
```

## Features

- **Automated workflow** - Single command generates everything
- **Professional layout** - QR code left, logo right, WISE ID below
- **Configurable sizing** - Easy to adapt for different label formats
- **Error handling** - Graceful handling of missing files
- **Clean output** - Automatic cleanup of temporary files
- **Batch processing** - Processes all unpublished items at once

## Author

Yash Patel - November 11, 2025