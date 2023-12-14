from io import StringIO
from itertools import islice
import tracemalloc
import pandas as pd
from sqlalchemy import create_engine, inspect,text
import pymysql
import re
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from datetime import datetime, timedelta
import chardet
from concurrent.futures import as_completed
import concurrent.futures

from sqlalchemy.orm import sessionmaker
import aiohttp
import asyncio
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
import time


diff_price_data=[]
current_price_data=[]
previous_close_data=[]
diff_percent_data=[]




session = requests.Session()



chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 숨기는 옵션

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def login(username,password):
    # url = "https://login.office.hiworks.com/ostech.co.kr"
    company="@ostech.co.kr"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


    login_url = "https://login.office.hiworks.com/ostech.co.kr"

    driver.get(login_url)
    
    id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="로그인 ID"]'))
    )

    # 입력란에 값을 입력
    id_input.send_keys('mcbaek')
    
 
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > main > div > div:nth-child(1) > form > fieldset > button'))
    )

    # 찾은 요소 클릭
    element.click()
    
    password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys('alscjf92!!')
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
    # elements = driver.find_elements(By.CSS_SELECTOR, '#calendar > div.fc-view-container > div > table > tbody > tr > td > div > div > div:nth-child(1) > div.fc-content-skeleton > table > thead > tr > td.fc-day-number')

    # 각 엘리먼트의 data-date 속성 값을 출력
    # for element in elements:
    #  data_date_value = element.get_attribute('data-date')
    #  print(data_date_value)
    # elements = driver.find_elements(By.CLASS_NAME, 'fc-event-container')
    elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-event-container')))
  
    
    for element in elements :
        data = []

        time.sleep(1)
        # wait = WebDriverWait(driver, 10)
        # element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.fl#__cal_name')))        
    
        # element = driver.find_element(By.CSS_SELECTOR, '#__cal_name')
        # element = driver.find_element(By.CSS_SELECTOR, 'span.fl#__cal_name')

        # element = driver.find_element(By.CSS_SELECTOR, '#__schedule_time')
          
        # if element.text.strip():
        #     cal_name = element.text 

        #     element = driver.find_element(By.CSS_SELECTOR, '#__schedule_time')
        #     if element.text.strip():
        #         schedule_time = element.text 

        #     element = driver.find_element(By.CSS_SELECTOR, '#__subject')
        #     if element.text.strip():
        #         subject = element.text 

        #     element = driver.find_element(By.CSS_SELECTOR, '#__schedule_regidate')
        #     if element.text.strip():
        #         schedule_regidate = element.text 

        #     element = driver.find_element(By.CSS_SELECTOR, '#__contents')
        #     if element.text.strip():
        #         contents = element.text 
        #     data.append({
        #     'cal_name': cal_name,
        #     'schedule_time': schedule_time,
        #     'subject': subject,
        #     'schedule_regidate': schedule_regidate,
        #     'contents': contents
        #      })

        # else:
        try :        
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule_confirm > a.icon.btn_closelayer')
        # 찾은 엘리먼트가 있다면 여기에 수행할 작업 추가
            element.click() 
        except:
            element = driver.find_element(By.CSS_SELECTOR, '#layer_schedule > div.layer_button > button:nth-child(2)')
        # 찾은 엘리먼트가 없을 경우 여기에 수행할 작업 추가
            element.click()  

    time.sleep(1000)

    # encoding = chardet.detect(response.content)['encoding']
    # html_content = response.content.decode(encoding)
    # print(html_content)
    # 크롤링
    # CRAWLING_URL = '<https://example.com/crawling>'
    # response = session.get(CRAWLING_URL)

# HTML 출력
    # print(response)

def get_stocks(market=None):

    if market == 'kospi':
        market_type = '&marketType=stockMkt'
    elif market == 'kosdaq':
        market_type = '&marketType=kosdaqMkt'
    elif market == 'konex':
        market_type = '&marketType=konexMkt'
    else :
        market_type = '&marketType='

    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?currentPageSize=5000&pageIndex=1&method=download&searchType=13'
    response = requests.get(url+market_type)
    encoding = chardet.detect(response.content)['encoding']
    html_content = response.content.decode(encoding)
    html_buffer = StringIO(html_content)
    list_df_stocks = pd.read_html(html_buffer, header=0, converters={'종목코드': lambda x: str(x)})
   
    df_stocks = list_df_stocks[0]
    df_stocks = df_stocks.rename(columns={'회사명': 'name', '종목코드': 'stock_code','업종':'industry','주요제품':'product'})
    df_stocks['market_type']=market
    return    df_stocks[['name','stock_code','industry','market_type','product']]


  
