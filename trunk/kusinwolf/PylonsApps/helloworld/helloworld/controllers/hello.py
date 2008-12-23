import logging, math, random, datetime, re, socket
import pylons # this is not really needed
from pylons import config

from time import strftime
from Cookie import SimpleCookie
from math import floor, ceil

from helloworld.lib.base import *

from helloworld.model import meta
from helloworld.model.link_table import *
from helloworld.model.tags_table import *
from helloworld.lib import libtool

log = logging.getLogger(__name__)

class HelloController(BaseController):
    
    # I'm not liking this idea at all
    makoToController = {"inactivelist": "inactive", "alllinks": "allLinks",
                        "serverinfo": "index", "edit": "edit"}
    
    # Main Page
    def index(self):
        c.helloobj = self
        link = notes = tags = ''
        
        if request.params.has_key("link"):
            link = request.params['link']
            
        if request.params.has_key("notes"):
            notes = request.params['notes']
            
        if request.params.has_key("tags"):
            tags = request.params['tags']
        
        if link:
            if not libtool.isInTable(meta.Session, Links, "link = '%s'" % libtool.linkAppend(link)):
                meta.Session.save(Links(link, notes, tags, True))
                meta.Session.commit()
                c.success = "Save completed"
            else:
                id = meta.Session.query(Links).select_whereclause("link = '%s'" % libtool.linkAppend(link))[0].getID()
                c.success = "Save failed\nSaved here <a href='http://%s/hello/edit?id=%s'>link</a>" % (request.headers['Host'], id)
        
        if request.params.has_key('order'):
            if request.params['order'] == 'Added':
                c.link_data = meta.Session.query(Links).order_by(Links.addtime.desc()).limit(10).select_whereclause("active")
            elif request.params['order'] == 'Modifed':
                c.link_data = meta.Session.query(Links).order_by(Links.modtime.desc()).limit(10).select_whereclause("active")
            else:
                c.link_data = meta.Session.query(Links).order_by(Links.id.desc()).limit(10).select_whereclause("active")
        else:
            c.link_data = meta.Session.query(Links).order_by(Links.id.desc()).limit(10).select_whereclause("active")
        return render("/serverinfo.mako")
    
    # Entire Link's Page
    def allLinks(self):
        # Has to deal with the amount of items on a page
        c.pagelimits = [1, 5, 10, 20, 50, 100]
        
        if request.params.has_key('limit') and request.params.has_key('offset'):
            # Has to deal with which page they are currently on
            c.pagenumber = int(request.params['offset'])
            
            # Has to deal with the amount of items on a page
            c.pagesize = int(request.params['limit'])
            
            c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("active"))/float(c.pagesize)))

            if c.pagenumber > c.pageoffset:
                    c.pagenumber = 1

            c.link_data = meta.Session.query(Links).order_by(Links.id.desc()).limit(c.pagesize).offset(c.pagesize * (c.pagenumber - 1) ).select_whereclause("active")
            
        else:
            c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("active"))/float(20)))
            c.pagesize = 20 # selects a default amount limit
            c.pagenumber = 1 # They have not selected a page yet
            c.link_data = meta.Session.query(Links).order_by(Links.id.desc()).select_whereclause("active")
            
        return render('/alllinks.mako')
    
    
    # Inactive Page
    def inactive(self):
        c.link_data = meta.Session.query(Links).order_by(Links.id.desc()).select_whereclause("not active")
        return render("/inactivelist.mako")
    
    
    # Edit Page
    def edit(self):
        if request.params.has_key('id'):
            id = request.params['id']
            
        changed = False
        
        c.link_data = meta.Session.query(Links).filter_by(id=id).first()
    
        if request.params.has_key("link"):
            if c.link_data.setLink(request.params['link']):
                changed = changed or True
                
        if request.params.has_key("notes"):
            if c.link_data.setNotes(request.params['notes']):
                changed = changed or True
                
        if request.params.has_key("tags"):
            if c.link_data.setTags(request.params['tags']):
                changed = changed or True
            
        if request.params.has_key("active"):
            if c.link_data.setActivity(request.params['active']):
                changed = changed or True
        
        if changed:
            try:
                c.link_data.setModTime()
                meta.Session.commit()
                c.success = "Save completed"
            except:
                c.success = "Save failed"
            
        return render("/edit.mako")
    
    # Search through Tags Page
    def search(self):
        # Has to deal with the amount of items on a page
        c.pagelimits = [1, 5, 10, 20, 50, 100]
        
        if request.params.has_key('limit') and request.params.has_key('offset'):
            # Has to deal with which page they are currently on
            c.pagenumber = int(request.params['offset'])
            
            # Has to deal with the amount of items on a page
            c.pagesize = int(request.params['limit'])
            
            if request.params.has_key('tags'):
                c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("tags like '%%%s%%' and active" % str(request.params['tags'])))/float(request.params['limit'])))
                
                if c.pagenumber > c.pageoffset:
                    c.pagenumber = 1
                
                c.link_data = meta.Session.query(Links).limit(c.pagesize).offset(c.pagesize * (c.pagenumber - 1) ).select_whereclause("tags like '%%%s%%' and active" % str(request.params['tags']))
                c.tags = request.params['tags']
            else:
                c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("tags not like '' and active"))/float(request.params['limit'])))
                c.link_data = meta.Session.query(Links).limit(c.pagesize).offset(c.pagesize * (c.pagenumber - 1) ).select_whereclause("tags not like '' and active")
                c.tags = ""
        elif request.params.has_key('tags'):
            c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("active"))/float(20)))
            c.pagesize = 20 # selects a default amount limit
            c.pagenumber = 1 # They have not selected a page yet
            c.tags = request.params['tags']
            c.link_data = meta.Session.query(Links).select_whereclause("tags like '%%%s%%' and active" % str(request.params['tags']))
        else:
            c.pageoffset = int(ceil(len(meta.Session.query(Links).select_whereclause("active"))/float(20)))
            c.pagesize = 20 # selects a default amount limit
            c.pagenumber = 1 # They have not selected a page yet
            c.tags = ""
            c.link_data = meta.Session.query(Links).limit(c.pagesize).offset(c.pagesize * (c.pagenumber - 1) ).select_whereclause("tags not like '' and active")
            
        return render("/search.mako")
    
    # Amount of Use per word Page
    def stats(self):
        c.stats = {}
        for link in meta.Session.query(Links).select_whereclause("tags not like '' and active"): # this gets every entry with tags in it
            for tag in link.parseTags():
                try:
                    c.stats[str(tag)] += 1
                except:
                    c.stats[str(tag)] = 1
                    
        size = len(c.stats)
        sum = 0
        max = 0
        min = c.stats[c.stats.keys()[0]]
        for m in c.stats:
            if max < c.stats[m]:
                max = c.stats[m]
            if min > c.stats[m]:
                min = c.stats[m]
            sum += c.stats[m]
        ave = sum / size
        
        #Minimum 5pt
        #[ % ]
        #Average 15pt = int(ave)
        #[ % ]
        #Maximum 25pt
        
        for s in c.stats:
            fsize = int((c.stats[s] / float(max)) * 25)
            c.stats[s] = [c.stats[s], fsize]
        
        c.sorted = []
        for a in c.stats:
            c.sorted.append([c.stats[a], a])
        
        # This will return a list from low to high order
        def compare(x, y):
            # Orders by ticker number, then by name
            if x[0][0] > y[0][0]:
                return 1
            elif x[0][0] < y[0][0]:
                return -1
            else:
                return 0

        # This uses my compare function along with reverse the order in which it is being sorted
        c.sorted.sort(compare, None, True)
        
        
        #meta.Session.query(Links).select_whereclause("tags like ''") # this gets every entry with no tags in it

        return render("/stats.mako")
    
    def test(self):
        c.link_data = meta.Session.query(Links).order_by(Links.addtime.desc())
        try:
            location = str(request.params["Locations"])
        except:
            location = ''
        c.drops = []
        for data in c.link_data:
            if location == data.link:
                c.drops.append(("<option selected='selected' value=%s>%s</option>") % (data.id, data.link))
            else:
                c.drops.append(("<option value=%s>%s</option>") % (data.id, data.link))
        
        #${h.select("Locations", ["<option>%s - %s</option>" % (a.id, a.link) for a in c.link_data])}
        #% for a in range(50):
        #    ${"<font style=\"font-size: %spt\">Testing</font>" % a}
        #    <BR>
        #% endfor
        return render("/test.mako")
    
    
    #def authorized(self):
    #    cookie = SmartCookie( espy.request.http_cookie )
    #    if cookie.has_key('my_cookie'):
    #        return True
    #    else:
    #        return False
    #
    #def logit(self):
    #    my_cookie = SimpleCookie()
    #    my_cookie['my_cookie'] = "Andrew"
    #    my_cookie['my_cookie']['path'] = '/hello'
    #    my_cookie['my_cookie']['domain'] = request.headers['Host'] # Is this is the domain?
    #    my_cookie['my_cookie']['expires'] = 2592000 # 30 days
    #    
    #    response.headers['Set-Cookie'] = my_cookie.output(header='')
    #    
    #    response.write(response.headers)
    #    response.write("<BR><BR>")
    #    response.write(request.http_cookie)
    #    #redirect_to(controller="hello", action='index')
    #
    #def parse(self):
    #    # Old parse for links from playlist.com
    #    c.active = True # This is just a simi local value until I find a purpose for it on insertion
    #    self.strip()
    #    """<a href="%s">%s</a>""" % (c.link, c.link)
    #    if request.params.has_key('link'):
    #        if request.params['link'] != '' and request.params['link'] != ' ':
    #            if not c.link:
    #                c.link = request.params['link']
    #            if not c.songname:
    #                c.songname = "Unknown"
    #            
    #            if not meta.Session.query(Links).filter_by(newlink=c.link).first():
    #                meta.Session.save(Links(request.params['link'], c.link, c.songname, c.active))
    #                meta.Session.commit()
    #                if g.DEBUG:
    #                    print "Added link named '%s'" % c.link
    #            else:
    #                if g.DEBUG:
    #                    print "Failed Adding link named '%s'" % c.link
    #        else:
    #            if g.DEBUG:
    #                print "Failed Adding link named '%s'" % c.link
    #    
    #def strip(self):
    #    # used by the old Parse module
    #    parseTable = {'%20':' ', '%3C':'<', '%3E':'>', '%23':'#', '%25':'%', '%7B':'{', '%7D':'}',
    #                  '%7C':'|', '%5C':'\\', '%5E':'^', '%7E':'~', '%5B':'[', '%5D':']', '%60':'`', '%3B':';', '%2F':'/', '%3F':'?',
    #                  '%3A':':', '%40':'@', '%3D':'=', '%26':'&', '%24':'$', '%2025': ' '}
    #    parse = re.compile('.*originallink=(.*)')
    #    sname = re.compile('.*/(.*).mp3.*')
    #    
    #    #print request.params
    #    if request.params.has_key('link'): 
    #        a = request.params['link'] # if this is blank then it'll fault
    #        if parse.match(a):
    #            a = parse.match(a).groups()[0]
    #            for b in parseTable:
    #                a = a.replace("%s" % b, "%s" % parseTable[b])
    #            c.link = a
    #            if sname.match(a):
    #                c.songname = sname.match(a).groups()[0]
    #            else:
    #                c.songname = 'Unknown'
    #        
    #    return "" # complete
    
    # Setting the front end of links to inactive
    # Just inactivates an object to keep the user from completely deleting the information
    def inactivateObject(self):
        for id in request.POST.getall('Delete'):
            object = meta.Session.query(Links).filter_by(id=int(id)).first()
            object.active = False
            object.inatime = strftime("%b %d %Y - %H:%M:%S")
            object.modtime = strftime("%b %d %Y - %H:%M:%S")
            meta.Session.commit()
        controller = request.params['Redirect']
        redirect_to(controller="hello", action=self.makoToController[controller])

    # Reactivating Links
    # This is just to select all the inactive fields of data in reverse order
    def activateObject(self):
        for id in request.POST.getall('Activate'):
            object = meta.Session.query(Links).filter_by(id=int(id)).first()
            object.active = True
            object.inatime = "Reactivated"
            object.modtime = strftime("%b %d %Y - %H:%M:%S")
            meta.Session.commit()
        controller = request.params['Redirect']
        redirect_to(controller="hello", action=self.makoToController[controller])
    
    # Master controller for multi button page [Where is this used?]
    def caseDelete(self):
        if request.params.has_key('Delete'):
            self.deleteObject()
        elif request.params.has_key('Activate'):
            self.activateObject()
        else:
            response.write("How did you break it, there's only two buttons!")
            
        controller = request.params['Redirect']
        redirect_to(controller="hello", action=self.makoToController[controller])
    
    # This is a complete deletion of the item
    def deleteObject(self):
        # Old Link setup -> ${h.link_to("Delete", h.url(controller="hello", action="deleteObjectA", id=l.id), confirm="Are you sure?")}
        #Clear all input values with a null string to fix link error
        
        for id in request.POST.getall('Delete'):
            meta.Session.delete(meta.Session.query(Links).filter_by(id=int(id)).first())
            meta.Session.commit()
        
        controller = request.params['Redirect']
        redirect_to(controller="hello", action=self.makoToController[controller])
        