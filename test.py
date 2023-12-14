

from dotenv import load_dotenv
import pandas as pd
import os
import ast
# 예시 데이터

load_dotenv()
employees_with_positions =  os.environ.get('employees_with_positions')
employees_with_positions = ast.literal_eval(employees_with_positions)
# 입력값
input_names = ['조성희', '김지연', '이준태']

# 직급 우선순위 정의
position_priority = {'이사': 1, '상무': 2, '부장': 3, '차장': 4, '과장': 5, '대리': 6}

# 직급 우선순위에 따라 정렬
sorted_input_names = sorted(input_names, key=lambda x: position_priority.get(employees_with_positions[x], float('inf')))

df = pd.DataFrame()

# # SE 칼럼 추가
for i, name in enumerate(sorted_input_names, start=1):
    df[f'SE{i}'] = [name]


print(df)