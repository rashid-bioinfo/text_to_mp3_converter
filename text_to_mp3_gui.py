import os
import sys
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "Text to MP3 Converter"


def resource_path(relative_path: str) -> str:
    """Get absolute path for bundled files inside PyInstaller exe."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_ffmpeg_path() -> str:
    """Use bundled ffmpeg.exe if present, otherwise fall back to system ffmpeg."""
    bundled = resource_path(os.path.join("bin", "ffmpeg.exe"))
    if os.path.exists(bundled):
        return bundled
    return "ffmpeg"


def powershell_escape(text: str) -> str:
    """Escape text safely for a single-quoted PowerShell string."""
    return text.replace("'", "''")


def convert_text_to_wav(text: str, wav_path: str, voice_name: str | None = None, rate: int = 0) -> None:
    escaped_text = powershell_escape(text)
    escaped_wav = powershell_escape(wav_path)

    select_voice = ""
    if voice_name and voice_name != "Default":
        select_voice = f"$speaker.SelectVoice('{powershell_escape(voice_name)}');"

    ps_script = f"""
Add-Type -AssemblyName System.Speech;
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer;
{select_voice}
$speaker.Rate = {rate};
$speaker.SetOutputToWaveFile('{escaped_wav}');
$speaker.Speak('{escaped_text}');
$speaker.Dispose();
"""

    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def convert_wav_to_mp3(wav_path: str, mp3_path: str, bitrate: str = "192k") -> None:
    ffmpeg = get_ffmpeg_path()
    subprocess.run(
        [ffmpeg, "-y", "-i", wav_path, "-b:a", bitrate, mp3_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def convert() -> None:
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Missing text", "Please enter text first.")
        return

    output_mp3 = filedialog.asksaveasfilename(
        title="Save MP3 file",
        defaultextension=".mp3",
        filetypes=[("MP3 audio", "*.mp3")],
    )
    if not output_mp3:
        return

    voice = voice_var.get()
    bitrate = bitrate_var.get()
    rate = int(rate_var.get())

    convert_button.config(state="disabled", text="Converting...")
    root.update_idletasks()

    wav_path = os.path.join(tempfile.gettempdir(), "text_to_mp3_temp_output.wav")

    try:
        convert_text_to_wav(text, wav_path, voice, rate)
        convert_wav_to_mp3(wav_path, output_mp3, bitrate)
        messagebox.showinfo("Done", f"MP3 saved successfully:\n{output_mp3}")
    except subprocess.CalledProcessError as e:
        error_text = e.stderr if e.stderr else str(e)
        messagebox.showerror("Conversion failed", error_text)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        convert_button.config(state="normal", text="Convert to MP3")
        try:
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception:
            pass


def load_voices() -> list[str]:
    """Read installed Windows voices. In development on Mac/Linux, return Default only."""
    if os.name != "nt":
        return ["Default"]

    ps_script = """
Add-Type -AssemblyName System.Speech;
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$speaker.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
$speaker.Dispose();
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            check=True,
            capture_output=True,
            text=True,
        )
        voices = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return ["Default"] + voices if voices else ["Default"]
    except Exception:
        return ["Default"]


root = tk.Tk()
root.title(APP_TITLE)
root.geometry("720x560")
root.minsize(650, 480)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

title = ttk.Label(main, text="Text to MP3 Converter", font=("Segoe UI", 18, "bold"))
title.pack(anchor="w", pady=(0, 6))

subtitle = ttk.Label(
    main,
    text="Paste text below, choose voice settings, and save as an MP3 file.",
    font=("Segoe UI", 10),
)
subtitle.pack(anchor="w", pady=(0, 12))

text_box = tk.Text(main, wrap="word", font=("Segoe UI", 11), height=14)
text_box.pack(fill="both", expand=True)
text_box.insert("1.0", "Type or paste your text here...")

settings = ttk.Frame(main)
settings.pack(fill="x", pady=12)

voice_var = tk.StringVar(value="Default")
voices = load_voices()

voice_label = ttk.Label(settings, text="Voice")
voice_label.grid(row=0, column=0, sticky="w", padx=(0, 8))
voice_menu = ttk.Combobox(settings, textvariable=voice_var, values=voices, state="readonly", width=28)
voice_menu.grid(row=1, column=0, sticky="w", padx=(0, 20))

rate_var = tk.StringVar(value="0")
rate_label = ttk.Label(settings, text="Speed")
rate_label.grid(row=0, column=1, sticky="w", padx=(0, 8))
rate_menu = ttk.Combobox(settings, textvariable=rate_var, values=["-3", "-2", "-1", "0", "1", "2", "3"], state="readonly", width=8)
rate_menu.grid(row=1, column=1, sticky="w", padx=(0, 20))

bitrate_var = tk.StringVar(value="192k")
bitrate_label = ttk.Label(settings, text="MP3 quality")
bitrate_label.grid(row=0, column=2, sticky="w")
bitrate_menu = ttk.Combobox(settings, textvariable=bitrate_var, values=["128k", "192k", "256k", "320k"], state="readonly", width=10)
bitrate_menu.grid(row=1, column=2, sticky="w")

convert_button = ttk.Button(main, text="Convert to MP3", command=convert)
convert_button.pack(anchor="e", pady=(8, 0))

footer = ttk.Label(
    main,
    text="Windows app. No Python installation required when packaged as EXE.",
    font=("Segoe UI", 9),
)
footer.pack(anchor="w", pady=(12, 0))

root.mainloop()
