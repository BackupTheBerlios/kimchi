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

class BigTextEditorDialog(QDialog):
    
    def __init__(self, parent = None):
        super(BigTextEditorDialog, self).__init__(parent)
        
        self.setModal(True)
        self.textArea = QTextEdit()
        self.ok = False
        
        """
            Button box
        """
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok 
                                     | QDialogButtonBox.Cancel)
        
        """CONNECTIONS"""
        self.connect(buttonBox, SIGNAL("accepted()"),
                     self.accept)
        
        self.connect(buttonBox, SIGNAL("rejected()"),
                     self.reject)
        
        """LAYOUT"""
        
        layout = QVBoxLayout()
        layout.addWidget(self.textArea)
        layout.addWidget(buttonBox)
        
        self.setLayout(layout)
        
        self.textArea.setFocus()
        self.textArea.grabKeyboard()
        
    def setText(self, text):
        self.textArea.setPlainText(text)
        
    def text(self):
        return self.textArea.toPlainText()
    
    def accept(self):
#        print 'Accepted'
        self.ok = True
        QDialog.accept(self)
        
#        self.done(QDialog.Accepted)
        
    def reject(self):
#        print 'Rejected'
        QDialog.reject(self)
#        self.done(QDialog.Rejected)
#        self.close()

        
