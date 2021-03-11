from selenium import webdriver
import time

url = "http://www.kofiabond.or.kr/websquare/popup.html?w2xPath=/xml/Com/pop/BISItmIssInfoPop.xml"
driver = webdriver.Chrome("../chromedriver")  # chromedriver.exe 파일 위치
driver.get(url)

time.sleep(1)

cd = "KR63123638B5"
driver.find_element_by_id('poinput1').send_keys(cd)  # 검색
driver.find_element_by_id('poimage1').click()  # 조회 버튼

time.sleep(1)

result = driver.find_element_by_id("potextbox6").text  # 결과값 리턴
print(result)

driver.close()





