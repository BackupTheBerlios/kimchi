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
import os
import sqlite3

import user_storage_manager as userStorageManager
import config_storage_manager as configStorageManager

dbFileName = 'kimchi.db'
dbFolderName = '.kimchi'

def create_storage():
    homeDir = os.path.expanduser('~')
    storageDir = homeDir + os.sep + dbFolderName 
 
    if not os.path.isdir(storageDir):
        os.mkdir(storageDir)    
    
    dbPath = storageDir + os.sep + dbFileName
    if not os.path.isfile(dbPath):
        is_first_time=True
        
    return dbPath

class DaoEngine(object):
    
    def __init__(self):
        
        self.dbPath = create_storage()
        
        self.connection = None
        
        self.initConfigStorage()
    
    
        
    def initConfigStorage(self):
        """Config Storage consists of the following tables:
            ktable - holds the definitions for user defined tables 
            kcolumn - holds the column definitions for user defined tables
        """
        sqlite3.enable_callback_tracebacks(True)
        self.connection = sqlite3.connect(self.dbPath)
        self.connection.row_factory=sqlite3.Row
        
        configStorageManager.createConfigTables(self.connection)
    
    def initUserStorage(self, config):
        
        userStorageManager.createTablesForEntries(self.connection, config)


