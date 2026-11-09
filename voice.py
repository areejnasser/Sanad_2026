"""Arabic voice: record a question, transcribe it, and speak the answer."""
import os
import tempfile

SAMPLE_RATE = 16000
_stt_model = None


def record(seconds=4, path=None):
    import sounddevice as sd
    import soundfile as sf
    path = path or os.path.join(tempfile.gettempdir(), "sanad_question.wav")
    print("... تكلم الآن")
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    sf.write(path, audio, SAMPLE_RATE)
    return path


def transcribe(path, model_size="small"):
    """Speech-to-text with faster-whisper, forced to Arabic."""
    global _stt_model
    if _stt_model is None:
        from faster_whisper import WhisperModel
        _stt_model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = _stt_model.transcribe(path, language="ar", beam_size=5)
    return "".join(s.text for s in segments).strip()


def speak(text):
    """Text-to-speech with gTTS (needs internet) played through pygame."""
    from gtts import gTTS
    import pygame, time
    path = os.path.join(tempfile.gettempdir(), "sanad_answer.mp3")
    gTTS(text, lang="ar", slow=True).save(path)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
