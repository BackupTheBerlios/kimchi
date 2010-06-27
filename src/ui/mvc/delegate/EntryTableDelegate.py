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

from backend.domain.config.kcolumn import SMALL_TEXT, BIG_TEXT
from ui.dialog.BigTextEditorDialog import BigTextEditorDialog

class EntryTableDelegate(QItemDelegate):
    
    def __init__(self, ktable, parent = None):
        super(EntryTableDelegate, self).__init__(parent)
        self.ktable = ktable
        
    def createEditor(self, parent, option, index):
        
        colIndex = index.column()
        # we need to get the column type based on columnIndex
        columnType = self.getColumnTypeByIndex(colIndex)
        
        editor = None
        if columnType == SMALL_TEXT:
            editor = QLineEdit(parent)
        else:
            editor = BigTextEditorDialog(parent)
#            editor.setFocus()
            editor.show()
#            editor.move(300,300)
        
        self.connect(self, SIGNAL("closeEditor(QWidget*)"), 
                     self.cellEditFinished)
        
        return editor
    
#    def commitAndCloseEditor(self):
#        
#        editor = self.sender()
#        if isinstance(editor, (QTextEdit, QLineEdit)):
#            self.emit(SIGNAL("commitData(QWidget*)"), editor)
#            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)
            
            
    def setEditorData(self, editor, index):
        # we need to get the column type based on columnIndex
#        columnType = self.getColumnTypeByIndex(index.column())
#        if columnType == SMALL_TEXT: 
        text = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(text)

        
    def setModelData(self, editor, model, index):
        columnType = self.getColumnTypeByIndex(index.column())
        if columnType == SMALL_TEXT: 
            model.setData(index, QVariant(editor.text()))
        else:
# I dont know wtf it doesn't work, no matter what I do, the result is 0;
# So I added a custom field, as a workaround for the fact that QDialog.result()
# is always Qt.Rejected, no matter what I do
#   
# 
#            result = editor.result()
#            if result == QDialog.Accepted:
            result = editor.ok
            if result is True:
                model.setData(index, QVariant(editor.text()))
        
        # emit this signal which notifies other views that 
        # something in this row has been edited         
        self.entryHasChanged(model.getEntryByModelIndex(index))
        
        
    def updateEditorGeometry(self, editor, option, index):
        columnType = self.getColumnTypeByIndex(index.column())
        if columnType == BIG_TEXT:
            editor.mapToParent(QPoint(0,0))
            #            editor.move(editor.parent().parent().pos())
        else:
            super(EntryTableDelegate, self).updateEditorGeometry(editor, option, index)
 
        
    def cellEditFinished(self):
        self.emit(SIGNAL("cellEditFinished"))
        
    def entryHasChanged(self, modelIndex):
        self.emit(SIGNAL('entryHasChanged'), modelIndex)
        
        
    def getColumnTypeByIndex(self, colIndex):
        return self.ktable.columns[colIndex].type
        