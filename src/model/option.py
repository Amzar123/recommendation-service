from app import db 

class Options(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.String, primary_key=True)
    option = db.Column(db.String(50))
    question_id = db.Column(db.String, db.ForeignKey('questions.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, option, question_id, created_at, updated_at):
        self.option = option
        self.question_id = question_id
        self.created_at = created_at
        self.updated_at = updated_at