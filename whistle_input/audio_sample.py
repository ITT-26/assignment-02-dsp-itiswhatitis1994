import sounddevice as sd
import numpy as np
import pyqtgraph as pg

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024 # Number of audio frames per buffer
RATE = 44100 # Audio sampling rate (HZ)
CHANNELS = 1 # Mono audio

data=[]

# print info about audio devices
print("Available input devices:\n")
devices = sd.query_devices()

input_devices = []
for i, dev in enumerate(devices):
    if dev['max_input_channels'] > 0:
        print(f"{i}: {dev['name']}")
        input_devices.append(i)

# let user select audio device
input_device = int(input("\nSelect input device: "))

# audio callback to safe data
def audio_callback(indata, frames, time, status):
    global data
    if status:
        print(status)

    data = indata[:, 0]  # mono

# open audio input stream
stream = sd.InputStream(
    device=input_device,
    channels=CHANNELS,
    samplerate=RATE,
    blocksize=CHUNK_SIZE,
    callback=audio_callback,
    latency='low'
)

def getFrequency():
    global data

    signal = np.frombuffer(data, dtype=np.int16)

    if signal is None or len(signal) == 0:
        return 0
    
    # Apply window (important for cleaner FFT)
    #window = np.hanning(len(signal))
    #signal = signal * window

    # FFT
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(len(signal), 1 / RATE)

    # Only positive frequencies
    magnitudes = np.abs(yf[:len(yf)//2])
    freqs = xf[:len(xf)//2]

    # Find dominant frequency
    dominant_freq = freqs[np.argmax(magnitudes)]

    if dominant_freq < 50 or dominant_freq > 1000:
        return 0

    #print(dominant_freq)
    return dominant_freq


stream.start()
print("\nStreaming...")