import requests
import json

def get_mondial_pickup_points(zipcode, city):
    headers = {
        'authority': 'www.mondialrelay.fr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr-FR',
        'referer': f'https://www.mondialrelay.fr/trouver-le-point-relais-le-plus-proche-de-chez-moi/?codePays=FR&codePostal={zipcode}',
        'requestverificationtoken': 'VRMZ-6oSgJoMPCKSPfvptpkzQ6TyFek_lYpi69-XaHGPzODs12jS2AbFbvHKKxVGbodS1Haon-vBlV1VsxcNJzIGtuk1:uQ0aA4Q6Y_hdgwfbWiV6iHi88CNCaMA-_gbxx0B4VMlTnLWJ8d-1DGbAedgy4Yw0_xil6wfyrAvbzDJijqi76jRypME1',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://www.mondialrelay.fr/api/parcelshop?country=FR&postcode={zipcode}&city={city}&services=&excludeSat=false&naturesAllowed=1,A,E,F,D,J,T,S,C&agencesAllowed=',
        headers=headers,
    )

    return(json.loads(response.text))