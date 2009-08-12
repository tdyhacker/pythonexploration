"""The application's Globals object"""

from webhelpers.html.tags import link_to
from routes import url_for

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.sitemap = [('Homepage', 'index'), ('Change Password', 'change_password'), ('Sign Out', 'signout'),]
        self.externallinks = [("Question Blog", url_for(controller="blog", action="index", id=None)),
                              ("Todo List", url_for(controller="todo", action="index", id=None)),
                              ]
        self.in_ban = False