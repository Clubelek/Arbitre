# https://rocket.chat/docs/developer-guides/rest-api/

from datetime import datetime as dt
from pprint import pprint
import secrets

import rocketcomm





####################
# SCORE MANAGEMENT #
####################

def _add_score(scores, name, date):
    time = [date.hour, date.minute]
    rekt = None

    # Create if new player
    if name not in scores:
        scores[name] = {}
        scores[name]['dates'] = []
        scores[name]['time'] = []
        scores[name]['score'] = 0

    # Append date (to get the last one)
    scores[name]['dates'].append(date)

    # Check time in all last times
    for _name in scores:
        for t in scores[_name]['time']:
            if t == time:  # We got a match !
                rekt = _name  # sorry :(
                scores[_name]['score'] -= 1
                scores[name]['score'] -= 1
                scores[_name]['time'].remove(t)

    # Someone get rekt
    if rekt is None:
        scores[name]['time'].append(time)
        scores[name]['score'] += 1

    return scores, rekt;


def _add_scores(config, msgs, scores=None, imgSet=None, rektSet=None):
    if scores is None:
        scores = {}
    if imgSet is None:
        imgSet = []
    if rektSet is None:
        rektSet = []

    for msg in msgs:
        # if this msg contains a picture
        if ("attachments" in msg) and (msg["attachments"] is not None) and (len(msg["attachments"]) > 0) and (
                "image_url" in msg["attachments"][0]):
            url = msg["attachments"][0]["image_url"]
            imgSet.append(url)

            date = dt.strptime(msg["ts"], config["parseDate"])
            name = msg["u"]["username"]
            scores, rekt = _add_score(scores, name, date)
            if rekt is not None:
                rektSet.append([rekt, name, date])

    return scores, imgSet, rektSet;


def _get_last_date(scores):
    ld = None

    for name in scores:
        for d in scores[name]['dates']:
            if (ld is None) or (d > ld):
                ld = d

    return ld


#############################
####### MAIN FUNCTION #######
#############################

def manage(sumUp=False, toChat=True):
    config = ids.config
    rocket = _connect(config)

    if sumUp:
        msgs = _retrieve_msgs(rocket, config, True)
        scores, imgSet, rektSet = _add_scores(config, msgs)
    else:
        scores, imgSet, rektSet = _retrieve_scores()
        date = _get_last_date(scores)
        msgs = _retrieve_msgs(rocket, config, since=date)
        scores, imgSet, rektSet = _add_scores(config, msgs, scores, imgSet, rektSet)

    _print_scores(rocket, config, scores, imgSet, rektSet, toChat)
    _save_scores(scores, imgSet, rektSet)
