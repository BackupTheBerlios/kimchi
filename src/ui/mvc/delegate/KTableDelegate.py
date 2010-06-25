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

from properties import NEW_TABLE

class KTableDelegate(QItemDelegate):
    
    def __init__(self, parent = None):
        super(KTableDelegate, self).__init__(parent)
        
        
#    def createEditor(self, parent, option, index):
#        
#        editor = QLineEdit(parent)
#        self.connect(editor, SIGNAL("returnPressed()"), 
#                         self.commitAndCloseEditor)
#        
#        return editor
    
    
    def commitAndCloseEditor(self):
        
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)
        
            
    def setEditorData(self, editor, index):
        
        text = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(text)
        
        
    def setModelData(self, editor, model, index):
        text = unicode(editor.text())
        if not text:
            text = NEW_TABLE
        model.setData(index, QVariant(text))
        