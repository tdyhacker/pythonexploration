from sqlalchemy import *
from sqlalchemy.types import *

class DB(object):
	#db = Database/Creating db in SQLite
	db = create_engine('sqlite:///bunsy.db')
	
	#makes it not print out
	db.echo = False
	
	def create_DB(self):
		#Binds MetaData to single Engine
		#MetaData is to describe tables
		metadata = MetaData(self.db) 
		
		#equation table
		equations = Table('equations', metadata,
			Column('equation_name', String(5)),
			Column('formula', String(40)))
		
		
		#Basic node array table
		Basic_node = Table('basic_node_array', metadata,
			Column('basic_node_array', String(40)),
			Column('values', String(40)))
		
		
		#Routing table, table
		Route = Table('Node', metadata,
			Column('id', Integer, primary_key=True),
			Column('Node', String(2)),
			Column('RTS', String(15)),
			Column('NPT', Integer),
			Column('NP$', Integer),
			Column('STS', String(15)),
			Column('RN', String(10)),
			Column('CN', String(2)),
			Column('VT', Integer),
			Column('V$', Integer),
			Column('QRT', Integer),
			Column('QRTS', String(10)))
			
		
		#Creates all tables
		metadata.create_all()
	
	def test_inserts(self):
		#incerting values into equation table
		equ = equations.insert()
		equ.execute({'equation_name':'QRT', 'formula':'((DPT * 2) + Z_PT)'},
			{'equation_name': 'RTS', 'formula': 'STS_previous_node + vector_time'},
			{'equation_name': 'STS', 'formula': 'RTS + PT'},
			{'equation_name': 'QRT2', 'formula': '(DPT * 2)'})
		
		#incerting values into basic_node table
		basic = Basic_node.insert()
		basic.execute({'basic_node_array':'basic node array','values':'{A,B,C,D,E,F,G,H,I,J,K,L,Z}'})
		
		#incerting values into Routing table, table through the program
		insert_into_route = Route.insert()
		#fills in the table with NULL for every row :D
		insert_into_route.execute({})
	
	def test_query(self):
		#Selecting the equations table
		s1 = equations.select()
		#Executing the equations table
		rs1 = s.execute()
		
		#Selecting the Basic_node table
		s2 = Basic_node.select()
		#Executing the Basic_node table
		rs2 = s.execute()
		
		#Selecting the Route table
		s3 = Route.select()
		#Executing the Route table
		rs3 = Route.execute()
		
		print rs1.fetchall() # checker to see if all data went into tables
		print rs2.fetchall() # checker to see if all data went into tables
		print rs3.fetchall() # checker to see if all data went into tables