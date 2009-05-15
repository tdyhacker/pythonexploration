"""Setup the ogameinfo application"""
import logging

from paste.deploy import appconfig
from pylons import config

from ogameinfo.config.environment import load_environment
from ogameinfo.model import meta, setup_model

from sqlalchemymanager import SQLAlchemyManager
import authkit.users.sqlalchemy_04_driver

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup ogameinfo here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Load the models
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    log.info("Creating database tables")
    meta.metadata.create_all(checkfirst=True)
    log.info("Finished setting up")
    
    manager = SQLAlchemyManager(None, conf.local_conf, 
        [setup_model, authkit.users.sqlalchemy_04_driver.setup_model])
    manager.create_all()

    connection = manager.engine.connect()
    session = manager.session_maker(bind=connection)
    try:
        environ = {}
        environ['sqlalchemy.session'] = session
        environ['sqlalchemy.model'] = manager.model
        users = authkit.users.sqlalchemy_04_driver.UsersFromDatabase(environ)
        session.flush()
        session.commit()
    finally:
        session.close()
        connection.close()
