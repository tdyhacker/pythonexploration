import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from movies.lib.base import BaseController, render
from movies.model import meta
from movies.model.titles import Title

log = logging.getLogger(__name__)

class TitlesController(BaseController):

    def index(self):
        c.titles = meta.Session.query(Title).all()
        return render('/titles_index.mako')
    
    def add(self): # new
        return render('/titles_add.mako')
    
    def insert(self): # save
        save = Title(**{"name": request.params['name'],
                "duration": request.params['duration'],
                "month": int(request.params['month']),
                "day": int(request.params['day']),
                "year": int(request.params['year']),
                "rating": request.params['rating'],
                "categories": request.params['category']})
        meta.Session.save(save)
        meta.Session.commit()
        return "SAVED!"
    
    def show(self, id):
        c.title = meta.Session.query(Title).filter_by(id=id).one()
        return render("/titles_show.mako")