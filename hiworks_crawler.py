
import datetime
import time
from io import StringIO
from itertools import islice
import tracemalloc
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import difflib
from dotenv import load_dotenv
import os
import json
import ast

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 숨기는 옵션

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def sorted_employee_with_position(input_names):
    
    employee = os.environ.get("employee")
    name_priority = os.environ.get('name_priority')
    
    name_priority_dic= json.loads(name_priority)
    employee_dic = json.loads(employee)
   

    sorted_employee = sorted(input_names, key=lambda x: name_priority_dic[x])
    sorted_employee_with_position = [employee_dic[name] for name in sorted_employee]

    return sorted_employee_with_position
    




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

def is_weekend(date_str):
    date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    
    if date_object.weekday() in [5, 6]:  
        return True
    else:
        return False
    
def classify_day_night(time_value, day_start_hour=6, night_start_hour=24):
    if isinstance(time_value, str):
        time_value = datetime.datetime.strptime(time_value, '%H:%M')
    
    hour = time_value.hour
    
    if day_start_hour <= hour < night_start_hour:
        return '주간'
    else:
        return '야간'    
    

def convert_to_24hr_format(time_str):
    parts = time_str.split()
    
    if(parts[0]=='오전') :
        time_24hr_str = parts[1]

    elif (parts[0]=='오후') :
          time_24hr_str = str(int(parts[1].split(":")[0]) + 12) + ":"+parts[1].split(":")[1]
    
    return time_24hr_str


def extract_date_and_time_range(input_str):
    parts = input_str.split()

    # 날짜 추출
    date_result = parts[0]
    result_str = input_str.replace(date_result, '')
 
    # 시간 범위 추출
    if len(result_str)>2 :
        time_range_parts = result_str.split('~')
        start_time = time_range_parts[0]  
        end_time = time_range_parts[1]    

        start_time_result =convert_to_24hr_format(start_time)
        end_time_result =convert_to_24hr_format(end_time)

        return date_result, start_time_result, end_time_result
    else :
        return date_result,None,None


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

def extract_region(input_str,candidate):
    result = find_most_similar(input_str,candidate)
    return result
def extract_employee(input_str,candidate):
    result = find_most_similar(input_str,candidate)
    return result

def extract_customer(input_str,candidate):
    result = find_most_similar(input_str,candidate)
    return result

def get_employees(employee,content):
    result_employees=[]   
    for emp in employee:
        if emp in content:
            result_employees.append(emp)
    return result_employees
    
def hiworks_crawler(username, password):
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
           
            if scheduleTime_element.text.strip():
                schedule_date, start_time, end_time = extract_date_and_time_range(scheduleTime_element.text )
                if len(scheduleTime_element.text .split()) > 1 :
                    schedule_date, start_time, end_time = extract_date_and_time_range(scheduleTime_element.text )
                    workTime=start_time + "~" + end_time
                    if is_weekend(schedule_date) :
                        shift="주말"
                    else :
                        shift= classify_day_night(end_time)

                else :
                        workTime="" 
                
            subject_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="__subject"]')))
            if subject_element.text.strip():
                subject = subject_element.text 
                
            scheduleRegidate_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_regidate')))        
            if scheduleRegidate_element.text.strip():
                schedule_regidate = scheduleRegidate_element.text 
     
            contents_element = wait.until(  EC.presence_of_element_located((By.XPATH, '//div[@id="__contents"]')))
            if contents_element.text.strip():
                contents = contents_element.text 
                employees = get_employees(contents)
            if(cal_name=="근태" or "검진"  in subject or "연차"  in subject  or "휴가" in subject ):
                pass
            else :
                data.append({
                'cal_name': cal_name,
                'schedule_date': schedule_date,
                'schedule_time': workTime,
                'shift' : shift,
                'subject': subject,
                # 'customer':customer,
                # 'region' : region,
                'schedule_regidate': schedule_regidate,
                'contents': contents
                })

        try :        
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')
            element.click() 
        except:
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')
            element.click() 
    

    df = pd.DataFrame(data)

    sorted_names=sorted_employee()
    # # SE 칼럼 추가
    for i, name in enumerate(sorted_names, start=1):
        df[f'SE{i}'] = [name]

    YearMonth = YearMonth.replace(".","-")
    df = df[df['schedule_date'].str.contains(YearMonth)]
    
    # df['schedule_time'] = pd.to_datetime(df['schedule_time'], errors='coerce')
 
    # df['shift'] = df['schedule_time'].dt.date
   
    
    print(df)
    # df['shift ']
    # df_sorted = df.sort_values(by='schedule_time', ascending=True)

if __name__ == "__main__":
    id = os.environ.get('id')
    password = os.environ.get('password')
    
    hiworks_crawler(id, password)