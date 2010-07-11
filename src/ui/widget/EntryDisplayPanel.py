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

import ui.util as util

from backend.domain.config.kcolumn import SMALL_TEXT, BIG_TEXT
from ui.widget.ResizableFont import ResizableFont

#class LabelContainer(QWidget):
#    
#    def __init__(self, label, parent = None):
#        super(LabelContainer, self).__init__(parent)
#        
#        self.label = label
#
#        layout=QVBoxLayout()
#        layout.addWidget(label)
#        
#        self.setLayout(layout)

class EntryDisplayPanel(ResizableFont, QWidget):
    
    def __init__(self, ktable, parent = None):
        super(EntryDisplayPanel, self).__init__(parent)
        
#        self.setAlignment(Qt.AlignLeft)
#        self.setTitle("Display panel")
        
        
        
        layout=QGridLayout()
        
        self.values = []
        
        self.columnNames = ktable.columnsNames
        
        columns = ktable.columns
        
        for index, column in enumerate(columns):
            label = QLabel(column.label + ':')
#            label.setMaximumWidth(label.minimumSizeHint().width())
            layout.addWidget(label, index, 0)
            layout.setAlignment(label, Qt.AlignTop)
#            util.setGreenBackground(label)
            
            value = None
            if column.type == SMALL_TEXT:
                value = QLabel('N/A')
                value.setWordWrap(True)
            else:
                value = QTextEdit('N/A')
                value.setReadOnly(True)
#            label.setWordWrap(True)
#            labelContainer = LabelContainer(label)
#            layout.addWidget(labelContainer, index, 1)
#            util.setGreenBackground(label)
            value.setAlignment(Qt.AlignTop)
            layout.addWidget(value, index, 1)
            layout.setAlignment(value, Qt.AlignTop)
            
            
            self.values.append(value)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addStretch()
        self.setLayout(mainLayout)
        
#        util.setRedBackground(self)
        
    def update(self, entry):
        for index, name in enumerate(self.columnNames):
            text = getattr(entry, name)
            self.values[index].setText(text)
    
        