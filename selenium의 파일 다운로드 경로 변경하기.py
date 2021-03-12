'''
selenium의 파일 다운로드 경로 변경하기
https://cozynow.tistory.com/43
'''

from selenium import webdriver
import time

testUrl = "http://localhost:8080/download/avocado-prices.zip"
driver = "../chromedriver.exe"
screenshot_name = "my_mail_box.png"


options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR") # 한국어!
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

options.add_experimental_option("prefs", {
  "download.default_directory": "C:\Users\Administrator\PycharmProjects\download",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(driver, chrome_options=options)
driver.set_window_size(1920, 1080)
driver.get(testUrl)
driver.implicitly_wait(3)
driver.get_screenshot_as_file(screenshot_name)
driver.implicitly_wait(3)
driver.save_screenshot(screenshot_name)
driver.quit()


