from ogameinfo.tests import *

class TestOgameController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ogame', action='index'))
        # Test response...
