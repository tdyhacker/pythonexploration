from eve_data.tests import *

class TestOverviewController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='overview', action='index'))
        # Test response...
