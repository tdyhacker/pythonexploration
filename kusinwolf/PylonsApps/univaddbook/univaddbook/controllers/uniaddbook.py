import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from univaddbook.lib.base import BaseController, render
from univaddbook.model import meta
from univaddbook.model.tables import Contact, Email, Type, Relationship

log = logging.getLogger(__name__)

class UniaddbookController(BaseController):
    states = {
        "AL": "ALABAMA",
        "AK": "ALASKA",
        "AZ": "ARIZONA",
        "AR": "ARKANSAS",
        "CA": "CALIFORNIA",
        "CO": "COLORADO",
        "CT": "CONNECTICUT",
        "DE": "DELAWARE",
        "FL": "FLORIDA",
        "GA": "GEORGIA",
        "HI": "HAWAII",
        "ID": "IDAHO",
        "IL": "ILLINOIS",
        "IN": "INDIANA",
        "IA": "IOWA",
        "KS": "KANSAS",
        "KY": "KENTUCKY",
        "LA": "LOUISIANA",
        "ME": "MAINE",
        "MD": "MARYLAND",
        "MA": "MASSACHUSETTS",
        "MI": "MICHIGAN",
        "MN": "MINNESOTA",
        "MS": "MISSISSIPPI",
        "MO": "MISSOURI",
        "MT": "MONTANA",
        "NE": "NEBRASKA",
        "NV": "NEVADA",
        "NH": "NEWHAMPSHIRE",
        "NJ": "NEWJERSEY",
        "NM": "NEWMEXICO",
        "NY": "NEWYORK",
        "NC": "NORTHCAROLINA",
        "ND": "NORTHDAKOTA",
        "OH": "OHIO",
        "OK": "OKLAHOMA",
        "OR": "OREGON",
        "PA": "PENNSYLVANIA",
        "RI": "RHODEISLAND",
        "SC": "SOUTHCAROLINA",
        "SD": "SOUTHDAKOTA",
        "TN": "TENNESSEE",
        "TX": "TEXAS",
        "UT": "UTAH",
        "VT": "VERMONT",
        "VA": "VIRGINIA",
        "WA": "WASHINGTON",
        "WV": "WESTVIRGINIA",
        "WI": "WISCONSIN",
        "WY": "WYOMING",
    }
    
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
        return request.params.items(), request.POST.items(), request.GET.items()
    
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
    
    # 2,47,(11, 12)