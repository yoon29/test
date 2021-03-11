from selenium import webdriver

# Webdriver 실행
dr = webdriver.Chrome('../chromedriver.exe')
# Webdriver에서 네이버 페이지 접속
dr.get('https://www.naver.com/')

print(dr.current_url)  # 현재 URL 가져 오기
# dr.back()  # 브라우저의 뒤로 버튼 누르기
# dr.forward()  # 브라우저의 앞으로 버튼 누르기
# dr.refresh()  # 현재 페이지 새로 고침
print(dr.title)  # 브라우저에서 현재 페이지 제목
# dr.current_window_handle  # 창 핸들 가져 오기






