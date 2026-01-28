import os
import shutil
import urllib.request
import sys
from pathlib import Path

# URLs for Tesseract data
TAM_URL = "https://github.com/tesseract-ocr/tessdata/raw/main/tam.traineddata"
# Using 'best' or 'fast' is also an option, but main (standard) is usually a good balance.
# TAM_URL = "https://github.com/tesseract-ocr/tessdata_best/raw/main/tam.traineddata" 

DEFAULT_TESS_DIR = r"C:\Program Files\Tesseract-OCR\tessdata"
LOCAL_TESS_DIR = os.path.join(os.getcwd(), "tessdata")

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        with urllib.request.urlopen(url) as response, open(dest_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Download complete.")
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def setup_tesseract_lang():
    # Check if we can write to default directory
    target_dir = DEFAULT_TESS_DIR
    writable = False
    
    if os.path.exists(DEFAULT_TESS_DIR):
        try:
            test_file = os.path.join(DEFAULT_TESS_DIR, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            writable = True
            print(f"Has write access to {DEFAULT_TESS_DIR}")
        except PermissionError:
            print(f"No write access to {DEFAULT_TESS_DIR}. Will use local directory.")
            writable = False
    else:
        print(f"Tesseract default dir {DEFAULT_TESS_DIR} not found.")

    if writable:
        tam_dest = os.path.join(DEFAULT_TESS_DIR, "tam.traineddata")
        if not os.path.exists(tam_dest):
            success = download_file(TAM_URL, tam_dest)
            if success:
                print("Tamil language pack installed globally.")
            else:
                print("Failed to install Tamil pack globally.")
        else:
            print("Tamil language pack already exists globally.")
    else:
        # Use local directory
        if not os.path.exists(LOCAL_TESS_DIR):
            os.makedirs(LOCAL_TESS_DIR)
            print(f"Created local tessdata dir: {LOCAL_TESS_DIR}")
        
        # We also need eng.traineddata in the local dir if we change TESSDATA_PREFIX
        # Or we can point pytesseract to use this config.
        # Actually, Tesseract can look in multiple places or we just point to one.
        # If we use a custom dir, we need ALL language files there usually, or verify if it chains.
        # Safest is to copy eng.traineddata too if we switch to local.
        
        tam_dest = os.path.join(LOCAL_TESS_DIR, "tam.traineddata")
        if not os.path.exists(tam_dest):
            download_file(TAM_URL, tam_dest)
            
        # Copy eng.traineddata from system if possible, or download it
        eng_dest = os.path.join(LOCAL_TESS_DIR, "eng.traineddata")
        if not os.path.exists(eng_dest):
            sys_eng = os.path.join(DEFAULT_TESS_DIR, "eng.traineddata")
            if os.path.exists(sys_eng):
                try:
                    shutil.copy(sys_eng, eng_dest)
                    print("Copied eng.traineddata from system.")
                except Exception as e:
                    print(f"Could not copy eng.traineddata: {e}")
            else:
                # Download eng if not found
                ENG_URL = "https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata"
                download_file(ENG_URL, eng_dest)

        print(f"Language packs set up in {LOCAL_TESS_DIR}")
        print("Please ensure your script sets tessdata_dir_config to point here.")

if __name__ == "__main__":
    setup_tesseract_lang()
