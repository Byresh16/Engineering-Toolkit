import os
import shutil
import subprocess

LOG_FOLDERS = {
    "android": "Android_Logs",
    "dropbox": "Dropbox_Logs",
    "bugreport": "Bugreport_Logs",
    "meminfo": "Meminfo_ECS_Logs",
    "teraterm": "Teraterm_Logs",
    "can": "CAN_Logs",
}


def locate_7zip():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.path.dirname(here), "VideoCutterPro", "7z.exe"),
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return shutil.which("7z") or shutil.which("7za")


def zip_with_7zip(entry_folder, entry_sw, logger=None):
    seven_zip = locate_7zip()
    if not seven_zip:
        raise FileNotFoundError(
            "7-Zip was not found. Install 7-Zip or place 7z.exe in "
            "the VideoCutterPro folder."
        )
    for folder in LOG_FOLDERS.values():
        folder_name = "{}_{}".format(folder, entry_sw)
        source_folder = os.path.join(entry_folder, folder_name)
        if not os.path.isdir(source_folder) or not os.listdir(source_folder):
            continue
        output_archive = source_folder + ".7z"
        cmd = [seven_zip, "a", "-r", "-mx=9", "-v14M", output_archive, source_folder]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if logger:
            if result.returncode == 0:
                logger("7-Zip archive created: {}".format(output_archive))
            else:
                logger("7-Zip failed for {}: {}".format(folder_name, result.stderr or result.stdout))
        if result.returncode != 0:
            raise RuntimeError("7-Zip failed for {} (exit code {}).".format(folder_name, result.returncode))
