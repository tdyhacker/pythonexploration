import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta

# Database tables
from iman.model.todo_tables import Task, Priority, Category
from iman.model.account_tables import User

log = logging.getLogger(__name__)

class TodoController(BaseController):  
    
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
    
    def index(self):
        '''functional and mako method'''
        # Gather all needed information ahead of time
        user = meta.Session.query(User).filter_by(uid=session['identity'].uid).first()
        order_type = session.get("order", None) # This will tell us what order the user wants to see their tasks in
        sort_type = request.POST.get("sort_type", None) # Sorting Column
        sort_direction = request.POST.get("sort_direction", None) # Sorting Column Ascending/Decending
        history_order = request.POST.get("history_order", None) # Date Ascending/Decending
        
        if order_type:
            # Options are:
            # Priority, Ascending (a-z), Decending (z-a)
            # Category, Ascending (a-z), Decending (z-a)
            # Sub Orders are
            # Date Ascending (a-z), Decending (z-a)
            order_type = str(order_type).split(",")
            sort_type = sort_type or order_type[0]
            sort_direction = sort_direction or order_type[1]
            history_order = history_order or order_type[2]
        else:
            sort_type = sort_type or "Priority"
            sort_direction = sort_direction or "Ascending"
            history_order = history_order or "Ascending"
        
        # convert unicode
        sort_type = str(sort_type)
        sort_direction = str(sort_direction)
        history_order = str(history_order)
        
        # Send the order criteria to the session for memory
        order_type = sort_type + "," + sort_direction + "," + history_order
        session["order"] = order_type
        session.save()
        
        # Sort Types and Directions
        c.sort_type = ["Priority", "Category"]
        c.direction = ["Ascending", "Decending"]
        
        # Start with hash tables, will be replaced with lists of tuples
        c.priorities = {}
        c.categories = {}
        
        # Breaker category
        pre_sort = {}
        # What is printed out on the page
        c.tasks = []
        
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
        
        if sort_type == "Priority":
            # Breaks all tasks out by priority
            for task in meta.Session.query(Task).filter_by(user=user).all():
                if pre_sort.get(task.priority[0].severity):
                    pre_sort[task.priority[0].severity].append(task)
                else:
                    pre_sort[task.priority[0].severity] = [task,]
            
        elif sort_type == "Category":
            # Breaks all tasks out by category
            for task in meta.Session.query(Task).filter_by(user=user).all():
                if pre_sort.get(task.category[0].name):
                    pre_sort[task.category[0].name].append(task)
                else:
                    pre_sort[task.category[0].name] = [task,]
        
        # Order by Ascending
        keys = pre_sort.keys()
        
        if sort_direction == "Decending":
            # Order by Decending
            keys.reverse()
        
        for group in keys:
            if history_order == "Decending": # Newest to oldest
                pre_sort[group].reverse()
            
            # Else sort by Ascending Date / Oldest to Newest
            c.tasks.extend(pre_sort[group])
        
        return render('/todo/index.mako')
    
    def task_delete(self):
        '''functional method'''
        if id: # if the method is called directly, then ignore the deletion
            meta.Session.delete(meta.Session.query(Task).filter_by( id = int(request.POST.get("id")) ).first()) # Filter for the object and pend it for deletion
            meta.Session.commit() # Delete the task from the database now.
        
        return redirect_to(controller="todo", action="index", id=None)

    def task_create(self):
        '''functional method'''
        
        meta.Session.begin()
        meta.Session.save(
            Task(task = str(request.POST.get("task")),
                 user_id = int(session['identity'].uid),
                 user = meta.Session.query(User).filter_by(uid=int(session['identity'].uid)).first(),
                 priority = [meta.Session.query(Priority).filter_by(id=int(request.POST.get("priority"))).first(),],
                 category = [meta.Session.query(Category).filter_by(id=int(request.POST.get("category"))).first(),])
            )
        meta.Session.commit()
        
        return redirect_to(controller="todo", action="index", id=None)