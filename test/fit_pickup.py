import json

def fit_uuid(text) :
    """
    Get the default uuid's from Vinted.
    These are then used in the param file for the pickup point update.

    :param text: Checkout content

    :return: rate_uuid, rooot_rate_uuid
    """
    rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["rate_uuid"]
    root_rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["root_rate_uuid"]
    return(rate_uuid, root_rate_uuid)

def code_pup(p):
    """
    Returns the transporter code as defined by Vinted

    :param p: pickup point

    :return: transporter code
    """
    if p['point']['carrier_id'] == 4:
        m = 1017
    elif p['point']['carrier_id'] == 27 :
        m = 118
    else :
        m = 0
    return(m)

def fit_pup(pick_up_available, saved_pup) :
    """
    Scans the nearby pickup points and tries to find one of the user's defined point.
    If no match, returns the first point of the list.

    :param pick_up_available: list of nearby pickup points
    :param saved_pup: list of points chosen by the user

    :return: point uuid, point code, transporter code
    """
    with open(saved_pup, "r") as file:
        pick_up_saved = json.load(file)

    pup1 = [pick_up_saved[1]['chronopost_pup_latitude'], pick_up_saved[1]['chronopost_pup_longitude']]
    pup2 = [pick_up_saved[2]['mondial_pup_latitude'], pick_up_saved[2]['mondial_pup_longitude']]

    i = 0
    try :
        while float(pick_up_available[i].get('point').get('latitude')) != pup1[0] and float(pick_up_available[i].get('point').get('latitude')) != pup2[0]:
            i+=1
        if float(pick_up_available[i].get('point').get('longitude')) == pup1[1] or float(pick_up_available[i].get('point').get('longitude')) == pup2[1]:
            marker = i
        else :
            marker = 0
    except IndexError:
        marker = 0
    return(pick_up_available[marker].get('point').get('uuid'), pick_up_available[marker].get('point').get('code') , code_pup(pick_up_available[marker]))