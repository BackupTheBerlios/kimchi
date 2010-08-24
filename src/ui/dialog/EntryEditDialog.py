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

from backend.domain.config.kcolumn import SMALL_TEXT
from ui.widget.ResizableFont import ResizableFont

class EntryEditContainer(ResizableFont, QWidget):

    def __init__(self, entry, ktable, parent = None):
        super(EntryEditContainer, self).__init__(parent)
        
        self.entry = entry
        
        layout = QGridLayout()
        
        # a dictionary of dialog editors mapped by the column name of the entry
        self.editors = {}
        
        self.columnNames = ktable.columnsNames
        
        self.columns = ktable.columns
        
        for index, column in enumerate(self.columns):
            label = QLabel(column.label + ':')
#            label.setMaximumWidth(label.minimumSizeHint().width())
            layout.addWidget(label, index, 0)
            layout.setAlignment(label, Qt.AlignTop)
            
            editor = None
            value = getattr(self.entry, column.name) 
            if column.type == SMALL_TEXT:
                editor = QLineEdit(value)
            else:
                editor = QTextEdit(value)

            editor.setAlignment(Qt.AlignTop)
#            editor = QLabel(column.label)
            layout.addWidget(editor, index, 1)
            layout.setAlignment(editor, Qt.AlignTop)
            
            
            self.editors[column.name] = editor
            
        self.setLayout(layout)
            
            
class EntryEditDialog(QDialog):
    
    def __init__(self, entry, ktable, parent = None):
        super(EntryEditDialog, self).__init__(parent)
        
        self.setModal(True)
        
        self.entry = entry
        
        self.container = EntryEditContainer(entry, ktable, self)
        
        
        
        """
            Button box
        """
        buttonBox = QDialogButtonBox(QDialogButtonBox.Save
                                     | QDialogButtonBox.Reset 
                                     | QDialogButtonBox.Cancel)
        
        
        """CONNECTIONS"""
        
        self.connect(buttonBox.button(QDialogButtonBox.Save), SIGNAL("clicked()"),
                     self, SLOT("accept()"))
        
        self.connect(buttonBox.button(QDialogButtonBox.Reset), SIGNAL("clicked()"),
                     self.reset)
        
        self.connect(buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        
        layout = QVBoxLayout()
        layout.addWidget(self.container)
        layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)
    
    def accept(self):
        for column in self.container.columns:
            editor = self.container.editors[column.name]
            value = None
            if column.type == SMALL_TEXT:
                value = editor.text()
            else:
                value = editor.toPlainText()
            value = unicode(value)
            setattr(self.entry, column.name, value)
        
        QDialog.accept(self)
        
        
    def reset(self):
        for column in self.container.columns:
            editor = self.container.editors[column.name]
            value = getattr(self.entry, column.name)
            editor.setText(value)
            