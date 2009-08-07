import logging
from re import compile
from datetime import datetime

from webhelpers.html.tags import link_to
from routes import url_for

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta
from iman.model.tables import *

log = logging.getLogger(__name__)

class AccountController(BaseController):
    
    def create_account(self):
        #Create User Object, then assign the key
        pass

    def change_password(self):
        c.failed = ""
        if request.POST.get("Change Password"):
            user = User().getByID(session['identity'].uid)
            
            if request.POST.get("password1") == request.POST.get("password2") and request.POST.get("password1"):
                if user.validatePassword(str(request.POST.get("current_password"))):
                    user.changePassword(str(request.POST.get("password1")))
                    # Update current indentity in session
                    session['indentity'] = User().getByID(user.uid) # Reload the object from the database to save and refresh everything
                    session.save()
                    return redirect_to(controller="blog", action="index") # Send them back to where they came from
                else:
                    c.failed = "The current password does not match what is currently being used"
                    return render('/change_password.mako')
            elif request.POST.get("password1") == request.POST.get("password2") and ((str(request.POST.get("password1")) == '' or request.POST.get("password1") is None) or (str(request.POST.get("password2")) == '' or request.POST.get("password2") is None)):
                c.failed = "Please enter a new password greater than or equal to 5 characters"
                return render('/change_password.mako')
            elif request.POST.get("password1") != request.POST.get("password2"):
                c.failed = "The new password and confirm new password do no match"
                return render('/change_password.mako')
            else:
                c.failed = "Failed...."
                return render('/change_password.mako')
        else:
            return render('/change_password.mako')
    
    def login(self):
        '''functional and mako method'''
        c.failed = "" # Nothing to return
        if request.POST.get("Login"):
            user = User().authenticate(username=str(request.POST.get("login_name")), password=str(request.POST.get("password")))
            if user is None:
                c.failed = "Incorrect Username and/or Password"
                return render('/login.mako')
            else:
                session['identity'] = user
                session.save()
                return redirect_to(controller="blog", action="index") # Send them back to where they came from
        else:
            return render('/login.mako')
    
    def logout(self):
        del session['identity']
        session.save()
        return "You have successfully logged out<br /><br />%s" % link_to("Log back in?", url_for(controller="account", action="login"))
