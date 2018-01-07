from datetime import datetime as dt
from pprint import pprint

import arbitre
import rocketcomm
import ids

config = ids.config
settings = ids.settings

rocket = rocketcomm.connect(config)

pprint(rocketcomm.check_special_string(rocket, settings, dt.strptime('2018-01-01', "%Y-%m-%d"), "test", "telec"))

rocketcomm.logout(rocket)

# arbitre.manage(True, False)
