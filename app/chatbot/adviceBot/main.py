from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_ADVICE
from langchain_core.output_parsers import StrOutputParser

from app.services.advice_service import AdviceService

class AdviceBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_ADVICE

    async def format_results(self, quiz_records, assignment_records):
        # Initialize result dictionary
        course_results = {}

        # Process quiz records
        for record in quiz_records:
            course_name = record['course_name']
            quiz_name = record['quiz_name']

            # Initialize course if not exists
            if course_name not in course_results:
                course_results[course_name] = {
                    'quizzes': {}
                }

            # Initialize quiz if not exists
            if quiz_name not in course_results[course_name]['quizzes']:
                course_results[course_name]['quizzes'][quiz_name] = {
                    'grade': record['grade'],
                    'questions': []
                }

            # Add question details
            course_results[course_name]['quizzes'][quiz_name]['questions'].append({
                'name': record['question_name'],
                'is_wrong': record['is_wrong'],
                'source': record['source']
            })
        # Process assignment records
        for assignment in assignment_records:
            course_name = assignment['course_name']
            if course_name not in course_results:
                course_results[course_name] = {
                    'quizzes': {},
                    'assignments': []
                }

            course_results[course_name]['assignments'].append({
                'name': assignment['assignment_name'],
                'grade': assignment['grade'],
                'source': assignment['source'],
                'teacher_comment': assignment['teacher_comment']
            })

        return course_results

    def format_quiz_results(self, quiz_records):
        course_results = {}

        for record in quiz_records:
            course_name = record['course_name']
            quiz_name = record['quiz']

            # Initialize course if not exists
            if course_name not in course_results:
                course_results[course_name] = {
                    'quizzes': [],
                    'assignments': []
                }

            # Find existing quiz or create new one
            quiz = next(
                (q for q in course_results[course_name]['quizzes'] if q['quiz_name'] == quiz_name),
                None
            )

            if not quiz:
                quiz = {
                    'quiz_name': quiz_name,
                    'grade': float(record['quiz_grade']),
                    'questions': []
                }
                course_results[course_name]['quizzes'].append(quiz)

            # Only add question if source is not empty
            if record['source']:
                quiz['questions'].append({
                    'source': record['source'],
                    'is_wrong': record['is_wrong']
                })

        return course_results

    async def get_combined_results(self, quiz_records, assignment_records):
        results = self.format_quiz_results(quiz_records)

        # Add assignments
        for assignment in assignment_records:
            course_name = assignment['course_name']

            if course_name not in results:
                results[course_name] = {
                    'quizzes': [],
                    'assignments': []
                }

            results[course_name]['assignments'].append({
                'name': assignment['assignment_name'],
                'grade': float(assignment['grade']),
                'source': assignment['source'],
                'teacher_comment': assignment['teacher_comment']
            })

        return results

    # Result structure:
    # {
    #     "Course A": {
    #         "quizzes": [
    #             {
    #                 "quiz_name": "Quiz 1",
    #                 "grade": 8,
    #                 "questions": [
    #                     {
    #                         "source": "Chuong 1",
    #                         "is_wrong": true
    #                     },
    #                     {
    #                         "source": "Chuong B",
    #                         "is_wrong": false
    #                     }
    #                 ]
    #             }
    #         ],
    #         "assignments": [...]
    #     }
    # }

    async def run(self, message, user_id):
        # get infor of user
        quiz, assignment = await AdviceService.get_advice_information(user_id)
        #
        print("QUIZ: ", quiz)
        print("ASSIGN: ",assignment)

        summary = await self.get_combined_results(quiz, assignment)
        print("SUMMARY: ", summary)
        yield "hahaha"
        chain = self.prompt | self.model_gemini_1_5 | StrOutputParser()
        print("Talk", chain)
        for chunk in chain.stream({"context":summary, "input": message}):
            print("CHUNK INSIDE: ", chunk)
            yield chunk
