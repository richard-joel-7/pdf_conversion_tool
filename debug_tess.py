import pytesseract
from PIL import Image
import os
import sys

# Setup paths (copied from main script)
possible_tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.join(os.getenv('LOCALAPPDATA'), r"Tesseract-OCR\tesseract.exe")
]
TESSERACT_CMD = None
for path in possible_tesseract_paths:
    if os.path.exists(path):
        TESSERACT_CMD = path
        break
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

local_tessdata = os.path.join(os.getcwd(), "tessdata")
if os.path.exists(os.path.join(local_tessdata, "tam.traineddata")):
    os.environ["TESSDATA_PREFIX"] = local_tessdata
    print(f"Set TESSDATA_PREFIX to {local_tessdata}")

def test_pdf_gen():
    print("Creating test image...")
    img = Image.new('RGB', (100, 100), color = 'white')
    
    print("Attempting image_to_pdf_or_hocr...")
    try:
        pdf = pytesseract.image_to_pdf_or_hocr(img, extension='pdf', lang='eng+tam')
        print(f"Success! PDF bytes length: {len(pdf)}")
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_gen()
