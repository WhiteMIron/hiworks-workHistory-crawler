import difflib

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

# 예시
original_word = "결제"
candidate_words = ["KERIS", "kt m&s", "ktds", "KTM&S", "ktskylife", "대검찰청", "링네트", "매그나칩반도체", "메니인소프트",
                   "서울시사이버안전센터", "아리랑TV", "아이넵소프트", "엘비유세스(구 엘비휴넷)", "예탁결제원", "우리금융캐피탈", "중소벤처기업진흥공단",
                   "지니뮤직", "플레이디", "합동참모본부", "해치텍"]

most_similar_word = find_most_similar(original_word, candidate_words)
print(f"Original Word: {original_word}")
print(f"Most Similar Word: {most_similar_word}")