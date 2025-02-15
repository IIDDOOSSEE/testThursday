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
    def test_home(self):
        self.title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        ).text

        question = Question.objects.create(question_text="1 + 1 = ?", pub_date=timezone.now())

        Choice.objects.create(question=question, choice_text="1")
        Choice.objects.create(question=question, choice_text="2")
        Choice.objects.create(question=question, choice_text="3")

        # Reload หน้าเว็บหลังจากสร้างคำถาม
        self.driver.refresh()

        self.question = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "poll-link"))
        ).text

        self.assertEqual(self.title, "poll list")
        self.assertEqual(self.question, "1 + 1 = ?")

    def test_poll(self):
        self.title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        ).text

        question = Question.objects.create(question_text="1 + 1 = ?", pub_date=timezone.now())

        Choice.objects.create(question=question, choice_text="1")
        Choice.objects.create(question=question, choice_text="2")
        Choice.objects.create(question=question, choice_text="3")

        # Reload หน้าเว็บหลังจากสร้างคำถาม
        self.driver.refresh()
        
        self.question = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "poll-link"))
        ).text
        # เช็คว่ามีหัวข้อกับคำถามรวมถึงลิงค์ตรงกับหน้าหลักมั้ย

        self.assertEqual(self.title, "poll list")
        self.assertEqual(self.question, "1 + 1 = ?")
        self.question = self.driver.find_element(By.LINK_TEXT,self.question)

        # กดลิงค์คำถามเพื่อไปยังหน้าโหวด
        self.question.click()

        choices = self.driver.find_elements(By.NAME, "choice")
        self.assertEqual(len(choices), 3)  # ✅ ต้องมี 3 ตัวเลือก

        # เช็คว่าข้อความของตัวเลือกถูกต้อง => ดึง label ที่ติดกับ input
        choices_text = [choice.find_element(By.XPATH, "./following-sibling::label").text for choice in choices]
        self.assertListEqual(choices_text, ["1", "2", "3"]) 
        
        # เลือกตัวเลือก "2"
        choices[1].click()

        #  กดปุ่มโหวต
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        # รอหน้า Result โหลด และตรวจสอบผลโหวต
        result_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
        )
        
        # หาข้อความผลโหวตของตัวเลือก "2"
        choice_2_result = next(item.text for item in result_items if "2" in item.text)
        self.assertEqual(choice_2_result, "2 -- 1 vote")
        # time.sleep(2)

      

