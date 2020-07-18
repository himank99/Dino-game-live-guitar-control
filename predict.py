import os
import tensorflow as tf
import keras
from tensorflow import keras
from tensorflow.keras import layers
import chords_imp
import data_set
import pyaudio
import wave
import HPCP
from message import create_msg
import numpy as np
checkpoint_path = "Desktop/dino/wts/cp.ckpt"
IPC_FIFO_NAME = "Desktop/dino/ipc1"
fifo = os.open(IPC_FIFO_NAME, os.O_WRONLY)
checkpoint_dir = os.path.dirname(checkpoint_path)
inputs = keras.Input(shape=(12,))
dense = layers.Dense(1000, activation="relu")
x = dense(inputs)
x = layers.Dropout(0.3)(x)
x = layers.Dense(35, activation="relu")(x)
outputs = layers.Dense(len(chords_imp.chords))(x)
model = keras.Model(inputs=inputs, outputs=outputs)
model.load_weights(checkpoint_path)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "Desktop/dino/output.wav"
while True:
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    #print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    #print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    chroma = HPCP.hpcp(WAVE_OUTPUT_FILENAME, norm_frames=False, win_size=4096, hop_size=1024, output='numpy')
    chroma = np.mean(chroma, axis=0)
    chroma /= sum(chroma)
    chroma = chroma.reshape((1,12))
    #print(chroma.shape)
    predictions = model.predict(chroma)
    pred_class = np.argmax(predictions, axis=1)
    #print(pred_class)
    #print("predictions array:", predictions)
    content = f"{pred_class[0]}".encode("utf8")
    msg = create_msg(content)
    os.write(fifo, msg)
os.close(fifo)
