from backend.utils.items.items import Items

vinted = Items()

# search(url, number_of_items, page_number)
# items = vinted.search("https://www.vinted.fr/vetement?search_text=Raph%20lauren%20Hommes&order=newest_first&price_from=0&currency=EUR&price_to=60&country_id[]=FR",5000,2)
items = vinted.search("https://www.vinted.fr/vetement?search_text=Ralph%20Lauren%20Hommes&order=newest_first&currency=EUR&price_to=60",5000,1)

# items = vinted.items.search("https://www.vinted.fr/vetement?order=newest_first&currency=EUR",10,1)
#returns a list of objects: item
item = items[0]

import urllib.request

from PIL import Image

urllib.request.urlretrieve(item.photo, "test.png")

img = Image.open("test.png")

img.show()

print('here')