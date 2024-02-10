from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

start = time.time()

playwright = sync_playwright().start()

browser = playwright.firefox.launch()

page = browser.new_page()
page.goto("https://www.vinted.fr/items/4079209349-guanti-militari")

#page.screenshot(path="example.png")

################# THESE TWO TO COMMENT IF NO COOKIES TO HANDLE
page.wait_for_selector("#onetrust-reject-all-handler")
page.click('#onetrust-reject-all-handler')

# page.wait_for_timeout(3000)
page.locator("#content > div > section > div > figure.item-description.u-flexbox.item-photo.item-photo--1 > div > div > img").click()

# page.click('#onetrust-reject-btn-handler')

html = page.content()

soup = BeautifulSoup(html, 'html.parser')

carousel = soup.find("div", {"class": "image-carousel"})

images = carousel.find_all("img")

for img in images:
    src = img.get("src")
    print(src)

# page.screenshot(path="example.png")
browser.close()

playwright.stop()

end = time.time()
print(end - start)