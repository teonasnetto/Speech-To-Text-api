import os
import speech_recognition as sr

class ReconhecerVoz:
    def __init__(self, src):
        self.src = src

    def reconhecer(self):
        r = sr.Recognizer()
        audio_file = sr.AudioFile(self.src)
        with audio_file as source:
            audio = r.record(source)

        return r.recognize_google(audio, language='pt-BR')