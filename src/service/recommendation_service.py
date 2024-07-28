"""
Import required dependencies
"""
from src.service.data_preprocessing import DataPreProcessing
from src.repo.recommendation_repo import RecommendationRepo
from src.repo.student_repo import StudentRepo
from flask import jsonify
from multiprocessing import Pool 

from mlxtend.frequent_patterns import fpgrowth, association_rules

from src.service.apriori import Apriori

import pandas as pd

class RecommendationService:
    """
    This class is for serve recommendation
    """

    def __init__(
            self,
            recommendation_repo: RecommendationRepo,
            student_repo: StudentRepo):
        self.recommendation_repo = recommendation_repo
        self.student_repo = student_repo

    def get_recommendations(self, ids: list):
        """
        Function to handle get recommendation
        """
        result = self.recommendation_repo.get_recommendations(ids)
        return result

    def generate_recommendations(self, ids: list):
        """
        Function to handle generate recommendation
        """
        try:
            # Create object for data preprocessing
            data_preprocessing = DataPreProcessing()

            # create object apriori 
            apriori = Apriori()

            # read data from csv file
            df_mapping_question_comp = pd.read_csv("./data/mapping-assessment-question-competency.csv")
            df_questions = pd.read_csv("./data/assessment-questions.csv")
            df_test_results = pd.read_csv("./data/assessment-result.csv")

            # Data preprocessing
            transformed_data = data_preprocessing.transform_result_to_biner(df_test_results, df_questions)
        
            student_comp = data_preprocessing.mapping_student_competency(transformed_data, df_mapping_question_comp)
            
            final_dataset = data_preprocessing.generate_final_dataset(student_comp)
            
            transform_dataset = data_preprocessing.data_transformation(final_dataset)

            # Data modelling
            items = apriori.apriori(transform_dataset, 0.97, use_colnames=True)

            # Building association rules
            rules = association_rules(items, metric="confidence", min_threshold=0.97)

            # Define the mapping of competencies to materials
            competency_to_material = {
                "main_verbs": [
                    "Penggunaan kata kerja utama dalam kalimat",
                    "Perbedaan antara kata kerja aksi dan kata kerja statis",
                    "Bentuk kata kerja dalam tenses berbeda"],
                "tense":  [
                    "Simple dan Present Continuous",
                    "Past Simple dan Past Continuous",
                    "Future Simple dan Future Continuous",
                    "Present Perfect dan Past Perfect",
                    "Penggunaan tenses dalam konteks berbeda"],
                "infinitives": [
                    "Penggunaan infinitive (to + verb) dalam kalimat",
                    "Infinitive dengan dan tanpa 'to'",
                    "Penggunaan infinitive setelah kata kerja tertentu"],
                "passives": [
                    "Struktur kalimat pasif",
                    "Perubahan dari kalimat aktif ke pasif",
                    "Penggunaan pasif dalam berbagai tenses"],
                "have_+_participle": [
                    "Penggunaan Present Perfect Tense",
                    "Struktur kalimat Present Perfect",
                    "Penggunaan Past Perfect Tense"],
                "auxiliary_verbs": [
                    "Penggunaan kata kerja bantu (do, does, did)",
                    "Penggunaan modal verbs (can, could, may, might, must, etc.)",
                    "Bentuk negatif dan pertanyaan menggunakan kata kerja bantu"],
                "pronouns": [
                    "Penggunaan pronoun subjek (I, you, he, she, it, we, they)",
                    "Penggunaan pronoun objek (me, you, him, her, it, us, them)",
                    "Penggunaan possessive pronouns (my, your, his, her, its, our, their)"],
                "nouns": [
                    "Penggunaan kata benda dalam kalimat",
                    "Singular dan plural nouns",
                    "Countable dan uncountable nouns"],
                "determiners": [
                    "Penggunaan determiners (a, an, the)",
                    "Penggunaan quantifiers (some, any, few, many, etc.)",
                    "Penggunaan demonstrative determiners (this, that, these, those)"],
                "other_adjectives": [
                    "Penggunaan adjective dalam kalimat",
                    "Perbandingan adjective (comparative dan superlative)",
                    "Penggunaan adjective dalam berbagai posisi dalam kalimat"],
                "prepositions": [
                    "Penggunaan prepositions of place (in, on, at, etc.)",
                    "Penggunaan prepositions of time (in, on, at, etc.)",
                    "Prepositions setelah kata kerja tertentu (depend on, listen to, etc.)"],
                "conjunctions": [
                    "Penggunaan coordinating conjunctions (and, but, or, etc.)",
                    "Penggunaan subordinating conjunctions (because, although, if, etc.)",
                    "Penggunaan correlative conjunctions (either...or, neither...nor, etc.)"],
                "subject_verb_agreement": [
                    "Kesepakatan antara subjek dan kata kerja",
                    "Penggunaan kata kerja dengan subjek tunggal dan jamak",
                    "Kesepakatan dalam kalimat kompleks"]
            }

            try:
                with Pool(processes=4) as pool:
                    # Map the recommend_materials function to the list of students
                    results = pool.starmap(
                        data_preprocessing.recommend_materials, 
                        [(student, rules, competency_to_material) for student in student_comp]
                    )

                # Combine the results into a single dictionary
                student_recommendations = {k: v for d in results for k, v in d.items()}
                return student_recommendations

            except Exception as e:
                # app.logger.error(f"An error occurred during parallel processing: {str(e)}")
                return str(e), 500

        except Exception as e:
            # app.logger.error(f"An error occurred: {str(e)}")
            return ("An error occurred: {str(e)}"), 500
