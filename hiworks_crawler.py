import os
import shutil
import time
import pandas as pd
from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import difflib
from dotenv import load_dotenv
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows



def sorted_employees(input_names,NAME_PRIORITY_DIC):

    sorted_employees = sorted(input_names, key=lambda x: NAME_PRIORITY_DIC[x])
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

def is_weekend(date):
    if date.weekday() in [5, 6]:  
        return True
    else:
        return False
    
def write_data_to_excel(filePath,df):
    directory, filename = os.path.split(filePath)

    backup_filename = f"{filename}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    backup_filepath = os.path.join(directory, backup_filename)

    # 원본 파일을 백업 파일로 복사
    shutil.copyfile(filePath, backup_filepath)
    
    workbook = openpyxl.load_workbook(filePath)
    sheet = workbook.active
   
    for row_values in df.values.tolist():
        sheet.append(row_values)
    workbook.save(filePath)
    print(f"데이터가 성공적으로 추가되어 '{filePath}' 파일이 업데이트되었습니다.")

def classify_day_night(start_time, end_time, day_start_time_str="09:00", night_start_time_str="18:30"):
    # 문자열을 datetime 객체로 변환
    day_start_time = datetime.strptime(day_start_time_str, '%H:%M').time()
    night_start_time = datetime.strptime(night_start_time_str, '%H:%M').time()


    # 문자열을 datetime 객체로 변환
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%H:%M')
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%H:%M')


    # if day_start_time <= start_time < night_start_time and end_time <= night_start_time:
    if  start_time < night_start_time and end_time <= night_start_time:

        return '주간'
    elif  start_time < night_start_time and night_start_time <= end_time:
   
    # elif day_start_time <= start_time < night_start_time and night_start_time <= end_time:
        return '주/야간'
    elif night_start_time <= start_time:
        return '야간'


    


def convert_to_24hr_format(time_str):
    parts = time_str.split()
    
    if(parts[0]=='오전') :
        time_24hr_str = parts[1]

    elif (parts[0]=='오후') :
        if(parts[1].split(":")[0]!="12"):
            time_24hr_str = str(int(parts[1].split(":")[0]) + 12) + ":"+parts[1].split(":")[1]
        else :
            time_24hr_str = parts[1]
    return  datetime.strptime(time_24hr_str, "%H:%M").time()


def extract_date_and_time_range(input_time_str) :
    date_start_str, end_date_str = input_time_str.split("~")

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

