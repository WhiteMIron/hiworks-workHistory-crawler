

import ast
import configparser
import difflib
import json



def find_most_similar(original, candidates, weights=None):
    if weights is None:
        # 가중치가 제공되지 않으면 모든 후보에 대해 동일한 가중치를 사용합니다.
        weights = {candidate: 1 for candidate in candidates}

    similarity_scores = []

    for candidate in candidates:
        # SequenceMatcher를 사용하여 유사도 측정
        matcher = difflib.SequenceMatcher(None, original, candidate)
        similarity_score = matcher.ratio()
        if similarity_score ==1.0 :
            return candidate

        # 가중치 적용
        weighted_similarity = similarity_score * weights[candidate]

        # 유사도 점수 저장
        similarity_scores.append((candidate, weighted_similarity))

    # 가장 유사도가 높은 순서대로 정렬
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    if similarity_scores[0][1] < 0.5 :
        return original

    # 가장 유사도가 높은 값들 반환 (동일한 최고 유사도를 갖는 모든 후보 반환)
    # most_similar_candidates = [candidate for candidate, _ in similarity_scores if _ == similarity_scores[0][1]]
    # # most_similar_candidates_str = ', '.join(most_similar_candidates)
    # # return most_similar_candidates_str
    most_similar = similarity_scores[0][0]
    return most_similar



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


file_path = 'config.ini'
config_data = read_ini_file(file_path)
    
CUSTOMER_CANDIDATE = config_data['config']['CUSTOMER_CANDIDATE']
 
print(find_most_similar("매그나칩",CUSTOMER_CANDIDATE))
