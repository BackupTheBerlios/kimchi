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
from ui.widget.EntrySearchPanel import EntrySearchPanel
from ui.widget.EntryDisplayPanel import EntryDisplayPanel
from ui.widget.EntryTablePanel import EntryTablePanel

from ui.widget.KTablePanel import KTablePanel

import ui.util as util

class DictionarySelectorPanel(QWidget):
    
    def __init__(self, config, parent = None):
        super(DictionarySelectorPanel, self).__init__(parent)
                
        self.tablePanel = KTablePanel(config, False, False, self)
        self.tablePanel.setMaximumWidth(self.tablePanel.minimumSizeHint().width())
#        util.setGreenBackground(self.tablePanel)        

        label = QLabel(u'김치')
#        util.setBackgroundColor(label, QColor.fromRgb(0, 255, 0))
                
        """CONNECTIONS"""
        self.connect(self.tablePanel, SIGNAL('tableSelected'),
                     self.dictionarySelected)

        """LAYOUT"""
        layout = QVBoxLayout()
        layout.addWidget(self.tablePanel)
        layout.addStretch()

        label.setAlignment(Qt.AlignHCenter)        
#        layout.addWidget(label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def dictionarySelected(self, ktable):
        self.emit(SIGNAL('dictionarySelected'), ktable)
        