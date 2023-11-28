import os
from pydub import AudioSegment

class ConverterAudio:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def convert_to_wav(self):
        sound = AudioSegment.from_file(self.src)
        sound.export(self.dst, format="wav")