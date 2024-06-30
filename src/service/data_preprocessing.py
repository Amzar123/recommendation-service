from mlxtend.preprocessing import TransactionEncoder
import pandas as pd


from src.service.nlg_core import NLGCore


class DataPreProcessing:
    """
    Class for handling data preprocessing
    """

    def __init__(self) -> None:
        self.obj_nlg = NLGCore()

    def recommend_materials(self, student_data, rules, competency_to_material):
        """
        Generate recommendation materials for a single student.
        """
        student_name = student_data["name"]
        competencies = set(student_data["competencies"])
        recommendations = set()

        print(student_data)

        for competency in competencies:
            recommendations.update(competency_to_material.get(competency, []))

            # Mencari rules yang relevan untuk kompetensi saat ini
            # matching_rules = rules[rules['antecedents'].apply(lambda x: competency in x)]

            # for _, rule in matching_rules.iterrows():
            #     consequents = rule['consequents']
            #     for consequent in consequents:
            #         recommendations.update(competency_to_material.get(consequent, []))
        
        # student_recommendations = {student_name:  self.obj_nlg.generate_text(list(recommendations))}
        student_recommendations = {student_name:  list(recommendations)}
        return student_recommendations

    def transform_result_to_biner(self, test_result, questions):
        """
        This function is to transform result to biner data
        """
        question_list = []

        for i in range(len(questions)):
            question_list.append(f"soal {i+1}")
        
        for q in question_list:
            for i in range(len(test_result)):
                if questions["key"][question_list.index(q)] == "":
                    test_result[q][i] = 0
                elif test_result[q][i] == questions["key"][question_list.index(q)]:
                    test_result[q][i] = 1
                else:
                    test_result[q][i] = 0

        return test_result

    def mapping_student_competency(
            self,
            transformed_data,
            df_mapping_question_comp):
        '''
        Implement to map student wrong answers with competencies.
        '''

        # Convert the first column (score) to a separate series and drop it
        # from the DataFrame
        scores = transformed_data.iloc[:, 0]
        student_answers = transformed_data.iloc[:, 1:]

        # Competencies list
        lib = [
            "main_verbs",
            "tense",
            "infinitives",
            "passives",
            "have_+_participle",
            "auxiliary_verbs",
            "pronouns",
            "nouns",
            "determiners",
            "other_adjectives",
            "prepositions",
            "conjunctions",
            "subject_verb_agreement"
        ]

        student_list = []

        for idx, row in student_answers.iterrows():
            student = {"name": f"student_{idx+1}", "competencies": set()}

            for question_index, answer in row.items():
                if answer == 0:  # If the answer is wrong
                    try:
                        # Strip any leading or trailing spaces
                        question_index = question_index.strip()
                        # Extract the question number
                        question_num = int(question_index.split(' ')[-1]) - 1
                        if question_num < len(df_mapping_question_comp):
                            for comp in lib:
                                if df_mapping_question_comp.at[question_num, comp]:
                                    student["competencies"].add(comp)
                    except (ValueError, IndexError) as e:
                        print(
                            f"Skipping invalid question index '{question_index}' for student {idx+1}: {e}")

            # Convert the set to a list for JSON serialization or other
            # processing
            student["competencies"] = list(student["competencies"])
            student_list.append(student)
        return student_list

    def generate_final_dataset(self, mapped_data):
        """
        This function can generate final dataset
        """
        final_dataset = []
        for element in mapped_data:
            final_dataset.append(element['competencies'])
        return final_dataset

    def data_transformation(self, final_dataset):
        """
        This function is to transform data after final data set was generated
        """
        tr = TransactionEncoder()
        tr_ary = tr.fit(final_dataset).transform(final_dataset)
        df_incorrect = pd.DataFrame(tr_ary, columns=tr.columns_)
        return df_incorrect
