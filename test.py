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

# r = session.get("https://www.vinted.fr/member/general/session_from_token", headers=headers)
s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
# s.headers = headers
req = s.get("https://www.vinted.fr")
csrfToken = extract_csrf_token(req.text)

"""Ici routes pour full login si on veut faire tout le process de connexion"""

# s.headers = {
# "Access-Control-Allow-Origin":"*",
# "Cache-Control":"no-cache, no-store, must-revalidate",
# "Content-Length":"230",
# "Content-Type":"application/json;charset=utf-8",
# "Date":"Thu, 18 Jan 2024 20:07:58 GMT",
# "Expires":"0",
# "Pragma":"no-cache",
# "Server":"DataDome",
# "Strict-Transport-Security":"max-age=63072000; includeSubDomains; preload",
# "Via":"1.1 9f25aa45df27e50f380232059fde4c1a.cloudfront.net (CloudFront)",
# "X-Amz-Cf-Id":"hGn_oDOzYYUkbIp5JCQrvsR4i1LFyvXqHOE8fjEW8SwFI9wKiLoVqA==",
# "X-Amz-Cf-Pop":"ZRH55-P1",
# "X-Cache":"Miss from cloudfront"
#
# }
# req2 = s.post("https://dd.vinted.lt/js")
#
# print("req2")
#
#
#
#
#
# s.headers = {
# "Accept":"application/json, text/plain, */*",
# "Accept-Encoding":"gzip, deflate, br",
# "Accept-Language":"fr",
# "Content-Length":"63",
# "Content-Type":"application/json",
# "Cookie": "anonymous-locale=fr; v_udt=OGk2eFpwOExHaTNzY1hKYjVMdnVkaDVsLS1yQWpNL2VzNXRpaDlPM1JDLS1IdmlzWGJBWkVPMDZXZTFkajBBS1BRPT0%3D; domain_selected=true; OptanonAlertBoxClosed=2024-01-11T21:01:24.831Z; eupubconsent-v2=CP4N05gP4N05gAcABBENAiEsAP_gAAAAAChQg1NX_H__bX9j8Xr16ft0eY1f99j7rsQxBhfJk-4FyLvW_JwX32EzNA26pqYKmRIEu3ZBIQFlHIHURUigaogVryHsYkGcgTNKJ6BkgFMRc2cYCF5vmYlD-QKY5_p_d3f52T-9_dv83dzzz8VHv3e5fmclcICdQ58tDfn9bRKb-5IOd_78v4v09FgAAAAAABAAAAAAAAAAAAAAAAAAABcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAABQSB-AAgABcAFAAVAA4AB4AEAAMIAZABqADwAIgATAAqgBvAD0AH4AQkAhgCJAEcAJYATQAw4BlAGWANkAd8A9gD4gH2AfoBAACKQEXARgAjQBKQCggFQAKuAXMAxQBogDaAG4AOIAkQBOwChwFHgKRAU2AtgBcgC7wF5gMGAYaAyQBk4DOYGsAayA28BuoDggHJgOXAeOBCEIAdAAcACQAc4BBwCfgI9ASKAlYBNoCnwFhALyAYgAxaBkIGRgNGAamA2gBtwDdIHkgeUA-QB-4EBAIGQQRBBMCDAEKwIXDgGYACIAHAAeABcAEgAPwA0ADnAHcAQCAg4CEAERAJ-AVAAvQBxwDpAI9ASKAlYBMQCZQE2gKQAUmAqoBXYCygFqALoAYgAxYBkIDJgGjANNAamA14BtADbAG3AOPgc6Bz8DyQPKAfEA-2B-wH7gQPAgiBBgCDYEKx0E0ABcAFAAVAA4ACAAF0AMAA1AB4AEQAJgAVYAuAC6AGIAMwAbwA9AB-gEMARIAlgBNACjAGGAMoAaIA2QB3gD2gH2AfoA_4CKAIwASkAoIBVwCxAFzALyAYoA2gBuADiAHUAReAkQBKgCZAE7AKHAUfApoCmwFWALFgWwBbIC4AFyALtAXeAvMBfQDBgGGgMeAZIAycBlQDLAGcgNEAaqA1gBt4DdQHFgOTAcuA8cB9YEAQIWkACYACAA0ADnALEAj0BNoCkwF5ANTAbYA24Bz8DyQPKAfEA_YCB4EGAINgQrIQJAAFgAUABcADEAJgAUwAqgBcADEAG8APQAjgB3gD_AIoASkAoIBVwC5gGKANoAdQBKgCmgFigLRAXAAuQBk4DOQGiANVAcAA8cCFAELSUCAABAACwAKAAcgBgAGIAPAAiABMACqAFwAMUAhgCJAEcAKMAbIA7wB-AFXAMUAdQBF4CRAFHgLFAWwAvMBk4DOQGsANvAcABA8kAPAAuAO4AgABUAEegJFASsAm0BSYCygGLAPKAfuBBECDBSBwAAuACgAKgAcABBADAANQAeABEACYAFIAKoAYgAzAB-gEMARIAowBlADRAGyAO-AfgB-gEWAIwASkAoIBVwC5gF5AMUAbQA3ACLwEiAJ2AUOApsBYoC2AFwALkAXaAvMBfQDDQGSAMnAZYAzmBrAGsgNvAbqA4IByYDlwHjgQhAhaUARgAXABIAI4Ac4A7gCAAEiALEAXUA14B2wD_gI9ASKAmIBNoCkAFPgK7AXQAvIBiwDJgGiANTAa8A8oB8UD9gP3AgYBA8CCYEGAINgQrA.f_wAAAAAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.320.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.16831; cf_clearance=8EbIgYF05sWd84t0BaPM3euaKLCrbJLWbOB79PPkfAg-1705440174-1-Aat+U+0P3XVaCRgtSgaMExcECD4bdfGwRJ3QOD8/lRwe24MJKq01k8iHnGPCv394uekXGZO4DwFXZ5D9reSOen8=; anon_id=2402f1b4-04dd-41ab-a2a3-fd3e2da4f23b; last_user_id=1; v_sid=366ec62c-1705523878; __cf_bm=p_aw_TgTdRfUmIDa9.OFmaq8VcbCWIphPbYwK32MjcQ-1705524652-1-AdOIK7a16srl3Hxz/PBxeDcD72SmqLOBIveyeLjGwGAT6zQRsSHO+J3Y4tJWRfj4pNzHVps9FZJ/PfFlNwNF8oD7fzB7FJ97LXyYXKv95wLA; ab.optOut=This-cookie-will-expire-in-2025; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jan+17+2024+21%3A50%3A53+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=2402f1b4-04dd-41ab-a2a3-fd3e2da4f23b&interactionCount=24&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CV2STACK42%3A1%2CC0015%3A1&AwaitingReconsent=false&geolocation=CH%3BZH; _vinted_fr_session=blRRTlBrWjUyMlhvOGxKenBMajNlQ25IVzEwVlBsQU5GRGhIVHRRQ3RsK0REMDdPK2srS2ZDVk9Ia2VnUDkyRGFQYldmbjcvOW4xeC9VUDZ1ZWZwbmpNUURHR3pKM1FXK1lFVjVUaW5Lb01VZFpuNHcvRlBQSG1sUkp0em95NHJxSVNMTUlaeW10MGM2V2NHWTlXT1BaOFZQYkxSMHd5cTlPbGtDZzd6enNrNnFic0tZUkZyS1Rpcno0STdxRDZxaDhlWXV4MXduNTluYm9lV1doMmpoQVVZRytjTC96ODRlWjQ0UThpcTgwOTJUN0M4VHgybTNJZ3BReWUrMDRZTU8xWEJOR0hhTnJ5eEtKWkp5YndYMVdJb2Vsb3hlVmltWjljTG9mUEJWdjRNdERQOFJ4blkxVVhsS3pJL0tQaWtlWDFUUGtzeXZXb1A4V2RRQlRVZkQ5bDY4aWNwa0tldFhlN1dmMVQ0dWN5STl4UTIrT2hsb2c4V3R2cThPSEdidlBoSnJYK1g0WFdKWTV1RXg2bVo2cG1zS21BTGRPdElqUmE1eE41ZXY5cjNOMzVIOXkxRkZ2aXF5SkVwS2R1dzVMbG9Jdy9Qd1hFMnBOcjJvNmFJR3pUcXl0S0RvMEY4OXkyYWJtZG5UV1pTbWd6ZmZKeWpzZHpoU3pHbW5VWEdEUE5rYnFsbDhOMGhSdmt4ZGM4d1lVZDFma21iczdWNlpTT0w3UWVLUDhpNkx2V0N2d0J5a3ZLWnFQSFYzakVEZW5RRmZWelVGZ2poV0dHN1RQK0U2eElHVjRybDJ5bGxBRXVpL1B1K1lGdDc2RStobG5OWi9PeWRpRTZvTlZOMDJ2SjVNcC9UOHR5dnJWcGxXeStNM29jTnhKR3dwM3pYY0RUOFIvbStkRjBwNHgrdkpsUjlxWFd3ZS9uVXYrcUlrL0VZM2drV0FhZU5pZy9FRTk3WUpYNUZoN2RvaTV0bHhjTHJROXBMakNZcTIrcnFRdVl5Nzh3dXh5aDFkMFhOSmtGMjlOUXJ1YjlVR01HREJoQUlJUk5qdG9Zd0F2ZEFSeWpMUkRkYVN3UFdIY21RUWhzQ0RHbUxzMlg5aGYwOHhPQTk4VDduellGUExJYndIQmJoWWcwTlllRkJjdmhvYUF5NVEwQThlNlEzTnhGdWQ3U2YzcVlVNUE2dFBNeHFFT3NPeVdQOUJzVkt1TlB5RDVoSmd0Q1ZjamRZY0pBZkEwZDllWlFQMTl3L0E0eWV3eG5xSEhNRkpVRkxKY3JJWkNVSGQybjR3YzkyQzlnQ1VqNEJ1Nlp1aDhMREt3N2RoRjdFT2EzM0lxYmNEczlFaEJLS0Z2cE5ONy9jaUtYZlpBOU9qaHAwQ1k0YWEzYTBmRXdnS2JIeDZPTUJsS25CRVZrMEY5dndmY2RuYU95dUR6VXFtKzFVUTYvazVOSXJSUUY3L0VLajdCenI3LytRNXE4UUdGRXB3M1hpNmdmd05qY0g0VW5qNTZlWjFHTkRJaUhaaW10eDNKWXp0eHRWdDJNbHZQOGRiVjYwU2thNGREZmU3VDBZTlE5UzNtbDUySVVuanN1a2srOHZCTlhKUFhGa2tyTGtibjk5dC8vWXRtQ3l6cnFyNUJnb3V1RE0wZitvcDh5VFFLR0pLdFQ2dFErOGdMM0d0TkdPcUZyaTZuRjhJSnNHQ1QxTlpuYXFmQnp6ZWk0RUpoOUV2MkZhS3F3ek5CQ2thRXRyRzVnZU9UOXVSY0pPbllBakJzNzBua0hPaEZuRk02ZGduNlJnMlpvTUVCZG1DSFpIZjhLai9xVWYrT2YwRkZCekVndEN0Ry80b2VsYWVxNVpVb0Q0TzNVczBhRXBBNHE1UzlFcVJjSVR4c1BFUlJiRnlSVDF0VitiWkh4eVNpRjQ2Sm1MSFVBR1dvRjB5bU1Ba1BCTXNCSVR1eVhOV1ZSMVlaS0k2cUZFRHMyc2NiZXM0dmtuMHFhRXk1R2oxOGtyOGNDbTg2YzNvSUlnZlpkRjB5NG9ZMlVUaUdxK2FVa3hNS0oyTjJsR2ZTRHR2Mlh6QXhFdmJ0QWRHNmpHNWN1Uk1GTEMzNnNxQ2ZnZitlL2xuZDc4UkgxVWpnZ2FiNmZ0RThuMW9ienJCUVkyazd0dG80clordTRHWXVKU1d6c1B0R2JmNnVvK1IxZm9EQWxpRlJrczkyU2RCWVFSaTFMaTlySzhRY29VRFB2dDJMN2hLODA1VC81eXhEdzNOcmtGUkgxdEF0M1Y5K05EL3hwN0JVQ2lYbUF1T0V0LzUrZmZ1NTdsLS1HbUdRWm5reW9CU1AxLzhzUGsxWW9RPT0%3D--cb70a627edf5875c9a3c25bd54d90cba34beb456; datadome=3Q5M48K3Wr9t1GsXDvCb3~IdVVb~DQiZxx20nc7ZKWYU5dWXXDuzWxtP8BPNVXWV47wUGJsQ_Fu_soci5ChO2FShIVRwUb2La851dYNHshY7BwgWjPDLJzfHW6WRFlld; viewport_size=1372; _dd_s=rum=0&expire=1705525658802",
# "Origin":"https://www.vinted.fr",
# "Referer":"https://www.vinted.fr/",
# "Sec-Ch-Ua":'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
# "Sec-Ch-Ua-Mobile":"?0",
# "Sec-Ch-Ua-Platform":'"Windows"',
# "Sec-Fetch-Dest":"empty",
# "Sec-Fetch-Mode":"cors",
# "Sec-Fetch-Site":"same-origin",
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# "X-Anon-Id":req.cookies.get_dict()['anon_id'],#"2402f1b4-04dd-41ab-a2a3-fd3e2da4f23b",
# "X-Csrf-Token":csrfToken
# }
#
#
# urlCaptcha = "https://www.vinted.fr/api/v2/captchas"
# dataCaptcha = {"entity_type":"login", "payload":{"username": "NEekoHugo_xX69" }}
# token_endpoint  = "https://www.vinted.fr/oauth/token"
# uuid = s.post(urlCaptcha, data=json.dumps(dataCaptcha), cookies=req.cookies.get_dict()).json()["uuid"]
#
# params_req3 = {
#     "client_id": "web",
#     "scope": "user",
#     # "fingerprint": "e75ac229755438a997ec0df72e581527",
#     "username": "NEekoHugo_xX69",
#     "password": "", # A METTRE
#     "uuid": uuid,
#     "grant_type": "password"
# }
#
# req3 = s.post("https://www.vinted.fr/oauth/token", data=json.dumps(params_req3))
#
# print("req3")

