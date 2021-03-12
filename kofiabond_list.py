
############################################################################
from selenium import webdriver
import time

driver = webdriver.Chrome('../chromedriver.exe')  # chromedriver.exe 파일 위치
# find_element_by_ 함수를 사용해 element를 찾을때 최대 30초까지 기다립니다.
driver.implicitly_wait(10)

url = 'http://www.kofiabond.or.kr/websquare/websquare.html?w2xPath=/xml/subMain.xml&divisionId=MBIS01020020000000&parentDivisionId=MBIS01020000000000&parentMenuIndex=1&menuIndex=1'
driver.get(url)

# time.sleep(1)

############################################################################

# # 현재 웹페이지에서 iframe이 몇개가 있는지 변수에 넣고 확인해 봅니다.
# iframes = driver.find_elements_by_tag_name('iframe')
# print('현재 페이지에 iframe은 %d개가 있습니다.' % len(iframes))

# iframe 페이지로 전환
# driver.switch_to.frame(0)
driver.switch_to.frame('maincontent')

# # 현재 페이지 소스 가져오기
# import bs4
# html = driver.page_source
# # BeautifulSoup로 페이지 소스 파싱
# bs = bs4.BeautifulSoup(html,"html.parser")
# print('html =\n', bs)

############################################################################
from selenium.webdriver.support.select import Select

# 잔존기간
# source = driver.find_element_by_id("selectbox2_input_0")
source = driver.find_element_by_xpath("//*[@id='selectbox2_input_0']")
print('source =', source.text)

select = Select(source)
print('select = ', select)
# select.select_by_value("3개월")  # Select option value
select.select_by_visible_text("3개월")  # select visible text

# driver.close()



