from univaddbook.tests import *

class TestBookcontrolController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='uniaddbook', action='index'))
        # Test response...
