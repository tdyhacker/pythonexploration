"""The application's Globals object"""

from webhelpers.html.tags import link_to
from routes import url_for

from datetime import timedelta

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.site_prefix = ""
        self.sitemap = []
        self.pylons_path = '/home/pylons/invenimus'
        self.pylons_eggs = '/home/pylons/egg'
        self.picture_path = "/home/kusinwolf/Pictures/"
