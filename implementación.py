import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import random
import tkinter as tk
from tkinter import scrolledtext
import threading
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import webbrowser
import pyjokes 
import time

name = 'asistente'

listener = sr.Recognizer() 
engine = pyttsx3.init() 
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)

def talk(text):
  engine.say(text)
  engine.runAndWait()

def listen():
  try:
    with sr.Microphone() as source:
      print("Escuchando...")
      voice = listener.listen(source)
      rec = listener.recognize_google(voice, language='es-ES')
      rec = rec.lower()
      if name in rec:
        rec = rec.replace(name, '')
      return rec
  except sr.UnknownValueError:
    return "No se entendió el audio"
  except sr.RequestError as e:
    return f"Error al solicitar resultados: {e}"
  except Exception as e:
    return f"Error inesperado: {e}"

def process_command(rec):
  text_area.insert(tk.END, f"Tú: {rec}\n")
  
  if 'reproduce' in rec:
    music = rec.replace('reproduce', '')
    response = f'Reproduciendo {music}'
    pywhatkit.playonyt(music)
  elif 'hora' in rec:
    hora = datetime.datetime.now().strftime('%I:%M %p')
    response = f"Son las {hora}"
  elif 'busca' in rec:
    order = rec.replace('busca', '')
    wikipedia.set_lang("es")
    info = wikipedia.summary(order, 1)
    response = info
    
  elif 'abre' in rec:
    app = rec.replace('abre', '')
    if 'google' in app:
      webbrowser.open('https://www.google.com')
      response = 'Abriendo Google'
    elif 'youtube' in app:
      webbrowser.open('https://www.youtube.com')
      response = 'Abriendo YouTube'
    elif 'facebook' in app:
      webbrowser.open('https://www.facebook.com')
      response = 'Abriendo Facebook'
    elif 'instagram' in app:
      webbrowser.open('https://www.instagram.com')
      response = 'Abriendo Instagram'
    else:
      response = 'No puedo abrir esa aplicación'
  elif 'noticias' in rec:
    webbrowser.open('https://www.bbc.com/mundo')
    response = 'Abriendo noticias de BBC Mundo'
  elif 'chiste' in rec:
    response = pyjokes.get_joke(language='es')
  elif 'adiós' in rec or 'hasta luego' in rec:
    response = 'Hasta luego, ¡que tengas un buen día!'
    root.destroy()
  else:
    response = "No entendí la instrucción. ¿Puedes repetirla?"
  text_area.insert(tk.END, f"Asistente: {response}\n\n") 
  talk(response)

def run_assistant():
  rec = listen()
  process_command(rec)

def start_listening():
  threading.Thread(target=run_assistant, daemon=True).start()

def get_random_image():
  try:
    response = requests.get("https://source.unsplash.com/random/400x500")
    img = Image.open(BytesIO(response.content))
    return ImageTk.PhotoImage(img)
  except Exception as e:
    print(f"Error al obtener la imagen: {e}")
    return None

def change_background():
  global photo
  photo = get_random_image()
  if photo:
    canvas.itemconfig(background_image, image=photo)
  root.after(30000, change_background)  # Cambia la imagen cada 30 segundos

def send_command():
  rec = command_entry.get().lower()
  command_entry.delete(0, tk.END)  # Limpiar el cuadro de texto
  process_command(rec)

root = tk.Tk()
root.title("Asistente de Voz")
root.geometry("400x600")

canvas = tk.Canvas(root, width=400, height=500)
canvas.pack(fill="both", expand=True)

canvas.configure(bg='#E6F3FF')

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15, bg='white')
text_area.place(relx=0.5, rely=0.4, anchor='center')

command_entry = tk.Entry(root, width=40)
command_entry.place(relx=0.5, rely=0.7, anchor='center')

send_button = tk.Button(root, text="Enviar", command=send_command, bg='#4CAF50', fg='white')
send_button.place(relx=0.5, rely=0.77, anchor='center')

start_button = tk.Button(root, text="Iniciar Asistente", command=start_listening, bg='#4CAF50', fg='white')
start_button.place(relx=0.5, rely=0.85, anchor='center')

background_image = canvas.create_image(0, 0, anchor='nw')
change_background()

root.mainloop()