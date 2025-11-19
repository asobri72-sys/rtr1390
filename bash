.github
└── workflows
    └── windows-build.yml

name: Build Windows EXE

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    steps:
    - name: Checkout source
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Install PyInstaller
      run: pip install pyinstaller

    - name: Build EXE
      run: pyinstaller --onefile dtf_printer_manager.py

    - name: Upload build artifact
      uses: actions/upload-artifact@v3
      with:
        name: dtf-printer-manager-exe
        path: dist/dtf_printer_manager.exe
