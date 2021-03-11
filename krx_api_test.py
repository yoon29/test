'''
https://tariat.tistory.com/892

파이썬 실시간 주가, 주식시세 데이터 수집하는 방법은?
실시간 주가 및 주식시세 데이터를 제공하는 사이트가 있다. 바로 한국거래소이다.
한국거래소에서는 XML포맷으로 실시간 주가 및 기업 재무제표를 제공하고 있다.
별도의 API KEY를 발급받을 필요도 없다. 하지만, 많은 사람들이 사용하지는 않는 듯 하다.
약간의 결함도 있기 때문이다. 오늘은 파이썬 실시간 주가, 주식시세 데이터 수집하는 방법에 대해서 알아보도록 하겠다.

1. 한국거래소에서 제공하는 데이터는?
한국 거래소에서 제공하는 데이터의 종류는 4가지다. '실시간시세, 공시정보, 재무종합, 텍스트'가 있다. 텍스트는 자세한 설명이 없어 어떤 데이터인지 알기가 어렵다. 하지만, 실시간시세와 재무정보를 제공하는 것만으로도 충분히 가치가 있는 듯 하다. 한국거래소에서 제공하는 데이터의 자세한 내용은 아래 링크를 참조하기 바란다.
( 참조: KRX 상장기업 지원 서비스 안내 바로가기 )

* 한국거래소 XML 서비스 URL
1. 실시간시세(국문)
 http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=단축종목코드
2. 실시간시세(영문)
 http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code=단축종목코드
3. 공시정보(국,영문)
 http://asp1.krx.co.kr/servlet/krx.asp.DisList4MainServlet?code=단축코드&gubun=K (K:국문/E:영문)
4. 재무종합(국문)
  http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu?code=단축종목코드
5. 재무종합(영문)
  http://asp1.krx.co.kr/servlet/krx.asp.XMLJemuEng?code=단축종목코드
6. 재무종합2(국문)
   http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu2?code=단축종목코드
7. 재무종합3(국문)
   http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu3?code=단축종목코드
8. 텍스트
   http://asp1.krx.co.kr/servlet/krx.asp.XMLText?code=단축종목코드

단축종목코드는 주식종목코드를 의미한다. 예를 들어 삼성전자는 005930이다. 구글에서 삼성전자를 검색하면, 종목코드는 쉽게 확인할 수 있다.

2. 주의할 점은?
일단 위의 URL주소에 단축종목코드를 넣어서, 웹브라우저에서 검색하면 에러가 발생한다.
하지만, 개의치 말고 마우스 우클릭한 후 [소스 보기]를 클릭하면 XML포맷으로 데이터가 정상 회신된 것을 확인할 수 있다.
이상하게도 실시간 시세(국문)에 '삼성전자 단축코드(005930)'를 넣으면, 값이 하나도 회신되지 않는다.
하지만, 실시간 시세(영문)으로 접속하면 값이 이상없이 회신된다.
아마도 실시간시세(국문)보다는 영문을 많은 사람들이 사용하는 듯 하다.
사실 왜 국문과 영문으로 나눠서 2개의 서비스를 운영하고 있는지 모르겠다.

3. 파이썬으로 데이터를 수집하는 방법은?
XML포맷으로 데이터를 제공하기 때문에, urllib모듈을 이용해서 데이터를 가져와서 형식에 맞게 파싱하면 된다.
이는 필자의 블로그에서도 많이 다루었기 때문에, 자세한 내용은 생략하도록 하겠다.
수집하는 부분을 함수로 만들고, SQLite3 DB에 저장하였다. SQLite3 DB에 대한 자세한 내용은 아래 포스팅을 참조바란다.
( 참조: SQLite3 파이썬 pandas 데이터프레임으로 불러오기 )

데이터를 수집할 때, 네트워크에서 병목이 발생하여 에러가 나는 경우가 있다.
이런 경우 해당 건만 다시 골라서 수집하기가 번거럽다.
그래서, HTTPError 에러가 발생할 경우 한번 더 URL에 접속하도록 작성하였다.

'''

import pandas as pd
import sqlite3
import logging
import time
from urllib.error import HTTPError
from tqdm import tqdm
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_sise(stock_code, try_cnt):
    try:
        url="http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code={}".format(stock_code)
        req=urlopen(url)
        result=req.read()
        xmlsoup=BeautifulSoup(result,"lxml-xml")
        stock = xmlsoup.find("TBL_StockInfo")

        stock_df=pd.DataFrame(stock.attrs, index=[0])
        stock_df=stock_df.applymap(lambda x: x.replace(",",""))

        return stock_df

    except HTTPError as e:
        logging.warning(e)
        if try_cnt>=3:
            return None
        else:
            get_sise(stock_code,try_cnt=+1)

# 주식 시세 DB에 저장하기
# con=sqlite3.connect("./data/div.db")
# stock_code=['005930','066570']
#
# for s in tqdm(stock_code):
#     temp=get_sise(s,1)
#     temp.to_sql(con=con,name="div_stock_sise",if_exists="append")
#     time.sleep(0.5)
#
# con.close()

stock_code=['005930','066570']

for s in tqdm(stock_code):
    temp=get_sise(s,1)
    time.sleep(0.5)
    print('temp = \n{arg1}'.format(arg1=temp))


