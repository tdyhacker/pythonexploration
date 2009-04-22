import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from univaddbook.lib.base import BaseController, render
from univaddbook.model import meta
from univaddbook.model.tables import Contact, Email, Type, Relationship, State

log = logging.getLogger(__name__)

class UniaddbookController(BaseController):
    
    def index(self):
        c.contacts = meta.Session.query(Contact).order_by("last_name").all()
        return render('/index.mako')
    
    def contact_add(self):
        
        c.relationships = {}
        for group in meta.Session.query(Relationship).all():
            c.relationships[group.id] = group
        c.relationships = c.relationships.items()
        c.relationships.sort()
        
        c.states = {}
        for state in meta.Session.query(State).all():
            c.states[state.id] = state.name.title()
        c.states = c.states.items()
        session['id'] = meta.Session.query(Contact).order_by('id DESC').all()[0].id
        session.save()
        return render('/contact_add.mako')

    def contact_addemail(self):
        meta.Session.begin()
        contact = meta.Session.query(Contact).filter_by(id=request.params['id']).one()
        email = Email(email=request.params['email'], type_id=request.params['group'])
        contact.emails.append(email)
        meta.Session.add(email)
        meta.Session.commit()
        session['id'] = contact.id
        session.save()
        return redirect_to(controller='uniaddbook', action='contact_show', method="post")
    
    def contact_insert(self):
        meta.Session.begin()
        meta.Session.add(Contact(first_name = str(request.params['fname']),
                    middle_name = str(request.params['mname']),
                    last_name = str(request.params['lname']),
                    nick_name = str(request.params['nname']),
                    birthday = datetime(year=int(request.params['year']), month=int(request.params['month']), day=int(request.params['day'])),
                    street_address = str(request.params['street']),
                    country = str(request.params['country']),
                    city = str(request.params['city']),
                    zipcode = int(request.params['zipcode']),
                    state_id = int(request.params['State']),
                    relationship_id = int(request.params['relationship'])))
        meta.Session.commit()
        session["id"] = meta.Session.query(Contact).order_by("id DESC").all()[0].id
        session.save()
        return redirect_to(controller='uniaddbook', action='contact_show', method="post")
    
    def contact_delete(self):
        meta.Session.begin()
        meta.Session.delete(meta.Session.query(Contact).filter_by(id=int(request.params['id'])).one())
        meta.Session.commit()
        return redirect_to(controller='uniaddbook', action='index')
    
    def contact_show(self):
        if session.has_key("id"):
            id = session['id']
            del session['id']
            session.save()
        else:
            id = int(request.params['id'])
            
        c.contact = meta.Session.query(Contact).filter_by(id=id).one()
        
        c.emails = {}
        for email in c.contact.emails:
            if not c.emails.has_key(email.group):
                c.emails[email.group] = []
            c.emails[email.group].append(email.email)
        
        c.groups = {}
        for group in meta.Session.query(Type).all():
            c.groups[group.id] = group.name
        c.groups = c.groups.items()
        return render('/contact_show.mako')
    
    def contact_import(self):
        return "Is a be importin'! :D"
    
    def contact_export(self):
        return "Is a be exportin'! :D"
