"""Setup the iman application"""
import logging

from iman.model import meta
from iman.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup iman here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Load the models
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    log.info("Creating database tables")
    meta.metadata.create_all(checkfirst=True)
    log.info("Finished setting up")
