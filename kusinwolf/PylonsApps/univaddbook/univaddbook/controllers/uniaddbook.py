import logging
from datetime import datetime
import csv

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from univaddbook.lib.base import BaseController, render
from univaddbook.model import meta
from univaddbook.model.tables import Contact, Email, Type, Relationship, State

log = logging.getLogger(__name__)

class UniaddbookController(BaseController):
    '''All mako and functional controllers are expressed in their docs. Each controller is specific to their function'''
    
    def csv_import(self):
        '''functional controller'''
        myfile = request.params['contacts']
        contacts = csv.reader(myfile.value.split("\n"), delimiter="|")
        
        # Column names
        columns = contacts.next()
        
        meta.Session.begin()
        
        # row in the file
        for contact in contacts:
            # position in the row
            row = {}
            for pos in range(len(contact)):
                row[columns[pos].lower()] = contact[pos]
            
            if row: # has something
                state = meta.Session.query(State).filter_by(name=row['state']).all()
                
                # If the state is not apart of the database
                if not state:
                    meta.Session.begin(subtransactions=True)
                    meta.Session.add(State(name=row['state'], short=""))
                    meta.Session.commit()
                
                state_id = meta.Session.query(State).filter_by(name=row['state']).one().id
                
                c = Contact(
                        first_name = row['firstname'],
                        middle_name = "",
                        last_name = row['lastname'],
                        nick_name = "",
                        birthday = datetime(year=int(row['birthday'][6:10]), month=int(row['birthday'][0:2]), day=int(row['birthday'][3:5])),
                        street_address = row['street'],
                        country = row['country'],
                        city = row['city'],
                        zipcode = row['zipcode'],
                        state_id = state_id,
                        relationship_id = int(row['relationship']))
                e = Email(email=row['email'], type_id=int(row['group']))
                c.emails.append(e)
                meta.Session.add_all([c, e])
        
        meta.Session.commit()
        return redirect_to(controller='uniaddbook', action='index')
    
    def csv_export(self):
        '''functional controller'''
        return "Now I'm really exporting!"

    def contact_add(self):
        '''mako controller'''
        
        self.contact_selection_boxes()
        
        session['id'] = meta.Session.query(Contact).order_by('id DESC').all()[0].id
        session.save()
        return render('/contact_add.mako')

    def contact_addemail(self):
        '''functional controller'''
        meta.Session.begin()
        contact = meta.Session.query(Contact).filter_by(id=request.params['id']).one()
        email = Email(email=request.params['email'], type_id=request.params['group'])
        contact.emails.append(email)
        meta.Session.add(email)
        meta.Session.commit()
        session['id'] = contact.id
        session.save()
        return redirect_to(controller='uniaddbook', action='contact_show', method="post")
    
    def contact_delete(self):
        '''functional controller'''
        meta.Session.begin()
        meta.Session.delete(meta.Session.query(Contact).filter_by(id=int(request.params['id'])).one())
        meta.Session.commit()
        return redirect_to(controller='uniaddbook', action='index')
    
    def contact_edit(self):
        '''mako controller'''
        c.contact = meta.Session.query(Contact).filter_by(id=request.params['id']).one()
        
        session['edit'] = True
        session['fname'] = c.contact.first_name
        session['lname'] = c.contact.last_name
        session['mname'] = c.contact.middle_name
        session['nname'] = c.contact.nick_name
        session['State'] = c.contact.state_id
        session['city'] = c.contact.city
        session['street'] = c.contact.street_address
        session['year'] = c.contact.birthday.year
        session['month'] = c.contact.birthday.month
        session['day'] = c.contact.birthday.day
        session['zipcode'] = c.contact.zipcode
        session['relationship'] = c.contact.relationship_id
        session['id'] = request.params['id']
        session.save()
        
        self.contact_selection_boxes()
        
        return render('/contact_add.mako')

    def contact_export(self):
        '''mako controller'''
        return "Is a be exportin'! :D"
    
    def contact_import(self):
        '''mako controller'''
        return render('/contact_import.mako')
    
    def contact_insert(self):
        '''functional controller'''
        if session.has_key("edit"):
            session['update'] = {}
            for item in request.params.items():
                session['update'][item[0]] = item[1]
            session.save()
            return redirect_to(controller='uniaddbook', action='contact_update', method="post")
        else:
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
    
    def contact_selection_boxes(self):
        '''functional controller'''
        c.relationships = {}
        for group in meta.Session.query(Relationship).all():
            c.relationships[group.id] = group
        c.relationships = c.relationships.items()
        c.relationships.sort()
        
        c.states = {}
        for state in meta.Session.query(State).all():
            c.states[state.id] = state.name.title()
        c.states = c.states.items()
    
    
    def contact_show(self):
        '''mako controller'''
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
    
    def contact_update(self):
        '''functional controller'''
        meta.Session.begin()
        #Update the information
        contact = meta.Session.query(Contact).filter_by(id=session['id']).one()
        contact.first_name = str(session['update']['fname'])
        contact.middle_name = str(session['update']['mname'])
        contact.last_name = str(session['update']['lname'])
        contact.nick_name = str(session['update']['nname'])
        contact.birthday = datetime(year=int(session['update']['year']), month=int(session['update']['month']), day=int(session['update']['day']))
        contact.street_address = str(session['update']['street'])
        contact.country = str(session['update']['country'])
        contact.city = str(session['update']['city'])
        contact.zipcode = int(session['update']['zipcode'])
        contact.state_id = int(session['update']['State'])
        contact.relationship_id = int(session['update']['relationship'])
        meta.Session.update(contact)
        meta.Session.commit()
        
        #Clean the session for bugs
        for key in session:
            del session[key]
        session['id'] = contact.id
        session.save()
        return redirect_to(controller='uniaddbook', action='contact_show', method="post")

    def index(self):
        '''mako controller'''
        c.contacts = meta.Session.query(Contact).order_by("last_name").all()
        return render('/index.mako')