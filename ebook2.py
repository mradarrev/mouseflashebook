import tkinter as tk
import tkinter.font as tkFont
from win32api import GetSystemMetrics
from win32gui import SetWindowLong, GetWindowLong
from win32con import WS_EX_LAYERED, WS_EX_TOPMOST, GWL_EXSTYLE, LWA_COLORKEY
from ctypes import windll
import pyautogui
import keyboard
import time
import subprocess
import threading
import psutil

def speak1(word, speed=300):  # Changed 'palabra' to 'word', 'velocidad' to 'speed'
    try:
        process = subprocess.Popen([r"C:\Program Files (x86)\eSpeak\command_line\espeak.exe", "-v", "es-la", word], creationflags=subprocess.CREATE_NO_WINDOW)
        # Get the psutil.Process object
        p = psutil.Process(process.pid)

        # Try to set priority to real-time (requires administrator privileges)
        try:
            p.nice(psutil.REALTIME_PRIORITY_CLASS)
        except psutil.AccessDenied:
            print("Could not set real-time priority. Run as administrator.")
            # Try to set priority to high
            try:
                p.nice(psutil.HIGH_PRIORITY_CLASS)
            except psutil.AccessDenied:
                print("Could not set high priority.")

        process.wait()  # Wait for the subprocess to finish

    except FileNotFoundError:
        print("eSpeak not found. Check the path.")
    except Exception as e:
        print(f"Error running eSpeak: {e}")


def key():
    keyboard.add_hotkey('esc', close_app)  # Changed 'cerrar_app' to 'close_app'




def speak(word, speed=600): # Changed 'palabra' to 'word', 'velocidad' to 'speed'
    try:
        subprocess.run([r"C:\Program Files (x86)\eSpeak\command_line\espeak.exe", "-v", "es-la", "-s", str(speed), word], creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        print("eSpeak not found. Check the path.")
    except Exception as e:
        print(f"Error running eSpeak: {e}")

def close_app(event=None): # Changed 'cerrar_app' to 'close_app', added optional event parameter
    global keep_running # Changed 'seguir_ejecutando' to 'keep_running'
    keep_running = False
    root.destroy()
    keyboard.unhook_all()

def display_word():  # Changed 'mostrar_palabra' to 'display_word'
    global word_index # Changed 'indice_palabra' to 'word_index'

    if word_index < len(words) and keep_running:
        word = words[word_index] # Changed 'palabra' to 'word'
        # Removed commented-out code for clarity

        text_width = font.measure(word) # Changed 'ancho_texto' to 'text_width', 'fuente' to 'font'
        x, y = pyautogui.position()
        offset = 40
        line_height = 30 # Changed 'altura_linea' to 'line_height'
        text_x = min(max(0, x - text_width // 2), screen_width - text_width) # Changed 'ancho_pantalla' to 'screen_width', 'texto_x' to 'text_x'
        canvas.coords(text_id, text_x, 0)
        canvas.itemconfig(text_id, text=word)
        root.geometry(f"{screen_width}x{line_height}+0+{y - line_height // 2 - offset}")
        word_index += 1
        words_per_minute = 250 # Added clarification comment: words per minute
        ms_per_word = int(60000 / words_per_minute)
        root.after(ms_per_word, display_word_cycle) # Schedule the next word display
    else:
        word_index = 0

def display_word_cycle(): # Changed 'mostrar_palabra_ciclo' to 'display_word_cycle'
    if keep_running:
        display_word()


# Removed unused threading code

with open("libro3.txt", "r", encoding="utf-8") as file: # Changed 'archivo' to 'file'
    text = file.read()
    words = text.split() # Changed 'palabras' to 'words'


root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

root.bind("<Escape>", close_app)


hwnd = int(root.frame(), 16)
exstyle = GetWindowLong(hwnd, GWL_EXSTYLE)
SetWindowLong(hwnd, GWL_EXSTYLE, exstyle | WS_EX_LAYERED | WS_EX_TOPMOST)
windll.user32.SetLayeredWindowAttributes(hwnd, 0xFFFFFF, 0, LWA_COLORKEY)

screen_width = GetSystemMetrics(0) # Changed 'ancho_pantalla' to 'screen_width'
line_height = 30  # Changed 'altura_linea' to 'line_height'
font = tkFont.Font(family="Arial", size=18) # Changed 'fuente' to 'font'

canvas = tk.Canvas(root, width=screen_width, height=line_height, bg="white", highlightthickness=0)
canvas.pack()

# Removed black rectangle code for simplicity


text_id = canvas.create_text(0, 0, text="", font=font, fill="black", anchor="nw")

word_index = 0  # Changed 'indice_palabra' to 'word_index'
keep_running = True # Changed 'seguir_ejecutando' to 'keep_running'

display_word()

keyboard.on_press_key("Escape", close_app)

root.mainloop()