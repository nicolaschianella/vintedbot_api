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
token = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsInN1YiI6MTgyNjEwOTU2LCJpYXQiOjE3MDY0NDA1MjIsInNpZCI6IjgwMDgwNjEyLTE3MDY0NDA1MjIiLCJzY29wZSI6InVzZXIiLCJhY3QiOnsic3ViIjoxODI2MTA5NTZ9LCJleHAiOjE3MDY0NDc3MjJ9.pglqewBXHuttmCEIaJGMBpM9nQEwX-kpY1gpdqynVvdH09h1SkSN6wQFSSN0RVn0G1zCvTYe-ZuI3BeJXkVJi6qWdYLVpTVRpWlUJydNOjTLnM2tF32Ft032lyCVbkGeTqQE1bjaAOQLBAXGkwcQSzFyR4qpxp1mSJEQ1kyZ6dZ96yikb-s4cba3JOJf3r9M2MrPphGba0bf8UoboRn6OlFaznd9F0fFiBc-Wpa1O2sBjPPtTgCsukzTXtwu5bk1Z6XJi7Scm0dAlFFZpxc6FnTkqsV-KLhASn6v8gDYSoRq-De-8twG5_-FRPaXWM0VFqx2h2mRNXkGvsVPP85DiQ"

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


### GET CREDIT CARD INFOS

if not cookies:
    # req4
    anon = req4.cookies.get_dict()['anon_id']
    cookies = req4.cookies.get_dict()
else:
    # req car on se relog pas entre temps
    anon = req.cookies.get_dict()['anon_id']
    cookies = req.cookies.get_dict()

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'if-none-match': 'W/"887824d2c853545bd6b7040e211f1d5c"',
    'referer': 'https://www.vinted.fr/',
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

ccard = s.get("https://www.vinted.fr/api/v2/payments/credit_cards", cookies=cookies)

print('Credit card : ', ccard.status_code)


### GET PAYMENT METHOD

s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'if-none-match': 'W/"4b48902588dc74d2a5ad6618f16bfcf4"',
    'referer': 'https://www.vinted.fr/',
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

pay_meth = s.get('https://www.vinted.fr/api/v2/extra_services/pay_in_methods', cookies = ccard.cookies.get_dict())

print('Pay in method : ', pay_meth.status_code)


### BUY REQUEST
s.headers = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'content-type': 'application/json',
    'origin': 'https://www.vinted.fr',
    'referer': 'https://www.vinted.fr/items/4032042766-jeux-switch-neuf',
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

params_buy = {"initiator": "buy", "item_id": "4032042766", "opposite_user_id": "126782861"}

buy = s.post("https://www.vinted.fr/api/v2/conversations", data=json.dumps(params_buy), cookies=pay_meth.cookies.get_dict())


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

### SET DELIVERY AT USER ADDRESS

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
            "rate_uuid":"371b956c-fe5a-4760-9a52-7a3e26d9e590" # IL VARIE DONC A VOIR COMMENT LE RECUP
        },
        "buyer_debit":{},
        "offline_verification":{}
    }
}

