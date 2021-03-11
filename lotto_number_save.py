import pandas as pd
import requests
from tqdm import tqdm
import json

def getLottoWinInfo(minDrwNo, maxDrwNo):
    drwtNo1 = []
    drwtNo2 = []
    drwtNo3 = []
    drwtNo4 = []
    drwtNo5 = []
    drwtNo6 = []
    bnusNo = []
    totSellamnt = []
    drwNoDate = []
    firstAccumamnt = []
    firstPrzwnerCo = []
    firstWinamnt = []
    for i in tqdm(range(minDrwNo, maxDrwNo+1, 1)):
        req_url = "http://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)
        req_lotto = requests.get(req_url)
        lottoNo = req_lotto.json()

        drwtNo1.append(lottoNo['drwtNo1'])
        drwtNo2.append(lottoNo['drwtNo2'])
        drwtNo3.append(lottoNo['drwtNo3'])
        drwtNo4.append(lottoNo['drwtNo4'])
        drwtNo5.append(lottoNo['drwtNo5'])
        drwtNo6.append(lottoNo['drwtNo6'])
        bnusNo.append(lottoNo['bnusNo'])
        totSellamnt.append(lottoNo['totSellamnt'])
        drwNoDate.append(lottoNo['drwNoDate'])
        firstAccumamnt.append(lottoNo['firstAccumamnt'])
        firstPrzwnerCo.append(lottoNo['firstPrzwnerCo'])
        firstWinamnt.append(lottoNo['firstWinamnt'])

        lotto_dict = {
            "추첨일":drwNoDate
            , "Num1":drwtNo1
            , "Num2":drwtNo2
            , "Num3":drwtNo3
            , "Num4":drwtNo4
            , "Num5":drwtNo5
            , "Num6":drwtNo6
            , "bnsNum":bnusNo
            , "총판매금액":totSellamnt
            , "총1등당첨금":firstAccumamnt
            , "1등당첨인원":firstPrzwnerCo
            , "1등수령액":firstWinamnt
        }

    df_lotto = pd.DataFrame(lotto_dict)
    return df_lotto

# main 사용
if __name__ == "__main__":

    lotto_df = getLottoWinInfo(1,100)

    # 엑셀저장
    lotto_df.to_csv("lotto_win_info.csv", index=False)

    # 엑셀로드
    # pd.read_csv("lotto_win_info.csv")

    num_list = list(lotto_df['Num1']) + list(lotto_df['Num2']) + list(lotto_df['Num3']) + list(lotto_df['Num4']) + list(
        lotto_df['Num5']) + list(lotto_df['Num6'])

    # 당첨번호 중 가장 많이 나온 번호
    from collections import Counter
    count = Counter(num_list)
    common_num_45 = count.most_common(45)
    print('common_num_45 = \n{arg1}'.format(arg1=common_num_45))

    # 가장 많이 당첨번호로 등장한 숫자 10개만 뽑아보면
    common_num_10 = count.most_common(10)
    print('common_num_10 = \n{arg1}'.format(arg1=common_num_10))

    # 가장 1등 당첨금 수령액이 높았던 날 Top 10
    lotto_df.sort_values(by=['1등수령액'], axis=0, ascending=False).head(10)
    print('1 lotto_df = \n{arg1}'.format(arg1=lotto_df))

    # 가장 1등 당첨자가 많았던 날 Top 10
    lotto_df.sort_values(by=['1등당첨인원'], axis=0, ascending=False).head(10)
    print('2 lotto_df = \n{arg1}'.format(arg1=lotto_df))



