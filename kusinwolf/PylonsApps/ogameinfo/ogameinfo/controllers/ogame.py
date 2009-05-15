import logging
from re import compile
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from ogameinfo.lib.base import BaseController, render
from ogameinfo.model import meta
from ogameinfo.model.tables import *

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn

log = logging.getLogger(__name__)

class OgameController(BaseController):
    
    @authorize(ValidAuthKitUser())
    def __before__(self):
        '''functional and mako method'''
        pass
        #if not request.environ.get("REMOTE_USER"):
        #    response.status = "401 Not authenticated"
        #    return "You are not authenticated"
        #if not session.has_key('login') or not session.has_key('password') or meta.Session.query(User).filter_by(username=str(session['login']), password=str(session['password'])).first() == None:
        #    c.fail = "Login attempt failed"
        #    return render('/login.mako')
        # They passed the auth, let them through

    def signout(self):
        return "You're now signed out."
    
    def auth(self):
        login = str(request.params['login'])
        password = str(request.params['password'])
        
        if meta.Session.query(User).filter_by(username=login, password=password).first():
            session['login'] = login
            session['password'] = password
            session.save()
        
        return redirect_to(action='index')

    def auth_change_display(self):
        '''mako method'''
        return render("/auth_change_display.mako")
    
    def auth_change_password(self):
        '''functional method'''
        user = meta.Session.query(User).filter_by(username=login, password=password).first()
        
        if str(request.params['password_1']) == str(request.params['password_2']):
            user.password = str(request.params['password_1'])
            meta.Session.save_or_update(user)
        else:
            c.fail = "Passwords did not math"
            return redirect_to(action="auth_change_display")

    def index(self):
        '''mako method'''
        c.e_reports = meta.Session.query(Espionage).order_by("id DESC").all()
        return render('/index.mako')
    
    def espionage_insert(self):
        '''functional method'''
        e_report = str(request.params['report'])
        
        e_report = e_report.replace(".", "")
        
        info = {}
        info['year'] = datetime.now().year
        
        fleet_rows = 0
        defence_rows = 0
        building_rows = 0
        research_rows = 0
        
        stage = 0
        
        for row in e_report.split("\r\n"):
            if compile(".*Resources on (.*) \[(.*)\] \(Player \'(.*)\'\).*").match(row):
                info['planet_location_player'] = compile(".*Resources on (.*) \[(.*):(.*):(.*)\] \(Player \'(.*)\'\).*").match(row).groups()
            
            if compile(".*at (\d\d)-(\d\d) (\d\d):(\d\d):(\d\d).*").match(row):
                info['date'] = compile(".*at (\d\d)-(\d\d) (\d\d):(\d\d):(\d\d).*").match(row).groups()
            
            if stage == 0 and compile(".*Metal:\t(.*)\tCrystal:\t(.*)").match(row):
                info['metal_and_crystal'] = compile(".*Metal:\t(.*)\tCrystal:\t(.*)").match(row).groups()
            elif stage == 5 and compile(".*Metal:\t(.*)\tCrystal:\t(.*)").match(row):
                info['debris_metal_and_crystal'] = compile(".*Metal:\t(.*)\tCrystal:\t(.*)").match(row).groups()
            
            if compile(".*Deuterium:\t(.*)\tEnergy:\t(.*)").match(row):
                info['deuterium_and_energy'] = compile(".*Deuterium:\t(.*)\tEnergy:\t(.*)").match(row).groups()
            
            if row == "Fleets":
                stage = 1
                
            if row == "Defense":
                stage = 2
                
            if row == "Buildings":
                stage = 3
                
            if row == "Research":
                stage = 4
            
            if row == "Debris Field":
                stage = 5
            
            
            if compile("(.*)\t(.*) \t(.*)\t(.*)").match(row):
                if stage == 1: # fleet
                    info['fleet_row%d' % fleet_rows] = compile("(.*)\t(.*) \t(.*)\t(.*)").match(row).groups()
                    fleet_rows += 1
                    
                if stage == 2: # defense
                    info['defence_row%d' % defence_rows] = compile("(.*)\t(.*) \t(.*)\t(.*)").match(row).groups()
                    defence_rows += 1
                    
                if stage == 3: # buildings
                    info['building_row%d' % building_rows] = compile("(.*)\t(.*) \t(.*)\t(.*)").match(row).groups()
                    building_rows += 1
                    
                if stage == 4: # research
                    info['research_row%d' % research_rows] = compile("(.*)\t(.*) \t(.*)\t(.*)").match(row).groups()
                    research_rows += 1
            
            if compile(".*Chance of counter-espionage:(.*)%.*").match(row):
                info['counter-espionage'] = compile(".*Chance of counter-espionage:(.*)%.*").match(row).groups()
        
        meta.Session.begin()
        
        player = meta.Session.query(Player).filter_by(name=info['planet_location_player'][4]).first()
        planet = meta.Session.query(Planet).filter_by(galaxy=int(info['planet_location_player'][1]), system=int(info['planet_location_player'][2]), orbit=int(info['planet_location_player'][3])).first()
        
        if player == None:
            player = Player(name=info['planet_location_player'][4])
        
        if planet == None:
            planet = Planet(name=info['planet_location_player'][0], galaxy=int(info['planet_location_player'][1]), system=int(info['planet_location_player'][2]), orbit=int(info['planet_location_player'][3]))
            player.planets.append(planet)
        
        espionage_report = Espionage(counter_espionage=int(info['counter-espionage'][0]), created=datetime(year=info['year'], month=int(info['date'][0]), day=int(info['date'][1]), hour=int(info['date'][2]), minute=int(info['date'][3]), second=int(info['date'][4])))
        player.espionaged.append(espionage_report)
        espionage_report.planet.append(planet) # This report is tied to this planet
        
        metal = Resource(amount=int(info['metal_and_crystal'][0]))
        crystal = Resource(amount=int(info['metal_and_crystal'][1]))
        deuterium = Resource(amount=int(info['deuterium_and_energy'][0]))
        energy = Resource(amount=int(info['deuterium_and_energy'][1]))
        metal_debris = Resource(amount=int(info['debris_metal_and_crystal'][0]))
        crystal_debris = Resource(amount=int(info['debris_metal_and_crystal'][1]))
        
        metal.type = meta.Session.query(Resource_type).filter_by(name="Metal").first()
        crystal.type = meta.Session.query(Resource_type).filter_by(name="Crystal").first()
        deuterium.type = meta.Session.query(Resource_type).filter_by(name="Deuterium").first()
        energy.type = meta.Session.query(Resource_type).filter_by(name="Energy").first()
        metal_debris.type = meta.Session.query(Resource_type).filter_by(name="Metal Debris").first()
        crystal_debris.type = meta.Session.query(Resource_type).filter_by(name="Crystal Debris").first()
        
        espionage_report.resources.append(metal)
        espionage_report.resources.append(crystal)
        espionage_report.resources.append(deuterium)
        espionage_report.resources.append(energy)
        espionage_report.resources.append(metal_debris)
        espionage_report.resources.append(crystal_debris)
        
        for total in range(fleet_rows):
            for col in range(0, len(info['fleet_row%d' % total]), 2):
                s = Ship(amount=int(info['fleet_row%d' % total][col + 1]))
                s.type = meta.Session.query(Ship_type).filter_by(name=info['fleet_row%d' % total][col].capitalize()).first()
                espionage_report.fleet.append(s)
        
        for total in range(research_rows):
            for col in range(0, len(info['research_row%d' % total]), 2):
                r = Research(level=int(info['research_row%d' % total][col + 1]))
                r.type = meta.Session.query(Research_type).filter_by(name=info['research_row%d' % total][col].capitalize()).first()
                espionage_report.research.append(r)
        
        for total in range(defence_rows):
            for col in range(0, len(info['defence_row%d' % total]), 2):
                d = Defence(amount=int(info['defence_row%d' % total][col + 1]))
                d.type = meta.Session.query(Defence_type).filter_by(name=info['defence_row%d' % total][col].capitalize()).first()
                espionage_report.defences.append(d)
        
        for total in range(building_rows):
            for col in range(0, len(info['building_row%d' % total]), 2):
                b = Building(level=int(info['building_row%d' % total][col + 1]))
                b.type = meta.Session.query(Building_type).filter_by(name=info['building_row%d' % total][col].capitalize()).first()
                espionage_report.buildings.append(b)
        
        meta.Session.save_or_update(espionage_report)
        meta.Session.commit()
        
        return redirect_to(controller="ogame", action="index")
    
    def espionage_show(self, id):
        c.e_report = meta.Session.query(Espionage).filter_by(id=int(id)).first()
        
        amount = c.e_report.resources[0].amount + c.e_report.resources[1].amount + c.e_report.resources[2].amount
        samount = ""
        for l in range(len(str(amount))):
            if l % 3 == 0 and l != 0:
                samount = "," + samount
            
            samount = str(amount)[len(str(amount)) - l - 1] + samount
        c.samount = samount
        return render('/espionage_show.mako')
    
    def planet_search(self):
        id = str(request.params['galaxy'])
        id += "%03d" % int(request.params['system'])
        id += "%02d" % int(request.params['orbit'])
        return redirect_to(action='planet_show', id=id)
    
    def planet_show(self, id):
        id = str(id)
        if len(id) != 6:
            return "Invalid ID"
        c.planet = meta.Session.query(Planet).filter_by(galaxy = int(id[0]), system = int(id[1:4]), orbit = int(id[4:6])).first()
        if c.planet == None:
            return "Planet either does not exist or has not been scanned yet"
        else:
            return render('/planet_show.mako')
    
    def player_show(self, id):
        c.player = meta.Session.query(Player).filter_by(id=id).first()
        return render('/player_show.mako')
