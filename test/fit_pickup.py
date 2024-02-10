import json

def fit_uuid(text) :
    # uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["selected_rate_uuid"]
    # points = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_options"]
    # for p in points :
    #     if p["rate_uuid"] == uuid :
    #         root_uuid = p["root_rate_uuid"]
    rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["rate_uuid"]
    root_rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["root_rate_uuid"]
    return(rate_uuid, root_rate_uuid)

def code_pup(p):
    if p['point']['carrier_id'] == 4:
        m = 1017
    elif p['point']['carrier_id'] == 27 :
        m = 118
    else :
        m = 0
    return(m)

def fit_pup(pick_up_available, saved_pup) :

    with open(saved_pup, "r") as file:
        pick_up_saved = json.load(file)

    pup1 = [float(pick_up_saved[1]['latitude']), float(pick_up_saved[1]['longitude'])] #CHRONOPOST
    pup2 = [pick_up_saved[2]['Adresse']['Latitude'], pick_up_saved[2]['Adresse']['Longitude']] #MONDIAL

    i = 0
    try :
        while float(pick_up_available[i].get('point').get('latitude')) != pup1[0] and float(pick_up_available[i].get('point').get('latitude')) != pup2[0]:
            i+=1
        if float(pick_up_available[i].get('point').get('longitude')) == pup1[1] or float(pick_up_available[i].get('point').get('longitude')) == pup2[1]:
            marker = i
        else :
            marker = 0   ### FAIRE UNE FONCTION QUI RENVOIE LE CODE DU TRANSPORTEUR
    except IndexError:
        marker = 0
    return(pick_up_available[marker].get('point').get('uuid'), pick_up_available[marker].get('point').get('code') , code_pup(pick_up_available[marker]))