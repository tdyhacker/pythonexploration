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
        return render('/contact_add.mako')

    def contact_insert(self):
        meta.Session.save(
            Contact(first_name = request.params['fname'],
                    middle_name = request.params['mname'],
                    last_name = request.params['lname'],
                    nick_name = request.params['nname'],
                    birthday = datetime(year=int(request.params['year']), month=int(request.params['month']), day=int(request.params['day'])),
                    street_address = request.params['street'],
                    state = request.params['state'],
                    country = request.params['country'],
                    city = request.params['city'],
                    zipcode = int(request.params['zipcode']),
                    relationship_id = int(request.params['fname']),)
        )
        meta.Session.commit()
        return request.params.items()
    
    def contact_delete(self):
        return request.params.items()
    