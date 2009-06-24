import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta
from iman.model.tables import *

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
import authkit

log = logging.getLogger(__name__)

class BlogController(BaseController):

    @authorize(ValidAuthKitUser())
    def __before__(self):
        '''functional and mako method'''
        pass
        #if not request.environ.get("REMOTE_USER"):
        #    response.status = "401 Not authenticated"
        #    return "You are not authenticated"
        #if not session.has_key('login') or not session.has_key('password') or meta.Session.query(User).filter_by(username=str(session['login']), password=str(session['password'])).first() == None:
        #    c.fail = "Login attempt failed"
        #    return render('/login.mako')
        # They passed the auth, let them through

    def signout(self):
        return "You're now signed out."
    
    def auth(self):
        login = str(request.params['login'])
        password = str(request.params['password'])
        
        if meta.Session.query(User).filter_by(username=login, password=password).first():
            session['login'] = login
            session['password'] = password
            session.save()
        
        return redirect_to(action='index')
    
    def index(self):
        '''functional and mako method'''
        return render('/index.mako')
