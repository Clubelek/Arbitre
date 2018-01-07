from rocketchat_API.rocketchat import RocketChat
from datetime import datetime as dt

# debug
from pprint import pprint


############################
# ROCKETCHAT COMMUNICATION #
############################

def connect(config):
    rocket = RocketChat(config['user'], config['pass'], config['type'] + '://' + config['host'])
    return rocket


def logout(rocket):
    rocket.logout()


def _retrieve_msgs(rocket, settings, since=None):
    if since is None:
        hist = rocket.channels_history(settings['channel'], count=10000).json()
        msgs = hist['messages']
    else:
        old = dt.strftime(since, settings["parseDate"])
        hist = rocket.channels_history(settings['channel'], count=10000, oldest=old).json()
        msgs = hist['messages']

    return msgs


def _retrieve_userlist(rocket):
    count = 0
    users = []

    stop = False
    while not stop:
        req = rocket.users_list(count=50, offset=count).json()
        count += 50
        stop = count > req['total']
        users.extend(req['users'])

    return users


def get_name_from_id(rocket, _id):
    users = _retrieve_userlist(rocket)
    for user in users:
        if user['_id'] == _id:
            if 'username' in user:
                return user['username']
            elif 'name' in user:
                return user['name']
            else:
                return user['_id']

    return ""


def get_id_from_name(rocket, username):
    users = _retrieve_userlist(rocket)
    for user in users:
        if 'username' in user:
            _username = user['username']
        elif 'name' in user:
            _username = user['name']
        else:
            _username = user['_id']

        if _username == username:
            return user['_id']
    return ""


def get_active_users(rocket, settings, since, pic=False):
    users = []

    msgs = _retrieve_msgs(rocket, settings, since)
    for msg in msgs:
        if not pic or (("attachments" in msg)
                       and (msg["attachments"] is not None)
                       and (len(msg["attachments"]) > 0)
                       and ("image_url" in msg["attachments"][0])):
            user = msg["u"]["username"]
            if user not in users:
                users.append(user)

    return users


def get_image_list(rocket, settings, since):
    imgs = []

    msgs = _retrieve_msgs(rocket, settings, since)
    for msg in msgs:
        if (("attachments" in msg)
                and (msg["attachments"] is not None)
                and (len(msg["attachments"]) > 0)
                and ("image_url" in msg["attachments"][0])):
            user = msg["u"]["username"]
            url = msg["attachments"][0]["image_url"]
            date = dt.strptime(msg["ts"], settings["parseDate"])

            imgs.append(dict(user=user, url=url, date=date))

    return imgs


def check_special_string(rocket, settings, since, string, name=""):
    dates = []

    msgs = _retrieve_msgs(rocket, settings, since)
    for msg in msgs:
        if string in msg['msg'] and (name == "" or msg['u']['username'] == name):
            date = dt.strptime(msg["ts"], settings["parseDate"])

            dates.append(dict(fullstring=msg['msg'], date=date))

    return dates


def get_raw_msgs(rocket, settings, since):
    rmsgs = []

    msgs = _retrieve_msgs(rocket, settings, since)
    for msg in msgs:
        url = ""
        if (("attachments" in msg)
                and (msg["attachments"] is not None)
                and (len(msg["attachments"]) > 0)
                and ("image_url" in msg["attachments"][0])):
            url = msg["attachments"][0]["image_url"]
        date = dt.strptime(msg["ts"], settings["parseDate"])
        rmsg = msg['msg']
        user = msg['user']

        rmsgs.append(dict(user=user, date=date, msg=rmsg, url=url))

    return rmsgs


def print_scores(rocket, settings, scores, to_chat=False):
    url = ""
    alias = ""

    print("avatar: " + url + "  alias: " + alias)
    pprint(scores)

    # Make the scoreboard and send it if required
    out = "Tableau des scores : \n"
    for name in scores:
        out += name + " a totalisé " + str(scores[name]['score']) + " points\n"
    print(out)
    if to_chat:
        rocket.chat_post_message(out, room_id=settings['channel'], avatar=url, alias=alias)
