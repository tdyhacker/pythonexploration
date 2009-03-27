from movies.model import meta
from movies.model.titles import Title

meta.Session.save(Title({"name": "Watchmen", "release_date": "2009-03-06", "duration": 2, "rating": "PG-13"}))