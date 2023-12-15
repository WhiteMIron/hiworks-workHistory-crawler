

from dotenv import load_dotenv
import pandas as pd
import os
import ast
import json



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
    

