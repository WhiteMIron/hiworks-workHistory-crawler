

import difflib
import shutil
from dotenv import load_dotenv
import numpy as np
import openpyxl
import pandas as pd
import os
import ast
import json
from datetime import datetime,timedelta


load_dotenv()
# 예시 데이터
# content = """mac주소 정리
# mac값 고정
# nutanix vm 보안취약점

# 최진호고수비"""

# employee = ["최진호", "고수비"]

# employee_contents = []

# for emp in employee:
#     if emp in content:
#         employee_contents.append(emp)

# print(employee_contents)




def sorted_employee_with_position(input_names):
    

    employee = os.environ.get("employee")
    name_priority = os.environ.get('name_priority')
    
    name_priority_dic= json.loads(name_priority)
    employee_dic = json.loads(employee)
   

    sorted_employee = sorted(input_names, key=lambda x: name_priority_dic[x])
    sorted_employee_with_position = [employee_dic[name] for name in sorted_employee]

    return sorted_employee_with_position
    


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
    # most_similar_candidates = [candidate for candidate, _ in similarity_scores if _ == similarity_scores[0][1]]
    most_similar = similarity_scores[0][0]
    return most_similar



# data = {'employees': ['John', 'Alice', 'Bob', 'Eve']}

# df = pd.DataFrame(data)

# # "employees" 열의 값으로 SE 열 동적으로 추가
# for i, employee in enumerate(df['employees'], start=1):
#     df[f'SE{i}'] =employee

# # DataFrame 출력
# print(df)


df = pd.DataFrame({'title': ['1', '2', '3', '4']})
workers = ['Jon', 'Alice', 'Bob', 'Eve', 'Charlie', 'David', '']
EMPLOYEES={"조성희":"조성희 부장","최진호":"최진호 대리","고수비":"고수비 대리","백민철":"백민철 대리"}


# 'worker' 열에 랜덤으로 여러 명의 값 할당
df['worker'] = [np.random.choice(workers, size=np.random.randint(1, 4), replace=False).tolist() for _ in range(len(df))]



# print(df)


# max_len = max(len(worker_list) for worker_list in df['worker'])
# for i in range(1, max_len + 1):
#     df[f'SE{i}'] = df['worker'].apply(lambda x: x[i-1] if len(x) >= i else None)

# # DataFrame 출력
# print(df)

# 'worker' 리스트에 대해 위치에 해당하는 값을 'SE' 열에 할당
# for i, worker in enumerate(workers):
#     df[f'SE{i + 1}'] = df['worker'].apply(lambda x: worker if worker in x else None)

# for i, worker in enumerate(workers):
#     df[f'SE{i + 1}'] = df['worker'].apply(lambda x: worker if worker in x and worker != '' else None)

# # DataFrame 출력
# print(df)


# EMPLOYEES = {"조성희": "조성희 부장", "최진호": "최진호 대리", "고수비": "고수비 대리", "백민철": "백민철 대리","":""}
# df['worker'] = [np.random.choice(list(EMPLOYEES.keys()), size=np.random.randint(1, 4), replace=False).tolist() for _ in range(len(df))]

# print(EMPLOYEES.items())
# for i, (worker,name_with_position) in enumerate(EMPLOYEES.items()):
#     df[f'SE{i + 1}'] = df['worker'].apply(lambda x: name_with_position if worker in x and worker != '' else None)



from datetime import datetime, timedelta


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



# # 주어진 문자열
time_range = "2023-12-01 오전 9:00 ~ 2023-12-02 오전 3:40"

# # 날짜와 시간을 분리
# start_date,end_date,start_time,end_time = extract_date_and_time_range(time_range)


# current_date = start_date
# while current_date <= end_date:
#     current_date += timedelta(days=1)



# def classify_day_night(start_time, end_time, day_start_time_str="09:00", night_start_time_str="18:30"):
#     # 문자열을 datetime 객체로 변환
#     day_start_time = datetime.strptime(day_start_time_str, '%H:%M')
#     night_start_time = datetime.strptime(night_start_time_str, '%H:%M')


#     # 문자열을 datetime 객체로 변환
#     if isinstance(start_time, str):
#         start_time = datetime.strptime(start_time, '%H:%M')
#     if isinstance(end_time, str):
#         end_time = datetime.strptime(end_time, '%H:%M')


#     if day_start_time <= start_time < night_start_time and end_time <= night_start_time:
#         return '주간'
#     elif day_start_time <= start_time < night_start_time and night_start_time <= end_time:
#         return '주/야간'
#     elif night_start_time <= start_time:
#         return '야간'
# print( classify_day_night(start_time,end_time))

# date_range_str = "2023-11-10 오전 9:00~2023-11-11 오후 3:30"

# 문자열에서 날짜 부분 추출

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
  



def is_weekend(date):
    # date_object = datetime.strptime(date_str, '%Y-%m-%d')
    
    if date.weekday() in [5, 6]:  
        return True
    else:
        return False
    

def classify_day_night(start_time, end_time, day_start_time_str="09:00", night_start_time_str="18:30"):
    # 문자열을 datetime 객체로 변환
    day_start_time = datetime.strptime(day_start_time_str, '%H:%M').time()
    night_start_time = datetime.strptime(night_start_time_str, '%H:%M').time()

    # 문자열을 datetime 객체로 변환
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%H:%M')
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%H:%M')

    if day_start_time <= start_time < night_start_time and end_time <= night_start_time:
        return '주간'
    elif day_start_time <= start_time < night_start_time and night_start_time <= end_time:
        return '주/야간'
    elif night_start_time <= start_time:
        return '야간'



# date="2023-11-27 오전 9:00~오후 6:00"
# start_date,end_date, start_time, end_time = extract_date_and_time_range(date)



