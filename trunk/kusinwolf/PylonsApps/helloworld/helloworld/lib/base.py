"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render
from helloworld.model import meta

import helloworld.lib.helpers as h
import helloworld.model as model

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        conn = meta.engine.connect()
        meta.Session.configure(bind=conn)
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
            conn.close()


# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
