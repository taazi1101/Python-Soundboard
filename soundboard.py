# Config file format = {Path to audio}|{Activation key}
import numpy as np
import keyboard
import sounddevice
import soundfile
import time


devices = (sounddevice.default.device[0],"VB-Audio Virtual Ca, MME")

def callback(indata, outdata, frames, time, status):
        if status:
                print(status)
        outdata[:] = indata

def play(files,devices):
    with sounddevice.Stream(device=devices,
                   samplerate=44100, blocksize=1000,
                   dtype='float32', latency='high',
                   channels=2, callback=callback):
        while True:
            for x in files:
                time.sleep(0.1)
                try:
                    if keyboard.is_pressed(x[1]):
                        #print("Playing")
                        array, smp_rt = soundfile.read(x[0], dtype = 'float32') 
                        sounddevice.play(array,smp_rt,device=devices[1])
                        status = sounddevice.wait() 
                        sounddevice.stop()
                        
                except:
                    print("Error")
                    continue


files = []
with open("sound.conf","r") as infile:
    for lin in infile.readlines():
        temp = []
        sgem = lin.split("|")
        for y in sgem:
            temp.append(y.replace("\n",""))
        sgem = temp
        files.append((sgem[0],sgem[1]))
        
play(files,devices)
