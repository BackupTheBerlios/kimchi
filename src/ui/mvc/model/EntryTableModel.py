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
# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from backend.domain.entry import Entry

class EntryTableModel(QAbstractTableModel):
    
    def __init__(self, appManager, ktable):
        super(EntryTableModel, self).__init__()
        
        self.appManager = appManager
        self.dataAccessService = appManager.dataAccessService
        
        self.entryColumnsNames = ktable.columnsNames
        self.entryColumnsLabels = ktable.columnsLabels

        self.ktable = ktable
        
        self.entries = self.dataAccessService.getAllEntries(self.ktable)
        
        
    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or \
            not (0 <= index.row() < len(self.entries)):
            return QVariant()
        
        entry = self.entries[index.row()]
        column = index.column()
        
        if role == Qt.DisplayRole:
            text = getattr(entry, self.entryColumnsNames[column])
            return QVariant(text)
            
        if role == Qt.UserRole:
            if entry.id is not None:
                return QVariant(int(entry.id))
            else:
                return QVariant(int(0))
        
        return QVariant()
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QVariant(self.entryColumnsLabels[section])

        return QVariant()  

    
    def rowCount(self, index = QModelIndex()):
        return len(self.entries)

    
    def columnCount(self, index = QModelIndex()):
        return len(self.entryColumnsNames)

    
    def setData(self, index, value, role = Qt.EditRole):
        
        if index.isValid() and 0 <= index.row() < len(self.entries):

            entry = self.entries[index.row()]
            
            column = index.column()
            setattr(entry, self.entryColumnsNames[column],
                     unicode(value.toString()))
            
            self.dataAccessService.updateEntry(entry, self.ktable)
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            
            return True
        
        return False

    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                            Qt.ItemIsEditable)
        
    def insertRows(self, position, rows = 1, index = QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows -1)
        
        for row in range(rows):
            entry = self.createEntry()
            self.dataAccessService.addEntry(entry, self.ktable)
            self.entries.insert(position + row, entry)
        
        self.endInsertRows()
        
        return True
        
    def removeRows(self, position, rows = 1, index = QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows -1)
        
        for row in range(rows):
            self.dataAccessService.removeEntry(self.entries[position], self.ktable)
            del self.entries[position]
        
        self.endRemoveRows()
        
        return True
    
    def getEntryId(self, index):
        if not index.isValid():
            return 0, False
        
        return index.data(Qt.UserRole).toInt()
    
    def createEntry(self):
        entry = Entry()
        for column in self.entryColumnsNames:
            setattr(entry, column, u'')
            
        return entry
    
    def getEntryById(self, id):
        return self.dataAccessService.getEntryById(self.ktable, id)
     
        