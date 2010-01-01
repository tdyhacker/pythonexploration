"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from iman.model import meta
from iman.model.question_tables import *
from iman.model.todo_tables import *
from iman.model.ban_tables import *
from iman.model.account_tables import *
from iman.model.health_tables import *
from iman.model.timeline_tables import *

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

# =======================================================================================================
# By doing all of the mapping here, this prevents the python files from importing each other and breaking
# =======================================================================================================
# Ban tables
# =======================================================================================================
mapper(IP, ips_table)

# =======================================================================================================
# Health tables
# =======================================================================================================
mapper(Unit, units_table)
mapper(Weight, weights_table, properties={'unit' : relation(Unit, backref="all_weights"),
                                          'user' : relation(User, backref="all_weights")})

# =======================================================================================================
# Question / Blogs tables
# =======================================================================================================
mapper(Question, questions_table, properties={'user' : relation(User, backref="questions")})
mapper(Response, responses_table, properties={'question' : relation(Question, secondary=r_to_q_xref_table, backref="responses"),
                                              'user' : relation(User, backref="responses")})
mapper(View, u_v_of_q_xref_table, properties={'question': relation(Question)})
mapper(Comment, comments_table, properties={'response' : relation(Response, secondary=c_to_r_xref_table, backref="comments"),
                                            'user' : relation(User, backref="comments")})

# =======================================================================================================
# Timeline tables
# =======================================================================================================
mapper(Event, events_table)

# =======================================================================================================
# Todo tables
# =======================================================================================================
mapper(Task, tasks_table, properties={'category' : relation(Category, secondary=t_to_c_xref_table, backref="tasks"),
                                      'priority' : relation(Priority, secondary=t_to_p_xref_table, backref="tasks"),
                                      'user' : relation(User, backref="tasks")})
mapper(Priority, priorities_table)
mapper(Category, categories_table)

# =======================================================================================================
# User tables
# =======================================================================================================
mapper(User, users_table, properties={'last_viewed': relation(View)})

