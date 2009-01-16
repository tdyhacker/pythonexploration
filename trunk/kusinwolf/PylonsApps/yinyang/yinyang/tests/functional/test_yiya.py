from yinyang.tests import *

class TestYiyaController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='yiya'))
        # Test response...
