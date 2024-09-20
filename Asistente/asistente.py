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
import psutil
import webbrowser

name = 'asistente'
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

bromas = [
  "¿Por qué la computadora fue al doctor? ¡Tenía un virus!",
  "¿Por qué el astronauta se divorció? ¡Porque necesitaba espacio!",
  "¿Qué le dice un semáforo a otro semáforo? ¡No me mires, que me estoy cambiando!",
  "¿Por qué la bicicleta se cayó? ¡Porque estaba dos-tired!",
  "¿Qué hace un pez en el espacio? ¡Nada, porque no hay agua!"
]

# Definir los enlaces HTML y archivos locales
links = {
    "quechua": "quechua.html",  # Ejemplo de enlace
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "comienzo": "comienzo.html"  # Archivo HTML local
}

# Variable global para el contexto de la conversación
conversation_mode = False

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

def open_application(app_name):
    apps = {
        "excel": "start excel",
        "google": "start chrome",
        "microsoft": "start winword"
    }
    if app_name in apps:
        os.system(apps[app_name])
        return f'Abriendo {app_name.capitalize()}'
    else:
        return f'No puedo abrir {app_name}, lo siento.'

def close_application(app_name):
    app_processes = {
        "excel": "EXCEL.EXE",
        "google": "chrome.exe",
        "notas": "notepad.exe"
    }
    if app_name in app_processes:
        for proc in psutil.process_iter():
            if proc.name().lower() == app_processes[app_name].lower():
                proc.kill()
                return f'Cerrando {app_name.capitalize()}.'
    return f'No pude cerrar {app_name}, lo siento.'

def get_weather(city):
    api_key = 'tu_api_key'  # Usa tu API key de OpenWeatherMap
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es'
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"La temperatura en {city} es de {temp} grados Celsius con {description}."
    else:
        return "No pude obtener el clima en este momento."

def open_link(link_name):
    if link_name in links:
        link = links[link_name]
        if link.endswith('.html'):
            # Abrir archivo HTML local
            os.system(f'start {link}')  # Funciona en Windows, para MacOS/Linux usa open
            return f'Abriendo el archivo {link_name}.'
        else:
            # Abrir enlace en navegador web
            webbrowser.open(link)
            return f'Abriendo {link_name.capitalize()}'
    else:
        return f'No tengo el enlace para {link_name}.'

def run_assistant():
    global conversation_mode
    rec = listen()
    text_area.insert(tk.END, f"Tú: {rec}\n")

    if 'activar conversación' in rec:
        conversation_mode = True
        response = "Modo conversación activado. Puedes hablarme como si estuviéramos conversando."
    elif 'desactivar conversación' in rec:
        conversation_mode = False
        response = "Modo conversación desactivado."
    elif conversation_mode:
        if 'cómo estás' in rec:
            response = 'Estoy bien, gracias. ¿Y tú?'
        elif 'bien' in rec or 'mal' in rec:
            response = 'Me alegra saberlo.' if 'bien' in rec else 'Lo siento, espero que te sientas mejor pronto.'
        elif 'cuéntame algo' in rec:
            response = random.choice(bromas)
        elif 'repite' in rec:
            response = 'Claro, repito: ' + rec
        else:
            response = "No entendí bien, ¿puedes repetir?"
    else:
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
        elif 'broma' in rec or 'cuenta un chiste' in rec:
            response = random.choice(bromas)
        elif 'abrir' in rec:
            app = rec.replace('abrir', '').strip()
            response = open_application(app)
        elif 'cerrar' in rec:
            app = rec.replace('cerrar', '').strip()
            response = close_application(app)
        elif 'clima en' in rec:
            city = rec.replace('clima en', '').strip()
            response = get_weather(city)
            pywhatkit.search(f"Clima en {city}")
        elif 'imagen de' in rec:
            search_term = rec.replace('imagen de', '').strip()
            pywhatkit.search(f"Imagen de {search_term}")
            response = f"Buscando imágenes de {search_term} en Google."
        elif 'abre a' in rec:
            link_name = rec.replace('abre a', '').strip()
            response = open_link(link_name)
        else:
            response = "No entendí la instrucción. ¿Puedes repetir?"

    text_area.insert(tk.END, f"Asistente: {response}\n\n")
    talk(response)

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

# Crear la ventana principal
root = tk.Tk()
root.title("Asistente de Voz")
root.geometry("600x600")

# Crear un canvas para el fondo
canvas = tk.Canvas(root, width=400, height=500)
canvas.pack(fill="both", expand=True)

# Configurar el fondo celeste
canvas.configure(bg='#E6F3FF')  # Color celeste claro

# Crear y configurar el área de texto
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20, bg='white')
text_area.place(relx=0.5, rely=0.4, anchor='center')

# Botón para iniciar el asistente
start_button = tk.Button(root, text="Iniciar Asistente", command=start_listening, bg='#4CAF50', fg='white')
start_button.place(relx=0.5, rely=0.85, anchor='center')

# Configurar el cambio de fondo
background_image = canvas.create_image(0, 0, anchor='nw')
change_background()

# Iniciar la interfaz gráfica
root.mainloop()