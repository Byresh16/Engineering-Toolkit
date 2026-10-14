### FFmpeg

FFmpeg is used for video processing, cutting, encoding, and format handling in the Video Cutter Pro module.

👉 **Download FFmpeg for Windows:**

[Download FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

After downloading FFmpeg, make sure `ffmpeg.exe` is available in the location expected by the application.

### 7-Zip

7-Zip is required only when using the **Create archive after trimming** feature.

👉 **Download 7-Zip for Windows:**

[Download 7-Zip](https://www.7-zip.org/download.html)

For Windows x64, download the **64-bit `.exe` installer**. If the application uses a bundled `7z.exe`, ensure that the executable is available in the location expected by the application.

---

### 📁 Required Application Structure

The project folder should contain the following files and folders. The exact structure may vary depending on whether you run the Python source code or a packaged executable.

**For the packaged Video Cutter Pro application:**

```text
Video Cutter Pro/
│
├── Video Cutter Pro.exe
├── ffmpeg.exe
├── 7z.exe
└── _internal/
```

**For the Engineering Toolkit source project:**

```text
EngineeringToolkit_Merged/
│
├── main.py
├── VideoCutterPro/
│   └── video_cutter_pro.py
├── LogFinder/
│   └── ...
└── .gitignore
```

Make sure the executable paths match the paths configured in the application.
