"""Setup the yinyang application"""
import logging

from paste.deploy import appconfig
from pylons import config

from yinyang.config.environment import load_environment
from yinyang import model

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup yinyang here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    log.info("Creating database tables")
    model.meta.create_all(bind=model.engine)
    log.info("Finished setting up")
