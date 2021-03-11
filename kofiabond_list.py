from selenium import webdriver
import time

############################################################################

driver = webdriver.Chrome('../chromedriver.exe')  # chromedriver.exe 파일 위치
url = 'http://www.kofiabond.or.kr/websquare/websquare.html?w2xPath=/xml/subMain.xml&divisionId=MBIS01020020000000&parentDivisionId=MBIS01020000000000&parentMenuIndex=1&menuIndex=1'
driver.get(url)

time.sleep(20)

############################################################################
from selenium.webdriver.support.select import Select

# 잔존기간
select = Select(driver.find_element_by_id("selectbox2_input_0"))
print('select = ', select)
select.select_by_value("3개월")  # Select option value


