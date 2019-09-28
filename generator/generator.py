from random import random

from models.line import Line


class LyricsGenerator:
    song_template = '{verse}\n\n{pre_chorus}\n\n{chorus}\n\n{pre_chorus}\n\n{chorus}\n\n{bridge}'


    def __init__(self):
        pass


    def get_chorus(self):
        return Line.get_random('chorus')


    def get_pre_chorus(self):
        return Line.get_random('pre-chorus')


    def get_verse(self):
        return Line.get_random('verse')


    def get_bridge(self):
        return Line.get_random('bridge')


    def generate(self):
        return {
            'chorus': self.get_chorus() or Line(),
            'pre-chorus': self.get_pre_chorus() or Line(),
            'verse': self.get_verse() or Line(),
            'bridge': self.get_bridge() or Line(),
        }

    
    def generate_string(self):
        generated = self.generate()

        result = self.song_template.format(
            pre_chorus=generated['pre-chorus'].text,
            chorus=generated['chorus'].text,
            verse=generated['verse'].text,
            bridge=generated['bridge'].text,
        )

        return result