def write_data_to_excel(filePath):
    
    directory, filename = os.path.split(filePath)

    # 백업 파일 이름 생성 (현재 날짜와 시간을 이용하여 고유한 이름 생성)
    backup_filename = f"{filename}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"

    # 백업 파일 경로 생성
    backup_filepath = os.path.join(directory, backup_filename)

    print(backup_filepath)
    # 원본 파일을 백업 파일로 복사
    shutil.copyfile(filePath, backup_filepath)
 
    
    
    # workbook = openpyxl.load_workbook(filePath)
    # sheet = workbook.active
   
    # for row_values in df.values.tolist():
    #     sheet.append(row_values)
    # workbook.save(filePath)
    # print(f"데이터가 성공적으로 추가되어 '{filePath}' 파일이 업데이트되었습니다.")
    

# write_data_to_excel("2023년 서비스 내역_20231205.xlsx")


CUSTOMER_CANDIDATE=['','kt cloud','ktds','kt m&s','ktskylife','대검찰청','링네트','매그나칩반도체','메니인소프트','서울사이버안전센터','아리랑TV','아이넵소프트','엘비유세스(구 엘비휴넷)','예탁결제원','우리금융캐피탈','중소벤쳐기업진흥공단','지니뮤직','플레이디','합동참모본부','해치텍']
REGION_CANDIDATE=['','강남구청','cloud','ktskylife','LGU+','가산','강남','과천','과천청사','광주고등검찰청','김천','대구','대구지방검찰청','목동','목동,백석','방배동','백석동','분당','분당kt idc','상암고비즈','상암동','서울사무소','서초','서초본청','신사','아리랑TV','안양','야탑동','여의도','오창','용산','지니뮤직','창원지방검찰청','청주','케이뱅크(목동ktidc)','하나은행청라데이터센터']
REGION_CANDIDATE_WEIGHTS = {"":1,"강남구청":2,"cloud": 1, "ktskylife": 1, "LGU+": 1, "가산": 1, "강남": 1, "과천": 1, "과천청사": 1, "광주고등검찰청": 1, "김천": 1, "대구": 1, "대구지방검찰청": 1, "서초본청":3,"목동": 5, "목동,백석": 4, "방배동": 1, "백석동": 4, "분당": 5, "분당kt idc": 2, "상암고비즈": 1, "상암동": 3, "서울사무소": 1, "서초": 1, "신사": 3, "아리랑TV": 1, "안양": 1, "야탑동": 1, "여의도": 1, "오창": 1, "용산": 1, "지니뮤직": 1, "창원지방검찰청": 1, "청주": 2, "케이뱅크(목동ktidc)": 1, "하나은행청라데이터센터": 1}

CUSTOMER_DIC={"예탁결제원":"여의도","서울사이버안전센터":"상암","중소벤처기업진흥공단":"상암고비즈","플레이디":"가산","엘비유세스(구 엘비휴넷)":"안양","kt m&s":"과천","아이넵소프트":"하나은행청라데이터센터","메니인소프트":"케이뱅크(목동ktidc)","키파운드리(서울)":"서울사무소","링네트":"아리랑TV"}

def get_similarity(original,candidate) : 
    matcher = difflib.SequenceMatcher(None, original, candidate)
    similarity_score = matcher.ratio()
    return similarity_score

def get_resion_by_custormer(subject,candidate, customerDic):
    customer = find_most_similar(subject,candidate)
    print(customer)
    if get_similarity(subject,customer) > 0.7 :
        return customerDic.get(customer)
    else :
        return None
def extract_customer(input_str,candidate):
    result = find_most_similar(input_str,candidate)
    return result
   
def find_most_similar(original, candidates, weights=None):
    if weights is None:
        # 가중치가 제공되지 않으면 모든 후보에 대해 동일한 가중치를 사용합니다.
        weights = {candidate: 1 for candidate in candidates}

    similarity_scores = []
    for candidate in candidates:
        # SequenceMatcher를 사용하여 유사도 측정
        matcher = difflib.SequenceMatcher(None, original, candidate)
        similarity_score = matcher.ratio()
        print(candidate, similarity_score)
        if similarity_score==1.0 :
            return candidate
        # 가중치 적용
        weighted_similarity = similarity_score * weights[candidate]
        # 유사도 점수 저장
        similarity_scores.append((candidate, weighted_similarity))

    # 가장 유사도가 높은 순서대로 정렬
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    # print(similarity_scores)
    # 가장 유사도가 높은 값들 반환 (동일한 최고 유사도를 갖는 모든 후보 반환)
    most_similar_candidates = [candidate for candidate, _ in similarity_scores if _ == similarity_scores[0][1]]
    most_similar_candidates_str = ', '.join(most_similar_candidates)
    return most_similar_candidates_str


def extract_region(input_str,candidate,weights):
    result = find_most_similar(input_str,candidate,weights)
    return result

# result = get_resion_by_custormer("키파운드리(청주)",CUSTOMER_CANDIDATE,CUSTOMER_DIC)
# print(result)
# if result :
#     region = result
# else :
#     region = extract_region("키파운드리(청주)",REGION_CANDIDATE_WEIGHTS,REGION_CANDIDATE_WEIGHTS)

# print(region)

# customer =extract_customer("키파운드리(청주)")



def is_weekend(date):
    if date.weekday() in [5, 6]:  
        return True
    else:
        return False
date_string = "2023-12-30"
formatted_date = datetime.strptime(date_string, "%Y-%m-%d")

print(formatted_date)
print(is_weekend(formatted_date))


customer = extract_customer("고비즈코리아",CUSTOMER_CANDIDATE)
print(customer)                