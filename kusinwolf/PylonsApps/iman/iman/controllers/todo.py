import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta
from iman.model.todo_tables import *

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
import authkit

log = logging.getLogger(__name__)

class TodoController(BaseController):

    @authorize(ValidAuthKitUser())
    def __before__(self):
        '''functional and mako method'''
        pass

    def signout(self):
        # look into this http://wiki.pylonshq.com/display/pylonscookbook/Authentication+and+Authorization for replacing authkit
        return "Thank you come again! ^_^"
    
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
        c.user = meta.Session.query(User).filter_by(username=request.environ.get("REMOTE_USER")).first()
        
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
