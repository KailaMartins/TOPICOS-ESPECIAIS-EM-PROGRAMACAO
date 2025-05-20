import os
import tkinter as tk
from tkinter import filedialog, messagebox
from groq import Groq
import pygame  # Importando pygame para controle de áudio

# Inicializando o pygame mixer
pygame.mixer.init()

def select_audio_file():
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.flac")])
    if filepath:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filepath)

def transcribe_audio():
    filepath = entry_path.get()
    if not os.path.isfile(filepath):
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de áudio válido.")
        return
    
    try:
        client = Groq()
        with open(filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(filepath), file.read()),
                model="whisper-large-v3-turbo",
                response_format="json",
                language="en",
                temperature=0.0
            )
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, transcription.text)
    except Exception as e:
        messagebox.showerror("Erro na Transcrição", str(e))

def clear_text():
    text_output.delete("1.0", tk.END)
    entry_path.delete(0, tk.END)

def play_audio():
    filepath = entry_path.get()
    if not os.path.isfile(filepath):
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de áudio válido.")
        return
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

# Criar a interface gráfica
root = tk.Tk()
root.title("Transcrição de Áudio")
root.geometry("650x450")
root.configure(bg="#F0F0F0")

# Cabeçalho estilizado
header_frame = tk.Frame(root, bg="#5F9EA0", height=50)
header_frame.pack(fill=tk.X)

header = tk.Label(header_frame, text="Transcrição de Áudio", font=("Verdana", 12, "bold"), bg="#5F9EA0", fg="white")
header.pack(pady=10)

# Área de seleção de arquivo
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=20)

entry_path = tk.Entry(frame, width=50, font=("Arial", 12))
entry_path.pack(side=tk.LEFT, padx=5, ipadx=5, ipady=3)

btn_browse = tk.Button(frame, text="Selecionar Arquivo", command=select_audio_file, font=("Verdana", 10, "bold"), bg="#5F9EA0", fg="white", padx=5, pady=5)
btn_browse.pack(side=tk.LEFT, padx=5)

# Botões
btn_frame = tk.Frame(root, bg="#F0F0F0")
btn_frame.pack(pady=10)

btn_transcribe = tk.Button(btn_frame, text="Transcrever Áudio", command=transcribe_audio, font=("Verdana", 8, "bold"), bg="white", fg="black", padx=8, pady=4)
btn_transcribe.pack(side=tk.LEFT, padx=10)

btn_clear = tk.Button(btn_frame, text="Limpar", command=clear_text, font=("Verdana", 8, "bold"), bg="white", fg="black", padx=8, pady=4)
btn_clear.pack(side=tk.LEFT, padx=10)

btn_play = tk.Button(btn_frame, text="Reproduzir", command=play_audio, font=("Verdana", 8, "bold"), bg="white", fg="black", padx=8, pady=4)
btn_play.pack(side=tk.LEFT, padx=10)

btn_stop = tk.Button(btn_frame, text="Parar", command=stop_audio, font=("Verdana", 8, "bold"), bg="white", fg="black", padx=8, pady=4)
btn_stop.pack(side=tk.LEFT, padx=10)

# Área de saída do texto
text_output = tk.Text(root, height=12, width=70, font=("Verdana", 12), wrap=tk.WORD, bd=2, relief=tk.GROOVE)
text_output.pack(pady=10, padx=10)

root.mainloop()