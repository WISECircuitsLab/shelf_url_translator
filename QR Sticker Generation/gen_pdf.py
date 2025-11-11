# file: gen_pdf.py
# Author: Yash Patel
# Date: 2025-11-11
# Description: This script generates a PDF from the generated QR codes. It compiles all PNG files in the 'qr_codes' directory into a single PDF file named 'qr_codes.pdf'.
# It uses the following libraries: pylabels and reportlab

import labels
import os
import glob
from reportlab.graphics import shapes
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

# Configuration - EASILY CUSTOMIZABLE LABEL SETTINGS
qr_dir = "qr_codes"
output_pdf = "qr_codes.pdf"
logo_file = "logo.JPG"  # Path to the logo image file (using JPG instead of jpeg)

# ===== LABEL DIMENSIONS CONFIGURATION =====
# Current: Avery 1" x 2-5/8" (25.4mm x 66.675mm) labels
# To change label size, modify these values:
LABEL_WIDTH_MM = 66.675  # 2.625 inches - Width of each label
LABEL_HEIGHT_MM = 25.4   # 1 inch - Height of each label

# Page settings (standard 8.5" x 11" paper)
PAGE_WIDTH_MM = 215.9   # 8.5 inches  
PAGE_HEIGHT_MM = 279.4  # 11 inches

# Spacing and sizing settings (relative to label size)
LABEL_PADDING_PERCENT = 0.10  # 10% padding inside each label
QR_CODE_WIDTH_PERCENT = 0.70  # QR code takes 70% of available width
LOGO_SIZE_PERCENT = 0.80      # Logo max size as % of available height

# Margins around the entire page
PAGE_MARGINS_MM = 5  # Margins on all sides of the page

