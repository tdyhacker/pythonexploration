import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.question_tables import Question, Response
from iman.model.account_tables import User

log = logging.getLogger(__name__)

class BlogController(BaseController):
    
    def __before__(self):
        # Basic Home grown security layer
        if environment.config.debug:
            session['identity'] = meta.Session.query(User).first()
            session.save()
        elif session.get("identity") is None:
            return redirect_to(controller="account", action="login")

    def signout(self):
        return redirect_to(controller="account", action="logout")
    
    def change_password(self):
        return redirect_to(controller="account", action="change_password")
    
    def convertHTMLTags(self, text):
        '''functional method'''
        
        text = text.replace("[br]","<br />").replace("[BR]","<br />")
        text = text.replace("[p]","<p>").replace("[/p]","</p>").replace("[P]","<p>").replace("[/P]","</p>")
        text = text.replace("[ul]","<ul>").replace("[/ul]","</ul>").replace("[UL]","<ul>").replace("[/UL]","</ul>")
        text = text.replace("[li]","<li>").replace("[/li]","</li>").replace("[LI]","<li>").replace("[/LI]","</li>")
        text = text.replace("[b]","<b>").replace("[/b]","</b>").replace("[B]","<b>").replace("[/B]","</b>")
        text = text.replace("[i]","<i>").replace("[/i]","</i>").replace("[I]","<i>").replace("[/I]","</i>")
        text = text.replace("[u]","<u>").replace("[/u]","</u>").replace("[U]","<u>").replace("[/U]","</u>")
        
        return text
    
    def index(self):
        '''functional and mako method'''
        user = meta.Session.query(User).filter_by(username=session['identity'].username).first()
        c.user_id = user.uid
        c.lastlogin = user.lastlogin
        if meta.Session.query(Question).all() != []:
            c.personal_questions = meta.Session.query(Question).filter_by(user=user).order_by("id DESC").all() # Queries for only what you own
            c.not_personal_questions = meta.Session.query(Question).filter("public").filter("user_id != %d" % user.uid).order_by("id DESC").all() # Queries for everything but what you own
        else:
            c.personal_questions = c.not_personal_questions = []
        return render('/index.mako')
    
    def question_show(self, id):
        '''mako method'''
        c.question = meta.Session.query(Question).filter_by(id=id).first()
        c.question.responses.sort(lambda x,y: cmp(x.created, y.created)) # Sort the responses by creation date, not by ID like the ORM is doing
        
        c.convert_text = []
        for response in c.question:
            c.convert_text.append(self.convertHTMLTags(response))
        
        if c.question.user == None:
            # Temp name to help with error checking and debugging on the dev side
            c.question.user = User(username="Anonymous", firstname="Anonymous", lastname="McNonymous")
        
        return render('/question_show.mako')
    
    def question_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username=session['identity'].username).first()
        
        question = Question(question = str(request.params['question'].replace("'", "\'")))
        response = Response(response = str(request.params['response'].replace("'", "\'")))
        response.user = user
        
        if response.response == '' or response.response == None:
            del response
        else:
            question.responses.append(response)
        
        question.user = user
        
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="index")
    
    def question_public(self):
        '''functional method to show a question to the public'''
        q = meta.Session.query(Question).filter_by(id=int(request.params['id'])).first()
        q.public = True
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="question_show", id=int(request.params['id']))
    
    def question_private(self):
        '''functional method to hide a question from the public'''
        q = meta.Session.query(Question).filter_by(id=int(request.params['id'])).first()
        q.public = False
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="question_show", id=int(request.params['id']))
    
    def response_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username=session['identity'].username).first()
        
        q = meta.Session.query(Question).filter_by(id=int(request.params['id'])).first()
        r = Response(response = str(request.params['response'].replace("'", "\'")), user = user)
        
        if r.response == '' or r.response == None:
            del r
        else:
            q.responses.append(r)
        
        meta.Session.commit()
        
        return redirect_to(controller="blog", action="question_show", id=int(request.params['id']))
    
    def comment_insert(self):
        '''functional method'''
        pass
