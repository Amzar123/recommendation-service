from app import db 

class Competencies:
    __tablename__ = 'competencies'

    id = db.Column(db.String(36), primary_key=True)
    competency = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'))

    def __init__(self, competency, created_at, updated_at, question_id):
        self.competency = competency
        self.created_at = created_at
        self.updated_at = updated_at
        self.question_id = question_id