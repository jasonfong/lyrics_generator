from datetime import datetime
import uuid

from google.cloud import firestore


class Line:
    collection_name = 'lines'
    line_type_choices = ['chorus', 'pre-chorus', 'verse', 'bridge']
    social_type_choices = ['instagram', 'twitter']
    status_choices = ['accepted', 'rejected', 'pending']


    def __init__(self, id=None, text=None, line_type=None, social_type=None,
                 social_id=None, status='pending', created=None, modified=None):
        now = datetime.utcnow()
        self.db = firestore.Client()
        self.id = id or str(uuid.uuid4())
        self.text = text
        self.line_type = line_type
        self.social_type = social_type
        self.social_id = social_id
        self.status = status
        self.created = created or now
        self.modified = modified or now


    @classmethod
    def get(cls, line_id):
        db = firestore.Client()
        results = [
            item
            for item in db.collection(cls.collection_name).where('id', '==', line_id).stream()
        ]
        if results:
            return cls().populate(**(results[0].to_dict()))
        else:
            return None


    @classmethod
    def get_all(cls):
        db = firestore.Client()
        return [
            cls().populate(**item.to_dict())
            for item in db.collection(cls.collection_name).stream()
        ]

    
    @classmethod
    def get_unapproved(cls):
        db = firestore.Client()
        return [
            cls().populate(**item.to_dict())
            for item in db.collection(cls.collection_name).where('status', '==', 'pending').stream()
        ]

    
    @classmethod
    def get_random(cls, line_type):
        db = firestore.Client()
        random_id = str(uuid.uuid4())

        result = None

        qry = db.collection(cls.collection_name)
        qry = qry.where('line_type', '==', line_type)
        qry = qry.where('id', '>=', random_id)

        for item in qry.stream():
            result = cls().populate(**item.to_dict())
            break

        if not result:
            qry = db.collection(cls.collection_name).where('id', '<', random_id)

            for item in qry.stream():
                result = cls().populate(**item.to_dict())
                break

        return result

    
    def populate(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
        return self


    def save(self):
        doc_ref = self.db.collection(self.collection_name).document(self.id)
        doc_ref.set({
            'id': self.id,
            'text': self.text,
            'line_type': self.line_type,
            'social_type': self.social_type,
            'social_id': self.social_id,
            'status': self.status,
            'created': self.created,
            'modified': datetime.utcnow(),
        })
