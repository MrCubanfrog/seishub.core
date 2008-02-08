# -*- coding: utf-8 -*-

import os
import sqlalchemy as sa

from seishub.defaults import DEFAULT_DB_URI


class DatabaseManager(object):
    """A wrapper around SQLAlchemy connection pool."""
    
    pool_size = 5
    max_overflow = 10
    
    def __init__(self, env):
        self.env = env
        self.uri = self.env.config.get('seishub', 'database') or DEFAULT_DB_URI
        self.engine = self._getEngine()
        self.metadata = None 
        self.env.log.info('DB connection pool started')
    
    def _getEngine(self):
        if self.uri.startswith('sqlite:///'):
            #sqlite db
            filename =  self.uri[10:]
            filepart = filename.split('/')
            #it is a plain filename without sub directories
            if len(filepart)==1:
                self.uri = 'sqlite:///' + os.path.join(self.env.path, db,
                                                       filename)
                return self._getSQLiteEngine()
            #there is a db sub directory given in front of the filename
            if len(filepart)==2 and filepart[0]=='db':
                self.uri = 'sqlite:///' + os.path.join(self.env.path, filename)
                return self._getSQLiteEngine()
            #check if it is a full absolute file path
            if os.path.isdir(os.path.dirname(filename)):
                return self._getSQLiteEngine()
            #ok return a plain memory based database
            else:
                self.uri='sqlite://'
                return self._getSQLiteEngine()
        
        return sa.create_engine(self.uri,
                                echo = True,
                                encoding = 'utf-8',
                                convert_unicode = True,
                                max_overflow = self.max_overflow, 
                                pool_size = self.pool_size)
    
    def _getSQLiteEngine(self):
        """Return a sqlite engine without a connection pool."""
        return sa.create_engine(self.uri,
                                echo = True,
                                encoding = 'utf-8',
                                convert_unicode = True,)
        
    def _checkVersion(self):
        self.version = sa.__version__
        if not self.version.startswith('0.4'):
            self.env.log.error("We need at least a SQLAlchemy 0.4.0")
