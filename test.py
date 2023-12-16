

import difflib
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
    return most_similar_candidates


region_candidate_str = os.environ.get('region_candidate')
REGION_CANDIDATE_WEIGHTS_str = os.environ.get('REGION_CANDIDATE_WEIGHTS')
region_candidate =ast.literal_eval(region_candidate_str)
REGION_CANDIDATE_WEIGHTS_dic =json.loads(REGION_CANDIDATE_WEIGHTS_str)
text="kt skylife server relocation(분당 분당kt idc 강남)"
print(find_most_similar(text,region_candidate,REGION_CANDIDATE_WEIGHTS_dic))