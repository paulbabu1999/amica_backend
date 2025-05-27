import whisper
import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(duration=5, filename="input.wav"):
    recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, 16000, recording)
    return filename

def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]
