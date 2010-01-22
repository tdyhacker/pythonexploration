import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.question_tables import Question, Response, View, Comment
from iman.model.account_tables import User

log = logging.getLogger(__name__)

class BlogController(BaseController):
    
    def __before__(self):
        # Basic Home grown security layer
        if session.get("identity") is None:
            return redirect_to(controller="account", action="login")
    
    def change_password(self):
        return redirect_to(controller="account", action="change_password")
    
    def convertHTMLTags(self, text):
        '''functional method'''
        
        text = text.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;") # This prevents any HTML code from being inserted into the page causing unwanted execution within a question
        text = text.replace("[br]","<br />").replace("[BR]","<br />")
        text = text.replace("[p]","<p>").replace("[/p]","</p>").replace("[P]","<p>").replace("[/P]","</p>")
        text = text.replace("[ul]","<ul>").replace("[/ul]","</ul>").replace("[UL]","<ul>").replace("[/UL]","</ul>")
        text = text.replace("[li]","<li>").replace("[/li]","</li>").replace("[LI]","<li>").replace("[/LI]","</li>")
        text = text.replace("[b]","<b>").replace("[/b]","</b>").replace("[B]","<b>").replace("[/B]","</b>")
        text = text.replace("[i]","<i>").replace("[/i]","</i>").replace("[I]","<i>").replace("[/I]","</i>")
        text = text.replace("[u]","<u>").replace("[/u]","</u>").replace("[U]","<u>").replace("[/U]","</u>")
        text = text.replace("[url]", "<a href=\"").replace("[/url]", "\" target=\"_blank\">link</a>").replace("[URL]", "<a href=\"").replace("[/URL]", "\">link</a>")
        
        return text
    
    def index(self):
        '''functional and mako method'''
        user = meta.Session.query(User).filter_by(username=session['identity'].username).one()
        c.user_id = user.uid
        c.user = user
        
        c.personal_questions = c.not_personal_questions = []
        
        if meta.Session.query(Question).all() != []:
            c.personal_questions = meta.Session.query(Question).filter_by(user=user).order_by("modified DESC").all() # Queries for only what you own
            c.not_personal_questions = meta.Session.query(Question).filter("public").filter("user_id != %d" % user.uid).order_by("modified DESC").all() # Queries for everything but what you own
        
        return render('/index.mako')

    def comment_edit(self, id):
        '''mako method'''
        if meta.Session.query(Comment).filter_by(id = id).count():
            c.comment = meta.Session.query(Comment).filter_by(id = id).one()
            c.user_id = session['identity'].uid
            
            self.security_ownership(c.comment.user_id)
            
            return render('/comment_edit.mako')
        else:
            return redirect_to(action = "index")
    
    def comment_update(self, id):
        '''functional method'''
        if meta.Session.query(Comment).filter_by(id=id).count():
            meta.Session.begin()
            comment = meta.Session.query(Comment).filter_by(id=id).one()
            user_response = comment.response[0]
            question = user_response.question[0]
            user_id = session['identity'].uid
            
            self.security_ownership(comment.user_id)
            
            comment.comment = request.POST.get("comment", '')
            self.question_update_changed(question.id) # Update the question/blog/thread to signify a modification has occured
            meta.Session.commit()
            
            return redirect_to(action = "question_show", id = question.id)
        else:
            return redirect_to(action = "index")

    def comment_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username=session['identity'].username).one()
        
        response = meta.Session.query(Response).filter_by(id = int(request.POST.get('id'))).one()
        question = response.question[0]
        comment = Comment(comment = str(request.params['comment'].replace("'", "\'")), user = user)
        
        if comment.comment == '' or comment.comment == None:
            del comment
        else:
            response.comments.append(comment)
            if not question.public:
                self.security_ownership(question.user_id)
            
            self.question_update_changed(question.id) # Update the question/blog/thread to signify a modification has occured
        
        meta.Session.commit()
        
        return redirect_to(action = "question_show", id = question.id)
    
    def question_edit(self, id):
        '''mako method'''
        if meta.Session.query(Question).filter_by(id = id).count():
            c.question = meta.Session.query(Question).filter_by(id = id).one()
            c.user_id = session['identity'].uid
            
            self.security_ownership(c.question.user_id)
            
            return render('/question_edit.mako')
        else:
            return redirect_to(action = "index")
    
    def question_update(self, id):
        '''functional method
            Commits all changes of the question to the database
        '''
        if meta.Session.query(Question).filter_by(id=id).count():
            meta.Session.begin()
            question = meta.Session.query(Question).filter_by(id = id).one()
            user_id = session['identity'].uid
            
            self.security_ownership(question.user_id)
            
            question.question = request.POST.get("question", '')
            meta.Session.commit()
            self.question_update_changed(question.id) # Update the question/blog/thread to signify a modification has occured
            
            return redirect_to(action = "question_show", id = question.id)
        else:
            return redirect_to(action = "index")
    
    def question_update_changed(self, id):
        '''functional method with no default return
            Updates the question's modified record in the database
        '''
        if meta.Session.query(Question).filter_by(id=id).count():
            meta.Session.begin()
            question = meta.Session.query(Question).filter_by(id = id).one()
            user_id = session['identity'].uid
            
            question.modified = datetime.now()
            meta.Session.commit()
    
    def question_show(self, id):
        '''mako method'''
        if meta.Session.query(Question).filter_by(id = id).count():
            c.question = meta.Session.query(Question).filter_by(id = id).one()
            c.user_id = session['identity'].uid
            last_viewed = None
            
            if not c.question.public:
                self.security_ownership(c.question.user_id)
            
            c.question.responses.sort(lambda x,y: cmp(x.created, y.created)) # Sort the responses by creation date, not by ID like the ORM is doing
            
            c.convert_text = self.convertHTMLTags
            
            if c.question.user == None:
                # Temp name to help with error checking and debugging on the dev side
                c.question.user = User(username = "Anonymous", firstname = "Anonymous", lastname = "McNonymous")
            
            user = meta.Session.query(User).filter_by(uid = int(session['identity'].uid)).one()
            
            if meta.Session.query(View).filter_by(user_id = user.uid).filter_by(question_id = c.question.id).count():
                # If there already existing an entry for the last time the user viewed the question
                last_viewed = meta.Session.query(View).filter_by(user_id = user.uid).filter_by(question_id = c.question.id).one()
            else: # last_viewed == None:
                # If there does not already existing an entry
                last_viewed = View(user_id = user.uid, question_id = c.question.id, last_viewed = datetime.now())
                meta.Session.save(last_viewed)
            
            last_viewed.last_viewed = datetime.now()
            meta.Session.commit()
        
            return render('/question_show.mako')
        else:
            return redirect_to(action = "index")
    
    def question_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username = session['identity'].username).one()
        
        question = Question(question = str(request.params['question'].replace("'", "\'")))
        user_response = Response(response = str(request.params['response'].replace("'", "\'")))
        user_response.user = user
        
        if user_response.response == '' or user_response.response == None:
            del user_response
        else:
            question.responses.append(user_response)
        
        question.user = user
        
        meta.Session.commit()
        
        return redirect_to(action = "index")
    
    def question_public(self):
        '''functional method to show a question to the public'''
        q = meta.Session.query(Question).filter_by(id = int(request.params['id'])).one()
        q.public = True
        meta.Session.commit()
        
        return redirect_to(action="question_show", id = int(request.params['id']))
    
    def question_private(self):
        '''functional method to hide a question from the public'''
        q = meta.Session.query(Question).filter_by(id = int(request.params['id'])).one()
        q.public = False
        meta.Session.commit()
        
        return redirect_to(action = "question_show", id = int(request.params['id']))

    def response_edit(self, id):
        '''mako method'''
        if meta.Session.query(Response).filter_by(id=id).count():
            c.response = meta.Session.query(Response).filter_by(id = id).one()
            c.user_id = session['identity'].uid
            
            self.security_ownership(c.response.user_id)
            
            return render('/response_edit.mako')
        else:
            return redirect_to(action = "index")
    
    def response_update(self, id):
        '''functional method'''
        if meta.Session.query(Response).filter_by(id = id).count():
            meta.Session.begin()
            user_response = meta.Session.query(Response).filter_by(id = id).one()
            question = user_response.question[0]
            user_id = session['identity'].uid
            
            self.security_ownership(user_response.user_id)
            
            user_response.response = request.POST.get("response", '')
            self.question_update_changed(question.id) # Update the question/blog/thread to signify a modification has occured
            meta.Session.commit()
            
            return redirect_to(action = "question_show", id = question.id)
        else:
            return redirect_to(action = "index")

    def response_insert(self):
        '''functional method'''
        meta.Session.begin()
        
        user = meta.Session.query(User).filter_by(username = session['identity'].username).one()
        
        question = meta.Session.query(Question).filter_by(id = int(request.params['id'])).one()
        user_response = Response(response = str(request.params['response'].replace("'", "\'")), user = user)
        
        if user_response.response == '' or user_response.response == None:
            del user_response
        else:
            question.responses.append(user_response)
            
            if not question.public:
                self.security_ownership(question.user_id)
            
            self.question_update_changed(question.id) # Update the question/blog/thread to signify a modification has occured
        
        meta.Session.commit()
    
        return redirect_to(action = "question_show", id = int(request.params['id']))
    
    def response_show(self, id):
        '''mako method'''
        if meta.Session.query(Response).filter_by(id = id).count():
            c.response = meta.Session.query(Response).filter_by(id = id).one()
            c.user_id = session['identity'].uid
            
            if not c.response.question[0].public and c.response.question[0].user_id != c.user_id:
                return redirect_to(action="index") # They do not have permission to view this page and should not be allowed to "hack" into it
            
            c.response.comments.sort(lambda x,y: cmp(x.created, y.created)) # Sort the responses by creation date, not by ID like the ORM is doing
            
            c.convert_text = self.convertHTMLTags
            
            return render('/comment_on_response.mako')
        else:
            return redirect_to(action="index") # The response does not exist
    
    def security_ownership(self, id):
        if not session["identity"]:
            raise "User not Authorized"
        
        user_id = session['identity'].uid
        if id != user_id: # If the user id does not equal the provided id
            raise "User not Authorized" # They do not have permission to view this page and should not be allowed to "hack" into it

    def signout(self):
        return redirect_to(controller="account", action="logout")