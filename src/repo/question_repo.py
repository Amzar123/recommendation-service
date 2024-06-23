from sqlalchemy import text
import uuid


class QuestionRepo:
    """
    This class represents the recommendation repository.
    """

    def __init__(self, db):
        self.db = db

    def create_many(self, data):
        """
        This function is used to insert multiple questions into the database using transactions.
        """
        try:
            with self.db.session.begin():
                # Insert questions
                question_query = text(
                    'INSERT INTO questions (id, question, key_answer, created_at, updated_at) VALUES (:id, :question, :key_answer, NOW(), NOW())')
                print(data)
                questions = [{'id': uuid.uuid4(), 'question': q['question'], 'key_answer': q['key']} for q in data]
                self.db.session.execute(question_query, questions)

                # Insert options
                # option_query = text(
                #     'INSERT INTO options (question_id, option_text) VALUES (:question_id, :option_text)')
                # options = [{'question_id': q['question_id'], 'option_text': o['option_text']} for q in data for o in q['options']]
                # self.db.session.execute(option_query, options)

                # # Insert competencies
                # competency_query = text(
                #     'INSERT INTO competencies (question_id, competency_text) VALUES (:question_id, :competency_text)')
                # competencies = [{'question_id': q['question_id'], 'competency_text': c['competency_text']} for q in data for c in q['competencies']]
                # self.db.session.execute(competency_query, competencies)

            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e

    def row_to_dict(self, row):
        """
        Convert a Row object to a dictionary.
        """
        if row is None:
            return None
        return dict(row._asdict())
