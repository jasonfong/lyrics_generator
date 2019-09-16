from random import random

from models.line import Line


class LyricsGenerator:
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
            'chorus': self.get_chorus(),
            'pre-chorus': self.get_pre_chorus(),
            'verse': self.get_verse(),
            'bridge': self.get_bridge(),
        }
