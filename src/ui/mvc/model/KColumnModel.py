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

import ui.mvc.descriptor.kcolumn_descriptor as kcolumnDescriptor
from backend.domain.config.kcolumn import KColumn

from properties import NEW_COLUMN

class KColumnModel(QAbstractTableModel):
    
    def __init__(self, columns):
        super(KColumnModel, self).__init__()
        
        self.columns = columns
        
    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or \
            not (0 <= index.row() < len(self.columns)):
            return QVariant()
        
        kcolumn = self.columns[index.row()]
        columnIndex = index.column()
        
        if role == Qt.DisplayRole:
            return QVariant(kcolumnDescriptor.getValue(kcolumn, columnIndex))       
        
        return QVariant()
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
#                if section == LABEL:
#                    return QVariant(u"Label")
                return QVariant(kcolumnDescriptor.header(section))

        return QVariant()  
    
    def rowCount(self, index = QModelIndex()):
        return len(self.columns)
    
    def columnCount(self, index = QModelIndex()):
        return kcolumnDescriptor.columnCount()
    
    def setData(self, index, value, role = Qt.EditRole):
        
        if index.isValid() and 0 <= index.row() < len(self.columns):
            
            kcolumn = self.columns[index.row()]

            columnIndex = index.column()

            kcolumnDescriptor.setValue(kcolumn, columnIndex, value.toString())
            
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
            self.columns.insert(position + row, KColumn(NEW_COLUMN))
        
        self.endInsertRows()
        
        return True
        
    def removeRows(self, position, rows = 1, index = QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows -1)
        
        for row in range(rows):
            del self.columns[position]
        
        self.endRemoveRows()
        
        return True

    def getColumnByIndex(self, index):
        return self.columns[index.row()]
    
        