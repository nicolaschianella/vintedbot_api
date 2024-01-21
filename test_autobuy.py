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
token = ""

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

### BUY REQUEST
s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'content-type': 'application/json',
    'origin': 'https://www.vinted.fr',
    'referer': 'https://www.vinted.fr/items/4007479751-bo-te-animal-crossing-vide',
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

params_buy = {"initiator": "buy", "item_id": "4007479751", "opposite_user_id": "29922603"}

if not cookies:
    # req4
    buy = s.post("https://www.vinted.fr/api/v2/conversations", data=json.dumps(params_buy), cookies=req4.cookies.get_dict())
else:
    # req car on se relog pas entre temps
    buy = s.post("https://www.vinted.fr/api/v2/conversations", data=json.dumps(params_buy), cookies=req.cookies.get_dict())

print('buy : ', buy.status_code)

transaction_id = re.search(r'"transaction":{"id":([^"]+),"',buy.text).group(1)
# print(transaction_id)

### SELECT PICK-UP POINT

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
# param_pup = {"transaction":{
#                     "shipment":{
#                         "package_type_id":118,
#                         "pickup_point_code":"1619524",
#                         "rate_uuid":"63c43f53-3a20-4b7e-8558-39742cac729b",
#                         "point_uuid":"361d081a-1177-45a5-af7b-768adaa8f547",
#                         "root_rate_uuid":"77261877-afa1-4cf0-ad75-7ecac6d2a875"
#                     },
#                     "buyer_debit":{},
#                     "offline_verification":{}
#                 }
#             }
#
# pup = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout',params=json.dumps(param_pup),cookies=buy.cookies.get_dict())
# print("pup : ", pup.status_code)

### SET USER ADDRESS

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
    'x-money-object': 'true',
}

params_add = {"transaction":{
        "shipment":{
            "delivery_type":1,
            "rate_uuid":"63c43f53-3a20-4b7e-8558-39742cac729b"
        },
        "buyer_debit":{},
        "offline_verification":{}
    }
}

pup = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout', params=json.dumps(params_add), cookies = buy.cookies.get_dict())
print('pup : ', pup.status_code)

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

params_pay = {"checksum":"33e9ee3a5b53f518571984669d5f79ec",
             "browser_attributes":{
                 "language":"en-US",
                 "color_depth":24,
                 "java_enabled":"false",
                 "screen_height":1080,
                 "screen_width":1920,
                 "timezone_offset":-60}
             }

pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',params=json.dumps(params_pay),cookies = pup.cookies.get_dict())
print('pay : ', pay.status_code)

# Sauvegarde des cookies de session
with open("cookies.json", "w") as outfile:
    json.dump(buy.cookies.get_dict(), outfile, indent=4)


print('here')

# url = "https://www.vinted.fr/items/4007663345-jeu-switch-lol?homepage_session_id=65448000-bf41-4ee1-8b5d-38f9180e19b8"
