from selenium import webdriver
import time

driver = webdriver.Chrome("../chromedriver")  # chromedriver.exe 파일 위치
url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"  # 영화목록
driver.get(url)

time.sleep(3)

############################################################################
# test html

'''
<td class="title">
    <div class="tit3">
        <a href="/movie/bi/mi/basic.nhn?code=163834" title="원더 우먼 1984">원더 우먼 1984</a>
    </div>
</td>

xpath = /html/body/div/div[4]/div/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div
'''

############################################################################
# test1 : find_element_by_class_name 사용

find_class = driver.find_elements_by_class_name("tit3")  # element/elements 차이
print(find_class)  # [<selenium.webdriver.remote.webelement.WebElement (session="8581b4f544f4941be2ffa661bb77c6e4", element="a5eb5711-acad-4b8d-8c69-c8e0f0b3bb95")>, ...]
# print(len(find_class))  # 1

for tag in find_class:
    find_element = tag.find_element_by_tag_name("a")
    print(find_element)  # [<selenium.webdriver.remote.webelement.WebElement (session="8581b4f544f4941be2ffa661bb77c6e4", element="dd22e59c-e3b8-4373-bbc0-e858b76b8d34")>]
    # print(len(find_element))  # 1

    print(find_element.get_attribute("href"))  # https://movie.naver.com/movie/bi/mi/basic.nhn?code=163834
    print(find_element.get_property("href"))  # https://movie.naver.com/movie/bi/mi/basic.nhn?code=163834




############################################################################
# test2 : xpath 사용

# list = driver.find_element_by_xpath("/html/body/div/div[4]/div/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div")
# print(list)
#
# element = list.find_elements_by_tag_name('a')
# print("element = ")
# print(element)
# print(len(element))
# print(element[0].tag_name)  # a
# print(element[0].get_attribute("href"))  # https://movie.naver.com/movie/bi/mi/basic.nhn?code=163834
# print(element[0].get_property("href"))  # https://movie.naver.com/movie/bi/mi/basic.nhn?code=163834
# print(element[0].text)  # 원더 우먼 1984

############################################################################

driver.close()


