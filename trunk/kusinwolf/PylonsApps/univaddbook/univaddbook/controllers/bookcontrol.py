import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from univaddbook.lib.base import BaseController, render

log = logging.getLogger(__name__)

class BookcontrolController(BaseController):
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
        return render('/index.mako')
    
    def contact_add(self):
        c.states = self.states.items()
        c.states.sort()
        return render('/contact_add.mako')

    def insert(self):
        return request.params.items()