import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import sys

def record_audio(filename="input.wav", duration=5, fs=44100):
    """
    Records audio for a fixed duration.
    
    Args:
        filename (str): Output filename.
        duration (int): Duration in seconds.
        fs (int): Sampling frequency.
    """
    print(f"Recording for {duration} seconds... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)
    print(f"Recording saved to {filename}")
    return filename

def play_audio(filename):
    """
    Plays an audio file using system default player or sounddevice if possible.
    Since playing MP3s (from gTTS) with sounddevice requires decoding (e.g. via pydub),
    and pydub requires ffmpeg, it is often easier to just use the OS default player 
    for a simple bot, OR use IPython if in a notebook.
    
    This function attempts to use the OS default command to open the file.
    """
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        # MacOS/Linux
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        os.system(f"{opener} {filename}")

def record_audio_interactive(filename="input.wav", fs=44100):
    """
    Records audio until the user presses Enter.
    """
    import queue
    import soundfile as sf
    
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    print("Recording... Press Ctrl+C to stop.")
    try:
        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=fs,
                          channels=1, subtype='PCM_16') as file:
            with sd.InputStream(samplerate=fs, device=None,
                                channels=1, callback=callback):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print(f"\nRecording finished: {filename}")
    return filename
