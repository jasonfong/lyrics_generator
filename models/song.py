from datetime import datetime
import hashlib
import uuid

from google.cloud import firestore


SONG_TEMPLATE = '{verse}\n\n{pre_chorus}\n\n{chorus}\n\n{pre_chorus}\n\n{chorus}\n\n{bridge}'


class Song:
    collection_name = 'songs'
    
    def __init__(self, id, chorus_id=None, pre_chorus_id=None, verse_id=None,
                 bridge_id=None, created=None, modified=None):
        now = datetime.utcnow()
        self.db = firestore.Client()
        self.id = id
        self.chorus_id = chorus_id
        self.pre_chorus_id = pre_chorus_id
        self.verse_id = verse_id
        self.bridge_id = bridge_id
        self.created = created or now
        self.modified = modified or now


    @classmethod
    def get_id(cls, chorus, pre_chorus, verse, bridge):
        id_base = f'{chorus}|{pre_chorus}|{verse}|{bridge}'
        hasher = hashlib.sha1()
        hasher.update(id_base.encode('utf8'))
        song_id = hasher.hexdigest()[:7]
        return song_id


    @classmethod
    def get(cls, song_id):
        db = firestore.Client()
        results = [
            item
            for item in db.collection(cls.collection_name).where('id', '==', song_id).stream()
        ]
        if results:
            return cls(song_id).populate(**(results[0].to_dict()))
        else:
            return None


    @classmethod
    def get_all(cls):
        db = firestore.Client()
        return [
            cls(item.id).populate(**item.to_dict())
            for item in db.collection(cls.collection_name).stream()
        ]


    def populate(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
        return self


    def save(self):
        doc_ref = self.db.collection(self.collection_name).document(self.id)
        doc_ref.set({
            'id': self.id,
            'chorus_id': self.chorus_id,
            'pre_chorus_id': self.pre_chorus_id,
            'verse_id': self.verse_id,
            'bridge_id': self.bridge_id,
            'created': self.created,
            'modified': datetime.utcnow(),
        })
