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

from backend.config.Config import Config
from ui.widget.KTablePanel import KTablePanel
from ui.widget.KColumnPanel import KColumnPanel

import copy

class ConfigDialog(QDialog):
    """Receives application configuration
    object and returns a new configuration
        
    """
    def __init__(self, config, parent = None):
        super(ConfigDialog, self).__init__(parent)
        
        self.setWindowTitle('Manage dictionaries')
        
        self.config = copy.deepcopy(config)
        
        self.ktablePanel = KTablePanel(self.config)
        self.kcolumnPanel = KColumnPanel()

        
        """
            Button box
        """
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok 
                                     | QDialogButtonBox.Cancel)
        
        
        """CONNECTIONS"""
        
        self.connect(self.ktablePanel, SIGNAL('tableSelected'), 
                     self.kcolumnPanel.resetModel)
        
        self.connect(buttonBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        
        self.connect(buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))

        """LAYOUT"""
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.ktablePanel)
        mainLayout.addWidget(self.kcolumnPanel)
        
        layout = QVBoxLayout()
        layout.addLayout(mainLayout)
        layout.addWidget(buttonBox)
        
        self.setLayout(layout)
        
    
    def accept(self):
#        ktables = self.ktablePanel.ktables
#        
#        configDataAccessService = self.configEngine.dataAccessService
#        
#        for ktable in ktables:
#            configDataAccessService.updateKTable(ktable)
        
        
            
        QDialog.accept(self)
        
            
    def addTable(self):
#        print "addTable"
        
        row = self.ktableModel.rowCount()
        self.ktableModel.insertRows(row)
        index = self.ktableModel.index(row, 0)
        self.ktableView.setFocus()
        self.ktableView.setCurrentIndex(index)
        self.ktableView.edit(index)
        
        
    def removeTable(self):
#        print "removeTable"
        
        index = self.ktableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.ktableModel.removeRows(row)
        
