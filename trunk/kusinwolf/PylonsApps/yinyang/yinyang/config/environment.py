"""Pylons environment configuration"""
import os

from pylons import config

import yinyang.lib.app_globals as app_globals
import yinyang.lib.helpers
from yinyang.config.routing import make_map

import sqlalchemy as sa
from yinyang import model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='yinyang',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = yinyang.lib.helpers

    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    engine = sa.engine_from_config(config, "sqlalchemy.") # notice there is trailing dot
    model.init_model(engine)
