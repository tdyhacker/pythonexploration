import logging
import os
import math
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

	def index(self, id = 1):
		if request.POST.get("directories"):
			# Move to new sub directory
			c.path = g.directories[int(request.POST.get("directories"))]
			if c.path != "":
				c.path += "/"
			session['directory'] = c.path
			session.save()
			return redirect_to(action = "index", id = 1)
		elif session.get("directory"):
			# Load old sub directory
			c.path = str(session.get("directory"))
		else:
			c.path = ""
			session['directory'] = c.path
			session.save()
		
		if request.POST.get("destination"):
			c.move_to_path = g.directories[int(request.POST.get("destination"))]
			session['destination'] = c.move_to_path
			session.save()
		elif session.get("destination") or session.get("destination") == "": # because of the parent path is a blank string
			c.move_to_path = str(session.get("destination"))
		else:
			c.move_to_path = "Marked"
			session['destination'] = c.move_to_path
			session.save()
		
		c.request = request
		c.pictures = []
		c.directories = {}
		picture_list = os.listdir("%s%s." % (g.picture_path, c.path))
		picture_list.sort()
		
		c.min = 0
		c.max = int(math.ceil(len(picture_list) / 50.0))
		c.id = int(id)

		for group in range(len(g.directories)):
			c.directories[group] = g.directories[group]
		c.directories = c.directories.items()
		c.directories.sort()

		for i in range(0 + (50 * (c.id - 1)), 50 * c.id):
			if i < len(picture_list):
				c.pictures.append(picture_list[i])

		return render("index.mako")

	def move_images(self, id = 1):
		#os.rename("J:/Pictures/1.jpg", "J:/Pictures/Marked/1.jpg")
		path = ""
		move_to_path = "Marked" # Default location
		to_be_marked = request.POST.getall('Mark')
		id = int(id)
		
		if session.get("directory"):
			# If they're in a sub directory use it
			path = str(session.get("directory")).replace("\\", "/")
		
		if session.get("destination") or session.get("destination") == "": # because of the parent path is a blank string
			move_to_path = str(session.get("destination"))
		
		picture_list = os.listdir("%s%s." % (g.picture_path, path))
		picture_list.sort()
		
		if not os.access("%s%s" % (g.picture_path, move_to_path), os.F_OK):
			os.mkdir("%s%s" % (g.picture_path, move_to_path))
		
		for img in [picture_list[int(a)] for a in to_be_marked]:
			#return "move \"%s%s%s\" \"%sMarked/\"" % (g.picture_path, path, img, g.picture_path)
			os.rename("%s%s%s"% (g.picture_path, path, img), "%s%s/%s" % (g.picture_path, move_to_path, img))
		
		return redirect_to(action = "index")