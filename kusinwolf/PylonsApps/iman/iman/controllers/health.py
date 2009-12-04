import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.health_tables import Weight, Unit
from iman.model.account_tables import User

log = logging.getLogger(__name__)

class HealthController(BaseController):
    
    def __before__(self):
        # Basic Home grown security layer
        if session.get("identity") is None:
            return redirect_to(controller="account", action="login")

    def signout(self):
        return redirect_to(controller="account", action="logout")
    
    def change_password(self):
        return redirect_to(controller="account", action="change_password")
    
    def index(self):
        '''functional and mako method'''
        user = meta.Session.query(User).filter_by(username=session['identity'].username).one()
        c.user_id = user.uid
        c.user = user
        
        c.units = {}
        c.weight = []
        c.last_weight = None
        
        if meta.Session.query(Weight).all() != []:
            c.weight = meta.Session.query(Weight).filter_by(user=user).order_by("created DESC").all() # Queries for only what you own
            if c.weight != []:
                c.last_weight = c.weight[0]
        if meta.Session.query(Unit).all() != []:
            # Create Priority Grouping
            for group in meta.Session.query(Unit).all():
                c.units[group.id] = group._menu_repr_()
            c.units = c.units.items()
            c.units.sort()
        
        return render('/health/index.mako')
    
    def weight_delete(self):
        '''functional method'''
        if id: # if the method is called directly, then ignore the deletion
            meta.Session.delete(meta.Session.query(Weight).filter_by( id = int(request.POST.get("id")) ).first()) # Filter for the object and pend it for deletion
            meta.Session.commit() # Delete the task from the database now.
        
        return redirect_to(action="index")
    
    def weight_add(self):
        '''functional method'''
        
        meta.Session.begin()
        meta.Session.save(
            Weight(weight = float(request.POST.get("weight")),
                 user_id = int(session['identity'].uid),
                 units = int(request.POST.get("unit")))
            )
        meta.Session.commit()
        
        return redirect_to(action="index")
    