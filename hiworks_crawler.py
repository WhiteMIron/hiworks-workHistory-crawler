
import ast
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

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 숨기는 옵션

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()



def get_env_dic(input_str):
    str = os.environ.get(input_str)
    return json.loads(str)

def get_env_arr(input_str):
    str = os.environ.get(input_str)
    return ast.literal_eval(str)

EMPLOYEES_DIC = get_env_dic("EMPLOYEES")
NAME_PRIORITY_DIC=get_env_dic("NAME_PRIORITY")
REGION_CANDIDATE =get_env_arr('REGION_CANDIDATE')
REGION_CANDIDATE_WEIGHTS_DIC =get_env_dic('REGION_CANDIDATE_WEIGHTS')
CUSTOMER_CANDIDATE = get_env_arr('CUSTOMER_CANDIDATE')
NAME_PRIORITY_DIC = get_env_dic('NAME_PRIORITY')
NOT_WORK_CONTENT = get_env_arr('NOT_WORK_CONTENT')

# def sorted_employee_with_position(input_names):
def sorted_employees(input_names):

    sorted_employees = sorted(input_names, key=lambda x: NAME_PRIORITY_DIC[x])
    # sorted_employee_with_position = [EMPLOYEES_DIC[name] for name in sorted_employee]

    # return sorted_employee_with_position
    return sorted_employees 




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

def get_am_pm(time_str):
    parts = time_str.split()

    if(parts[0]=='오전') :
        return 'am'

    elif(parts[0]=='오후') :
        return 'pm'

    else :
        return None

    

def convert_to_24hr_format(time_str):
    parts = time_str.split()
    
    if(parts[0]=='오전') :
        time_24hr_str = parts[1]

    elif (parts[0]=='오후') :
          time_24hr_str = str(int(parts[1].split(":")[0]) + 12) + ":"+parts[1].split(":")[1]
    
    return time_24hr_str


# def extract_date_and_time_range(input_str):
#     parts = input_str.split()

#     # 날짜 추출
#     date_result = parts[0]
#     result_str = input_str.replace(date_result, '')
 
#     # 시간 범위 추출
#     if len(result_str)>2 :
#         time_range_parts = result_str.split('~')
#         start_time = time_range_parts[0]  
#         end_time = time_range_parts[1]    

#         start_time_result =convert_to_24hr_format(start_time)
#         end_time_result =convert_to_24hr_format(end_time)

#         return date_result, start_time_result, end_time_result
#     else :
#         return date_result,None,None


def extract_date_and_time_range(input_time_str) :
    date_start_str, end_date_str = input_time_str.split("~")

    # 날짜와 시간 정보 추출
    start_date_info = date_start_str.strip().split(" ")

    end_date_info = end_date_str.strip().split(" ")
    start_date = datetime.strptime(start_date_info[0], "%Y-%m-%d").date()
    start_date_info.pop(0)
    start_date_time = ' '.join(start_date_info)
    start_time = start_date_time
    start_time_result =convert_to_24hr_format(start_time)
       
    if len(end_date_info) == 3 : 
        end_date = datetime.strptime(end_date_info[0], "%Y-%m-%d").date()
        end_date_info.pop(0)
        end_date_time = ' '.join(end_date_info)

        end_time = end_date_time
        end_time_result =convert_to_24hr_format(end_time)

    elif len(end_date_info) ==2 :

        end_date_time = ' '.join(end_date_info)
        end_time = end_date_time
        end_time_result =convert_to_24hr_format(end_time)

        if start_time_result > end_time_result:
            end_date = start_date + timedelta(days=1)
        else:
            end_date = start_date

    return start_date, end_date, start_time_result, end_time_result
  




def find_most_similar(original, candidates, weights=None):
    if weights is None:
        # 가중치가 제공되지 않으면 모든 후보에 대해 동일한 가중치를 사용합니다.
        weights = {candidate: 1 for candidate in candidates}

    similarity_scores = []

    for candidate in candidates:
        # SequenceMatcher를 사용하여 유사도 측정
        matcher = difflib.SequenceMatcher(None, original, candidate)
        similarity_score = matcher.ratio()


        # 가중치 적용
        weighted_similarity = similarity_score * weights[candidate]

        # 유사도 점수 저장
        similarity_scores.append((candidate, weighted_similarity))

    # 가장 유사도가 높은 순서대로 정렬
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # 가장 유사도가 높은 값들 반환 (동일한 최고 유사도를 갖는 모든 후보 반환)
    most_similar_candidates = [candidate for candidate, _ in similarity_scores if _ == similarity_scores[0][1]]
    most_similar_candidates_str = ', '.join(most_similar_candidates)
    return most_similar_candidates_str



