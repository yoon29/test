'''
https://tariat.tistory.com/114?category=678887
[로또API 1] 회차별 로또 당첨번호 및 당첨금액 모으기(로또분석, 로또당첨확률계산)

로또 당첨결과 불러오기
나눔로또 싸이트에 공식적으로 오픈되어 있는 것은 아니지만, 특정 URL 뒤에 회차를 입력하면 로또 당첨결과가 json 형태로 제공된다.

* 로또 결과 제공싸이트 주소: http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=+(번호)
예를 들면 http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1 이라고 주소창에 입력하면, 1회차의 로또 당첨 결과가 회신된다.

json으로 회신받은 데이터를 파싱하고, DB에 저장하기 위해 파이썬을 사용하였다.
다른 프로그래밍 언어를 사용해도 되지만, 파이썬은 문법이 쉽고 이미 개발된 패키지들이 많아 쉽게 작업할 수 있다.
파이썬에 대한 자세한 내용은 아래 포스팅을 참조해보자.
( 참조: 파이썬(python) - 아나콘다(anaconda) 배포판 설치하기 )

파이썬으로 로또 번호를 수집하기 위해 우선 필요한 모듈을 불러온다.
위의 URL에 접속해서, 데이터를 수집하는 부분은 함수로 만들었다.
수집하고 하는 회차를 입력 파라미터로 넣으면, 해당 회차의 로또 당첨결과를 수집할 수 있다.
수집한 데이터는 json.loads() 함수로 파이썬 딕셔너리 자료형으로 바꿨다.
그리고, from_dict를 통해 딕셔너리 자료형을 판다스 데이터프레임으로 바꾼다.
행과 열이 바꿔져 있어 transpose 함수를 이용해 행과 열을 바꿔준다.

마지막으로 반복문을 이용하여 1회부터 100회까지의 당첨결과를 수집하였다.
수집한 데이터는 SQLite DB로 저장하였다.
SQLite는 개인 컴퓨터에서 사용하기 좋은 DB프로그램이다.
SQLite에 대한 자세한 내용이 궁금하다면, 아래 포스팅을 참조해보자.
( 참조: SQLite라는 DB로 저장하기, SQLite3 파이썬 pandas 데이터프레임으로 불러오기, SQLite의 기본 문법-CREATE, SELCT, INSERT, DELETE)

로또 당첨 결과를 분석해 당첨확률을 높이실 수 있는 분들이 있다면, 한 번 도전해 보는 것도 좋을 것 같다. 로또에 당첨될 지는 모르겠지만 확률 공부는 제대로 하지 않을까 하고 생각한다.
수집된 데이터를 가지고 역대 당첨금액 통계를 구해봤다. 자세한 내용이 궁금하다면, 아래 포스팅을 참조해보자.
( 참조: 로또의 역대 당첨금액 통계 ) - http://tariat.tistory.com/126

'''

# 인코딩선언
# coding=utf-8

import pandas as pd
import sqlite3
from tqdm import tqdm
from urllib.request import urlopen
import json

def lotto(chasu):
    url="http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="+str(chasu)
    result_data = urlopen(url)
    result = result_data.read()

    data = json.loads(result)
    data_1 = pd.DataFrame.from_dict(data,orient='index')
    data_1=data_1.transpose()

    return data_1

# # DB저장
# for i in tqdm(range(1,100)):
#     data_1=lotto(i)
#     if data_1.loc[0,"returnValue"]=="fail":
#         pass
#     else:
#         con = sqlite3.connect("./data/lotto.db")
#         data_1.to_sql('lent', con, if_exists='append', index=False)
#         con.close()

# # 화면출력
# df = pd.DataFrame()
# for i in tqdm(range(1,10)):
#     data_1=lotto(i)
#     print('data_1 = \n{arg1}'.format(arg1=data_1))
#     if data_1.loc[0,"returnValue"]=="fail":
#         pass
#     else:
#         df = df.append(data_1)
#         # df = pd.concat([df, data_1])
#
# # print('df.head() = \n{arg1}'.format(arg1=df.head()))
# print('df = \n{arg1}'.format(arg1=df))

# main 사용
if __name__ == "__main__":
    lotto_db = pd.DataFrame()
    for i in tqdm(range(1, 10), mininterval=1):
        data_1 = lotto(i)  # 인코딩 사용해야햠
        lotto_db = pd.concat([lotto_db, data_1])

    print('lotto_db = \n{arg1}'.format(arg1=lotto_db))


