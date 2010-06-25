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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui.mvc.model.EntryTableModel import EntryTableModel
from ui.mvc.delegate.EntryTableDelegate import EntryTableDelegate
from ui.mvc.view.EntryListTableView import EntryListTableView
from backend.domain.config.kcolumn import BIG_TEXT

class EntryTablePanel(QWidget):
    
    def __init__(self, appManager, ktable, parent = None):
        super(EntryTablePanel, self).__init__(parent)
        
        self.appManager = appManager
        
        self.ktable = ktable
        
        self.dataAccessService = appManager.dataAccessService
        
        self.entryTableModel = EntryTableModel(appManager, ktable)
        self.entryTableDelegate = EntryTableDelegate(ktable)
        
        self.entryTableView = EntryListTableView(self)
        self.entryTableView.setModel(self.entryTableModel)
        self.entryTableView.setItemDelegate(self.entryTableDelegate)
        
        self.addEntryButton = QPushButton("Add")
        self.removeEntryButton = QPushButton("Remove")
        
        layout=QVBoxLayout()
        layout.addWidget(self.entryTableView)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.addEntryButton)
        buttonLayout.addWidget(self.removeEntryButton)
        
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
        
        self.connect(self.addEntryButton, SIGNAL('pressed()'), self.addEntry)
        self.connect(self.removeEntryButton, SIGNAL('pressed()'), self.removeEntry)
        
        self.connect(self.entryTableView, SIGNAL('entrySelected'), self.entrySelected)
        
        #self.emit(SIGNAL("closeEditor(QWidget*)"), editor)
        self.connect(self.entryTableDelegate, SIGNAL('cellEditFinished'), self.resizeColumns)
        self.connect(self.entryTableDelegate, SIGNAL('entryHasChaged'), self.entrySelected)
        
        self.resizeColumns()
        
    def addEntry(self):
        row = self.entryTableModel.rowCount()
        self.entryTableModel.insertRows(row)
        index = self.entryTableModel.index(row, 0)
        self.entryTableView.setFocus()
        self.entryTableView.setCurrentIndex(index)
        self.entryTableView.edit(index)
        
#        self.resizeColumns()
        
    def removeEntry(self):
        index = self.entryTableView.currentIndex()
        if not index.isValid():
            return
        
        answer = QMessageBox.question(self, self.trUtf8(u'Remove table?'),
                    self.trUtf8(u'Are you sure you want to remove the selected row?'),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        if answer == QMessageBox.Yes:
            row = index.row()
            self.entryTableModel.removeRows(row)
            self.resizeColumns()
        
    def updateEntryList(self):
        pass
    
    def filterEntryList(self, columnName, text):
        self.entryTableModel.beginResetModel()
#        print "%s: %s" % (columnName, text)
        self.entryTableModel.entries = self.dataAccessService.getEntriesByFilter(self.ktable, columnName, text)
        
        self.entryTableModel.endResetModel()
        
        self.resizeColumns()
        
    def entrySelected(self, entry):
        self.emit(SIGNAL('entrySelected'), entry)
        
    def resizeColumns(self):
        # resize to content anything but BIG_TEXT columns
        for index, column in enumerate(self.ktable.columns):
            if column.type != BIG_TEXT:
                self.entryTableView.resizeColumnToContents(index)
                
    def selectEntryAtIndex(self, rowIndex):
        modelIndex = self.entryTableModel.index(rowIndex, 0)
        if modelIndex.isValid():
            self.entryTableView.setCurrentIndex(modelIndex)
        
        