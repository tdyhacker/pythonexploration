import logging
import os
from re import compile
from datetime import datetime, timedelta

from webhelpers.html.tags import link_to
from routes import url_for

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from invenimus.config import environment
from invenimus.lib.base import BaseController, render
from invenimus.model import meta


log = logging.getLogger(__name__)

class PicturesController(BaseController):
    
    def index(self):
        c.path = g.picture_path
        c.pictures = os.listdir("%s." % c.path)
        
        return render("/index.mako")