# Config file format = {Path to audio}|{Activation key}
from tkinter import *
import pyaudio
import numpy as np
import keyboard
import sounddevice
import threading
import soundfile
import time

exi = False
stop_button = "f2"

def callback(indata, outdata, frames, time, status):
        if status:
                print(status)
        outdata[:] = indata

def stopcheck(button):
        while True:
            if keyboard.is_pressed(button):
                    sounddevice.stop()
            time.sleep(0.2)

def play(devices):
    global exi
    files = []
    with open("sound.conf","r") as infile:
        for lin in infile.readlines():
            temp = []
            sgem = lin.split("|")
            for y in sgem:
                temp.append(y.replace("\n",""))
            sgem = temp
            files.append((sgem[0],sgem[1]))
    with sounddevice.Stream(device=devices,
                   samplerate=44100, blocksize=1000,
                   dtype='float32', latency='high',
                   channels=2, callback=callback):
        while True:
            for x in files:
                print(exi)
                if exi:
                    return
                time.sleep(0.1)
                try:
                    if keyboard.is_pressed(x[1]):
                        #print("Playing")
                        array, smp_rt = soundfile.read(x[0], dtype = 'float32') 
                        sounddevice.play(array,smp_rt,device=devices[1])
                        status = sounddevice.wait()
                        sounddevice.stop()
                        array = None
                        
                except:
                    print("Error")
                    continue

tk = Tk()

tk.title("Soundboard")
tk.resizable(False,False)

mic = StringVar()
mic.set("Select microphone.")

miclist = []
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    miclist.append(p.get_device_info_by_index(i).get("name"))

mic_select = OptionMenu(tk,mic,*miclist)

threading.Thread(target=lambda:stopcheck(stop_button)).start()
start_button = Button(command=lambda:threading.Thread(target=lambda:play((miclist.index(mic.get()),"VB-Audio Virtual Ca, MME"))).start(),text="Start",width=20)

mic_select.grid(row=0,column=0)
start_button.grid(row=1,column=0)

tk.mainloop()
