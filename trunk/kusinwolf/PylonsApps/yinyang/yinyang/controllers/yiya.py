import logging

from yinyang.lib.base import *

log = logging.getLogger(__name__)

class YiyaController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return render("/index.mako")