pup = s.put(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout', params=json.dumps(params_add), cookies = buy.cookies.get_dict())
print('pup : ', pup.status_code)

#### PAYMENT

cookies = {
    'v_udt': 'MXdYdldzK1ZQVTNqRWVnbFQyWHg0RDNqNU9Kbi0tdEhMYkRIMVI0Vm9LbVNwbS0tYTZLd3NwSEZWdExFalhmak1ZM3J4UT09',
    'anonymous-locale': 'fr',
    'OptanonAlertBoxClosed': '2024-01-13T18:55:13.196Z',
    'eupubconsent-v2': 'CP4UaxgP4UaxgAcABBENAjEsAP_gAAAAAChQg1NX_H__bX9j8Xr16ft0eY1f99j7rsQxBhfJk-4FyLvW_JwX32EzNA26pqYKmRIEu3ZBIQFlHIHURUigaogVryHsYkGcgTNKJ6BkgFMRc2cYCF5vmQlD-QKY5_p_d3f52T-9_dv83dzzz8VHv3e5fmclcICdA58tDfn9bRKb-5IOd_78v4v09FgAAAAAABAAAAAAAAAAAAAAAAAAABcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAABQSB8AAgABcAFAAVAA4AB4AEAAMIAZABqADwAIgATAAqgBvAD0AH4AQkAhgCJAEcAJYATQAw4BlAGWANkAd8A9gD4gH2AfoBAACKQEXARgAjQBKQCggFQAKuAXMAxQBogDaAG4AOIAkQBOwChwFHgKRAWwAuQBd4C8wGDAMNAZIAycBnMDWANZAbeA3UBwQDkwHLgPHAhCEAOgAOABIAOcAg4BPwEegJFASsAm0BT4CwgF5AMQAYtAyEDIwGjANTAbQA24BukDyQPKAfIA_cCAgEDIIIggmBBgCFYELhwDMABEADgAPAAuACQAH4AaABzgDuAIBAQcBCACIgE_AKgAXoA44B0gEegJFASsAmIBMoCbQFIAKTAVUArsBZQC1AF0AMQAYsAyEBkwDRgGmgNTAa8A2gBtgDbgHHwOdA5-B5IHlAPiAfbA_YD9wIHgQRAgwBBsCFY6CaAAuACgAKgAcABAAC6AGAAagA8ACIAEwAKsAXABdADEAGYAN4AegA_QCGAIkASwAmgBRgDDAGUANEAbIA7wB7QD7AP0Af8BFAEYAJSAUEAq4BYgC5gF5AMUAbQA3ABxADqAIvASIAlQBMgCdgFDgKPAU0AqwBYsC2ALZAXAAuQBdoC7wF5gL6AYMAw0BjwDJAGTgMqAZYAzkBogDVQGsANvAbqA4sByYDlwHjgPrAgCBC0gATAAQAGgAc4BYgEegJtAUmAvIBqYDbAG3AOfgeSB5QD4gH7AQPAgwBBsCFZCBIAAsACgALgAYgBMACmAFUALgAYgA3gB6AEcAO8Af4BFACUgFBAKuAXMAxQBtADqAJUAU0AsUBaIC4AFyAMnAZyA0QBqoDgAHjgQoAhaSgQAAIAAWABQADkAMAAxAB4AEQAJgAVQAuABigEMARIAjgBRgDZAHeAPwAq4BigDqAIvASIAo8BYoC2AF5gMnAZyA1gBt4DgAIHkgB4AFwB3AEAAKgAj0BIoCVgE2gKTAWUAxYB5QD9wIIgQYKQNwAFwAUABUADgAIIAYABqADwAIgATAApABVADEAGYAP0AhgCJAFGAMoAaIA2QB3wD8AP0AiwBGACUgFBAKuAXMAvIBigDaAG4AReAkQBOwChwFigLYAXAAuQBdoC8wF9AMNAZIAycBlgDOYGsAayA28BuoDggHJgOXAeOBCECFpQBGABcAEgAjgBzgDuAIAASIAsQBdQDXgHbAP-Aj0BIoCYgE2gKQAU-ArsBdAC8gGLAMmAaIA1MBrwDygHxQP2A_cCBgEDwIJgQYAg2BCsA.f_wAAAAAAAAA',
    'OTAdditionalConsentString': '1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.320.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1423.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.16831',
    '_lm_id': '4FML72WY7XOY3Y3V',
    '_gcl_au': '1.1.660184047.1705172114',
    '_ga': 'GA1.1.855019893.1705172114',
    '_fbp': 'fb.1.1705172114764.1858564670',
    'anon_id': '2402f1b4-04dd-41ab-a2a3-fd3e2da4f23b',
    'last_user_id': '1',
    'domain_selected': 'true',
    'RoktRecogniser': '4340f639-14ad-492a-bf91-264239d1358d',
    'beopid': '5589c120-ebb3-4277-852f-8d301b1437db',
    'seller_header_visits': '6',
    '_cc_id': '3dfd23b302f9a48611b09779cf2daeff',
    '_pbjs_userid_consent_data': '3524755945110770',
    'panoramaId_expiry': '1706460934410',
    'panoramaId': '9d4bc64aa273b71fb58867718303e32246b046d67c8efd4694d0189d6065184d',
    'panoramaIdType': 'panoIndiv',
    '__cf_bm': 'kbMxSWhE6b17eI_9FMEUPwAabIKWLv3VaLidnYesGbA-1706440479-1-ARSQ8B1grXoCHxkQUDRrGN1sFoPr2j8KzdFtKjgifQMIMihytH6GiNx2QYDcP70jDc9Gd6QaVizP+lKkbohHcT82AOXgQqnE0xL9ZAMAkaYa',
    'cf_clearance': '44LFE5__L..sfieHNIKZEXbKtUtojfQjmmYjjRB8C.U-1706440484-1-AQFZcZEEkuyS+PDn7w9ygnA3bimCr5vB+/IG7KmFaqZpXQ7C0ue3C3C2Sl84cWVJavThzXPOVm/MnnwZZemCNJc=',
    '__gads': 'ID=9b9ae254f2130525:T=1705172166:RT=1706440492:S=ALNI_MaZ-J4VnILzp2ndG2EmI03Sb9Mvxg',
    '__gpi': 'UID=00000cf5fa761679:T=1705172166:RT=1706440492:S=ALNI_MYTOKcR7rubkLeCVjK2aF8gRWsx9Q',
    'cto_bundle': '5pfj7l9mZHNNNDZjNXN0d0lnWkp3bU9HYklYRlRxSjluYzBWJTJGVVVmUzBwSlRNNWZBNlQlMkZsSjV0d3N5YlROb0hJMm5raWZjaTdGdlNzYVVOeUltTXRLWkxNWFYxMzRRaUlmSENVVTNTTHg0anF4SSUyRkhqb2V2UUF2aHgxYkZmek13WDd4dG1ZZU9VZFA1aVZhVkFzMmR6Z0FKMWclM0QlM0Q',
    'v_uid': '182610956',
    'v_sid': '80080612-1706440522',
    'viewport_size': '778',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Jan+28+2024+12%3A29%3A49+GMT%2B0100+(Central+European+Standard+Time)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=182610956&interactionCount=97&hosts=&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CV2STACK42%3A1%2CC0015%3A1&geolocation=FR%3BPAC',
    'ab.storage.sessionId.5ab85466-ca8e-4ddb-807d-857336edea71': '%7B%22g%22%3A%223c4adc71-df52-1a89-557a-8f6c7ca4eded%22%2C%22e%22%3A1706443189507%2C%22c%22%3A1706440483627%2C%22l%22%3A1706441389507%7D',
    '_uetsid': '6edfafb0bdce11eeaa86bb2e93b28f99',
    '_uetvid': '48d8e7b0b24511eebf685152ca95626c',
    '_ga_ZJHK1N3D75': 'GS1.1.1706440481.17.1.1706441389.0.0.0',
    '_ga_8H12QY46R8': 'GS1.1.1706440481.17.1.1706441390.0.0.0',
    'datadome': 'j1vEQn_NSy8zfI8TutkHFJKDT9jLNF6x3loLpCeFDpqo6RZNpe5FFksTCYj6FWq5FJHvi_cWEfb8fMV~SMS8Q5px26hXlvRLkBypvBT~OBQO2uLBJ1gYBw1UKrRExLpF',
    '_vinted_fr_session': 'cURsaHBZMUpEdWVnUEFKN0YreVhsaFZ6TWkvdVRJQXFUaisvSnR5aUlNK0U3cHQ5bEpROUs5blJNajJSUXVaSmhTSGliN0ZPM3ZlUDYrV1lCN1VXOWIyNG5JczNZSzQ5Vmg3R1ExUWRlUVRybFVtOXN6MDQxWWU0NGd6bGNNNzNsTFplNEZZN3JvR3JUamZaSll6MUhQZFFVUXNEZnNWbUlmaGo5SWhzZFFnUno1YmlDaldueUZDSnA2YXBKNXJmR0VtU09nd2NTYk16Q0FiNktObzE2V3hOWlZIN3dyVWErcFlHNXRmN1MrVDFwbHJKNjdqRHV1b1h0bHBFK20zZXc0TkVMUTNQNUNvRjlGK3Jtdkprdm1zVUcxZ1FnSUlCbFRwOHJOak1hL3N3TUlHcCtXQkE1TG1BZmh1ZFo5RWVpUkt5UElsOGt5UldnTnJPM2V0UkxsT2w5QXpFUjhOY2hoTFpzR25pNVZEcGZuUEdmUkxsVlpEYlFzdnJvYVg4T1VlTnpmbkdlV2xCR2l0MmpyaGM2UThiVjF6QVBia2RxeDZFS3o2SVhOTENGYmlGSHRGYlB5eDhOb3A3SGcwWHFTUk5uSFZDa09taW1rWGd3YnVNYlZtYm1QeFlTMmVDb2Z1WVFVa0FIYkpTRHBPM0ltZXZaTldySTZ6b2NxV0dLMHFFY0g3eWN6OFhwM0RVZUN1aWdPZmh1VU5jRkk1cnBLNFJuWUxlMlZLaWtna3VORjlmUkp0S1NEcVFJNVBpVEFaZWFSNlhMV1MwaU9nZ3lOUmFsaS8wbXRsS1UrQTJHRTVvdUt3Yk5oWFM5VjRXOW52dStuVVRheUw2TmdvblkwT0ZZYUsvcHR3WndqalVUTDhVU2lNWkEyR3ZicWt4SVZMdVZWWjBpKy9NMlgwUW5DdzUwVzlEQ3ZmZy83d0dtR29Bd3RXUDJqV28yeGxZNi9sR0ZoNStaRExGZ0dWeU03K2xIbHA1cms0Q1hYSERPaTBpQzVLRzZuc0M0cDFSWmt4cStCWTNtZ1FyZEVKd3U3bU5PSFRNaWxveW1KdmRvcHM1SWR6eVNVclFGYkVFVnROU05PYk13T3VrRWJEbmRuZmdTWnRMSzltNEJpd0xDSDlUQ3ZnRStLQ0IrVVgvbVRkeXVZT0g5ZXQrU2NvdWN2OUdCdi9ORGk2OTVBcU1QQjI0dFBab2lNUFhIVGtMQ0haOHhidW5vV2twb05vSWR1cFB5RjNwbW1Bdzh2SnEyc2tWUGlzb1BvdkxBTUJJUlhXK2tvTE92eGtDcUd2S21WWk0wd3FqMFBwak9YWW8vZk9talJWL1VhLzhPeWp2K05Ud3k2aHVQaE9QbDJsR1VnbCtka2ZPOEpOdHpmd2RUdndpSjI0WUp5bE9PRFlLZXVlSHpKV1JCN1ZlNFZBMzNNQ3U0b25BMVpCYlNDTWhKVXQrSUh5bkVqeU9GL1dNUzNQQmNxOUdlTlJTc2lVL2NZQ3cyTTEyOTRZMDRveXBmc29KblZXanlGdDlTUWpwQlUrSTY1Yy96T1lRTk5jb3FGYmRKOXkyVUVhWVM2Nkt1SmY2K1M3MFdYeVI2bVd2OWJJeEdJVktOZllEWUtCSE95U2dSZCt1SnNnR1hXN3Y3S2FSVlF1a25tangyeStoaXpvbHpuVy9yMW5raUxUbEl5TFBzaWE5aG90UkZjSk93N2RGZ0dOL2tMMk9PMkJMakZSQ0t3MnBUMitwc3BKZFFFVGJFSS9CVXg5bFNKSVNkM1VZV3RUSFFJam90TE5iWkVrRmpIc1JPdVdGVnlibHdZUWNuQkZGZ0VpbDFYVEVTaTIxa1BrS1h3cXBpeUZNZ3NGbXhENVViRVc5VkZ3KzhlZkVlQmtxaE5ucTQyWFBMaGlJUDJKL3JlTjVXODJkam1FM0p1WTA4a3VzeU8zcTYrYmZBNE9uN0E3aGp2VWdVaWcxMGJ1VG9nc1RHNC9mdEVHTWEyNzBJY2lJdGx4RllQeWlQL2dRTnhjbDFUZWtKU3pYZW9ENnhiUFlFL0dpMXVnSDBZVytJcndMR3psQm5FSnRqZTZHRmFnbkJPS2lRY3hoNHB6SEFxdExrSVBsTHN4d2EyYTBFcUlWSnR2Z1FPbVBmU0Q4cm8yaVZNazRtZ1MvMTdEK3lhdm9pZFhHTWF2aTZmWHE1aHlhT2FPVXQ0TXVjYThjZlpUa1dhZjYvQ0lnVUw1MFpsamE2c3hZT09MQ3BVK3llR0gzakpEcFh6VVYyT0JuOG9oSkdoNHVQbDl0OWVEL2FYRDN1MExKWWRRakdzNW5PR1hCbnlEbitjd3hkcEc5Ny9Fbi9iQStHcTVObk1INmRZSGVXUWVLNXJqTTZJRkZabWFUdnkxcnUzMnUxdmppcW1tN0JTbVRzNHhaNnZ6WXUveWptckNYZlpYR2lYV0lwTkU9LS1YcE9uUm9ha3k4WTB6VjdtSlo4YmV3PT0%3D--9408225a707f2d2527dd1e6ef14471b8368e09aa',
    '_dd_s': 'rum=0&expire=1706442563110',
}

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

params_pay = {"checksum":"375577fa151019c9272be7c85519ff1b",
             "browser_attributes":{
                 "language":"en-US",
                 "color_depth":24,
                 "java_enabled":"false",
                 "screen_height":1080,
                 "screen_width":1920,
                 "timezone_offset":-60}
             }

pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',params=json.dumps(params_pay),cookies = pup.cookies.get_dict())
# pay = s.post(f'https://www.vinted.fr/api/v2/transactions/{transaction_id}/checkout/payment',params=json.dumps(params_pay),cookies = cookies)
print('pay : ', pay.status_code)

# Sauvegarde des cookies de session
with open("cookies.json", "w") as outfile:
    json.dump(buy.cookies.get_dict(), outfile, indent=4)


print('here')

# url = "https://www.vinted.fr/items/4007663345-jeu-switch-lol?homepage_session_id=65448000-bf41-4ee1-8b5d-38f9180e19b8"
