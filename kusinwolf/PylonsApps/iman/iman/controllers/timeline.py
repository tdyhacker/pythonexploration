import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, app_globals as g
from pylons.controllers.util import abort, redirect_to

from iman.config import environment
from iman.lib.base import BaseController, render
from iman.model import meta
from iman.model.timeline_tables import Event

log = logging.getLogger(__name__)

class TimelineController(BaseController):
    
    def __before__(self):
        pass
    
    def index(self):
        '''functional and mako method'''
        
        c.years = range(1998, 2012)
        c.months = range(1, 13)
        c.days = range(1, 32)
        c.hours = range(0, 24)
        c.minutes = range(0, 60)
        c.seconds = range(0, 60)
        c.duration = ["False", "True"] # Default should be False
        c.icons = ["", "dark-red-circle.png"] # Default should be a blank icon text
        
        return render('/timeline/timeline.mako')
    
    def event_create(self):
        '''functional method'''
        meta.Session.begin_nested()
        
        event = Event(
                    start = datetime(year=int(request.POST.get("start_year")), month=int(request.POST.get("start_month")), day=int(request.POST.get("start_day")), hour=int(request.POST.get("start_hour")), minute=int(request.POST.get("start_minute")), second=int(request.POST.get("start_second"))),
                    title = str(request.POST.get("title", None)),
                    description = str(request.POST.get("description", None)),
                    image = str(request.POST.get("image", None)),
                    link = str(request.POST.get("link", None)),
                    isDuration = (str(request.POST.get("isDuration")) == "True")
                    )
        
        if (str(request.POST.get("isDuration")) == "True"):
            # If there is a duration of time then use the end time, else ignore it
            event.end = datetime(year=int(request.POST.get("end_year")), month=int(request.POST.get("end_month")), day=int(request.POST.get("end_day")), hour=int(request.POST.get("end_hour")), minute=int(request.POST.get("end_minute")), second=int(request.POST.get("end_second")))
        
        event.icon = None
        if request.POST.get("icon", None):
            event.icon = "../" + str(request.POST.get("icon"))
        event.caption = str(request.POST.get("caption", None))
        
        if request.POST.get("color") and len(request.POST.get("color").replace("#","")) == 6:
            event.color = str(request.POST.get("color", None)).replace("#", "") # remove any
        else:
            event.color = None # They didn't listen to the instructions or made a typo
        
        if request.POST.get("textColor") and len(request.POST.get("textColor").replace("#","")) == 6:
            event.textColor = str(request.POST.get("textColor", None)).replace("#", "") # remove any
        else:
            event.textColor = None # They didn't listen to the instructions or made a typo
        
        meta.Session.save(event)
        
        meta.Session.commit()
        
        self.renderJavaScript()
        
        return redirect_to(action="index")

    def renderJavaScript(self):
        '''
        functional method\n
        Render the JavaScript file required for the timeline\n
        '''
        events = meta.Session.query(Event).all()
        
        # WARNING: This file path may require a change for an exact path based on server configuration
        JS_file = file("iman/public/js/timeline.js", "w") 
        JS_file.write("""var timeline_data = {  // save as a global variable
                      'dateTimeFormat': 'iso8601',
                      'wikiURL': "http://simile.mit.edu/shelf/",
                      'wikiSection': "Simile Cubism Timeline",
                      
                      'events' : [\n""")
        
        for event in events:
            JS_file.write(event.js_repr())
            
        JS_file.write("]\n}\n")
        JS_file.close()