def generate_pdf_from_qr_codes():
    """Generate a PDF with QR codes and logos formatted for Avery 1" x 2-5/8" labels."""
    
    # Check if QR codes directory exists
    if not os.path.exists(qr_dir):
        print(f"Error: {qr_dir} directory not found. Please run gen_qr_codes.py first.")
        return
    
    # Get all PNG files from QR codes directory
    qr_files = glob.glob(os.path.join(qr_dir, "*.png"))
    if not qr_files:
        print(f"Error: No PNG files found in {qr_dir} directory.")
        return
    
    print(f"Found {len(qr_files)} QR code files in {qr_dir} directory")
    
    # Check if logo exists and prepare optimized version
    logo_file_path = None
    if not os.path.exists(logo_file):
        print(f"Warning: Logo file {logo_file} not found. Proceeding without logo.")
    else:
        print(f"Using logo file: {logo_file}")
        # Create an optimized logo for PDF generation
        optimized_logo = "temp_logo_optimized.png"
        try:
            with Image.open(logo_file) as img:
                # Resize logo to a reasonable size for PDF (max 200x200)
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(optimized_logo, "PNG", optimize=True)
                logo_file_path = optimized_logo
                print(f"Created optimized logo: {optimized_logo}")
        except Exception as e:
            print(f"Warning: Could not process logo file - {e}")
    
    # Extract WISE IDs from filenames - no CSV needed
    print("Extracting WISE IDs from QR code filenames...")
    
    # Calculate label specifications for a standard 8.5" x 11" sheet
    # Determine how many labels can fit based on configured dimensions
    cols = int(PAGE_WIDTH_MM // LABEL_WIDTH_MM)
    rows = int(PAGE_HEIGHT_MM // LABEL_HEIGHT_MM)
    
    print(f"Label configuration:")
    print(f"  - Label size: {LABEL_WIDTH_MM:.1f}mm x {LABEL_HEIGHT_MM:.1f}mm")
    print(f"  - Page size: {PAGE_WIDTH_MM:.1f}mm x {PAGE_HEIGHT_MM:.1f}mm")
    print(f"  - Grid: {cols} columns x {rows} rows = {cols*rows} labels per page")
    
    # Create label specifications with configurable margins
    specs = labels.Specification(
        PAGE_WIDTH_MM, PAGE_HEIGHT_MM, 
        cols, rows, 
        LABEL_WIDTH_MM, LABEL_HEIGHT_MM,
        left_margin=PAGE_MARGINS_MM, right_margin=PAGE_MARGINS_MM,
        top_margin=PAGE_MARGINS_MM, bottom_margin=PAGE_MARGINS_MM,
        corner_radius=1
    )
    
    # Create drawing function
    def draw_label(label, width, height, qr_file):
        """Draw QR code and logo on each label with configurable padding."""
        
        # Calculate padding based on configuration
        padding = min(width, height) * LABEL_PADDING_PERCENT
        usable_width = width - (2 * padding)
        usable_height = height - (2 * padding)
        
        # Extract WISE ID from filename
        filename = os.path.basename(qr_file)
        wise_id = filename.split('_')[0]  # Extract WISE-XX from filename
        
        try:
            # Calculate QR code size using configuration
            qr_size = min(usable_height, usable_width * QR_CODE_WIDTH_PERCENT)
            
            # Position QR code on the left side
            qr_x = padding
            qr_y = padding + (usable_height - qr_size) / 2  # Center vertically
            
            # Use the QR code file directly
            label.add(shapes.Image(qr_x, qr_y, qr_size, qr_size, qr_file))
            
            # Add logo on the right side if available
            if logo_file_path and os.path.exists(logo_file_path):
                try:
                    # Calculate logo size using configuration
                    remaining_width = usable_width - qr_size - (padding * 0.5)
                    logo_max_size = min(remaining_width, usable_height * LOGO_SIZE_PERCENT)
                    
                    # Position logo on the right side
                    logo_x = padding + qr_size + (padding * 0.5)
                    logo_y = padding + (usable_height - logo_max_size) / 2
                    
                    # Use the logo file directly
                    label.add(shapes.Image(logo_x, logo_y, logo_max_size, logo_max_size, logo_file_path))
                        
                except Exception as e:
                    print(f"Warning: Could not add logo - {e}")
            
            # Add WISE ID text below QR code
            text_y = padding + 2  # Small margin from bottom
            label.add(shapes.String(
                qr_x + qr_size/2, text_y, wise_id,
                fontName="Helvetica-Bold", fontSize=8,
                textAnchor="middle"
            ))
                
        except Exception as e:
            print(f"Error processing {qr_file}: {e}")
            # Fallback: just add the WISE ID as text
            label.add(shapes.String(
                width/2, height/2, wise_id,
                fontName="Helvetica", fontSize=12,
                textAnchor="middle"
            ))
    
    # Create the sheet
    sheet = labels.Sheet(specs, draw_label, border=True)
    
    # Add all QR code files to the sheet
    for qr_file in sorted(qr_files):
        sheet.add_label(qr_file)
    
    # Save the PDF with better error handling
    print("Saving PDF...")
    try:
        # Remove existing PDF if it exists
        if os.path.exists(output_pdf):
            os.remove(output_pdf)
        
        # Save the new PDF
        sheet.save(output_pdf)
        
        # Verify the PDF was created successfully
        if os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
            print(f"PDF saved successfully: {output_pdf}")
        else:
            raise Exception("PDF file was not created or is empty")
            
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return False
    
    # Cleanup temporary files
    if logo_file_path and logo_file_path.startswith("temp_"):
        try:
            os.remove(logo_file_path)
            print(f"Cleaned up temporary file: {logo_file_path}")
        except:
            pass  # Ignore cleanup errors
    
    print(f"Generated PDF: {output_pdf}")
    print(f"Total labels: {sheet.label_count} on {sheet.page_count} page(s)")
    print(f"Label specifications: {cols} columns x {rows} rows per page")
    print(f"Individual label size: {LABEL_WIDTH_MM:.1f}mm x {LABEL_HEIGHT_MM:.1f}mm")
    return True

if __name__ == "__main__":
    success = generate_pdf_from_qr_codes()
    if not success:
        exit(1)
