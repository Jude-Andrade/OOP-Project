"""
QR Code Generator Utility

This module provides functions to generate QR codes for registered users.
Each QR code encodes the user's information in a specific format.
"""

import qrcode
import os
from datetime import datetime


class QRCodeGenerator:
    """Handles QR code generation for user registration"""
    
    def __init__(self, output_dir="assets/qr_codes"):
        """
        Initialize QR code generator
        
        Args:
            output_dir: Directory to save generated QR codes
        """
        self.output_dir = output_dir
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Ensure the output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_qr_code(self, name, id_number, department, user_type, user_id=None):
        """
        Generate a QR code for a user
        
        The QR code contains user information in a pipe-delimited format:
        name|id_number|department|user_type
        
        Args:
            name: User's full name
            id_number: Student/Teacher ID or "Guest"
            department: Department name or "Guest"
            user_type: Student, Teacher, or Guest
            user_id: Optional user ID to use in filename
            
        Returns:
            str: Path to the generated QR code image, or None if failed
        """
        try:
            # Create the data string (pipe-delimited)
            qr_data = f"{name}|{id_number}|{department}|{user_type}"
            
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,  # Controls the size of the QR code
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
                box_size=10,  # Size of each box in pixels
                border=4,  # Border size in boxes
            )
            
            # Add data to the QR code
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if user_id:
                filename = f"QR_{user_id}_{timestamp}.png"
            else:
                # Use a safe version of the name for filename
                safe_name = "".join(c if c.isalnum() else "_" for c in name)
                filename = f"QR_{safe_name}_{timestamp}.png"
            
            # Full path to save the image
            filepath = os.path.join(self.output_dir, filename)
            
            # Save the image
            img.save(filepath)
            
            return filepath
        
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    def parse_qr_data(self, qr_string):
        """
        Parse QR code data string back into components
        
        Args:
            qr_string: The scanned QR code string (pipe-delimited)
            
        Returns:
            dict: Dictionary with name, id_number, department, user_type
                  or None if parsing failed
        """
        try:
            parts = qr_string.strip().split("|")
            
            if len(parts) != 4:
                return None
            
            return {
                'name': parts[0],
                'id_number': parts[1],
                'department': parts[2],
                'user_type': parts[3]
            }
        
        except Exception as e:
            print(f"Error parsing QR data: {e}")
            return None


def test_qr_generator():
    """Test function to demonstrate QR code generation"""
    generator = QRCodeGenerator()
    
    # Test with a student
    filepath = generator.generate_qr_code(
        name="Juan Dela Cruz",
        id_number="2021-00001",
        department="Computer Science",
        user_type="Student"
    )
    
    if filepath:
        print(f"QR code generated successfully: {filepath}")
    else:
        print("Failed to generate QR code")
    
    # Test parsing
    test_string = "Juan Dela Cruz|2021-00001|Computer Science|Student"
    parsed = generator.parse_qr_data(test_string)
    print(f"Parsed data: {parsed}")


if __name__ == "__main__":
    test_qr_generator()
