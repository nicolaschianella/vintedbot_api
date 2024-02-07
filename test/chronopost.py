import requests
import json

def get_colissimo_pickup_points(lattitude, longitude, zipcode, city, country):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'https://www.chronopost.fr/expeditionAvanceeSec/ounoustrouver.html?copyButton=1&key=7n8nI15pWlZ3wC6o16gigg==&zipCode={zipcode}&city={city}&backUrl=http://infosco.chronopost.fr&category=2&vue=relaissansservice',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'lat': lattitude,
        'lon': longitude,
        'r': '40',
        'z': zipcode,
        'c': city,
        'a': '',
        'p': country,
        'lang': 'null',
        '_': '170862393908',
    }

    response = requests.get(
        'https://www.chronopost.fr/expeditionAvanceeSec/stubpointsearchinterparservice.json',
        params=params,
        headers=headers,
    )

    return(json.loads(response.text)['olgiPointList'])