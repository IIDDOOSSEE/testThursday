import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question,Choice


class QuestionModelTests(TestCase):
    # เทสว่า สร้างคำถามแล้วมีคำถามขึ้นหรือป่าว จำนวนถูกต้องมั้ย 
    def test_create_question(self):
        question = Question.objects.create(question_text="What is 2+2?", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 1)  
        self.assertEqual(Question.objects.first().question_text, "What is 2+2?") 

    # เทสว่า ช้อยที่สร้างมาถูกต้องรึป่าว จำนวนถูกมั้ย
    def test_question_has_choices(self):
        question = Question.objects.create(question_text="What is 2+2?", pub_date=timezone.now())
        choice1 = Choice.objects.create(question=question, choice_text="4")
        choice2 = Choice.objects.create(question=question, choice_text="5")

        self.assertEqual(question.choice_set.count(), 2)  
        self.assertIn(choice1, question.choice_set.all())  
        self.assertIn(choice2, question.choice_set.all())  

    # จำลองการโหวต
    def test_vote_increases_count(self):
        question = Question.objects.create(question_text="What is 2+2?", pub_date=timezone.now())
        choice = Choice.objects.create(question=question, choice_text="4",)

        choice.votes += 1
        choice.save()

        self.assertEqual(Choice.objects.get(id=choice.id).votes, 1)  

