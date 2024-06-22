from app import db 

class Material(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    resource = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    question_id = db.Column(db.String(36), db.ForeignKey('question.id'))

    def __init__(self, resource, created_at, updated_at, question_id):
        self.resource = resource
        self.created_at = created_at
        self.updated_at = updated_at
        self.question_id = question_id