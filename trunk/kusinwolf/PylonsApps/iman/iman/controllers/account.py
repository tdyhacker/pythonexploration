import logging
from re import compile
from datetime import datetime, timedelta

from webhelpers.html.tags import link_to
from routes import url_for

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.account_tables import User
from iman.model.ban_tables import IP

log = logging.getLogger(__name__)

class AccountController(BaseController):
    def __before__(self):
        is_banned = meta.Session.query(IP).filter_by(ip=str(request.environ.get("REMOTE_ADDR"))).first()
        if is_banned and (is_banned.until == "0000-00-00 00:00:00" or is_banned.until == None):
            c.message = "Your IP '%s' has been banned permanently<br /><h1>Have a nice day ^_^</h1>" % is_banned.ip
            if not g.in_ban:
                g.in_ban = True
                return redirect_to(controller="%saccount" % g.site_prefix, action="banned")
        elif is_banned and is_banned.until > datetime.now():
            c.message = "Your IP '%s' has been banned from here until %s, which is another %s hours and %s minutes away<br />If this is not you, please contact the administrator and clear your name" % (is_banned.ip, is_banned.until, (is_banned.until - datetime.now()).seconds / 3600, (is_banned.until - datetime.now()).seconds % 3600 / 60)
            if not g.in_ban:
                g.in_ban = True
                return redirect_to(controller="%saccount" % g.site_prefix, action="banned")
        elif is_banned != None:
            meta.Session.delete(is_banned)
            meta.Session.commit() # Remove the ban because it is no longer valid
    
    def banned(self):
        # Calling this method creates a redundent __before__ call that losses it's message content
        return render('/banned.mako')
    
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
                    return redirect_to(controller="%sblog" % g.site_prefix, action="index") # Send them back to where they came from
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
                return redirect_to(controller="%sblog" % g.site_prefix, action="index") # Send them back to where they came from
        else:
            return render('/login.mako')
    
    def logout(self):
        del session['identity']
        session.save()
        return "You have successfully logged out<br /><br />%s" % link_to("Log back in?", url_for(controller="%saccount" % g.site_prefix, action="login"))
