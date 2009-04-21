import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from univaddbook.lib.base import BaseController, render
from univaddbook.model import meta
from univaddbook.model.tables import Contact, Email, Type, Relationship

log = logging.getLogger(__name__)

class UniaddbookController(BaseController):
    
    def index(self):
        c.contacts = meta.Session.query(Contact).all()
        return render('/index.mako')
    
    def contact_add(self):
        c.states = self.states.items()
        c.states.sort()
        c.relationships = {}
        for group in meta.Session.query(Relationship).all():
            c.relationships[group.id] = group
        c.relationships = c.relationships.items()
        c.relationships.sort()
        return render('/contact_add.mako')

    def contact_insert(self):
        meta.Session.save(
            Contact(first_name = str(request.params['fname']),
                    middle_name = str(request.params['mname']),
                    last_name = str(request.params['lname']),
                    nick_name = str(request.params['nname']),
                    birthday = datetime(year=int(request.params['year']), month=int(request.params['month']), day=int(request.params['day'])),
                    street_address = str(request.params['street']),
                    state = str(request.params['state']),
                    country = str(request.params['country']),
                    city = str(request.params['city']),
                    zipcode = int(request.params['zipcode']),
                    relationship_id = int(request.params['relationship']),)
        )
        meta.Session.commit()
        return request.params.items()
    
    def contact_delete(self):
        meta.Session.delete(meta.Session.query(Contact).filter_by(id=int(request.params['id'])).one())
        meta.Session.commit()
        return redirect()
    
    def contact_show(self, id):
        id = int(id)
        c.contact = meta.Session.query(Contact).filter_by(id=id).one()
        emails_list = c.contact.emails
        c.emails = {}
        
        for email in emails_list:
            if not c.emails.has_key(email.group):
                c.emails[email.group] = []
            c.emails[email.group].append(email.email)
        
        return render('/contact_show.mako')
