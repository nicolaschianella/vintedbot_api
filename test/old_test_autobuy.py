import requests
import re
import json

def extract_csrf_token(text):
    match = re.search(r'\\"CSRF_TOKEN\\":\\"([^"]+)\\"', text)
    if match:
        return match.group(1)
    else:
        return None

s = requests.Session()

# Chargement des cookies si existant
try :
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
except FileNotFoundError :
    cookies = ""

# print(cookies)

s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

# On charge la page avec les cookies si existant
if cookies:
    req = s.get("https://www.vinted.fr", cookies=cookies)
else:
    req = s.get("https://www.vinted.fr")
csrfToken = extract_csrf_token(req.text)

print('req : ', req.status_code)

# On exécute ceci uniquement pour se log, si pas de cookies existant
token = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsInN1YiI6MTgyNjEwOTU2LCJpYXQiOjE3MDcxMzMxOTUsInNpZCI6IjU1MWFhMDU5LTE3MDcxMzMxOTUiLCJzY29wZSI6InVzZXIiLCJhY3QiOnsic3ViIjoxODI2MTA5NTZ9LCJleHAiOjE3MDcxNDAzOTV9.iOzLWI9H09_Qe4sZe-earzUvxy2mSF3XaX1Ivm8WDclnvEmonNDCukagLRHqID2IW-K8NNJtVWGL-sCYaeVkGc_GUrV7rkaaNumpIexzu03Sbrj07GZsS_EVKJFOyU4uIzwI-vxBnblV8J3Tkp6BAdFw89AqOC783hz8RCKeXyIIwv2hP4LtkXcPk5q4FQbUYGxB1ZM0m_XckDAz6NQIZ426ycPpUbbTLPcitq1PYfSoGZxjkv24sQNlWElZq-XvsHI-nINnJHctzSDPFxqqB61S5rUuGD57ck-m8JpEJJmbxlZeJZ2ayULCLQSfei_OYIr9GieRuMyY8MCfLDQ6OQ"

if not cookies :
    s.headers = {
    "Accept":"application/json, text/plain, */*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization":f"Bearer {token}", # IMPORTANT
    "Referer":"https://www.vinted.fr/",
    "Sec-Ch-Ua":'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile":"?0",
    "Sec-Ch-Ua-Platform":'"Windows"',
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    req4 = s.get("https://www.vinted.fr/member/general/session_from_token", cookies=req.cookies.get_dict())
    print('req4 : ', req4.status_code)

if not cookies:
    # req4
    anon = req4.cookies.get_dict()['anon_id']
    cookies = req4.cookies.get_dict()
else:
    # req car on se relog pas entre temps
    anon = req.cookies.get_dict()['anon_id']
    cookies = req.cookies.get_dict()

### BUY REQUEST
s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'content-type': 'application/json',
    'origin': 'https://www.vinted.fr',
    'referer': 'https://www.vinted.fr/items/4065402982-jeux-tennis-world-tour-switch',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-anon-id': req.cookies.get_dict()['anon_id'],
    'x-csrf-token': csrfToken,
}

params_buy = {"initiator": "buy", "item_id": "4065402982", "opposite_user_id": "13779457"}

buy = s.post("https://www.vinted.fr/api/v2/conversations", data=json.dumps(params_buy), cookies=cookies)

print('buy : ', buy.status_code)

transaction_id = re.search(r'"transaction":{"id":([^"]+),"',buy.text).group(1)
# print(transaction_id)

#### FIRST CHECKOUT

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.vinted.fr',
    'referer': f'https://www.vinted.fr/checkout?transaction_id={transaction_id}',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-anon-id': req.cookies.get_dict()['anon_id'],
    'x-csrf-token': csrfToken,
    'x-money-object': 'true',
}

checkout = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout', cookies=buy.cookies.get_dict())
print('checkout :', checkout.status_code)

uuid = re.search(r'"selected_rate_uuid":"([^"]+)"',checkout.text).group(1)

### SET DELIVERY AT USER ADDRESS

# s.headers = {
#     'authority': 'www.vinted.fr',
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'fr',
#     'content-type': 'application/json',
#     'origin': 'https://www.vinted.fr',
#     'referer': f'https://www.vinted.fr/checkout?transaction_id={transaction_id}',
#     'sec-ch-device-memory': '8',
#     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
#     'sec-ch-ua-arch': '"x86"',
#     'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Linux"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#     'x-anon-id': req.cookies.get_dict()['anon_id'],
#     'x-csrf-token': csrfToken,
#     'x-money-object': 'true',
# }
#
# params_add = {
#     'transaction': {
#         'shipment': {
#             'delivery_type': 1,
#             'rate_uuid': uuid,
#         },
#         'buyer_debit': {},
#         'offline_verification': {},
#     },
# }
#
# pup = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout', data=json.dumps(params_add), cookies = checkout.cookies.get_dict())
# print('pup : ', pup.status_code)

# checksum = re.search(r'"checksum":"([^"]+)"',pup.text).group(1)


#### CHOOSE PICK-UP POINT

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'if-none-match': 'W/"6a123520f9a75da68e831939e619eb4f"',
    'referer': f'https://www.vinted.fr/checkout?transaction_id={transaction_id}',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-anon-id': req.cookies.get_dict()['anon_id'],
    'x-csrf-token': csrfToken,
}

map = s.get('https://www.vinted.fr/api/v2/countries/16/bounds', cookies=checkout.cookies.get_dict())

#### GET PICK-UP POINTS LIST

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'referer': f'https://www.vinted.fr/checkout?transaction_id={transaction_id}',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-anon-id': req.cookies.get_dict()['anon_id'],
    'x-csrf-token': csrfToken,
    'x-money-object': 'true',
}
params = {
    'country_code': 'FR',
    'latitude': '43.297798',
    'longitude': '5.373334',
    'should_label_nearest_points': 'false',
}

pickup = s.get(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/nearby_shipping_options',data=params,cookies=map.cookies.get_dict())

# checksum = re.search(r'"checksum":"([^"]+)"',checkout.text).group(1)


#### PAYMENT

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'content-type': 'application/json',
    'origin': 'https://www.vinted.fr',
    'referer': f'https://www.vinted.fr/checkout?transaction_id={transaction_id}',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-anon-id': req.cookies.get_dict()['anon_id'],
    'x-csrf-token': csrfToken,
}

params_pay = {"checksum":f"{checksum}",
             "browser_attributes":{
                 "language":"en-US",
                 "color_depth":24,
                 "java_enabled":"false",
                 "screen_height":1080,
                 "screen_width":1920,
                 "timezone_offset":-60}
             }

# pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',data=json.dumps(params_pay),cookies = pup.cookies.get_dict())
pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',data=json.dumps(params_pay),cookies = checkout.cookies.get_dict())


print('pay : ', pay.status_code)

# Sauvegarde des cookies de session
with open("cookies.json", "w") as outfile:
    json.dump(buy.cookies.get_dict(), outfile, indent=4)


print('Article acheté')