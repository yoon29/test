import pandas as pd
import lxml
import html5lib
import requests
from bs4 import BeautifulSoup

##############################################
# url : https://excelsior-cjh.tistory.com/111
##############################################

##############################################
'''
1) pandas.read_html()을 이용해 krx에서 종목코드 가져오기
네이버금융에서 원하는 종목의 주식데이터를 가져오기 위해 먼저 코스피(KOSPI)과 코스닥(KOSDAQ)의 종목코드가 필요하다.
한국거래소(krx)에서는 주식시장에 상장된 기업들에 대해 종목코드를 제공한다.
pandas모듈의 pandas.read_html()을 이용해 종목코드를 가져올 수 있다.
pandas.read_html()은 HTML에서 <table></table>태그를 찾아 자동으로 DataFrame형식으로 만들어준다.
아래의 소스코드를 통해 주식의 종목코드를 가져올 수 있다.

☞ 기업공시사이트
https://kind.krx.co.kr/main.do?method=loadInitPage&scrnmode=1
☞ 중시일정(유/무상증자 등등)
https://kind.krx.co.kr/common/stockschedule.do?method=StockScheduleMain
☞ 오늘의공시
https://kind.krx.co.kr/disclosure/todaydisclosure.do?method=searchTodayDisclosureMain&marketType=0
☞ 공시-회사별검색
https://kind.krx.co.kr/disclosure/searchdisclosurebycorp.do?method=searchDisclosureByCorpMain
☞ 공시-상세검색
https://kind.krx.co.kr/disclosure/details.do?method=searchDetailsMain
☞ 채권공시
https://kind.krx.co.kr/disclosure/searchbondcorpdisclosure.do?method=searchBondCorpDisclosureMain
☞ ETF
https://kind.krx.co.kr/disclosure/disclosurebystocktype.do?method=searchDisclosureByStockTypeEtf
☞ ELW
https://kind.krx.co.kr/disclosure/disclosurebystocktype.do?method=searchDisclosureByStockTypeElw
☞ ELN
https://kind.krx.co.kr/disclosure/disclosurebystocktype.do?method=searchDisclosureByStockTypeEtn
☞ 신규상장
https://kind.krx.co.kr/disclosure/details.do?method=searchDetailsMain&disclosureType=02&disTypevalue=0321&disTypename=6
☞ 신규상장기업현황
https://kind.krx.co.kr/listinvstg/listingcompany.do?method=searchListingTypeMain
☞ 자사주취득/처분
https://kind.krx.co.kr/corpgeneral/treasurystk.do?method=loadInitPage
☞ 기업분석리포트
https://kind.krx.co.kr/corpgeneral/companyAnalysisReport.do?method=listingForeignCompanyMain&searchGubun=companyAnalysisReport
'''

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
print('code_df = \n{code_df}'.format(code_df=code_df))

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
code_df.head()
print('1 code_df.head() = \n{head}'.format(head=code_df.head()))

##############################################

##############################################
'''
2) Naver금융에서 일자별 주식데이터 가져오기
이제 네이버금융에서 원하는 종목의 일자 데이터를 가져와 보도록 하자.
여기서는 신라젠(215600) 의 일자 데이터를 가져온다.
아래의 소스코드는 특정 종목뿐만 아니라 사용자가 원하는 종목의 일자데이터를 가져올 수 있도록 get_url이라는 함수를 만들어 줬다.
Naver금융에서 주식데이터를 가져오는 방법에 대해 자세히 알고 싶다면 5. Pandas를 이용한 Naver금융에서 주식데이터 가져오기를 참고하면 된다.
'''

# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌
def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)  # 사이트막혀있음

    print("요청 URL = {}".format(url))
    return url


# 종목의 일자데이터 url 가져오기
item_name = '대원'
url = get_url(item_name, code_df)

# 일자 데이터를 담을 df라는 DataFrame 정의
df = pd.DataFrame()

# ##########
# # test
# url = 'http://finance.naver.com/item/sise_day.nhn?code=011070&page=1'
# header = {'User-Agent':'Mozilla/5.0'}  # User-Agent를 넣어야 막히지 않음
# r = requests.get(url,headers=header)
# print('r.text = \n{r}'.format(r=r.text))
# test = pd.read_html(r.text,header=0)[0]
# print('test = \n{arg1}'.format(arg1=test))
# ##########

# 1페이지에서 20페이지의 데이터만 가져오기
for page in range(1, 2):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    print('▶▶▶ {page} pg_url = {pg_url}'.format(page=page,pg_url=pg_url))

    # df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    header = {'User-Agent': 'Mozilla/5.0'}  # User-Agent를 넣어야 막히지 않음
    r = requests.get(url, headers=header)
    df = df.append(pd.read_html(r.text, header=0)[0], ignore_index=True)
    print('▶▶▶ {arg1} df = \n{arg2}'.format(arg1=page, arg2=df))

