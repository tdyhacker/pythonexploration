import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta
from iman.model.todo_tables import *

log = logging.getLogger(__name__)

class TodoController(BaseController):  
    
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
        c.user = meta.Session.query(User).filter_by(username="kusinwolf").first()
        
        pre_sort = {}
        c.tasks = []
        for task in  meta.Session.query(Task).filter_by(user=c.user).all():
            if pre_sort.get(task.priority.severity):
                pre_sort[task.priority.severity].append(task)
            else:
                pre_sort[task.priority.severity] = [task,]
        
        for item in pre_sort.keys():
            c.tasks.extend(pre_sort[item])
            
        c.priorties = meta.Session.query(Priority).all()
        c.categories = meta.Session.query(Category).all()
        return render('/todo/index.mako')
