# Text to MP3 Converter for Windows

This project builds a Windows GUI app that converts pasted text into MP3 audio.

The final Windows user does not need to install Python, packages, or FFmpeg. FFmpeg is bundled into the `.exe` by GitHub Actions.

## Build from Mac using GitHub Actions

1. Create a GitHub repository.
2. Push this folder to GitHub.
3. Go to the repository on GitHub.
4. Open **Actions**.
5. Run **Build Windows EXE**.
6. Download the artifact named **TextToMP3-Windows**.
7. Inside it, you will find `TextToMP3.exe`.

## Local development

You can edit `text_to_mp3_gui.py` on Mac, but the EXE must be built on Windows or GitHub Actions Windows runner.
