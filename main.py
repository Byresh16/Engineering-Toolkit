import os
import sys
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "LogsFinder")
VIDEO_DIR = os.path.join(BASE_DIR, "VideoCutterPro")
if LOGS_DIR not in sys.path:
    sys.path.insert(0, LOGS_DIR)
if VIDEO_DIR not in sys.path:
    sys.path.insert(0, VIDEO_DIR)

from required_logs import All_Logs
from makesubfolders import subfolders, addlogs
from zipper import zip_with_7zip
from video_cutter_pro import VideoCutterPro


DEFAULT_SOURCES = {
    "android": r"D:\99.Log\1.Renault_AndroidLog",
    "dropbox": r"D:\99.Log\2.Renault_Dropbox_Log",
    "ecs": r"D:\99.Log\4.ecs",
    "teraterm": r"D:\99.Log\5.Teraterm",
    "can": r"D:\99.Log\3.LOG_CAN",
}


class LogsFinderFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.log_queue = queue.Queue()
        self.busy = False
        self.source_entries = {}
        self._build_ui()
        self.after(100, self._drain_log_queue)

    def _build_ui(self):
        title = ttk.Label(self, text="Logs Finder Tool", font=("Segoe UI", 17, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 3))
        subtitle = ttk.Label(
            self,
            text="",
        )
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 12))

        self.destination_var = tk.StringVar()
        self.sw_var = tk.StringVar()
        self.timestamp_var = tk.StringVar()

        ttk.Label(self, text="Destination folder").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.destination_var).grid(row=2, column=1, sticky="ew", padx=8, pady=4)
        ttk.Button(self, text="Browse", command=self._browse_destination).grid(row=2, column=2, pady=4)

        ttk.Label(self, text="Software version").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.sw_var).grid(row=3, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(self, text="Target timestamp").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.timestamp_var).grid(row=4, column=1, sticky="ew", padx=8, pady=4)
        ttk.Label(self, text="YYYY-MM-DD HH-MM-SS").grid(row=4, column=2, sticky="w", pady=4)

        paths = ttk.LabelFrame(self, text="Log source folders", padding=8)
        paths.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 8))
        paths.grid_columnconfigure(1, weight=1)
        source_labels = [
            ("android", "Android logs"),
            ("dropbox", "Dropbox logs"),
            ("ecs", "ECS / meminfo / bugreport"),
            ("teraterm", "TeraTerm logs"),
            ("can", "CAN logs"),
        ]
        for row, (key, label) in enumerate(source_labels):
            var = tk.StringVar(value=DEFAULT_SOURCES[key])
            self.source_entries[key] = var
            ttk.Label(paths, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
            ttk.Entry(paths, textvariable=var).grid(row=row, column=1, sticky="ew", pady=3)
            ttk.Button(paths, text="Browse", command=lambda v=var: self._browse_source(v)).grid(
                row=row, column=2, padx=(8, 0), pady=3
            )

        actions = ttk.Frame(self)
        actions.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(2, 8))
        self.run_button = ttk.Button(actions, text="Create zipped logs", command=self._start_work)
        self.run_button.pack(side="left")
        self.clear_button = ttk.Button(actions, text="Clear output", command=self._clear_output)
        self.clear_button.pack(side="left", padx=(8, 0))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(actions, textvariable=self.status_var).pack(side="left", padx=12)
        self.progress = ttk.Progressbar(actions, mode="indeterminate", length=180)
        self.progress.pack(side="right")

        output_frame = ttk.LabelFrame(self, text="Activity log", padding=6)
        output_frame.grid(row=7, column=0, columnspan=3, sticky="nsew")
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        self.output = tk.Text(output_frame, height=12, wrap="word", state="disabled")
        self.output.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scroll.set)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(7, weight=1)

    def _browse_destination(self):
        folder = filedialog.askdirectory(parent=self)
        if folder:
            self.destination_var.set(folder)

    def _browse_source(self, variable):
        folder = filedialog.askdirectory(parent=self)
        if folder:
            variable.set(folder)

    def _log(self, message):
        self.log_queue.put(str(message))

    def _drain_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.output.configure(state="normal")
                self.output.insert(tk.END, message + "\n")
                self.output.see(tk.END)
                self.output.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._drain_log_queue)

    def _clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")

    def _set_busy(self, busy):
        self.busy = busy
        self.run_button.configure(state="disabled" if busy else "normal")
        self.clear_button.configure(state="disabled" if busy else "normal")
        self.status_var.set("Working..." if busy else "Ready")
        if busy:
            self.progress.start(10)
        else:
            self.progress.stop()

    def _start_work(self):
        if self.busy:
            return
        destination = self.destination_var.get().strip()
        sw = self.sw_var.get().strip()
        timestamp = self.timestamp_var.get().strip()
        roots = {key: value.get().strip() for key, value in self.source_entries.items()}

        if not destination or not sw or not timestamp:
            messagebox.showwarning(
                "Missing information",
                "Enter the destination folder, software version, and target timestamp.",
                parent=self,
            )
            return
        try:
            from datetime import datetime
            datetime.strptime(timestamp, "%Y-%m-%d %H-%M-%S")
        except ValueError:
            messagebox.showerror(
                "Invalid timestamp",
                "Use this format: YYYY-MM-DD HH-MM-SS\nExample: 2026-10-14 15-30-00",
                parent=self,
            )
            return
        missing = [f"{key}: {path}" for key, path in roots.items() if not os.path.isdir(path)]
        if missing:
            messagebox.showerror(
                "Source folder not found",
                "Check these source paths:\n\n" + "\n".join(missing),
                parent=self,
            )
            return

        os.makedirs(destination, exist_ok=True)
        self._set_busy(True)
        threading.Thread(
            target=self._work,
            args=(destination, sw, timestamp, roots),
            daemon=True,
        ).start()

    def _work(self, destination, sw, timestamp, roots):
        try:
            self._log("Starting log collection...")
            self._log("Creating destination folders...")
            subfolders(destination, sw, self._log)

            logs = {}
            for key in ("android", "dropbox", "ecs", "teraterm", "can"):
                try:
                    self._log("Searching {} logs...".format(key))
                    logs[key] = All_Logs(roots[key], timestamp).threelogs()
                    self._log("Selected {}: {}".format(key, logs[key]))
                except Exception as exc:
                    logs[key] = []
                    self._log("Could not search {}: {}".format(key, exc))

            self._log("Copying selected logs...")
            addlogs(logs, destination, sw, roots["can"], self._log, source_roots=roots)
            self._log("Creating split 7-Zip archives...")
            zip_with_7zip(destination, sw, self._log)
            self._log("Log collection finished.")
            self.after(0, lambda: self.status_var.set("Completed"))
            try:
                os.startfile(destination)
            except Exception:
                pass
        except Exception as exc:
            self._log("ERROR: {}".format(exc))
            self.after(0, lambda e=str(exc): messagebox.showerror("Logs Finder failed", e, parent=self))
        finally:
            self.after(0, lambda: self._set_busy(False))


class EngineeringToolkit:
    def __init__(self, root):
        self.root = root
        root.title("Log Collector")
        root.geometry("1120x900")
        root.minsize(980, 720)

        outer = ttk.Frame(root, padding=(12, 8, 12, 12))
        outer.pack(fill="both", expand=True)
        ttk.Label(
            outer,
            text="Log Collector",
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)
        self.logs_tab = LogsFinderFrame(self.tabs)
        self.video_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.logs_tab, text="Logs Finder")
        self.tabs.add(self.video_tab, text="Video Cutter Pro")
        self.video_app = VideoCutterPro(self.video_tab)

        root.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        if hasattr(self, "video_app"):
            self.video_app.close_application()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    EngineeringToolkit(root)
    root.mainloop()


if __name__ == "__main__":
    main()
