import requests
import re
import json
import fit_pickup as f
def extract_csrf_token(text):
    """
    Extracts the CSRF token

    :param text: Request content
    :return: csrf token
    """
    match = re.search(r'\\"CSRF_TOKEN\\":\\"([^"]+)\\"', text)
    if match:
        return match.group(1)
    else:
        return None

# OPEN SESSION
s = requests.Session()

# OPEN USER'S DEFINED PICKUP POINTS OPTIONS
with open("pu_points.json", "r") as file:
    pick_up_info = json.load(file)

# LOAD COOKIES IF THEY EXIST
try :
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
except FileNotFoundError :
        cookies = ""

s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'DNT': '1',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

# LOG TO VINTED
if cookies:
    req = s.get("https://www.vinted.fr", cookies=cookies)
else:
    req = s.get("https://www.vinted.fr")
csrfToken = extract_csrf_token(req.text)

print('req : ', req.status_code)

# USER TOKEN
token = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsInN1YiI6MTgyNjEwOTU2LCJpYXQiOjE3MDczMjc3NDYsInNpZCI6IjcwZjVlY2QwLTE3MDczMjc3NDYiLCJzY29wZSI6InVzZXIiLCJhY3QiOnsic3ViIjoxODI2MTA5NTZ9LCJleHAiOjE3MDczMzQ5NDZ9.NQHRo2xKLp7GUQ2Glpj35M6FZEzhF_3XGcDxnxoLN_R50W05CT0zKKYIcwiw5E8lAPuc45D_muZHUAz8mUpGW4cKaeG8QcusY5iggJL8HYhikfoQIVwyj5niakwfKJHpDgOcmNfjSPq3fkLkYcGqVq-dSkq0wDijiNwk3xpdGRvmHdLpXwGDGAF7bmGv2M5MRe78HgYlRjkl_n9mGYIxSoJbVFnS7FcYYT0D1KHOUekA7O2Z_-0Aw6FJjYNGmn8EiBe-uv9Vf9t6L-piguRlzceDZo3TVKQ0ia_YhBXoVQsOoKRdCNoP1nf43AfyFQcGrbeZduNLJprHrdHxSPp7gw"

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
    'referer': 'https://www.vinted.fr/items/4083893191-jeu-switch-agatha-christie',
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

params_buy = {"initiator": "buy",
              "item_id": "4083893191",
              "opposite_user_id": "13705098"}

buy = s.post("https://www.vinted.fr/api/v2/conversations", data=json.dumps(params_buy), cookies=cookies)
print('buy : ', buy.status_code)

# GET THE ID OF THE TRANSACTION
transaction_id = re.search(r'"transaction":{"id":([^"]+),"',buy.text).group(1)

# GET DEFAULT PARAMETERS FOR THE SHIPPING PROCESS
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

# GET THE DEFAULT PICK UP POINT UUID's
rate_uuid, root_rate_uuid = f.fit_uuid(checkout.text)

# SEARCH FOR NEARBY AVAILABLE PICK UP POINTS
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
    'latitude': pick_up_info[0]['latitude'],
    'longitude': pick_up_info[0]['longitude'],
    'should_label_nearest_points': 'false',
}

pickup = s.get(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/nearby_shipping_options',data=params,cookies=checkout.cookies.get_dict())
print('pickup : ', pickup.status_code)

# GET DATA FOR THE CHOSEN PICK UP POINT
new_uuid, pup_code, trans_code = f.fit_pup(json.loads(pickup.text)['nearby_shipping_points'], "pu_points.json")

# REPLACE DEFAULT DATA BY THE CHOSEN PICK UP POINT
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

new_data = {
    "transaction":{
        "shipment":{
            "package_type_id":trans_code,
            "pickup_point_code":pup_code,
            "rate_uuid":rate_uuid,
            "point_uuid":new_uuid,
            "root_rate_uuid":root_rate_uuid
        },
        "buyer_debit":{},
        "offline_verification":{}
    }
}

new_infos = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout',data=json.dumps(new_data),cookies=pickup.cookies.get_dict())

print('update : ', new_infos.status_code)

# GET PAYMENT ID
checksum = re.search(r'"checksum":"([^"]+)"',new_infos.text).group(1)

# PROCESS TO PAYMENT

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
# }
#
# params_pay = {"checksum":f"{checksum}",
#              "browser_attributes":{
#                  "language":"en-US",
#                  "color_depth":24,
#                  "java_enabled":"false",
#                  "screen_height":1080,
#                  "screen_width":1920,
#                  "timezone_offset":-60}
#              }
#
# pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',data=json.dumps(params_pay),cookies = checkout.cookies.get_dict())
#
#
# print('pay : ', pay.status_code)
