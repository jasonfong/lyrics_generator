import uuid

from google.cloud import firestore


class Line:
    collection_name = 'lines'
    line_type_choices = ['any', 'chorus', 'verse', 'bridge']
    social_type_choices = ['instagram', 'facebook', 'twitter']

    def __init__(self, text=None, line_type=None, social_type=None, social_id=None):
        self.db = firestore.Client()
        self.id = str(uuid.uuid4())
        self.text = text
        self.line_type = line_type
        self.social_type = social_type
        self.social_id = social_id

    
    @classmethod
    def get_all(cls):
        db = firestore.Client()
        return [
            item.to_dict()
            for item in db.collection(cls.collection_name).stream()
        ]


    def save(self):
        doc_ref = self.db.collection(self.collection_name).document(self.id)
        doc_ref.set({
            'id': self.id,
            'text': self.text,
            'line_type': self.line_type,
            'social_type': self.social_type,
            'social_id': self.social_id,
        })
