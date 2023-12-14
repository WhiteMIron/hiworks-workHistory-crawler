from io import StringIO
from itertools import islice
import tracemalloc
import pandas as pd
from sqlalchemy import create_engine, inspect,text
import requests
from tqdm import tqdm
from concurrent.futures import as_completed
import requests
import json

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
import time
import difflib
from dotenv import load_dotenv
import os 

load_dotenv()
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 숨기는 옵션

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


employee=['김지연','이준태','조성희','백민철','고수비','최진호']


def find_most_similar(original, candidates):
    similarity_scores = []

    for candidate in candidates:
        # SequenceMatcher를 사용하여 유사도 측정
        matcher = difflib.SequenceMatcher(None, original, candidate)
        similarity_score = matcher.ratio()

        # 유사도 점수 저장
        similarity_scores.append((candidate, similarity_score))

    # 유사도가 높은 순서대로 정렬
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # 가장 유사도가 높은 값 반환
    most_similar = similarity_scores[0][0]
    return most_similar



def crawler(username,password):
    login_url = "https://login.office.hiworks.com/ostech.co.kr"

    driver.get(login_url)
    
    id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="로그인 ID"]'))
    )

    id_input.send_keys(username)
    
 
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > main > div > div:nth-child(1) > form > fieldset > button'))
    )

    element.click()
    
    password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > main > div > div:nth-child(1) > form > fieldset > button'))
    )
    element.click()
    
    
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#contents > div.header-wrapper > div > div > div > div:nth-child(4) > a'))
    )
    element.click()
    
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div.fc-view-container > div > table > tbody > tr > td > div > div > div:nth-child(1) > div.fc-content-skeleton > table > thead > tr > td.fc-day-number.fc-fri.fc-past'))
    )
   
   
    elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-event-container')))
  

    data=[]    

    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div.fc-toolbar > div.fc-center > h2'))
    )
    print(element.text)
    YearMonth = element.text
    
    for element in tqdm(elements, desc="Processing elements", unit="element"):
        element.click() 
        time.sleep(1)
      

        
        wait = WebDriverWait(driver, 10)
        calName_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.fl#__cal_name')))        
        cal_name=''
        schedule_time=''
        subject=''
        schedule_regidate=''
        contents=''
        if calName_element.text.strip():
            cal_name = calName_element.text 

            scheduleTime_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_time')))        
            if element.text.strip():
                schedule_time = scheduleTime_element.text 
                
            subject_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="__subject"]')))
            if subject_element.text.strip():
                subject = subject_element.text 
                
            scheduleRegidate_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_regidate')))        
            if scheduleRegidate_element.text.strip():
                schedule_regidate = scheduleRegidate_element.text 
     
            contents_element = wait.until(  EC.presence_of_element_located((By.XPATH, '//div[@id="__contents"]')))
            if contents_element.text.strip():
                contents = contents_element.text 

            if(cal_name!="근태"):
                data.append({
                'cal_name': cal_name,
                'schedule_time': schedule_time,
                'subject': subject,
                'schedule_regidate': schedule_regidate,
                'contents': contents
                })
        #__schedule_time

        try :        
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')
            element.click() 
        except:
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')
            element.click() 
    

    df = pd.DataFrame(data)
    YearMonth = element.text
    YearMonth = element.text.replace(".","-")
    
    print(YearMonth)
    df = df[df['schedule_time'].str.contains(YearMonth)]
    print(df)

if __name__ == "__main__":
    id = os.environ.get('id')
    password = os.environ.get('password')
    employee = os.environ.get('employee')
    employee_list = eval(employee)
    
    crawler(id,password)
