from app import db

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(db.Model):
        __tablename__ = 'students'

        id = db.Column(db.String, primary_key=True)
        name = db.Column(db.String(50))
        email = db.Column(db.String(50))
        password = db.Column(db.String(50))
        institution = db.Column(db.String(50))
        code = db.Column(db.String(50))
        created_at = db.Column(db.DateTime)
        updated_at = db.Column(db.DateTime)

        def __init__(
                self,
                name,
                email,
                password,
                code,
                institution,
                created_at,
                updated_at):
            self.name = name
            self.email = email
            self.password = password
            self.institution = institution
            self.code = code
            self.created_at = created_at
            self.updated_at = updated_at