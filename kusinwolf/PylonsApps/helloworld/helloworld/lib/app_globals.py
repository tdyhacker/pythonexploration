"""The application's Globals object"""
from pylons import config
from helloworld.controllers.hello import HelloController

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.DEBUG = False
        self.Auth = True
