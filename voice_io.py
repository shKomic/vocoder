import keyboard
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3

WAVEDIR = "./wave_data/"
READ_FILENAME = WAVEDIR + "test.wav"
OUT_FILENAME = WAVEDIR + "test.wav"

p = pyaudio.PyAudio()

def out_voice():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("- recording -")
    print("rate / chunk * record_second: {}".format(RATE/CHUNK*RECORD_SECONDS))
    frames = []
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data =stream.read(CHUNK)
        frames.append(data)

    print("- done recording -")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(OUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def read_voice():
    wf = wave.open(READ_FILENAME, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def echo_back():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    print(" - echo back - ")
    frames = np.array([])
    fframes = np.array([])
    amp = (2**8)**p.get_sample_size(FORMAT)/2
    wf = wave.open(OUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    while True:
        print("aaa")
        if keyboard.is_pressed('q'):
            print("stop echo back")
            break
        data=stream.read(CHUNK)
        frames = np.append(frames,[np.frombuffer(data)])
        plt.plot(frames)
        plt.draw()
        plt.cla()
        #fframes = np.append(fframes, np.fft.fft(np.frombuffer(data, dtype="int16")))
        stream.write(data)
        #wf.writeframes(b''.join(frames))
    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    #out_voice()
    #read_voice()
    echo_back()
