INSERT INTO ships (name) VALUES ('Small Cargo');
INSERT INTO ships (name) VALUES ('Large Cargo');
INSERT INTO ships (name) VALUES ('Light Fighter');
INSERT INTO ships (name) VALUES ('Heavy Fighter');
INSERT INTO ships (name) VALUES ('Cruiser');
INSERT INTO ships (name) VALUES ('Battleship');
INSERT INTO ships (name) VALUES ('Colony Ship');
INSERT INTO ships (name) VALUES ('Recylcer');
INSERT INTO ships (name) VALUES ('Espionage Probe');
INSERT INTO ships (name) VALUES ('Bomber');
INSERT INTO ships (name) VALUES ('Solar Satellite');
INSERT INTO ships (name) VALUES ('Destroyer');
INSERT INTO ships (name) VALUES ('Deathstar');
INSERT INTO ships (name) VALUES ('Battlecruiser');

INSERT INTO defences (name) VALUES ('Rocket Launcher');
INSERT INTO defences (name) VALUES ('Light Laser');
INSERT INTO defences (name) VALUES ('Heavy Laser');
INSERT INTO defences (name) VALUES ('Gauss Cannon');
INSERT INTO defences (name) VALUES ('Ion Cannon');
INSERT INTO defences (name) VALUES ('Plasma Turret');
INSERT INTO defences (name) VALUES ('Small Shield Dome');
INSERT INTO defences (name) VALUES ('Large Shield Dome');
INSERT INTO defences (name) VALUES ('Anti-Ballistic Missiles');
INSERT INTO defences (name) VALUES ('Interplanetary Missiles');

INSERT INTO buildings (name) VALUES ('Metal Mine');
INSERT INTO buildings (name) VALUES ('Crystal Mine');
INSERT INTO buildings (name) VALUES ('Deuterium Synthesizer');
INSERT INTO buildings (name) VALUES ('Solar Plant');
INSERT INTO buildings (name) VALUES ('Fusion Reactor');
INSERT INTO buildings (name) VALUES ('Robotics Factory');
INSERT INTO buildings (name) VALUES ('Nanite Factory');
INSERT INTO buildings (name) VALUES ('Shipyard');
INSERT INTO buildings (name) VALUES ('Metal Storage');
INSERT INTO buildings (name) VALUES ('Crystal Storage');
INSERT INTO buildings (name) VALUES ('Deuterium Tank');
INSERT INTO buildings (name) VALUES ('Research Lab');
INSERT INTO buildings (name) VALUES ('Terraformer');
INSERT INTO buildings (name) VALUES ('Alliance Depot');
INSERT INTO buildings (name) VALUES ('Missile Silo');
INSERT INTO buildings (name) VALUES ('Lunar Base');
INSERT INTO buildings (name) VALUES ('Sensor Phalanx');
INSERT INTO buildings (name) VALUES ('Jump Gate');

INSERT INTO researches (name) VALUES ('Espionage Technology');
INSERT INTO researches (name) VALUES ('Computer Technology');
INSERT INTO researches (name) VALUES ('Weapons Technology');
INSERT INTO researches (name) VALUES ('Shielding Technology');
INSERT INTO researches (name) VALUES ('Armor Technology');
INSERT INTO researches (name) VALUES ('Energy Technology');
INSERT INTO researches (name) VALUES ('Hyperspace Technology');
INSERT INTO researches (name) VALUES ('Combustion Drive');
INSERT INTO researches (name) VALUES ('Impulse Drive');
INSERT INTO researches (name) VALUES ('Hyperspace Drive');
INSERT INTO researches (name) VALUES ('Laser Technology');
INSERT INTO researches (name) VALUES ('Ion Technology');
INSERT INTO researches (name) VALUES ('Plasma Technology');
INSERT INTO researches (name) VALUES ('Intergalactic Research Network');
INSERT INTO researches (name) VALUES ('Expedition Technology');
INSERT INTO researches (name) VALUES ('Graviton Technology');

INSERT INTO resources (name) VALUES ('Metal');
INSERT INTO resources (name) VALUES ('Crystal');
INSERT INTO resources (name) VALUES ('Deuterium');
INSERT INTO resources (name) VALUES ('Energy');
INSERT INTO resources (name) VALUES ('Metal Debris');
INSERT INTO resources (name) VALUES ('Crystal Debris');


INSERT INTO alliances (name, rank, members, points) VALUES ('No Alliance', 0, 0, 0);

INSERT INTO planets (name, galaxy, system, orbit, moon) VALUES ('Homeworld', 2, 38, 11, 'f');
INSERT INTO players (name, rank, alliance_id, points) VALUES ('kusinwolf', 1690, 1, 2150);