# coding: utf-8
'''
Copyright (c) 2010, Alexandru Dancu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
3.  Neither the name of the project nor the names of its contributors may be 
    used to endorse or promote products derived from this software without 
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

import sqlite3

import user_storage_manager as userStorageManager
import config_storage_manager as configStorageManager

class DaoEngine(object):
    
    def __init__(self, dbPath):
        
        self.dbPath = dbPath
        
        """This is the default connection
        If we want to access the db from a different thread(for instance for indexing)
        we have to use another connection
        """
        self.connection = self.getNewConnection()
        
        self.initConfigStorage()
    
        
    def initConfigStorage(self):
        """Config Storage consists of the following tables:
            ktable - holds the definitions for user defined tables 
            kcolumn - holds the column definitions for user defined tables
        """
#        self.connection = self.createConnection()
        configStorageManager.createConfigTables(self.connection)
    
    def initUserStorage(self, config):
        userStorageManager.createTablesForEntries(self.connection, config)
        
    
    def createConnection(self):
        sqlite3.enable_callback_tracebacks(True)
        connection = sqlite3.connect(self.dbPath)
        connection.row_factory=sqlite3.Row
        
        return connection
    
    def getNewConnection(self):
        return self.createConnection()
    
    