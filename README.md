# Engineering Toolkit

A combined Windows desktop application with two tabs:
- **Logs Finder**: selects nearby logs for a target timestamp, copies them into categorized folders, and creates split 7-Zip archives.
- **Video Cutter Pro**: video trimming, issue-based cutting, progress/cancel controls, and optional archive creation.

## Requirements
- Windows
- Python 3.10+ (Python 3.11 or newer recommended)
- FFmpeg executable (`ffmpeg.exe`)
- 7-Zip command-line executable (`7z.exe`) for archive features

No third-party Python packages are required by the app itself.

## Run from source
1. Extract the entire `EngineeringToolkit` folder.
2. Place `ffmpeg.exe` and `7z.exe` inside `VideoCutterPro` if they are not already installed system-wide.
3. Open PowerShell or Command Prompt in the `EngineeringToolkit` folder.
4. Run:

   ```powershell
   python main.py
   ```

## Logs Finder setup
The Logs Finder tab contains editable source-folder paths. Change them to match your machine. The defaults reflect the paths used in the original version:
- `D:\99.Log\1.Renault_AndroidLog`
- `D:\99.Log\2.Renault_Dropbox_Log`
- `D:\99.Log\4.ecs`
- `D:\99.Log\5.Teraterm`
- CAN log folder: select the correct folder on your machine

Enter the destination folder, software version, and target timestamp in `YYYY-MM-DD HH-MM-SS` format.

`LogsFinder/app.ini` contains supported timestamp formats. The application also has built-in defaults if this file is missing or incomplete.

## Notes
- The app keeps the two tools in one window using separate tabs.
- The original Video Cutter Pro code is kept as the basis of the video tab.
- Archive features require 7-Zip. If it is not installed in a standard location, place `7z.exe` in `VideoCutterPro`.
