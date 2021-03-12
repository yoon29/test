
############################################################################
from selenium import webdriver
import time

driver = webdriver.Chrome('../chromedriver.exe')  # chromedriver.exe 파일 위치

# Selenium은 기본적으로 웹 자원들이 모두 로드될때까지 기다려주지만,
# 암묵적으로 모든 자원이 로드될때 까지 기다리게 하는 시간을 직접 implicitly_wait을 통해 지정할 수 있다.
driver.implicitly_wait(10)

url = 'http://www.kofiabond.or.kr/websquare/websquare.html?w2xPath=/xml/subMain.xml&divisionId=MBIS01020020000000&parentDivisionId=MBIS01020000000000&parentMenuIndex=1&menuIndex=1'
driver.get(url)

# 만약 XPath를 찾을 수 없다는 에러가 나오면
# time 을 import 하여 Facebook 페이지가 원활히 로딩이 끝날때 까지 time.sleep(5)로 5초정도 기다려주면 해결됩니다.
time.sleep(1)

############################################################################

# # 현재 웹페이지에서 iframe이 몇개가 있는지 변수에 넣고 확인해 봅니다.
# iframes = driver.find_elements_by_tag_name('iframe')
# print('현재 페이지에 iframe은 %d개가 있습니다.' % len(iframes))

# iframe 페이지로 전환
# driver.switch_to.frame(0)
driver.switch_to.frame('maincontent')

# 현재 페이지 소스 가져오기
# driver.page_source : 브라우저에 보이는 그대로의 HTML, 크롬 개발자 도구의 Element 탭 내용과 동일.
# requests 통해 가져온 req.text: HTTP요청 결과로 받아온 HTML, 크롬 개발자 도구의 페이지 소스 내용과 동일.
# 위 2개는 사이트에 따라 같을수도 다를수도 있습니다.
html = driver.page_source

# BeautifulSoup로 페이지 소스 파싱
# import bs4
# bs = bs4.BeautifulSoup(html,"html.parser")
# print('html =\n', bs)

############################################################################
'''
from selenium.webdriver.support.select import Select
select=Select(driver.find_element_by_id("sch_bub_nm"))
select.select_by_index(1) #select index value
select.select_by_visible_text("Case2") # select visible text
select.select_by_value("000201") # Select option value

<select class="w2selectbox_native_select" id="selectbox2_input_0">
	<option>전체</option>
	<option>3개월</option>
	<option>6개월</option>
	<option>9개월</option>
	<option>1년</option>
	<option>1년 6개월</option>
	<option>2년</option>
	<option>2년 6개월</option>
	<option>3년</option>
	<option>5년</option>
	<option>10년</option>
	<option>20년</option>
</select>

'''
from selenium.webdriver.support.select import Select

# ■■■ 잔존기간 선택
# source = driver.find_element_by_id('selectbox2_input_0')
source = driver.find_element_by_xpath('//*[@id="selectbox2_input_0"]')
print('source =', source.text)

select = Select(source)
print('select = ', select)
# select.select_by_value("3개월")  # Select option value
select.select_by_visible_text("3개월")  # select visible text


# ■■■ 조회버튼 클릭
driver.find_element_by_xpath('//*[@id="image21"]').click()
time.sleep(20)

# ■■■ 엑셀다운로드 클릭
driver.find_element_by_xpath('//*[@id="imgExcel"]').click()


# driver.close()