def extract_region(input_str,candidate,weights):
    result = find_most_similar(input_str,candidate,weights)
    return result


def extract_customer(input_str,candidate):
    result = find_most_similar(input_str,candidate)
    return result

def get_employees(employees,content):
    result_employees=[]
    for employee in employees:
        if employee in content:
            result_employees.append(employee)
    return result_employees

def extract_workContent(content,notCandidate):
    workContent=content
    for word in notCandidate:
       workContent = workContent.replace(word, '')

    return workContent.lstrip()

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
            if(cal_name=="근태" or "검진"  in subject or "연차"  in subject  or "휴가" in subject ):
                pass
                scheduleTime_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_time')))   
            
                if scheduleTime_element.text.strip():
                    start_date,end_date, start_time, end_time = extract_date_and_time_range(scheduleTime_element.text )
                    if len(scheduleTime_element.text.split()) > 1 :
                        # schedule_date, start_time, end_time = extract_date_and_time_range(scheduleTime_element.text )
                        workTime=start_time + "~" + end_time
                        if is_weekend(start_date) :
                            shift="주말"
                        else :
                            shift= classify_day_night(end_time)

                    else :
                            workTime="" 
                    
                subject_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="__subject"]')))
                if subject_element.text.strip():
                    subject = subject_element.text 
                    customer =extract_customer(subject,CUSTOMER_CANDIDATE)
                    region = extract_region(subject,REGION_CANDIDATE,REGION_CANDIDATE_WEIGHTS_DIC)
                scheduleRegidate_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_regidate')))        
                if scheduleRegidate_element.text.strip():
                    schedule_regidate = scheduleRegidate_element.text 
        
                contents_element = wait.until(  EC.presence_of_element_located((By.XPATH, '//div[@id="__contents"]')))
                if contents_element.text.strip():
                    contents = contents_element.text 
                    employees = get_employees(EMPLOYEES_DIC,contents)
                    # sorted_employees = sorted_employee_with_position(employees)
                    sorted_employees_result = sorted_employees(employees)
                
                    workContent = extract_workContent(contents,NOT_WORK_CONTENT)
           
            # if(cal_name=="근태" or "검진"  in subject or "연차"  in subject  or "휴가" in subject ):
            #     pass
            else :

                data.append({
                # 'cal_name': cal_name,
                # 'schedule_date': schedule_date,
                # 'schedule_time': workTime,
                # 'shift' : shift,
                # 'subject': subject,
                # 'employees':sorted_employees_result,
                # 'customer':customer,
                # 'region' : region,
                # 'schedule_regidate': schedule_regidate,
                # 'work':workContent
                '시작일': start_date,
                '종료일': end_date,
                '서비스종류':'',
                '고객사명':customer,
                '지역/장소' : region,
                '영업':"",
                'Vendor':"",
                "Model":"",
                "작업내역":"",
                "old_part":"",
                "new_part":"",
                "유형1":"",
                "유형2":"",
                "구분1":"",
                "구분2":"",
                '주/야/주말구분' : shift,
                'employees':sorted_employees_result,
                '비고(장애발생내역, 상세지원내역 등)':workContent
                

                })

        try :        
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')
            element.click() 
        except:
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')
            element.click() 
    

    df = pd.DataFrame(data)
    YearMonth = YearMonth.replace(".","-")
    df = df[df['schedule_date'].str.contains(YearMonth)]
    


    # df['schedule_time'] = pd.to_datetime(df['schedule_time'], errors='coerce')
    # df['shift'] = df['schedule_time'].dt.date

    for i, (worker,name_with_position) in enumerate(EMPLOYEES_DIC.items()):
        df[f'SE{i + 1}'] = df['employees'].apply(lambda x: name_with_position if worker in x and worker != '' else None)


    pd.set_option('display.max_rows', None)  # 모든 행 표시
    pd.set_option('display.max_columns', None)  # 모든 열 표시

    # selected_df =df[['employees','SE1','SE2','SE3','SE4','SE5']]
    # df_sorted = df.sort_values(by='schedule_time', ascending=True)
    df_sorted = df.sort_values(by='시작일', ascending=True)
   
    df_sorted.drop(['employees','schedule_date'],axis=1,inplace=True)
    selected_columns_order = ['시작일', '종료일', '서비스종류','고객사명','지역/장소','영업','SE1','SE2','SE3','SE4','SE5','Vendor','Model','작업내역','old_part','new_part','유형1','유형2','구분1','구분2','주/야/주말구분','비고(장애발생내역, 상세지원내역 등)']
    df_sorted[selected_columns_order].to_excel('output.xlsx', index=False)
 
if __name__ == "__main__":
    id = os.environ.get('id')
    password = os.environ.get('password')
    
    hiworks_crawler(id, password)