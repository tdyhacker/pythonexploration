import os, sys
from invenimus.lib.app_globals import Globals

sys.path.append(Globals.pylons_path)
os.environ['PYTHON_EGG_CACHE'] = Globals.pylons_eggs

from paste.deploy import loadapp

application = loadapp('config:%s/production.ini' % Globals.pylons_path)