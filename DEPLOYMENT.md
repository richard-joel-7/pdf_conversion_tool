# Phantom FX Doc Tools - Deployment Guide

This guide provides instructions for the IT team to deploy the **Phantom FX Doc Tools** application on a company server (Windows or Linux).

## 1. Prerequisites

Ensure the server has the following software installed:

### A. Python
- **Python 3.10** or higher.
- Ensure `pip` is installed.

### B. System Dependencies (OCR & PDF Engines)
The application requires **Tesseract OCR** and **Poppler** to process files.

#### **On Windows Server:**
1.  **Install Tesseract OCR:**
    - Download the installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
    - Install to `C:\Program Files\Tesseract-OCR`.
    - **Important:** During installation, select "Additional Script Data" -> **Tamil** (and any other required languages).
    - Add `C:\Program Files\Tesseract-OCR` to the System `PATH` environment variable.

2.  **Install Poppler:**
    - Download the latest binary from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/).
    - Extract the zip file (e.g., to `C:\Program Files\Poppler`).
    - Add the `bin` folder (e.g., `C:\Program Files\Poppler\Library\bin`) to the System `PATH` environment variable.

#### **On Linux (Ubuntu/Debian):**
Run the following commands:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip tesseract-ocr tesseract-ocr-tam poppler-utils ffmpeg libsm6 libxext6
```

## 2. Application Installation

1.  **Clone the Repository:**
    Copy the project files to the server

3.  **Install Python Libraries:**
    Open a terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Running the Application

### **Manual Start (Testing):**
Run the following command to start the server:
```bash
streamlit run app.py --server.port 8501
```
The app will be accessible at `http://<server-ip>:8501`.

### **Production Setup (Always On):**

#### **Option A: Windows Service (NSSM)**
1.  Download [NSSM](https://nssm.cc/download).
2.  Open Command Prompt as Administrator.
3.  Run: `nssm install PhantomDocTools`
4.  Set **Path**: `C:\Path\To\Python\python.exe`
5.  Set **Arguments**: `-m streamlit run "C:\Path\To\app.py" --server.port 80`
6.  Click "Install service".
7.  Start the service: `nssm start PhantomDocTools`

#### **Option B: Docker (Recommended for Linux/Windows)**
1.  Create a file named `Dockerfile` in the project root:
    ```dockerfile
    FROM python:3.10-slim

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-tam \
        poppler-utils \
        ffmpeg libsm6 libxext6 \
        && rm -rf /var/lib/apt/lists/*

    WORKDIR /app
    COPY . .

    RUN pip install --no-cache-dir -r requirements.txt

    EXPOSE 8501
    CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    ```
2.  Build and Run:
    ```bash
    docker build -t phantom-doc-tools .
    docker run -d -p 8501:8501 --restart always phantom-doc-tools
    ```

## 4. Troubleshooting

- **"Tesseract not found"**: Ensure `tesseract` is in the system PATH.
- **"Poppler not found"**: Ensure `poppler` binaries are in the system PATH.
- **Tamil text not appearing**: Ensure `tesseract-ocr-tam` is installed.

---
**Developer Contact:** Richard - TeamLead - Data Research - 9003257452
