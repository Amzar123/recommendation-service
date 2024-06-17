from app import db 

class Assesment(db.Model):
    __tablename__ = 'assesments'

    id = db.Column(db.String, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id'))
    teacher_id = db.Column(db.String, db.ForeignKey('teachers.id'))
    recommendation = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, student_id, teacher_id, recommendation, created_at, updated_at):
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.recommendation = recommendation
        self.created_at = created_at
        self.updated_at = updated_at