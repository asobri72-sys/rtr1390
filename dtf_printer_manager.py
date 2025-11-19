# dtf_printer_manager.py
# Simple DTF Print Manager (sederhana) - watches a folder, archives jobs, and auto-prints PNG/TIF files.
# See README for details.
import os
import time
import threading
import shutil
import queue
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import win32print
import win32api

BASE_DIR = Path.home() / "DTFPrinterManager"
WATCH_FOLDER = BASE_DIR / "inbox"
STORAGE_FOLDER = BASE_DIR / "storage"
LOG_FILE = BASE_DIR / "dtf_manager.log"
PRINTER_REAL_NAME = "EPSON Stylus Photo R1390"
SUPPORTED_EXT = [".png", ".tif", ".tiff"]
AUTO_PRINT = True

os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(STORAGE_FOLDER, exist_ok=True)

job_q = queue.Queue()
stop_event = threading.Event()

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def copy_to_storage(src_path: Path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = STORAGE_FOLDER / f"{ts}_{src_path.name}"
    shutil.copy2(src_path, dest)
    return dest

def send_to_physical_printer(file_path: Path):
    try:
        log(f"Sending to physical printer '{PRINTER_REAL_NAME}': {file_path}")
        printer_name = PRINTER_REAL_NAME
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("DTFJob", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            with open(file_path, "rb") as f:
                data = f.read()
                win32print.WritePrinter(hPrinter, data)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
        log("Print job sent.")
    except Exception as e:
        log(f"Error sending to physical printer: {e}")
        messagebox.showerror("Print Error", f"Failed to send to physical printer:\n{e}")

def worker_loop():
    while not stop_event.is_set():
        try:
            job = job_q.get(timeout=1)
        except queue.Empty:
            continue
        try:
            log(f"Processing job: {job}")
            dest = copy_to_storage(Path(job))
            try:
                os.remove(job)
            except Exception:
                pass
            if AUTO_PRINT:
                send_to_physical_printer(dest)
            log(f"Job completed: {dest}")
        except Exception as e:
            log(f"Error processing job {job}: {e}")

def start_worker():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()
    return t

def scan_existing():
    for p in WATCH_FOLDER.iterdir():
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXT:
            job_q.put(str(p))
            log(f"Queued existing file: {p}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DTF Print Manager (sederhana)")
        self.geometry("520x320")
        self.resizable(False, False)
        self.create_widgets()
        self.worker_thread = start_worker()
        scan_existing()
        self.after(1000, self.refresh_status)

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)
        lbl = ttk.Label(frm, text="DTF Print Manager — versi sederhana", font=("Segoe UI", 14))
        lbl.pack(anchor="w")
        self.status_var = tk.StringVar(value="Idle")
        ttk.Label(frm, textvariable=self.status_var).pack(anchor="w", pady=(8,0))
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Open Inbox Folder", command=self.open_inbox).pack(side="left")
        ttk.Button(btn_frame, text="Open Storage Folder", command=self.open_storage).pack(side="left", padx=(8,0))
        ttk.Button(btn_frame, text="Clear Storage Log", command=self.clear_log).pack(side="right")
        self.auto_var = tk.BooleanVar(value=AUTO_PRINT)
        ttk.Checkbutton(frm, text="Auto Print to Epson R1390", variable=self.auto_var, command=self.toggle_auto).pack(anchor="w", pady=(10,0))
        self.queue_list = tk.Listbox(frm, height=8)
        self.queue_list.pack(fill="both", expand=True, pady=(10,0))
        bottom = ttk.Frame(frm)
        bottom.pack(fill="x", pady=(8,0))
        ttk.Button(bottom, text="Rescan Inbox", command=self.rescan).pack(side="left")
        ttk.Button(bottom, text="Exit", command=self.on_exit).pack(side="right")

    def open_inbox(self):
        os.startfile(WATCH_FOLDER)

    def open_storage(self):
        os.startfile(STORAGE_FOLDER)

    def clear_log(self):
        try:
            open(LOG_FILE, "w").close()
            messagebox.showinfo("Cleared", "Log cleared.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_auto(self):
        global AUTO_PRINT
        AUTO_PRINT = self.auto_var.get()
        log(f"Auto Print set to {AUTO_PRINT}")

    def rescan(self):
        scan_existing()
        messagebox.showinfo("Rescan", "Inbox rescanned.")

    def refresh_status(self):
        self.queue_list.delete(0, tk.END)
        qlist = list(job_q.queue)
        if qlist:
            for item in qlist:
                self.queue_list.insert(tk.END, os.path.basename(item))
            self.status_var.set(f"Queued: {len(qlist)} jobs")
        else:
            self.status_var.set("Idle")
        self.after(1000, self.refresh_status)

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Stop DTF Print Manager?"):
            stop_event.set()
            self.destroy()

if __name__ == "__main__":
    log("DTF Print Manager started.")
    app = App()
    app.mainloop()