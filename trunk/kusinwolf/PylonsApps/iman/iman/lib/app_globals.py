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
        self.in_ban = False
        
        self.sitemap = [('Homepage', 'index'), ('Change Password', 'change_password'), ('Sign Out', 'signout'),]
        self.externallinks = [("Question Blog", {"controller": "blog", "action": "index", "id": None}),
                              ("Todo List", {"controller": "todo", "action": "index", "id": None}),
                              ]
        self.central_time = timedelta(hours = 5)