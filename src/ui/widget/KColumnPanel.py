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

from ui.mvc.model.KColumnModel import KColumnModel
from ui.mvc.delegate.KColumnDelegate import KColumnDelegate
#from ui.mvc.view.KColumnView import KColumnView

class KColumnPanel(QWidget):
   
    def __init__(self, parent = None):
        super(KColumnPanel, self).__init__(parent)
        
        """ model will be set using resetModel() slot when
            a table is selected in the Tables view
        """
        self.kcolumnModel = None
        kcolumnDelegate = KColumnDelegate()
        
        label = QLabel('Columns:')
        self.kcolumnView = QTableView()
        self.kcolumnView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.kcolumnView.setModel(self.kcolumnModel)
        self.kcolumnView.setItemDelegate(kcolumnDelegate)
        
        self.addButton = QPushButton("Add")
        self.removeButton = QPushButton("Remove")
        
        
        """CONNECTIONS"""
        
        self.connect(self.addButton, SIGNAL("clicked()"), self.addColumn)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeColumn)
        
        """LAYOUT"""
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addWidget(self.removeButton)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.kcolumnView)
        layout.addLayout(buttonsLayout)
        
        self.setLayout(layout)
        

    def addColumn(self):
#        print "addColumn"
        if self.kcolumnModel is None:
            return
        row = self.kcolumnModel.rowCount()
        self.kcolumnModel.insertRows(row)
        index = self.kcolumnModel.index(row, 0)
        self.kcolumnView.setFocus()
        self.kcolumnView.setCurrentIndex(index)
        self.kcolumnView.edit(index)
        
        
    def removeColumn(self):
#        print "removeColumn"
        
        index = self.kcolumnView.currentIndex()
        if not index.isValid():
            return
        
        selectedColumn = self.kcolumnModel.getColumnByIndex(index)
        
        answer = QMessageBox.question(self, self.trUtf8(u'Remove table?'),
                    self.trUtf8(u'Are you sure you want to remove the \'%1\' column?').arg(selectedColumn.label),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        
        if answer == QMessageBox.Yes:
            row = index.row()
            self.kcolumnModel.removeRows(row)
        
    def resetModel(self, ktable):
#        print "resetModel"
        self.kcolumnModel = KColumnModel(ktable.columns)
        self.kcolumnView.setModel(self.kcolumnModel)
