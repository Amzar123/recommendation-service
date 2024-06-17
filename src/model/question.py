from app import db 

class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.String, primary_key=True)
    question = db.Column(db.String(50))
    key_answer = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, question, key_answer, created_at, updated_at):
        self.question = question
        self.key_answer = key_answer
        self.created_at = created_at
        self.updated_at = updated_at