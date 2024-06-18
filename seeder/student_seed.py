from flask_seeder import Seeder, Faker, generator
from src.model.Student import Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class StudentSeed(Seeder): 
    def __init__(self, db=None):
        super().__init__(db)
        self.priority = 1

        # Buat koneksi database manual
        db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/db-recommendation')
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def run(self):
        session = self.Session()
        try:
            faker = Faker(
                cls=Student,
                init={
                    "id": generator.UUID(),
                    "name": generator.Name(),
                    "email": generator.Email(),
                    "password": generator.String("password", 10),
                    "institution": generator.String(100),
                    "code": generator.String(10),
                    "created_at": generator.Date(),
                    "updated_at": generator.Date()
                }
            )
            for student in faker.create(10):
                print("Adding student: %s" % student)
                session.add(student)
            session.commit()
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()

# Pastikan untuk mengeksekusi seeder dalam konteks yang tepat
if __name__ == '__main__':
    seeder = StudentSeed()
    seeder.run()
