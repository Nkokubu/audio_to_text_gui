import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import speech_recognition as sr
from pydub import AudioSegment
import os

def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer()
    file_ext = os.path.splitext(file_path)[-1].lower()

    # Convert MP3 to WAV if needed
    if file_ext == ".mp3":
        audio = AudioSegment.from_mp3(file_path)
        file_path = "converted.wav"
        audio.export(file_path, format="wav")

    try:
        with sr.AudioFile(file_path) as source:
            status_label.config(text="Listening to audio...")
            audio_data = recognizer.record(source)
            status_label.config(text="Transcribing...")
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Sorry, the audio could not be understood."
    except sr.RequestError as e:
        return f"Error with the Google API: {e}"

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        result = convert_audio_to_text(file_path)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result)
        status_label.config(text="Done")

# Set up GUI
window = tk.Tk()
window.title("Audio to Text Converter")

browse_btn = tk.Button(window, text="Choose Audio File", command=browse_file)
browse_btn.pack(pady=10)

text_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
text_output.pack(padx=10, pady=10)

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
