import sqlalchemy as sa
from yinyang.model import meta
import datetime

# Non-reflected tables may be defined and mapped at module level
login_attempts_table = sa.Table("login_attempts", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True, nullable=False),
    sa.Column("ip", sa.types.String(64), nullable=False),
    sa.Column("date", sa.types.String(16), nullable=False),
    )

class LoginAttempts(object):
    def __init__(self, ip):
        self.ip = ip
         #example: 2009-02-18-17-10 [year-month-day-hour-minute]
        today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        self.date = today
    
    def __cmp__(self, right):
        LDate = self.date.split("-")
        if type(right) == datetime.datetime:
            # The right is an object of the datetime.datetime class
            return cmp(datetime.datetime(LDate[0], LDate[1], LDate[2], LDate[3], LDate[4]),
                       right)
        else:
            # Both are objects of this class
            LDate = self.date.split("-")
            RDate = right.date.split("-")
            
            return cmp(datetime.datetime(LDate[0], LDate[1], LDate[2], LDate[3], LDate[4]),
                       datetime.datetime(RDate[0], RDate[1], RDate[2], RDate[3], RDate[4]))
    
    def __repr__(self):
        return "<LoginAttempts IP: %s Date: %s>" % (self.ip, self.date)

#orm.mapper(LoginAttempts, login_attempts_table) # Does this really have to be done in the __init__.py file?
