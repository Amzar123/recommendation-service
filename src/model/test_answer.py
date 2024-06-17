from app import db 

class Answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.String, primary_key=True)
    answer = db.Column(db.String(225))
    assessment_id = db.Column(db.String, db.ForeignKey('assessments.id'))
    is_correct = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, question_id, answer, assessment_id, is_correct, created_at, updated_at):
        self.question_id = question_id
        self.answer = answer
        self.is_correct = is_correct
        self.assessment_id = assessment_id
        self.created_at = created_at
        self.updated_at = updated_at