import pandas as pd
import openpyxl

# wb = openpyxl.load_workbook("C:\▶01.작업\excel_test.xlsx", data_only=True)
#
# sheet1 = wb["Sheet1"]
#
# for row in sheet1.rows:
# 	for cell in row:
# 		print(cell.value)

# df = pd.read_excel("C:\▶01.작업\excel_test.xlsx", sheet_name="Sheet1", usecols=[0], skiprows=[0])  #특정시트에 col과 row
# df = pd.read_excel("C:\▶01.작업\excel_test.xlsx", sheet_name="Sheet1")  #특 정시트
# df = pd.read_excel("C:\▶01.작업\excel_test.xlsx", None)  # 전체시트

##############################################

# 열이름 확인
# print(df.columns)
# print(df.keys())

# 자료형 확인
# print(df.dtypes)

# 상세정보 확인
# print(df.info())

##############################################

# 전체 시트데이터 출력
# print(df)

# 특정컬럼데이터 출력
# print(df['컬럼1'])

# 컬럼데이터를 지정해서 출력
# print(df[['컬럼3','컬럼2','컬럼1']])

# all_df.to_excel("C:\▶01.작업\excel_test_결과.xlsx", sheet_name="결과")

##############################################

input_file = 'C:\▶01.작업\excel_test.xlsx'
output_file = 'C:\▶01.작업\excel_test_결과.xlsx'

df = pd.read_excel(input_file, None)

all_df = []

for key in df.keys():
    # all_df.append(df[key])  # 전체컬럼
    all_df.append(df[key][['컬럼1','컬럼2']])  # 특정컬럼

data_concatenated = pd.concat(all_df,axis=0,ignore_index=True)

# writer = pd.ExcelWriter(output_file)
writer = pd.ExcelWriter(input_file,mode='a')  # 새로운시트 추가
data_concatenated.to_excel(writer,sheet_name='통합',index=False)
writer.save()




