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

import ui.mvc.descriptor.kcolumn_descriptor as descriptor

class KColumnDelegate(QItemDelegate):
    
    def __init__(self, parent = None):
        super(KColumnDelegate, self).__init__(parent)
        
        
    def createEditor(self, parent, option, index):
        
        columnIndex = index.column() 
        
        editor = None
        
        if descriptor.property(columnIndex)== u'Visible':
            editor = QComboBox(parent)
            editor.addItems([u'Yes', u'No'])
            editor.setEditable(False)
        elif descriptor.property(columnIndex)== u'Type':
            editor = QComboBox(parent)
            editor.addItems(descriptor.typesByValue.keys())
            editor.setEditable(False)
        else:
            editor = QLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"), 
                         self.commitAndCloseEditor)
        
        return editor
    
    def commitAndCloseEditor(self):
        
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)
        
            
    def setEditorData(self, editor, index):
        
        text = index.model().data(index, Qt.DisplayRole).toString()
        
        columnIndex = index.column()
        propertyValue = descriptor.property(columnIndex)  
        if propertyValue == u'Visible'\
        or propertyValue== u'Type':
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        else:
            editor.setText(text)
        
        
    def setModelData(self, editor, model, index):

        columnIndex = index.column() 
        propertyValue = descriptor.property(columnIndex)
        if propertyValue == u'Visible'\
        or propertyValue== u'Type':
            model.setData(index, QVariant(editor.currentText()))
        else:
            model.setData(index, QVariant(editor.text()))
        
        