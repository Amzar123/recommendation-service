from src.repo.question_repo import QuestionRepo

class QuestionService:
    def __init__(self, question_repository: QuestionRepo):
        self.question_repository = question_repository

    # def get_questions(self, user_id: int):
    #     return self.question_repository.get_questions(user_id)
    
    def create_question(self, data: list):
        return self.question_repository.create_many(data)