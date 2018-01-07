from datetime import datetime as dt
from pprint import pprint

# import arbitre
from rocketcomm import RocketComm
import ids

config = ids.config
settings = ids.settings

rc = RocketComm(config)
rc.login()

pprint(rc.check_special_string(settings, dt.strptime('2018-01-01', "%Y-%m-%d"), "test", "telec"))

rc.logout()

# #############################
# ####### MAIN FUNCTION #######
# #############################
#
# def manage(sumUp=False, toChat=True):
#     config = ids.config
#     rocket = _connect(config)
#
#     if sumUp:
#         msgs = _retrieve_msgs(rocket, config, True)
#         scores, imgSet, rektSet = _add_scores(config, msgs)
#     else:
#         scores, imgSet, rektSet = _retrieve_scores()
#         date = _get_last_date(scores)
#         msgs = _retrieve_msgs(rocket, config, since=date)
#         scores, imgSet, rektSet = _add_scores(config, msgs, scores, imgSet, rektSet)
#
#     _print_scores(rocket, config, scores, imgSet, rektSet, toChat)
#     _save_scores(scores, imgSet, rektSet)

# arbitre.manage(True, False)
