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
            return redirect_to(action='index')
    
    def index(self):
        '''functional and mako method'''
        
        user = meta.Session.query(User).filter_by(username=request.environ.get("REMOTE_USER")).first()
        
        c.personal_questions = meta.Session.query(Question).filter_by(user=user).order_by("id DESC").all() # Queries for only what you own
        c.not_personal_questions = meta.Session.query(Question).filter("user_id != %d" % user.uid).order_by("id DESC").all() # Queries for everything but what you own
        return render('/index.mako')
    
    def question_show(self, id):
        '''mako method'''
        c.question = meta.Session.query(Question).filter_by(id=id).first()
        return render('/question_show.mako')
    
    def question_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username=request.environ.get("REMOTE_USER")).first()
        
        question = Question(question = str(request.params['question']))
        response = Response(response = str(request.params['response']))
        response.user = user
        
        if response.response == '' or response.response == None:
            del response
        else:
            question.responses.append(response)
        
        question.user = user
        
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="index")
    
    def response_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username=request.environ.get("REMOTE_USER")).first()
        
        q = meta.Session.query(Question).filter_by(id=int(request.params['id'])).first()
        r = Response(response = str(request.params['response']), user = user.uid)
        
        if r.response == '' or r.response == None:
            del r
        else:
            q.responses.append(r)
        
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="question_show", id=int(request.params['id']))
    
    def comment_insert(self):
        '''functional method'''
        pass
