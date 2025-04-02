import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from subprocess import run
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import processing_onlines
import processing_sbp
from path_utils import create_directory_structure

BG_COLOR = "#f4f1e5"
BTN_BG = "#e0ddd3"
BTN_TEXT = "#222222"
HOVER_BG = "#d0ccc2"
IMAGE_PATH = os.path.join(ASSETS_DIR, "1C.png")
WIDTH, HEIGHT = 1024, 768

def create_pixel_button(master, text, command):
    btn = tk.Button(
        master, text=text, font=("Segoe UI", 10), bg=BTN_BG, fg=BTN_TEXT,
        activebackground=HOVER_BG, activeforeground="black", relief="flat",
        bd=1, highlightthickness=0, cursor="hand2"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_BG))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG))
    btn.config(command=command)
    return btn

class YearMonthDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Выбор года и месяца")
        self.geometry("250x150")
        self.resizable(False, False)
        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.result = None

        tk.Label(self, text="Год:").pack(pady=5)
        year_box = ttk.Combobox(self, textvariable=self.year, values=[str(y) for y in range(2020, datetime.now().year+1)])
        year_box.pack()

        tk.Label(self, text="Месяц:").pack(pady=5)
        month_box = ttk.Combobox(self, textvariable=self.month, values=[f"{i:02d}" for i in range(1, 13)])
        month_box.pack()

        btn = tk.Button(self, text="OK", command=self.on_ok)
        btn.pack(pady=10)
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def on_ok(self):
        year = self.year.get()
        month = self.month.get()
        if year.isdigit() and month.isdigit():
            self.result = (int(year), int(month))
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Введите корректные год и месяц")

class AccountingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Accounting Automation GUI")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.resizable(False, False)
        self.stop_event = threading.Event()

        bg_img = Image.open(IMAGE_PATH).resize((WIDTH, HEIGHT))
        bg_img = ImageEnhance.Brightness(bg_img).enhance(0.8)
        self.bg_img = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(self.master, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = tk.Frame(self.master, bg=BG_COLOR)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.base_dir = tk.StringVar()
        self.directory_path = None
        self.temp_dir = None
        self.readable_dir = None

        self._create_info_block()
        self._create_buttons_block()

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", background="#4CAF50", troughcolor=BG_COLOR, bordercolor=BG_COLOR)
        self.progress = ttk.Progressbar(self.frame, mode='indeterminate')
        self.progress.pack(pady=5, fill='x')

        self.log = scrolledtext.ScrolledText(
            self.frame, width=80, height=20,
            bg="#faf9f3", fg="#333333",
            insertbackground="black",
            font=("Segoe UI", 9), relief="flat", borderwidth=1
        )
        self.log.pack(pady=10, fill='both', expand=True)

    def _create_info_block(self):
        info_frame = tk.Frame(self.frame, bg=BG_COLOR)
        info_frame.pack(pady=5, fill='x')
        tk.Label(info_frame, text="Год:", bg=BG_COLOR).grid(row=0, column=0, padx=5, sticky='e')
        tk.Label(info_frame, textvariable=self.year, bg=BG_COLOR, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky='w')
        tk.Label(info_frame, text="Месяц:", bg=BG_COLOR).grid(row=1, column=0, padx=5, sticky='e')
        tk.Label(info_frame, textvariable=self.month, bg=BG_COLOR, font=("Segoe UI", 10, "bold")).grid(row=1, column=1, sticky='w')
        tk.Label(info_frame, text="Текущий путь:", bg=BG_COLOR).grid(row=2, column=0, padx=5, sticky='e')
        tk.Label(info_frame, textvariable=self.base_dir, fg="skyblue", bg=BG_COLOR).grid(row=2, column=1, sticky='w')

    def _create_buttons_block(self):
        btn_frame = tk.Frame(self.frame, bg=BG_COLOR)
        btn_frame.pack(pady=5, fill='x')
        create_pixel_button(btn_frame, "Выбрать базовую папку", self.select_base_dir).pack(pady=5, fill='x')
        create_pixel_button(btn_frame, "Запустить всё", lambda: self.run_in_thread(self.run_all)).pack(pady=2, fill='x')
        create_pixel_button(btn_frame, "Обработать SQL", lambda: self.run_in_thread(self.run_sql)).pack(pady=2, fill='x')
        create_pixel_button(btn_frame, "Обработать Online", lambda: self.run_in_thread(self.run_online)).pack(pady=2, fill='x')
        create_pixel_button(btn_frame, "Обработать SBP", lambda: self.run_in_thread(self.run_sbp)).pack(pady=2, fill='x')
        create_pixel_button(btn_frame, "Сделать readable-отчёты", lambda: self.run_in_thread(self.run_readable)).pack(pady=2, fill='x')
        stop_btn = create_pixel_button(btn_frame, "Остановить выполнение", self.stop_execution)
        stop_btn.configure(fg='red')
        stop_btn.pack(pady=5, fill='x')

    def log_print(self, message):
        self.log.insert(tk.END, message + '\n')
        self.log.see(tk.END)
        self.master.update()

    def select_base_dir(self):
        selected = filedialog.askdirectory(title="Выберите папку для сохранения")
        if selected:
            dialog = YearMonthDialog(self.master)
            if dialog.result:
                year, month = dialog.result
                try:
                    self.directory_path, self.temp_dir, self.readable_dir = create_directory_structure(selected, year, month)
                    self.base_dir.set(self.directory_path)
                    self.year.set(str(year))
                    self.month.set(f"{month:02d}")
                    self.log_print(f"Папка создана: {self.directory_path}")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                    self.log_print(f"Ошибка: {e}")

    def stop_execution(self):
        self.stop_event.set()
        self.log_print("Выполнение остановлено.")

    def run_in_thread(self, func):
        def wrapper():
            try:
                self.stop_event.clear()
                self.progress.start()
                func()
            except Exception as e:
                self.log_print(f"Ошибка: {e}")
            finally:
                self.progress.stop()
        threading.Thread(target=wrapper, daemon=True).start()

    def run_all(self):
        if not self.temp_dir: return
        self.run_sql()
        if self.stop_event.is_set(): return
        self.run_online()
        if self.stop_event.is_set(): return
        self.run_sbp()
        if self.stop_event.is_set(): return
        self.run_readable()

    def run_sql(self):
        if not self.temp_dir:
            self.log_print("Сначала выберите базовую папку.")
            return
        year = self.year.get()
        month = self.month.get()
        script_path = os.path.join(BASE_DIR, "src", "change_date_sql.py")
        real_dir = os.path.join(BASE_DIR, "src", "realisations_sql")
        card_dir = os.path.join(BASE_DIR, "src", "cardcash_sql")
        if not os.path.exists(script_path):
            self.log_print(f"Скрипт не найден: {script_path}")
            return
        result = run(["python", script_path, year, month, real_dir, card_dir], capture_output=True, text=True)
        self.log_print(result.stdout or result.stderr)
        export_script = os.path.join(BASE_DIR, "src", "export_data.py")
        venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python")
        result = run([venv_python, export_script, self.temp_dir], capture_output=True, text=True)
        self.log_print(result.stdout or result.stderr)

    def run_online(self):
        if not self.temp_dir:
            self.log_print("Сначала выберите базовую папку.")
            return
        folder = filedialog.askdirectory(title="Папка с online-файлами")
        if folder:
            processing_onlines.process_online_plus(folder, self.temp_dir)
            if self.stop_event.is_set(): return
            processing_onlines.process_online_minus(folder, self.temp_dir)
            if self.stop_event.is_set(): return
            processing_onlines.combine_files(self.temp_dir)
            processing_onlines.create_json_from_excel(self.temp_dir, 'onlines.xlsx')
            self.log_print("Online-файлы обработаны.")

    def run_sbp(self):
        if not self.temp_dir:
            self.log_print("Сначала выберите базовую папку.")
            return
        folder = filedialog.askdirectory(title="Папка с SBP-файлами")
        if folder:
            processing_sbp.process_all_sbp_files(folder, self.temp_dir)
            if self.stop_event.is_set(): return
            for name in os.listdir(folder):
                if name.endswith(".csv"):
                    xlsx_name = name.replace(".csv", ".xlsx")
                    try:
                        processing_sbp.create_json_from_excel(self.temp_dir, xlsx_name)
                    except Exception as e:
                        self.log_print(f"Ошибка в {xlsx_name}: {e}")
            self.log_print("SBP-файлы обработаны.")

    def run_readable(self):
        if not self.temp_dir:
            self.log_print("Сначала выберите базовую папку.")
            return
        script_path = os.path.join(BASE_DIR, "src", "make_readable.py")
        venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python")
        result = run([venv_python, script_path, self.temp_dir, self.readable_dir], capture_output=True, text=True)
        self.log_print(result.stdout or result.stderr)
        self.log_print("Отчёты сформированы.")

def main():
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