def parsing(code):
    html = get_html(code)
    
    content = html.decode('EUC-KR')
    soup = BeautifulSoup(content, 'html.parser')

    name = soup.select_one('#middle > div.h_company > div.wrap_company > h2 > a').text.strip()
    current_price = soup.select_one('#_nowVal').text.strip()
    diff_percent = soup.select_one('#_rate > span').text.strip()
    diff_price = soup.select_one('#_diff > span').text.strip()
    previous_close = soup.select_one('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(4) > span').text.strip()

    # 정규 표현식을 사용하여 숫자 추출
    regex = re.compile(r'[^\d.-]+')
    current_price = regex.sub('', current_price)
    diff_percent = regex.sub('', diff_percent)
    diff_price = regex.sub('', diff_price)
    previous_close = regex.sub('', previous_close)

    info = {
        'name': name,
        'diff_price': diff_price,
        'current_price': current_price,
        'diff_percent': diff_percent,
        'previous_close': previous_close,
    }

    return info

def get_html(code):

    url = f"https://finance.naver.com/item/sise.naver?code="
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url+code, headers=headers)
    response.raise_for_status()  # HTTP 요청이 실패한 경우 예외 발생


    # with session.get(url + code, headers=headers) as response:
    #     return response.content


    return response.content



async def get_html_async(session, code):
    url = f"https://finance.naver.com/item/sise.naver?code={code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with session.get(url, headers=headers) as response:
        # HTTP 응답 상태코드가 200인지 확인
        if response.status == 200:
            # HTML을 문자열로 반환
            return await response.text()
        else:
            # 에러가 발생한 경우 None을 반환하거나 예외를 발생시킬 수 있음
            return None  # 또는 raise SomeException("Failed to fetch HTML")



# def remove_7days_data(db_connection) :

#     try:
#         # 삭제할 데이터의 조건을 포함한 SQL 쿼리 생성
#         delete_query = """
#         DELETE FROM krx
#         WHERE reg_date < %s
#         """
#         # 일주일 전의 날짜 계산
#         one_week_ago = datetime.now() - timedelta(days=1)
        
        
#         # 쿼리 실행
#         cursor.execute(delete_query, (one_week_ago,))

#         # 변경사항을 저장
#         db_connection.commit()

#         print("삭제 완료")

#     except Exception as e:
#         print(f"오류 발생: {e}")

#     finally:
#         # 커서와 연결 닫기
#         cursor.close()
#         db_connection.close()

def remove_7days_data(session):
    try:
        # 삭제할 데이터의 조건을 포함한 SQL 쿼리 생성
        # delete_query = """
        # DELETE FROM krx
        # WHERE reg_date < %s
        # """
        # delete_query = text("""
        # DELETE FROM krx
        # WHERE reg_date < :one_week_ago
        # """)
        delete_query = text("""
          DELETE FROM krx
          WHERE DATE(reg_date) <= :one_week_ago
          """)
        # 일주일 전의 날짜 계산
        one_week_ago = datetime.now() - timedelta(days=7)
        # one_week_ago = datetime.now() 
        
        # 쿼리 실행
        # session.execute(delete_query, (one_week_ago,))
        session.execute(delete_query, {"one_week_ago": one_week_ago})

        # 변경사항을 저장
        session.commit()

        print("삭제 완료")

    except Exception as e:
        print(f"오류 발생: {e}")

  

# 사용 예시


# db_connection_str = 'mysql+pymysql://root:1234@svc.sel4.cloudtype.app/stock'

def create_db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# 주식 데이터 크롤링 및 저장
async def crawl_and_save(session, df_stocks, table_name):
    results_list = []

    # 비동기처리
    async with aiohttp.ClientSession() as session:
        tasks = [process_row_async(session, row) for _, row in df_stocks.iterrows()]

        for result in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            result_data = await result
            results_list.append(result_data)

    results_df = pd.DataFrame(results_list)

    # 주식 데이터와 크롤링 결과를 매칭
    merged_df = pd.merge(df_stocks, results_df, on='stock_code', how='left')
    merged_df['reg_date'] = datetime.now().strftime('%Y/%m/%d')

    # 데이터베이스 세션 생성 및 데이터 저장
    session = create_db_session()
    merged_df.to_sql(name=table_name, con=session.get_bind(), if_exists='append', index=False)

   
