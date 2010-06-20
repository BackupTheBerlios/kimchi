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

from ui.mvc.model.KTableModel import KTableModel
from ui.mvc.view.KTableView import KTableView
from ui.mvc.delegate.KTableDelegate import KTableDelegate

class KTablePanel(QWidget):
   
    def __init__(self, config, showTitle = True, showButtons = True, parent = None):
        super(KTablePanel, self).__init__(parent)
        
        self.ktableModel = KTableModel(config)
        ktableDelegate = KTableDelegate(self)
        
#        self.ktables = self.ktableModel.tables

        self.config = config
        
        label = QLabel('Tables:')
        self.ktableView = KTableView()
        self.ktableView.setModel(self.ktableModel)
        self.ktableView.setItemDelegate(ktableDelegate)
        
        self.addTableButton = QPushButton("Add")
        self.removeTableButton = QPushButton("Remove")
        
        
        """CONNECTIONS"""
        self.connect(self.ktableView, SIGNAL('tableSelected'), self.tableSelected)
        
        self.connect(self.addTableButton, SIGNAL("clicked()"), self.addTable)
        self.connect(self.removeTableButton, SIGNAL("clicked()"), self.removeTable)
        
        """LAYOUT"""
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.addTableButton)
        buttonsLayout.addWidget(self.removeTableButton)
        
        layout = QVBoxLayout()
        if showTitle:
            layout.addWidget(label)
        layout.addWidget(self.ktableView)
        if showButtons:
            layout.addLayout(buttonsLayout)
        
        self.setLayout(layout)
        

    def addTable(self):
        print "addTable"
        
        row = self.ktableModel.rowCount()
        self.ktableModel.insertRows(row)
        index = self.ktableModel.index(row, 0)
        self.ktableView.setFocus()
        self.ktableView.setCurrentIndex(index)
        self.ktableView.edit(index)
        
        
    def removeTable(self):
        print "removeTable"
        
        index = self.ktableView.currentIndex()
        if not index.isValid():
            return
        
        selectedTable = self.ktableModel.getTableByIndex(index)
        self.config.tablesToDelete.append(selectedTable)
        
        row = index.row()
        self.ktableModel.removeRows(row)
        
    def tableSelected(self, ktable):
#        print "tableSelected"
        self.emit(SIGNAL('tableSelected'), ktable)
        
