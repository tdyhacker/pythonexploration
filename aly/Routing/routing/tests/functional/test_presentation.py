from routing.tests import *

class TestPresentationController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='presentation', action='index'))
        # Test response...
