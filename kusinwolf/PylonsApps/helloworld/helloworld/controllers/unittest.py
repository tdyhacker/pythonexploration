import os
from unittest import TestCase
from sqlalchemy import create_engine
from helloworld.model import meta
from helloworld.model import init_model
# If myapp.model does  not import all your models you need to do that here so create_all
# will know how to create their tables and indices.

class TestSessionUtils(TestCase):
    def setUp(Self):
        meta.engine=create_engine("sqlite:///test.sqlite")
        init_model(meta.engine)
        meta.metadata.create_all(meta.engine)

    def tearDown(self):
        meta.Session.remove()
        os.unlink("test.sqlite")
