from random import random

from models.line import Line
from models.song import Song


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
        chorus = self.get_chorus() or Line()
        pre_chorus = self.get_pre_chorus() or Line()
        verse = self.get_verse() or Line()
        bridge = self.get_bridge() or Line()

        song_id = Song.get_id(chorus, pre_chorus, verse, bridge)

        existing_song = Song.get(song_id)

        if existing_song:
            return existing_song

        song = Song(
            id=song_id,
            chorus_id=chorus.id,
            pre_chorus_id=pre_chorus.id,
            verse_id=verse.id,
            bridge_id=bridge.id,
        )
        song.save()

        return song
