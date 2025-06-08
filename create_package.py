import os
import shutil
import subprocess
import sys

def create_package():
    # Create package directory
    package_dir = "offline_fraud_detector"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy necessary files
    files_to_copy = [
        "main.py",
        "config.py",
        "requirements_full.txt",
        "pipeline/",
        "data/",
        "models/",
        "outputs/"
    ]
    
    for item in files_to_copy:
        if os.path.isdir(item):
            shutil.copytree(item, os.path.join(package_dir, item))
        else:
            shutil.copy(item, package_dir)
    
    # Create README
    with open(os.path.join(package_dir, "README.txt"), "w") as f:
        f.write("""Offline Payment Fraud Detector Package

1. Create a virtual environment:
   python -m venv venv

2. Activate the virtual environment:
   - Windows: venv\Scripts\activate
   - Unix/MacOS: source venv/bin/activate

3. Install dependencies:
   pip install -r requirements_full.txt

4. Run the application:
   python main.py

The package includes all necessary files and dependencies to run the fraud detection system.
""")
    
    # Create a batch file for Windows users
    with open(os.path.join(package_dir, "run.bat"), "w") as f:
        f.write("""@echo off
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements_full.txt
echo Running application...
python main.py
pause""")
    
    print(f"Package created successfully at {package_dir}")

if __name__ == "__main__":
    create_package()
