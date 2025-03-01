# Project Setup Instructions

## Overview
This project requires Python and a few dependencies to run properly. It uses image processing, OCR, and translation functionalities among others.

## Prerequisites
Ensure you have Python installed (Python 3.6 or later is recommended).

### Steps to Set Up

1. **download the project files**: Place all files in a directory on your system.
2. **Install the dependencies**: 
   Open a terminal or command prompt in the project directory and run:
   pip install -r requirements.txt
   
3. **Install Tesseract-OCR**:
   This project uses `pytesseract` for OCR, which requires the Tesseract OCR software. 
   - **Windows**: Download the installer from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki) and follow the installation instructions.
   - **Linux**: Run `sudo apt-get install tesseract-ocr`.
   - **MacOS**: Run `brew install tesseract` (if Homebrew is installed).
   
   After installing, ensure that Tesseract is added to your system's PATH.

4. **Run the Program**:
   Use the following command to run the `main.py` file:
   python main.py
   

## Notes
- The application uses Tkinter for its GUI, so it should be run in an environment that supports GUI display.
- Make sure to install Tesseract OCR separately, as it is not included with Python packages.

## Troubleshooting
If you encounter any issues with missing libraries or errors, please make sure you have installed all dependencies correctly.

