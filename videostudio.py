
import pygetwindow as gw
import mss
import cv2
import numpy as np
import threading
import time
#pip install pygetwindow mss opencv-python-headless opencv-python

def record_screen(window_title):
    # Localizar a janela com o título especificado
    window = gw.getWindowsWithTitle(window_title)
    if not window:
        print(f'No window with title "{window_title}" found.')
        return
    
    window = window[0]

    # Obter a posição e tamanho da janela
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    width = right - left
    height = bottom - top
    
    # Configurar o gravador de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    out = cv2.VideoWriter(f'window_recording.avi', fourcc, fps, (width, height))

    sct = mss.mss()
    monitor = {"top": top, "left": left, "width": width, "height": height}
    
    print("Recording... Press Enter to stop.")
    while not stop_recording:
        img = sct.grab(monitor)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        out.write(frame)
        time.sleep(1/fps)

    out.release()
    print("Recording stopped.")

def wait_for_enter():
    input()  # Aguarda o pressionamento da tecla Enter
    global stop_recording
    stop_recording = True

if __name__ == "__main__":
    window_title = gw.getActiveWindow().title
    stop_recording = False
    
    # Iniciar a gravação em um thread separado
    recording_thread = threading.Thread(target=record_screen, args=(window_title,))
    recording_thread.start()

    # Esperar pela tecla Enter para parar a gravação
    wait_for_enter()

    # Aguardar o término da gravação
    recording_thread.join()
