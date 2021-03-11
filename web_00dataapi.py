'''
[Python] - 공공데이터 api 크롤링(날씨데이터 수집)
https://alex-blog.tistory.com/entry/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%B6%84%EC%84%9D%EC%9D%84-%EC%9C%84%ED%95%9C-Python-%EA%B3%B5%EA%B3%B5%EB%8D%B0%EC%9D%B4%ED%84%B0-api-%ED%81%AC%EB%A1%A4%EB%A7%81?category=865129

스크립트를 짜기 전에 우선 api 사용을 위한 서비스 활용 신청이 필요합니다. 
지상(종관, ASOS) 일자료 조회서비스
https://www.data.go.kr/data/15059093/openapi.do

로그인 이후, 활용신청이 승인되면 아래처럼 고유 계정 인증키가 발급됩니다.

'''

import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'

queryParams = '?' + \
              'ServiceKey=' + '개인 발급 KEY'+ \
              '&pageNo='+ '1' + \
              '&numOfRows='+ '999' + \
              '&dataType='+ 'JSON' + \
              '&dataCd='+ 'ASOS' + \
              '&dateCd='+ 'DAY' + \
              '&startDt='+ '20180601' + \
              '&endDt='+ '20200421' + \
              '&stnIds='+ '108' # \ 뒤에 공백 금지

result = requests.get(url + queryParams)
js = json.loads(result.content)
data = pd.DataFrame(js['response']['body']['items']['item'])

li = ['stnId','tm','avgTa','minTa','maxTa','sumRn','maxWs','avgWs','ddMes']

data.loc[:,li]

data[li].to_csv("weather.csv",index=False )





