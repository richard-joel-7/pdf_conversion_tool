from PIL import Image, ImageDraw, ImageFont
import os

def create_test_pdf(filename="test_document.pdf"):
    # Create a white image
    img = Image.new('RGB', (800, 1000), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a default font, otherwise use default
    try:
        # Arial is usually available on Windows
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    # Add some English text
    d.text((50, 50), "Test Document for OCR", fill='black', font=font)
    d.text((50, 100), "This is a sample PDF created to test the OCR script.", fill='black', font=font)
    d.text((50, 150), "It contains English text.", fill='black', font=font)
    
    # Note: Rendering Tamil text correctly requires a font that supports it.
    # We will skip rendering Tamil text in this simple test generation to avoid font issues,
    # but the script is configured to handle it if present in the input.
    d.text((50, 200), "OCR Verification Test.", fill='black', font=font)

    # Save as PDF
    img.save(filename, "PDF", resolution=100.0)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_pdf()
