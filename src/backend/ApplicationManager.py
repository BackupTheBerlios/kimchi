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
from backend.dao.dao_engine import DaoEngine
from backend.service.data_access_service import DataAccessService
from backend.config.ConfigEngine import ConfigEngine
from backend.service.config_data_access_service import ConfigDataAccessService

import backend.service.storage_manager as storageManager

from copy import copy
from time import time
from backend.service.indexing_service import IndexingService
from backend.service.search_service import SearchService

class ApplicationManager(object):
    
    def __init__(self):
        
        self._daoEngine = None 
        
        self.dataAccessService = None
        self.configEngine = None
        self.indexingService = None
        self.searchService = None
        
        
        self.initServices()
        
    def initServices(self):
        
        """
        DAO ENGINE
        """
        dbPath = copy(storageManager.appFilePath)
        self._daoEngine = DaoEngine(dbPath)
        
        """
        CONFIG ENGINE    configEngine reads current configuration 
        """
        self.initConfigEngine()
        
        """
        DATA ACCESS SERVICE
        """
        self.initDataAccessService()
        
        """
        INDEXING SERVICE
        """
        # for the indexing service we need a different connection
        conn = self._daoEngine.getNewConnection()
        self.indexingService = IndexingService(self.configEngine.config, conn)
        
        """
        SEARCH SERVICE
        """
        # for the indexing service we need a different connection
        conn = self._daoEngine.connection
        self.searchService = SearchService(conn)
        

    def initConfigEngine(self):
        self.configDataAccessService = ConfigDataAccessService(self._daoEngine.connection)
        self.configEngine = ConfigEngine(self.configDataAccessService)
        
    def initDataAccessService(self):
        self._daoEngine.initUserStorage(self.configEngine.config)
        self.dataAccessService = DataAccessService(self._daoEngine.connection)
        
    def updateConfiguration(self, newConfig):
        t0 = time()
        self.configEngine.update(newConfig)
        t1 = time()
        print 'configEngineUpdate %f' % (t1-t0, )
        
        t0 = time()
        self.initDataAccessService()
        t1 = time()
        print 'initDataAccess %f' % (t1-t0, )
        
        
    @property
    def appStorageDir(self):
        return copy(storageManager.appFolderPath)
    
    @property
    def appFileName(self):
        return copy(storageManager.appFileName)
    
    @property
    def appFilePath(self):
        return copy(storageManager.appFilePath)
    
    def createBackup(self, backupPath):
        storageManager.createBackup(backupPath)
        
    def restoreBackup(self, backupPath):
        storageManager.restoreBackup(backupPath)
        
    def indexData(self):
        self.indexingService.indexData()
        