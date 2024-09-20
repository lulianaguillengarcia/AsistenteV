import speech_recognition as sr
import subprocess
import pyautogui

recognizer = sr.Recognizer()
proceso = None
saludo = """ 
Hola, ¿cómo están?
Naruto es el Rey de los Reyes, ¡el papi! jajajaja xd"""

def ejecutar_comando(comando):
    global proceso
    if "abrir notepad" in comando:
        proceso = subprocess.Popen(["notepad.exe"])
    elif "saludar seguidores" in comando:
        pyautogui.write(saludo)
    elif "cerrar notepad" in comando and proceso is not None:
        proceso.terminate()
        proceso = None
    elif "abrir asistente" in comando:
        # Ejecutar el script de Python
        try:
            proceso = subprocess.Popen(["python", "asistente.py"])  # Asegúrate de que 'app.py' esté en el mismo directorio
            print("Ejecutando asistente.py")
        except FileNotFoundError:
            print("No se pudo encontrar asistente.py")
    elif "cerrar asistente" in comando and proceso is not None:
        proceso.terminate()
        proceso = None

def escuchar_comando():
    with sr.Microphone() as source:
        print("¿En qué te puedo ayudar en este momento?")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="es-ES")
        print(f"Comando reconocido: {comando}")
        return comando.lower()  # Convertir el comando a minúsculas para evitar problemas de mayúsculas/minúsculas

    except sr.UnknownValueError:
        print("No se pudo entender el comando.")
        return None
    except sr.RequestError as e:
        print(f"Error al realizar el comando: {e}")
        return None

while True:
    comando = escuchar_comando()
    if comando:
        if "stop" in comando:
            print("Deteniendo el programa.")
            break  # Rompe el ciclo y detiene el programa
        ejecutar_comando(comando) 