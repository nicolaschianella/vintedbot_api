from backend.utils.vinted_api import Vinted

vinted = Vinted()

# search(url, number_of_items, page_number)
items = vinted.items.search("https://www.vinted.fr/vetement?order=newest_first&price_to=60&currency=EUR&search_text=ralph%20lauren%20hommes",10,1)
# items = vinted.items.search("https://www.vinted.fr/vetement?order=newest_first&currency=EUR",10,1)
#returns a list of objects: item
item = items[1]

import urllib.request

from PIL import Image

urllib.request.urlretrieve(item.photo, "test.png")

img = Image.open("test.png")

img.show()

print('here')