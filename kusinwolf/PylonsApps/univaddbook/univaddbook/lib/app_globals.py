"""The application's Globals object"""

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.sitemap = [('Homepage', 'index'), ('Add Contact', 'contact_add'), ('Import Contacts', 'contact_import'), ('Export Contacts', 'contact_export')]