"""FIN ROUTES POUR LOGIN"""



token = "" # A METTRE
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


s.headers = {
"Accept":"application/json, text/plain, */*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"fr",
"Content-Length":"46",
"Content-Type":"application/json",
"Origin":"https://www.vinted.fr",
"Referer":"https://www.vinted.fr/items/3995562194-b-ton-majorette", # IMPORTANT, LIEN OBJET, LE NUMERO DOIT ETRE LE MEME QUE DANS USER_FAVOURITES EN BAS
"Sec-Ch-Ua":'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
"Sec-Ch-Ua-Mobile":"?0",
"Sec-Ch-Ua-Platform":'"Windows"',
"Sec-Fetch-Dest":"empty",
"Sec-Fetch-Mode":"cors",
"Sec-Fetch-Site":"same-origin",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# "X-Anon-Id":req4.cookies.get_dict()['anon_id'],
"X-Csrf-Token":csrfToken, # IMPORTANT
# "X-Datadog-Origin":"rum",
# "X-Datadog-Parent-Id":"8091249082714489693",
# "X-Datadog-Sampling-Priority":"1",
# "X-Datadog-Trace-Id":"498934100531349759"
}
params_like = {"type":"item","user_favourites":[3995562194]} # ICI NUMERO USER_FAVOURITES
like = s.post("https://www.vinted.fr/api/v2/user_favourites/toggle", data=json.dumps(params_like), cookies=req4.cookies.get_dict())


"""Quelques tests sur quelques routes supplémentaires

Note: le bearer token semble changer assez souvent, voir si le process de connexion complet règle le souci ?
Ou alors, comment/pourquoi est-il refresh ?"""

# test = s.get("https://www.vinted.fr/api/v2/users/current", cookies=like.cookies.get_dict())
#
#
#
#
# v_uid = req4.cookies.get_dict()["v_uid"]
#
# req5 = s.get(f"https://www.vinted.fr/api/v2/users/{v_uid}/balance", cookies=req4.cookies.get_dict())