async def process_row_async(session, row):
    # _, row_data = row
    # code = row[1]['stock_code']
    code = row['stock_code']
    html = await get_html_async(session,code)

    # content = html.encode('ISO-8859-1').decode('EUC-KR', 'replace')
    content = html
    soup = BeautifulSoup(content, 'html.parser')

    name = soup.select_one('#middle > div.h_company > div.wrap_company > h2 > a').text.strip()
    current_price = soup.select_one('#_nowVal').text.strip()
    diff_percent = soup.select_one('#_rate > span').text.strip()
    diff_price = soup.select_one('#_diff > span').text.strip()
    previous_close = soup.select_one('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(4) > span').text.strip()
    market_cap = soup.select_one('#_market_sum').text.strip()
  
    # 정규 표현식을 사용하여 숫자 추출
    regex = re.compile(r'[^\d.-]+')
    current_price = regex.sub('', current_price)
    diff_percent = regex.sub('', diff_percent)
    diff_price = regex.sub('', diff_price)
    previous_close = regex.sub('', previous_close)
    info = {
        # 'name': name,
        'stock_code' :code,
        'diff_price': diff_price,
        'current_price': current_price,
        'diff_percent': diff_percent,
        'previous_close': previous_close,
        'market_cap' :market_cap
    }

    return info


async def main():

    
    # KOSPI 주식 데이터 크롤링 및 저장
    df_stocks_kospi = get_stocks('kospi')
    session = create_db_session(engine)
    await crawl_and_save(session, df_stocks_kospi, 'krx')

    # KOSDAQ 주식 데이터 크롤링 및 저장
    df_stocks_kosdaq = get_stocks('kosdaq')
    await crawl_and_save(session, df_stocks_kosdaq, 'krx')
    session.close()
    

    

def get_krx_code(market=None):
   
    if market == 'kospi':
        market_type = '&marketType=stockMkt'
    elif market == 'kosdaq':
        market_type = '&marketType=kosdaqMkt'
    elif market == 'konex':
        market_type = '&marketType=konexMkt'
    else :
         market_type = '&marketType='
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13{0}'.format(market_type)
    response = requests.get(url)
    encoding = chardet.detect(response.content)['encoding']
    html_content = response.content.decode(encoding)
    html_buffer = StringIO(html_content)

    stock_code = pd.read_html(html_buffer, header = 0)[0]
    stock_code['종목코드'] = stock_code['종목코드'].map('{:06d}'.format)
    stock_code = stock_code[['회사명', '종목코드', '업종', '상장일']]
    stock_code = stock_code.rename(columns = {'회사명': 'name', '종목코드': 'code', '업종': 'sectors',
                                              '상장일': 'listing_date'})
    stock_code['listing_date'] = pd.to_datetime(stock_code['listing_date'])
    
    return stock_code




def calculate_status(df):
    df['status'] = ''
   
    df.loc[df['close'] - df['close'].shift(-1) > 0, 'status'] = '+'
    df.loc[df['close'] - df['close'].shift(-1) < 0, 'status'] = '-'

    subset_df = df.iloc[:2, :]
    # status가 연속으로 2개 이상인 경우를 확인하는 조건 추가
    consecutive_plus = (subset_df['status'] == '+') & (subset_df['status'].shift(1) == '+')
    consecutive_minus = (subset_df['status'] == '-') & (subset_df['status'].shift(1) == '-')

    # 연속으로 2개 이상인 경우가 있는지 여부 출력
    if any(consecutive_plus):
        # print("There are consecutive '+' statuses.")
        # df['condition2plus'] = True
        return True

    if any(consecutive_minus):
        # print("There are consecutive '-' statuses.")
        return False





def get_stock_price(code, num_of_pages, sort_date = True):
    url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
    headers = {'User-agent': 'Mozilla/5.0'} 
    bs = BeautifulSoup(requests.get(url=url, headers = headers).text, 'html.parser')
    pgrr = bs.find("td", class_="pgRR")
    # last_page = int(pgrr.a["href"].split('=')[-1])

    if pgrr is not None:
        try:
            last_page = int(pgrr.a["href"].split('=')[-1])
        except (AttributeError, ValueError):
            last_page = 1
    else:
        last_page = 1

    pages = min(last_page, num_of_pages) # 마지막 페이지와 가져올 페이지 수 중에 작은 값 선택
    df = pd.DataFrame()

    for page in range(1, pages+1):
        page_url = '{}&page={}'.format(url, page)
        response = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'})
        html_buffer = StringIO(response.text)
        df=pd.concat([df, pd.read_html(html_buffer)[0]])

    

    df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'}) #영문으로 컬럼명 변경
    
    df = df.dropna()
    df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']] # 컬럼 순서 정렬


    
    return df.dropna()

if __name__ == "__main__":

    login('mcbaek','alscjf92!!')
