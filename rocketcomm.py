from rocketchat_API.rocketchat import RocketChat
from datetime import datetime as dt


############################
# ROCKETCHAT COMMUNICATION #
############################

class RocketComm:
    rocket = None

    def __init__(self, config):
        self.user = config['user']
        self.password = config['pass']
        self.URL = config['type'] + '://' + config['host']

    def login(self):
        self.rocket = RocketChat(self.user, self.password, self.URL)

    def logout(self):
        self.rocket.logout()

    def _retrieve_msgs(self, settings, since=None):
        if since is None:
            hist = self.rocket.channels_history(settings['channel'], count=10000).json()
            msgs = hist['messages']
        else:
            old = dt.strftime(since, settings["parseDate"])
            hist = self.rocket.channels_history(settings['channel'], count=10000, oldest=old).json()
            msgs = hist['messages']

        return msgs

    def _retrieve_userlist(self):
        count = 0
        users = []

        stop = False
        while not stop:
            req = self.rocket.users_list(count=50, offset=count).json()
            count += 50
            stop = count > req['total']
            users.extend(req['users'])

        return users

    def get_name_from_id(self, id):
        users = self._retrieve_userlist()
        for user in users:
            if user['_id'] == _id:
                if 'username' in user:
                    return user['username']
                elif 'name' in user:
                    return user['name']
                else:
                    return user['_id']

        return ""

    def get_id_from_name(self, username):
        users = self._retrieve_userlist()
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

    def get_active_users(self, settings, since, pic=False):
        users = []

        msgs = self._retrieve_msgs(settings, since)
        for msg in msgs:
            if not pic or (("attachments" in msg)
                           and (msg["attachments"] is not None)
                           and (len(msg["attachments"]) > 0)
                           and ("image_url" in msg["attachments"][0])):
                user = msg["u"]["username"]
                if user not in users:
                    users.append(user)

        return users

    def get_image_list(self, settings, since):
        imgs = []

        msgs = self._retrieve_msgs(settings, since)
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

    def check_special_string(self, settings, since, string, name=""):
        dates = []

        msgs = self._retrieve_msgs(settings, since)
        for msg in msgs:
            if string in msg['msg'] and (name == "" or msg['u']['username'] == name):
                date = dt.strptime(msg["ts"], settings["parseDate"])

                dates.append(dict(fullstring=msg['msg'], date=date))

        return dates

    def get_raw_msgs(self, settings, since):
        rmsgs = []

        msgs = self._retrieve_msgs(settings, since)
        for msg in msgs:
            url = ""
            reac = None

            if (("attachments" in msg)
                    and (msg["attachments"] is not None)
                    and (len(msg["attachments"]) > 0)
                    and ("image_url" in msg["attachments"][0])):
                url = msg["attachments"][0]["image_url"]

            if (("reactions" in msg)
                    and (msg["reactions"] is not None)
                    and (len(msg["reactions"]) > 0)):
                reac = msg['reactions']

            date = dt.strptime(msg["ts"], settings["parseDate"])
            rmsg = msg['msg']
            user = msg['u']['username']

            rmsgs.append(dict(user=user, date=date, msg=rmsg, url=url, reactions=reac))

        return rmsgs

    def print_scores(self, settings, scores, to_chat=False):
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
            self.rocket.chat_post_message(out, room_id=settings['channel'], avatar=url, alias=alias)
