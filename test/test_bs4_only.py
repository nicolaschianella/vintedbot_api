from bs4 import BeautifulSoup
import time
import requests

start = time.time()

session = requests.Session()
session.headers = {
    "User-Agent": "PostmanRuntime/7.28.4",
    "Host": "www.vinted.fr"
}
r = session.get("https://www.vinted.fr/items/4079209349-guanti-militari")

html = r.text

soup = BeautifulSoup(html, 'html.parser')

carousel = soup.find("div", {"class": "item-photos"})

images = carousel.find_all("img")

for img in images:
    src = img.get("src")
    print(src)

end = time.time()
print(end - start)