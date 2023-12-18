import pandas as pd
import openpyxl


# 첫 번째 엑셀 파일 읽기
# excel_file1 = '2023년 서비스 내역_20231205.xlsx'
# df1 = pd.read_excel(excel_file1)

# # 두 번째 엑셀 파일 읽기
# excel_file2 = 'output.xlsx'
# df2 = pd.read_excel(excel_file2)

# # 두 데이터프레임을 합치기
# merged_df = pd.concat([df1, df2], ignore_index=True)

# # 합쳐진 데이터프레임을 새로운 엑셀 파일로 저장
# merged_df.to_excel('merged_file.xlsx', index=False)



# 기존 엑셀 파일 열기
existing_excel_path = '2023년 서비스 내역_20231205.xlsx'
workbook = openpyxl.load_workbook(existing_excel_path)

# 기존 시트 선택
sheet = workbook.active

# 추가할 데이터 생성 (예시)
new_data = [['D', 4], ['E', 5], ['F', 6]]

# 데이터를 기존 시트에 추가
for row in new_data:
    sheet.append(row)