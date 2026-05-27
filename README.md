<p align="center">
  <h1 align="center">Text to MP3 Converter</h1>
  <p align="center">
    <b>Windows GUI App for Text-to-Speech MP3 Generation</b><br>
    <i>Python · Tkinter · gTTS · PyInstaller · GitHub Actions CI/CD</i>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Interface-Tkinter-4EAA25?style=flat-square" alt="Tkinter">
  <img src="https://img.shields.io/badge/TTS-gTTS-FF4B4B?style=flat-square" alt="gTTS">
  <img src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Distribution-Standalone%20EXE-555?style=flat-square" alt="EXE">
</p>

---

## Overview

**Text to MP3 Converter** is a Windows desktop GUI application that converts user-pasted text into downloadable MP3 audio files using Google Text-to-Speech (gTTS). The application is packaged as a fully standalone `.exe` — end users do not need to install Python, pip packages, or FFmpeg; everything is bundled.

The build pipeline is automated via **GitHub Actions**, which compiles the Python application on a Windows runner, bundles FFmpeg, and produces a downloadable artifact.

---

## Key Features

| Feature | Description |
|---|---|
| **Simple GUI** | Paste text directly into the application window and click Convert |
| **MP3 output** | Generates standard MP3 audio files using gTTS (Google Text-to-Speech) |
| **Standalone EXE** | No Python or FFmpeg installation required on the target Windows machine |
| **Bundled FFmpeg** | FFmpeg is embedded into the executable by the GitHub Actions build workflow |
| **CI/CD pipeline** | Automated cross-platform builds via GitHub Actions Windows runner |
| **Zero-dependency distribution** | Single `.exe` file for end-user distribution |

---

## Download

To get the latest standalone Windows executable:

1. Go to the **Actions** tab of this repository on GitHub.
2. Open the most recent successful **Build Windows EXE** run.
3. Download the artifact named **TextToMP3-Windows**.
4. Extract the archive and run `TextToMP3.exe` — no installation needed.

---

## Usage

1. Launch `TextToMP3.exe`.
2. Paste or type your text into the input area.
3. Click **Convert to MP3**.
4. Choose a save location for the output `.mp3` file.
5. The audio file is ready for playback in any media player.

---

## Build from Source

### Prerequisites

| Tool | Purpose |
|---|---|
| Python 3.x | Application runtime |
| `gTTS` | Google Text-to-Speech synthesis |
| `pydub` | Audio processing and MP3 export |
| `PyInstaller` | Packaging Python app as a standalone EXE |
| FFmpeg | Audio encoding (bundled automatically by the build workflow) |

Install Python dependencies:

```bash
pip install gtts pydub pyinstaller
```

### Local development (macOS / Linux)

The source file `text_to_mp3_gui.py` can be edited on any platform, but the Windows EXE **must be built on a Windows runner** (or via GitHub Actions) due to PyInstaller's platform-specific compilation.

```bash
# Run directly on Windows for development/testing
python text_to_mp3_gui.py
```

### Build the Windows EXE via GitHub Actions

1. Push changes to the `main` branch.
2. Go to **Actions → Build Windows EXE** in the GitHub repository.
3. The workflow will:
   - Spin up a Windows runner
   - Install Python and all dependencies
   - Download and bundle FFmpeg
   - Run PyInstaller to produce `TextToMP3.exe`
   - Upload `TextToMP3-Windows` as a downloadable artifact
4. Download the artifact from the completed workflow run.

### Repository structure

```
text_to_mp3_converter/
├── text_to_mp3_gui.py            # Main application source
├── .github/
│   └── workflows/
│       └── build.yml             # GitHub Actions build workflow
└── README.md
```

---

## Author

**Rashid Hussain**, PhD, RSci, MRSC  
Postdoctoral Researcher in Computational Pathology  
Humanitas Research Hospital (IRCCS), Milan, Italy  
[rashid.bioinfo@gmail.com](mailto:rashid.bioinfo@gmail.com) · [https://rashid-bioinfo.github.io](https://rashid-bioinfo.github.io)

---

## License

This project is released under the MIT License. See `LICENSE` for details.

---

<p align="center">
  <i>Text-to-Speech · Python · Windows · GitHub Actions CI/CD</i>
</p>
