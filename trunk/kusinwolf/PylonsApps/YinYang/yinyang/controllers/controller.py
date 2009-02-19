import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from yinyang.lib.base import BaseController, render

from yinyang.model import meta
from yinyang.model.login_attempts import LoginAttempts

log = logging.getLogger(__name__)

class ControllerController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/controller.mako')
        # or, return a response
        return render('/index.mako')

    def login(self):
        meta.Session.begin()
        meta.Session.add(LoginAttempts("localhost"))
        meta.Session.commit()
        return render('/index.mako')