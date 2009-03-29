class Program():
    # Private Class
    class __IDS():
        def __init__(self, id, limit):
            self.__id = id
            self.__limit = limit
            self.__idName = "PLAYER_%s:%s" % (int(self.__id / self.__limit), self.__id % self.__limit)
        
        def __repr__(self):
            return "<ID: %s/%s>" % (self.__id, self.__idName)
        
        def getID(self):
            return self.__id
        
        def getIDName(self):
            return self.__idName
    
    # Private Globals
    __info = "release_date(year.month.day)\nversion(year.month)\nmodified(year.month.day)\nUbuntu Style version control"
    __modified = '9.1.14'
    __release_date = '0.0.0'
    __version = '9.1'
    __max = 10000
    __ids = 10000
    
    def __repr__(self):
        return self._program()
    
    def _getID(self):
        self.__ids += 1
        return self.__IDS(self.__ids, self.__max)

    def _program(self):
        return "<Version: %7s - Modified: %7s - Released: %7s>" % (self.__version, self.__modified, self.__release_date)

# When imported the var will live on in the scope of all programs, if %run, then the var is reloaded
try:
    if _master or not _master:
        if not _master:
            _master = Program()
except:
    _master = Program()