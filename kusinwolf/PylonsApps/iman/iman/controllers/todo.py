import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.todo_tables import Task, Priority, Category
from iman.model.account_tables import User

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
        user = meta.Session.query(User).filter_by(uid=session['identity'].uid).first()
        
        # Start with hash tables, will be replaced with lists of tuples
        c.priorities = {}
        c.categories = {}
        
        # Create Priority Grouping
        for group in meta.Session.query(Priority).all():
            c.priorities[group.id] = group._menu_repr_()
        c.priorities = c.priorities.items()
        c.priorities.sort()
        
        # Create Category Grouping
        for group in meta.Session.query(Category).all():
            c.categories[group.id] = group._menu_repr_()
        c.categories = c.categories.items()
        c.categories.sort()
        
        pre_sort = {}
        c.tasks = []
        for task in meta.Session.query(Task).filter_by(user=user).all():
            if pre_sort.get(task.priority.severity):
                pre_sort[task.priority.severity].append(task)
            else:
                pre_sort[task.priority.severity] = [task,]
        
        # Order by severity
        for group in pre_sort.keys():
            c.tasks.extend(pre_sort[group])
        
        return render('/todo/index.mako')
    
    def task_delete(self, id):
        '''functional method'''
        if id: # if the method is called directly, then ignore the deletion
            meta.Session.delete(meta.Session.query(Task).filter_by(id=id).first()) # Filter for the object and pend it for deletion
            meta.Session.commit() # Delete the task from the database now.
        
        return redirect_to(controller="todo", action="index", id=None)

    def task_create(self):
        '''functional method'''
        
        meta.Session.begin()
        meta.Session.save(Task(task=str(request.POST.get("task")), priority=meta.Session.query(Priority).filter_by(id=int(request.POST.get("priority"))).first(), category=meta.Session.query(Category).filter_by(id=int(request.POST.get("category"))).first(), user_id=session['identity'].uid))
        meta.Session.commit()
        
        return redirect_to(controller="todo", action="index", id=None)