:: build_exe.bat - local Windows build using PyInstaller
:: Run this in an Administrator Developer command prompt with Python installed.
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed dtf_printer_manager.py --name "DTF Print Manager"
echo Build finished. Executable in dist\DTF Print Manager.exe
pause