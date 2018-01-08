# https://rocket.chat/docs/developer-guides/rest-api/

from datetime import datetime as dt
from datetime import timedelta as td
from pprint import pprint
import secrets
import re

from rocketcomm import RocketComm

#########
# TOOLS #
#########


def _is_correct_image(url):
    return True


def _is_benoipocalypse(date, benoipocalypse_start): #la Benoipocalypse dure toute la journée suivant l'annonce, de minuit à minuit
    for set in benoipocalypse_start:
        msg = set["fullstring"]  # check something on msg, like the date ?
        dateStart = set["date"].date() + td(days=1)
        if dateStart == date.date():
            return True

    return False


def _is_troll(date, troll_start):
    for set in troll_start:
        msg = set["fullstring"]  # check something on msg, like the date ?
        dateStart = set["date"]
        if (dateStart.date() == date.date()) and (dateStart.format("%H%i") == date.format("%H%i")):  # same day, hour, min
            return True

    return False


def _check_benoipocalypse(msg, benoit):
    # Delete BENOIT
    msg = " ".join(re.split(benoit, msg))
    # Delete emotes
    msg = " ".join(re.split(":\w+?:", msg))
    # Delete non character
    msg = " ".join(re.split("\W+", msg))

    sp_msg = msg.split(" ")
    return len(sp_msg)


def _add_image(normal_mode, msg):
    token = msg["date"].strftime("%d%m%Y")
    hour = msg["date"].time()
    if token not in normal_mode:
        normal_mode[token] = {}
    normal_mode[token].append(dict(hour=hour, react=msg["reactions"], user=msg["user"]))

    return normal_mode


def _compute_normal_mode(scores, normal_mode):
    for day in normal_mode:
        user = day["user"]
        #if
        # TODO finish that !
    return scores

#########
# SCORE #
#########


def _compute_score(rocket, settings, scores, since=None):
    msgs = rocket.get_raw_msgs(settings, since)

    benoipocalypse_starts = rocket.check_special_string(settings, since, settings["Benoipocalypse_start"])
    troll_starts = rocket.check_special_string(settings, since, settings["DontFeedTheTroll"])

    normal_mode = {}

    for msg in msgs:
        pts = 0

        # BENOIT
        if _is_benoipocalypse(msg["date"], benoipocalypse_starts):
            bad_words = _check_benoipocalypse(msg["msg"], settings["Benoipocalypse_word"])
            if bad_words != 0:
                pts -= settings["benoit_base_pts"] + settings["benoit_pts"]*bad_words

        # Someone posted an image !
        if msg["url"] != "":
            if _is_correct_image(msg["url"]):  # That's benoit_jeune image
                if _is_troll(msg["date"], troll_starts):  # that's OK, we just feed the troll
                    pts += settings["troll_pts"]
                else:
                    # For now we just stack the valids messages
                    normal_mode = _add_image(normal_mode, msg)

            else:  # Uh oh, wrong image, why not try #memes ?
                pts -= settings["bad_pic_pts"]

    scores = _compute_normal_mode(scores, normal_mode)

    return scores

