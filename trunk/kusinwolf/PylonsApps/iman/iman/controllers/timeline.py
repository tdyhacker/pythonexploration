import logging

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta

log = logging.getLogger(__name__)

class TimelineController(BaseController):
    
    def __before__(self):
        pass
    
    def index(self):
        '''functional and mako method'''
        
        return render('/timeline/timeline.mako')
