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
import backend.dao.ktable_dao as ktableDao
import backend.dao.kcolumn_dao as kcolumnDao

class ConfigDataAccessService(object):
    
    def __init__(self, connection):
        self.initDaos(connection)
        self.conn = connection

    def initDaos(self, connection):
        ktableDao.conn = connection
        kcolumnDao.conn = connection
        
    
    def getAllKTables(self):
        
        ktables = ktableDao.getList() 
        for ktable in ktables:
            kcolumns = kcolumnDao.getListByKTable(ktable)
            ktable.columns = kcolumns
        
        return ktables 
    
    
    def getKTableById(self, id):
        return ktableDao.get(id)
    
        
    def addKTable(self, ktable):
        ktableDao.add(ktable)
        # this ktable columns have to be added too
        for index, col in enumerate(ktable.columns):
            col.ktableId = ktable.id
            col.seqNumber = index
            kcolumnDao.add(col)
        
        self.conn.commit()
    
    
    def updateKTable(self, ktable):
        ktableDao.update(ktable)
        # add ktable new columns and
        # update existing ones
        for index, col in enumerate(ktable.columns):
            col.seqNumber = index
            if col.id is None:
                col.ktableId = ktable.id
                kcolumnDao.add(col)
            else:
                kcolumnDao.update(col)
        
        self.conn.commit()
        
    def removeKTable(self, ktable):
        # remove table columns first
        kcolumnDao.removeByKTable(ktable)
        ktableDao.remove(ktable)
        
        self.conn.commit()
        
    def removeKTables(self, ktables):
        ktableDao.removeMultiple(ktables)
        
        self.conn.commit()
    
    """
    KColumn related
    """
    def getKColumnsByKTable(self, ktable):
        return kcolumnDao.getListByKTable(ktable)
        
#    def getKColumnById(self, id):
#        return kcolumnDao.get(id)
#    
    def removeKColumns(self, kcolumns):
        kcolumnDao.removeMultiple(kcolumns)
        
        self.conn.commit()
        
#    def addKColumn(self, kcolumn):
#        kcolumnDao.save(kcolumn)
        