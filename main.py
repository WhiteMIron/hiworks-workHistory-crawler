import ast
import configparser
from datetime import datetime
import json
from hiworks_crawler import hiworks_crawler
import os



def get_current_year():
    current_date = datetime.now()
    return current_date.year


def get_year_month(year,month):
    return datetime(year, month, 1)



def get_env_dic(input_str):
    return json.loads(input_str)

def get_env_arr(input_str):
    return ast.literal_eval(input_str)




def read_ini_file(file_path):
    config = configparser.ConfigParser()
    
    with open(file_path, encoding='utf-8') as f:
        config.read_file(f)

    

    ID = config.get('config', 'ID')
    PASSWORD = config.get('config', 'PASSWORD')
    EMPLOYEES_str = config.get('config', 'EMPLOYEES')
    NAME_PRIORITY_str= config.get('config', 'NAME_PRIORITY')
    CUSTOMER_CANDIDATE_str = config.get('config', 'CUSTOMER_CANDIDATE')
    NOT_WORK_CONTENT_str =  config.get('config', 'NOT_WORK_CONTENT')
    REGION_CANDIDATE_str = config.get('config', 'REGION_CANDIDATE')
    REGION_CANDIDATE_WEIGHTS_str =config.get('config', 'REGION_CANDIDATE_WEIGHTS')
    FILE_PATH = config.get('config', 'FILE_PATH')
    EXCLUDE_SUBJECT = config.get('config','EXCLUDE_SUBJECT')
    CUSTOMER_DIC=config.get('config','CUSTOMER_DIC')
    
    EMPLOYEES_DIC = get_env_dic(EMPLOYEES_str)
    REGION_CANDIDATE_ARR = get_env_arr(REGION_CANDIDATE_str)
    REGION_CANDIDATE_WEIGHTS_DIC = get_env_dic(REGION_CANDIDATE_WEIGHTS_str)
    CUSTOMER_CANDIDATE = get_env_arr(CUSTOMER_CANDIDATE_str)
    NAME_PRIORITY_DIC = get_env_dic(NAME_PRIORITY_str)
    EXCLUDE_WORK_CONTENT = get_env_arr(NOT_WORK_CONTENT_str)
    EXCLUDE_SUBJECT = get_env_arr(EXCLUDE_SUBJECT)
    CUSTOMER_DIC=get_env_dic(CUSTOMER_DIC)

    return {
        'config': {
            'ID': ID,
            'PASSWORD': PASSWORD,
            'FILE_PATH':FILE_PATH,
            'EMPLOYEES_DIC': EMPLOYEES_DIC,
            'NAME_PRIORITY_DIC': NAME_PRIORITY_DIC,
            'REGION_CANDIDATE_ARR': REGION_CANDIDATE_ARR,
            'REGION_CANDIDATE_WEIGHTS_DIC':REGION_CANDIDATE_WEIGHTS_DIC,
            'CUSTOMER_CANDIDATE':CUSTOMER_CANDIDATE,
            'EXCLUDE_WORK_CONTENT':EXCLUDE_WORK_CONTENT,
            'EXCLUDE_SUBJECT':EXCLUDE_SUBJECT,
            'CUSTOMER_DIC' : CUSTOMER_DIC
         }
    }

if __name__ == "__main__":
    id = os.environ.get('id')
    password = os.environ.get('password')

    file_path = 'config.ini'
    config_data = read_ini_file(file_path)
    

    while True:
        try:
            start_month = input("시작 월을 숫자만 입력하세요: ")
            start_month = int(start_month)

            if not (1 <= start_month <= 12):
                raise ValueError("1부터 12까지의 숫자만 입력하세요.")

            current_year = get_current_year()
            start_Year_Month = get_year_month(current_year, start_month)

            break

        except ValueError as e:
            print("다시 시도하세요.")
    while True:
        try:
            end_month = input("끝 월을 숫자만 입력하세요: ")
            end_month = int(end_month)

            if not (1 <= end_month <= 12):
                raise ValueError("1부터 12까지의 숫자만 입력하세요.")

            if start_month > end_month:
                raise ValueError("종료 월은 시작 월보다 작을 수 없습니다.")

            current_year = get_current_year()
            end_Year_Month = get_year_month(current_year, end_month)
            break

        except ValueError as e:
            print(e)
            print("다시 시도하세요.")
    hiworks_crawler(config_data,start_month,end_month) 