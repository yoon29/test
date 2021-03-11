
import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"

html = requests.get(url).text
# print(html)

soup = BeautifulSoup(html, "html.parser")
tags = soup.find_all("div", {"class":"tit3"})
print(tags)

for idx, tag in enumerate(tags):
    tag.a.get_text()
    print(idx + 1, tag.a.get_text())




