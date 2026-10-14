# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog
import os
import time
import threading

from required_logs import All_Logs
from makesubfolders import subfolders, addlogs
from zipper import zip_with_7zip


# ---------- UI logging ----------
def log_to_ui(message):
    text.insert(tk.END, message + "\n")
    text.see(tk.END)
    text.update()

def safe_log(message):
    # Ensure UI updates happen on the main thread
    root.after(0, lambda: log_to_ui(message))


# ---------- Browse handlers ----------
def browse_log_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)

def browse_can_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_can_log_folder.delete(0, tk.END)
        entry_can_log_folder.insert(0, folder)


# ---------- Operations ----------
def find_logs():
    folders = {
        "android": r"D:\99.Log\1.Renault_AndroidLog",
        "dropbox": r"D:\99.Log\2.Renault_Dropbox_Log",
        "ecs":     r"D:\99.Log\4.ecs",
        "teraterm": r"D:\99.Log\5.Teraterm",
        "can":     entry_can_log_folder.get()
    }
    ts = entry_time.get()
    logs = {}
    for key, path in folders.items():
        try:
            logs[key] = All_Logs(path, ts).threelogs()
            log_to_ui("Found logs for %s: %s" % (key, logs[key]))
        except Exception as e:
            log_to_ui("Error finding logs for %s: %s" % (key, e))
    return logs

def logfolders():
    try:
        subfolders(entry_folder.get(), entry_SW.get(), log_to_ui)
        log_to_ui("Log folders created.")
    except Exception as e:
        log_to_ui("Failed to create log folders: %s" % e)

def copy_logs():
    try:
        logs = find_logs()
        addlogs(logs, entry_folder.get(), entry_SW.get(),
                entry_can_log_folder.get(), log_to_ui)
        log_to_ui("Logs copied.")
    except Exception as e:
        log_to_ui("Failed to copy logs: %s" % e)


# ---------- Busy state & progress ----------
def set_busy(is_busy):
    state = tk.DISABLED if is_busy else tk.NORMAL
    btn_browse_log.configure(state=state)
    btn_browse_can.configure(state=state)
    btn_copyandzip.configure(state=state)
    entry_folder.configure(state=state)
    entry_can_log_folder.configure(state=state)
    entry_SW.configure(state=state)
    entry_time.configure(state=state)



def progress_update(pct):
    # Called from background thread; sync to UI thread
    def _upd():
        # Show % and set determinate progress value
        print("pct", pct)
        # status_var.set("Zipping… %d%%" % pct)
        progress.configure(mode='determinate', maximum=100)
        progress['value'] = pct
    root.after(0, _upd)


def zipper_async():
    try:
        zip_with_7zip(entry_folder.get(), entry_SW.get(), safe_log)
        safe_log("Zip completed.")
        try:
            os.startfile(entry_folder.get())
        except Exception as e:
            safe_log("Open folder failed: %s" % e)
    except Exception as e:
        safe_log("Failed to zip: %s" % e)
    finally:
        root.after(0, progress.stop)
        root.after(0, progress.grid_remove)  # HIDE after finish
        root.after(0, status_var.set, "")
        root.after(0, set_busy, False)

def zipper():
    # Show + start progress ONLY when user clicks the button
    status_var.set("Zipping…")
    progress.grid()        # make visible
    progress.start(10)     # start animation
    set_busy(True)
    t = threading.Thread(target=zipper_async)
    t.daemon = True
    t.start()
    t.join()

def copyandzip():
    log_to_ui("Starting: create folders, find/copy logs, then zip.")
    logfolders()
    find_logs()
    copy_logs()
    zipper()


# ------------------ UI ------------------
root = tk.Tk()
root.title("Log Finder Tool")
root.geometry("900x520")

# Make root responsive
for r in range(6):
    root.grid_rowconfigure(r, weight=(1 if r == 5 else 0))
root.grid_columnconfigure(0, weight=1)

# Row 0: Log Folder
frame_log = tk.Frame(root)
frame_log.grid(row=0, column=0, sticky='ew', padx=10, pady=6)
frame_log.grid_columnconfigure(1, weight=1)
tk.Label(frame_log, text="Destination Folder").grid(row=0, column=0, padx=5, sticky='w')
entry_folder = tk.Entry(frame_log)
entry_folder.grid(row=0, column=1, padx=5, sticky='ew')
btn_browse_log = tk.Button(frame_log, text="Browse", width=10, command=browse_log_folder)
btn_browse_log.grid(row=0, column=2, padx=5, sticky='e')

# Row 1: CAN Log Folder
frame_can = tk.Frame(root)
frame_can.grid(row=1, column=0, sticky='ew', padx=10, pady=6)
frame_can.grid_columnconfigure(1, weight=1)
tk.Label(frame_can, text="Select CAN Log Folder").grid(row=0, column=0, padx=5, sticky='w')
entry_can_log_folder = tk.Entry(frame_can)
entry_can_log_folder.grid(row=0, column=1, padx=5, sticky='ew')
btn_browse_can = tk.Button(frame_can, text="Browse", width=10, command=browse_can_folder)
btn_browse_can.grid(row=0, column=2, padx=5, sticky='e')

# Row 2: SW Version
frame_sw = tk.Frame(root)
frame_sw.grid(row=2, column=0, sticky='ew', padx=10, pady=6)
frame_sw.grid_columnconfigure(1, weight=1)
tk.Label(frame_sw, text="SW Version").grid(row=0, column=0, padx=5, sticky='w')
entry_SW = tk.Entry(frame_sw)
entry_SW.grid(row=0, column=1, padx=5, sticky='ew')

# Row 3: Target Timestamp
frame_ts = tk.Frame(root)
frame_ts.grid(row=3, column=0, sticky='ew', padx=10, pady=6)
frame_ts.grid_columnconfigure(1, weight=1)
tk.Label(frame_ts, text="Target Timestamp").grid(row=0, column=0, padx=5, sticky='w')
entry_time = tk.Entry(frame_ts, width=30)
entry_time.grid(row=0, column=1, padx=5, sticky='ew')
tk.Label(frame_ts, text="YYYY-MM-DD HH-MM-SS").grid(row=0, column=2, padx=5, sticky='e')

# Row 4: Actions + Progress + Status
frame_actions = tk.Frame(root)
frame_actions.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
frame_actions.grid_columnconfigure(0, weight=0)
frame_actions.grid_columnconfigure(1, weight=1)
frame_actions.grid_columnconfigure(2, weight=0)

btn_copyandzip = tk.Button(frame_actions, text="Create zipped logs", width=18, command=copyandzip)
btn_copyandzip.grid(row=0, column=0, padx=5, sticky='w')

progress = ttk.Progressbar(frame_actions, mode='indeterminate')
progress.grid(row=0, column=1, padx=10, sticky='ew')
progress.grid_remove()  # HIDE initially (so no green bar before click)

status_var = tk.StringVar()
status_label = tk.Label(frame_actions, textvariable=status_var)
status_label.grid(row=0, column=2, padx=5, sticky='w')

# Row 5: Log Output (expandable)
frame_text = tk.Frame(root)
frame_text.grid(row=5, column=0, sticky='nsew', padx=10, pady=8)
frame_text.grid_rowconfigure(0, weight=1)
frame_text.grid_columnconfigure(0, weight=1)

text = tk.Text(frame_text, wrap='word')
text.grid(row=0, column=0, sticky='nsew')

scroll = tk.Scrollbar(frame_text, command=text.yview)
scroll.grid(row=0, column=1, sticky='ns')
text.configure(yscrollcommand=scroll.set)

root.mainloop()