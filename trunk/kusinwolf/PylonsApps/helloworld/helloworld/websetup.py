"""Setup the helloworld application"""
import logging
from helloworld.model import meta
from sqlalchemy import create_engine
from sqlalchemy import MetaData

from helloworld.model import meta
from paste.deploy import appconfig
from pylons import config

from helloworld.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup helloworld here"""

    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    
    
    log.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully setup")
