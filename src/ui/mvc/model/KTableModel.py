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
from backend.domain.config.ktable import KTable


class KTableModel(QAbstractListModel):
    
    def __init__(self, config):
        super(KTableModel, self).__init__()
        
        self.tables = config.tables
        
    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or \
            not (0 <= index.row() < len(self.tables)):
            return QVariant()
        
        table = self.tables[index.row()]
        
        if role == Qt.DisplayRole:
            return QVariant(unicode(table.label))
            
#        if role == Qt.UserRole:
#            if table.id is None:
#                return QVariant(int(0))
#            else:
#                return QVariant(int(table.id))
        
        return QVariant()
    

    def rowCount(self, index = QModelIndex()):
        return len(self.tables)
    
    
    def setData(self, index, value, role = Qt.EditRole):
        
        if index.isValid() and 0 <= index.row() < len(self.tables):
            table = self.tables[index.row()]
            table.label = unicode(value.toString())
            
#            if table.id is None:
#                table = self.dataAccessService.addKTable(table)
#                self.tables[index.row()] = table
#            else:
#                self.dataAccessService.updateKTable(table)    
            
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
            self.tables.insert(position + row, KTable(''))
        
        self.endInsertRows()
        
        return True
        
    def removeRows(self, position, rows = 1, index = QModelIndex()):

        self.beginRemoveRows(QModelIndex(), position, position + rows -1)
        for row in range(rows):
#            self.dataAccessService.removeKTable(self.tables[position])
            del self.tables[position]
        self.endRemoveRows()
        
        return True
    
#    def _getTableId(self, index):
#        if not index.isValid():
#            return 0, False
#        
#        return index.data(Qt.UserRole).toInt()

    def getTableByIndex(self, index):
        return self.tables[index.row()]
        