from django.utils import timezone
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Changed from LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from mypoll.models import Choice,Question
import time

class pollApp(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)


        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)
    def tearDown(self):
        self.driver.quit()
    # def test_home(self):
    #     self.title = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "title"))
    #     ).text

    #     question = Question.objects.create(question_text="1 + 1 = ?", pub_date=timezone.now())

    #     Choice.objects.create(question=question, choice_text="1")
    #     Choice.objects.create(question=question, choice_text="2")
    #     Choice.objects.create(question=question, choice_text="3")

    #     # Reload หน้าเว็บหลังจากสร้างคำถาม
    #     self.driver.refresh()

    #     self.question = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "poll-link"))
    #     ).text

    #     self.assertEqual(self.title, "poll list")
    #     self.assertEqual(self.question, "1 + 1 = ?")

    # def test_poll(self):
    #     self.title = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "title"))
    #     ).text

    #     question = Question.objects.create(question_text="1 + 1 = ?", pub_date=timezone.now())

    #     Choice.objects.create(question=question, choice_text="1")
    #     Choice.objects.create(question=question, choice_text="2")
    #     Choice.objects.create(question=question, choice_text="3")

    #     self.driver.refresh()
        
    #     self.question = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "poll-link"))
    #     ).text

    #     self.assertEqual(self.title, "poll list")
    #     self.assertEqual(self.question, "1 + 1 = ?")
    #     self.question = self.driver.find_element(By.LINK_TEXT,self.question)

    #     self.question.click()

    #     choices = self.driver.find_elements(By.NAME, "choice")
    #     self.assertEqual(len(choices), 3)  

    #     choices_text = [choice.find_element(By.XPATH, "./following-sibling::label").text for choice in choices]
    #     self.assertListEqual(choices_text, ["1", "2", "3"]) 
        
    #     choices[1].click()

    #     submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    #     submit_button.click()

    #     result_items = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
    #     )
        
    #     choice_2_result = next(item.text for item in result_items if "2" in item.text)
    #     self.assertEqual(choice_2_result, "2 -- 1 vote")
    
    def test_warm_hot_display(self):
        question1 = Question.objects.create(question_text="What is 2+2?", pub_date=timezone.now())
        choice1 = Choice.objects.create(question=question1, choice_text="3")
        choice2 = Choice.objects.create(question=question1, choice_text="4")

        choice1.votes = 15  
        choice2.votes = 5  
        choice1.save()
        choice2.save()

        question2 = Question.objects.create(question_text="What's your favorite colour ?", pub_date=timezone.now())
        choice3 = Choice.objects.create(question=question2, choice_text="blue")
        choice4 = Choice.objects.create(question=question2, choice_text="green")

        choice3.votes = 25  
        choice4.votes = 30  
        choice3.save()
        choice4.save()
        url = self.live_server_url + '/warmhot'

        self.driver.get(url)
        time.sleep(2)
        warm_questions = WebDriverWait(self.driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'warm_question'))
        )
        hot_questions = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'hot_question'))
        )
        warm_question_text = [question.text for question in warm_questions]
        hot_question_text = [question.text for question in hot_questions]
        self.assertIn("What is 2+2?", warm_question_text[0])  
        self.assertIn("What's your favorite colour ?", hot_question_text[0])   

        self.assertEqual(len(warm_questions), 1)
        self.assertEqual(len(hot_questions), 1)
      