# df.dropna()를 이용해 결측값 있는 행 제거
df = df.dropna()

# 상위 5개 데이터 확인하기
df.head()
print('2 code_df.head() = \n{head}'.format(head=code_df.head()))

# 아래의 소스코드는 추후에 데이터 분석에서 편하게 하기위해 추가적으로 처리해 준 코드이다.

# 한글로 된 컬럼명을 영어로 바꿔줌
df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                        '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

# 데이터의 타입을 int형으로 바꿔줌
df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

# 컬럼명 'date'의 타입을 date로 바꿔줌
# df['date'] = pd.to_datetime(df['date'])

# 일자(date)를 기준으로 오름차순 정렬
df = df.sort_values(by=['date'], ascending=True)

# 상위 5개 데이터 확인
df.head()

##############################################

##############################################
'''
3) KDJ Stochastic 지표 구현하기
Stochastic을 구현하기 위해 필요한 데이터 들을 수집하였으면, 이제 Stochastic을 구현해 보도록 한다.
아래의 소스코드는 Stochastic을 get_stochastic()이라는 함수로 구현하였다.
입력값으로는 DataFrame , n=15, m=5, n=3을 입력받아 KDJ Stochastic 지표를 계산한 다음 DataFrame에 추가해준 뒤 리턴해 준다.
'''

# 일자(n,m,t)에 따른 Stochastic(KDJ)의 값을 구하기 위해 함수형태로 만듬  # def get_stochastic(df, n=15, m=5, t=3):
def get_stochastic(df, n=25, m=6, t=6):
    # 입력받은 값이 dataframe이라는 것을 정의해줌
    df = pd.DataFrame(df)

    # n일중 최고가
    ndays_high = df.high.rolling(window=n, min_periods=1).max()
    # n일중 최저가
    ndays_low = df.low.rolling(window=n, min_periods=1).min()

    # Fast%K 계산
    kdj_k = ((df.close - ndays_low) / (ndays_high - ndays_low)) * 100
    # Fast%D (=Slow%K) 계산
    kdj_d = kdj_k.ewm(span=m).mean()
    # Slow%D 계산
    kdj_j = kdj_d.ewm(span=t).mean()

    # dataframe에 컬럼 추가
    df = df.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j).dropna()

    return df

df = get_stochastic(df)
df.head()
print('3 code_df.head() = \n{head}'.format(head=code_df.head()))

##############################################

##############################################

'''
3. plotly를 이용한 Stochastic 차트 그리기
마지막으로 plotly를 이용하여 Stochastic차트를 그려보도록 한다.
plotly에 대한 설명은 이전 포스팅인 4. Plotly를 이용한 캔들차트-Candlestick chart 그리기를 참고하면 된다.
아래의 소스코드를 통해 Stochastic 차트를 그릴 수 있다
'''

import plotly.offline as offline
import plotly.graph_objs as go
from plotly import tools
import plotly.subplots as sp

# jupyter notebook 에서 출력
# offline.init_notebook_mode(connected=True)  # jupyter notebook용

kdj_k = go.Scatter(
    x=df.date,
    y=df['kdj_k'],
    name="Fast%K")

kdj_d = go.Scatter(
    x=df.date,
    y=df['kdj_d'],
    name="Fast%D")

kdj_d2 = go.Scatter(
    x=df.date,
    y=df['kdj_d'],
    name="Slow%K")

kdj_j = go.Scatter(
    x=df.date,
    y=df['kdj_j'],
    name="Slow%D")

trade_volume = go.Bar(
    x=df.date,
    y=df['volume'],
    name="volume")

# data = [kdj_k, kdj_d]
data1 = [kdj_d2, kdj_j]
data2 = [trade_volume]

# data = [celltrion]
# layout = go.Layout(yaxis=dict(
#         autotick=False,
#         ticks='outside',
#         tick0=0,
#         dtick=10,
#         ticklen=8,
#         tickwidth=4,
#         tickcolor='#000'
#     ))

# fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)  # 함수가 dedicate 됭
fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True)  # make_subplots => plotly.subplots.make_subplots로 변경

for trace in data1:
    fig.append_trace(trace, 1, 1)

for trace in data2:
    fig.append_trace(trace, 2, 1)
# fig = go.Figure(data=data, layout=layout)

# offline.iplot(fig)  # jupyter notebook용
offline.plot(fig)

##############################################

