# file: gen_qr_codes.py
# Author: Yash Patel
# Date: 2025-11-11
# Description: This script generates QR codes for a list of URLs and saves them as PNG files. 
# It looks for a csv with the following format/header:  "WISE_ID,Shelf_QR_ID,QR Code Printed"
# File format of .csv is                                "WISE-01,rwlenjke7h,FALSE"

# QR Code Link Format will be: https://wisecircuitslab.github.io/shelf_url_translator?wise_id=[&shelf_qr_id=]
# Only print QR Codes for rows with "QR Code Printed" marked as FALSE

import pandas as pd
import qrcode
import os

def generate_qr_codes():
    """Generate QR codes for items marked as not printed in the CSV file."""
    
    # Read the CSV file
    csv_file = "WISE Asset Matrix - Sheet1.csv"
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found in the current directory.")
        return
    
    # Create output directory for QR codes
    output_dir = "qr_codes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter rows where QR Code Printed is FALSE
    unprintedrows = df[df['QR Code Printed'] == False]
    
    if unprintedrows.empty:
        print("No QR codes to generate. All items are already marked as printed.")
        return
    
    generated_count = 0
    
    # Generate QR codes for each unprinted item
    for _, row in unprintedrows.iterrows():
        wise_id = row['WISE_ID']
        shelf_qr_id = row['Shelf_QR_ID']
        
        # Create the URL
        # Given reference URL: https://wisecircuitslab.github.io/shelf_url_translator?wise_id=WISE-01
        url = f"https://wisecircuitslab.github.io/shelf_url_translator?wise_id={wise_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create QR code image (clean, no text overlay)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code with filename format: WISE-ID_shelf-qr-id.png
        filename = f"{wise_id}_{shelf_qr_id}.png"
        filepath = os.path.join(output_dir, filename)
        qr_img.save(filepath)
        
        print(f"Generated QR code: {filename}")
        generated_count += 1
    
    print(f"\nGenerated {generated_count} QR codes in the '{output_dir}' directory.")

if __name__ == "__main__":
    generate_qr_codes()

