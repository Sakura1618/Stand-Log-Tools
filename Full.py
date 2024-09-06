import os
import re
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, font

highlight_lines = {
    "检测": "yellow",
    "崩溃": "red",
    "重复": "yellow",
    "攻击": "red",
    "踢出": "red",
    "主机": "Turquoise",
    "脚本主机": "LightSeaGreen",
    "事件": "red",
    "starting up": "Fuchsia",
    "Not skipping": "Fuchsia",
    "PopstarV": "Fuchsia",
    "Waiting for": "Fuchsia",
    "finished": "Fuchsia",
    "Doing minimal init": "Fuchsia",
}

timestamp_color = "gray"

def calculate_indices(widget, line_number_offset=2.0):
    start_idx = f"{float(widget.index(tk.END)) - line_number_offset} linestart"
    end_idx = f"{start_idx} lineend"
    return start_idx, end_idx

def read_all(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()

def read_log(file_path, text_widget):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, line)
            highlight_line(line, text_widget)
            text_widget.config(state=tk.DISABLED)
            text_widget.see(tk.END)

def highlight_line(line, text_widget):
    timestamp_match = re.match(r"(\[.*?\])", line)
    if timestamp_match:
        start_idx, _ = calculate_indices(text_widget)
        timestamp_end_idx = f"{start_idx} + {len(timestamp_match.group(1))}c"
        text_widget.tag_add("timestamp", start_idx, timestamp_end_idx)

    for word, color in highlight_lines.items():
        if word in line:
            start_idx, end_idx = calculate_indices(text_widget)
            text_widget.tag_add(color, start_idx, end_idx)

def start_logging(file_path, text_widget):
    all_lines = read_all(file_path)
    text_widget.config(state=tk.NORMAL)
    for line in all_lines:
        text_widget.insert(tk.END, line)
        highlight_line(line, text_widget)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

    log_thread = threading.Thread(target=read_log, args=(file_path, text_widget))
    log_thread.daemon = True
    log_thread.start()

def main():
    root = tk.Tk()
    root.title("Stand-Log-Tools By Sakura1618 https://github.com/Sakura1618/Stand-Log-Tools")
    root.configure(bg="black")
    root.tk.call('tk', 'scaling', 2.0)

    custom_font = font.Font(family="HarmonyOS Sans SC", size=10)

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80, bg="black", fg="white", font=custom_font)
    text_widget.pack(expand=True, fill='both')
    text_widget.config(state=tk.DISABLED)

    text_widget.tag_configure("timestamp", foreground=timestamp_color)
    for color in set(highlight_lines.values()):
        text_widget.tag_configure(color, foreground=color)

    user_home = os.path.expanduser("~")
    log_file_path = os.path.join(user_home, "AppData/Roaming/Stand/log.txt")

    start_logging(log_file_path, text_widget)

    icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
    root.iconphoto(True, tk.PhotoImage(file=icon_path))

    root.mainloop()

if __name__ == "__main__":
    import cProfile
    cProfile.run('main()')
