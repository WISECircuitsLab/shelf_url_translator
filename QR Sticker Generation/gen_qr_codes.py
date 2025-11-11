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
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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
        
        # Create QR code as bytes and then load as PIL Image
        import io
        from PIL import Image as PILImage
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes buffer and reload as PIL Image to ensure compatibility
        buffer = io.BytesIO()
        qr_img.save(buffer)
        buffer.seek(0)
        pil_img = PILImage.open(buffer)
        
        # Convert to RGB if needed
        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')
        
        # Try to use a system font, fall back to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except OSError:
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except OSError:
                font = ImageFont.load_default()
        
        # Get text dimensions
        temp_draw = ImageDraw.Draw(pil_img)
        text_bbox = temp_draw.textbbox((0, 0), wise_id, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Create a new image with extra space for text
        img_width, img_height = pil_img.size
        new_height = img_height + int(text_height) + 20  # 20px padding
        new_img = PILImage.new('RGB', (img_width, new_height), 'white')
        
        # Paste the QR code
        new_img.paste(pil_img, (0, 0))
        
        # Add text centered below QR code
        # draw = ImageDraw.Draw(new_img)
        # text_x = (img_width - text_width) // 2
        # text_y = img_height + 10  # 10px padding from QR code
        # draw.text((text_x, text_y), wise_id, fill='black', font=font)
        
        # Save QR code with filename format: WISE-ID_shelf-qr-id.png
        filename = f"{wise_id}_{shelf_qr_id}.png"
        filepath = os.path.join(output_dir, filename)
        new_img.save(filepath)
        
        print(f"Generated QR code: {filename}")
        generated_count += 1
    
    print(f"\nGenerated {generated_count} QR codes in the '{output_dir}' directory.")

if __name__ == "__main__":
    generate_qr_codes()