def hiworks_crawler(config_data,start_month,end_month):


    load_dotenv()

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창을 숨기는 옵션

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()


    pd.set_option('display.max_rows', None)  # 모든 행 표시
    pd.set_option('display.max_columns', None)  # 모든 열 표시



    username= config_data['config']['ID']
    password= config_data['config']['PASSWORD']


    EMPLOYEES_DIC = config_data['config']['EMPLOYEES_DIC']
    REGION_CANDIDATE_ARR =config_data['config']['REGION_CANDIDATE_ARR']
    REGION_CANDIDATE_WEIGHTS_DIC =config_data['config']['REGION_CANDIDATE_WEIGHTS_DIC']
    CUSTOMER_CANDIDATE = config_data['config']['CUSTOMER_CANDIDATE']
    NAME_PRIORITY_DIC=config_data['config']['NAME_PRIORITY_DIC']
    NOT_WORK_CONTENT = config_data['config']['NOT_WORK_CONTENT']


    login_url = "https://login.office.hiworks.com/ostech.co.kr"

    driver.get(login_url)   
    wait = WebDriverWait(driver, 5)
          
    id_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="로그인 ID"]'))
    )
    id_input.send_keys(username)
    
 
    element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > main > div > div:nth-child(1) > form > fieldset > button'))
    )
    element.click()
    
    password_input = wait.until(
    EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)

    element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > main > div > div:nth-child(1) > form > fieldset > button'))
    )
    element.click()
    
    
    element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#contents > div.header-wrapper > div > div > div > div:nth-child(4) > a'))
    )
    element.click()
    

    data=[]    
    
    element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div.fc-toolbar > div.fc-center > h2'))
    )
    YearMonth = element.text.replace(".","-")
    
    for month in range(end_month,start_month-1, -1):
     
       # 이전 월 이동
        while str(month) not in YearMonth :
            element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div.fc-toolbar > div.fc-center > button.icon.directleft'))
            )
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#calendar > div.fc-toolbar > div.fc-center > button.icon.directleft')))
            element.click()

            element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div.fc-toolbar > div.fc-center > h2'))
            )
            YearMonth = element.text.replace(".","-")
        

        elements = wait.until(

        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.share.fc-draggable.c1')))
       
            
        for element in tqdm(elements, desc=f"{YearMonth} 데이터 작업 진행", unit="element"):

            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.share.fc-draggable.c1')))
            element.click() 
            
            
            locator = (By.CSS_SELECTOR, 'span.fl#__cal_name')

            calName_element = wait.until(
            lambda driver: driver.find_element(*locator) if driver.find_element(*locator).text.strip() != '' else None
            )
            
            cal_name=''
            subject=''
            contents=''
            scheduleTime_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_time')))  
         
            if calName_element.text.strip():
                cal_name = calName_element.text 
                if cal_name=="근태" :
                    try :        
                        element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')))
                        element.click() 
                    except:
                        element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')))
                        element.click() 
                    continue
        
                    
                subject_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="__subject"]')))
                if subject_element.text.strip():
                    subject = subject_element.text 
                    if( "검진" in subject or "연차"  in subject  or "휴가" in subject ):
                        try :        
                            element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')))
                            element.click() 
                        except:
                            element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')))
                            element.click() 
                        continue
               
                
                    customer =extract_customer(subject,CUSTOMER_CANDIDATE)
                    region = extract_region(subject,REGION_CANDIDATE_ARR,REGION_CANDIDATE_WEIGHTS_DIC)

                scheduleTime_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__schedule_time')))   
 
                if scheduleTime_element.text.strip():
                    start_date,end_date, start_time, end_time = extract_date_and_time_range(scheduleTime_element.text )
        
                contents_element = wait.until(  EC.presence_of_element_located((By.XPATH, '//div[@id="__contents"]')))
                if contents_element.text.strip():
                    contents = contents_element.text 
                    employees = get_employees(EMPLOYEES_DIC,contents)
                    sorted_employees_result = sorted_employees(employees,NAME_PRIORITY_DIC)
                
                    workContent = extract_workContent(contents,NOT_WORK_CONTENT)
            
                    current_date = start_date

                    if is_weekend(start_date) :
                        shift="주말"
                    else :
                        shift= classify_day_night(start_time,end_time)

                

                    while current_date <= end_date:
                        if( YearMonth in current_date.strftime("%Y-%m-%d") ):
                            data.append({
                                'schedule_date' :  current_date.strftime("%Y-%m-%d"),
                                '시작일':  current_date.strftime("%Y-%m-%d"),
                                '종료일':  current_date.strftime("%Y-%m-%d"),
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
                        current_date += timedelta(days=1)
                


            try :        
                    element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')))
                    element.click() 
            except:
                    element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')))
                    element.click() 
        

    df = pd.DataFrame(data)
   
  
    for i, (worker,name_with_position) in enumerate(EMPLOYEES_DIC.items()):
        df[f'SE{i + 1}'] = df['employees'].apply(lambda x: name_with_position if worker in x and worker != '' else None)


    df_sorted = df.sort_values(by='시작일', ascending=True)
    df_sorted.drop(['employees','schedule_date'],axis=1,inplace=True)

    selected_columns_order = ['시작일', '종료일', '서비스종류','고객사명','지역/장소','영업','SE1','SE2','SE3','SE4','SE5','Vendor','Model','작업내역','old_part','new_part','유형1','유형2','구분1','구분2','주/야/주말구분','비고(장애발생내역, 상세지원내역 등)']
    df_sorted_columns_order =df_sorted[selected_columns_order]
    df_sorted_columns_order.to_excel('output.xlsx', index=False)
    

    excel_file = config_data['config']['FILE_PATH']

    write_data_to_excel(excel_file,df_sorted_columns_order)