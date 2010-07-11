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
from ui.widget.EntrySearchWidget import EntrySearchWidget


import ui.util as util
from ui.widget.ResizableFont import ResizableFont
 
class EntrySearchPanel(ResizableFont, QWidget):
    
    def __init__(self, appManager, ktable, parent = None):
        super(EntrySearchPanel, self).__init__(parent)
        
        layout=QGridLayout()
        
        self.entrySearchWidgetList = []
        
        self.columns = ktable.columns
        for index, column in enumerate(self.columns):
#            if column.visible:
            if True:
                entrySearchWidget = EntrySearchWidget(column.name, column.label)
#                entrySearchWidget = QLabel('ceva')
                self.entrySearchWidgetList.append(entrySearchWidget)
                label = QLabel(column.label + ":")
#                util.setRedBackground(label)
#                util.setRedBackground(entrySearchWidget)
                layout.addWidget(label, index, 0)
                layout.addWidget(entrySearchWidget, index, 1)
                self.connect(entrySearchWidget, SIGNAL("searchTextChanged"), self.searchTextChanged)

        mainLayout = QVBoxLayout()        
        mainLayout.addLayout(layout)
        mainLayout.addStretch()
        self.setLayout(mainLayout)
        
    def searchTextChanged(self, columnName, searchText):
#        print "%s: %s" % (columnName, searchText)
        self.emit(SIGNAL("searchTextChanged"), columnName, searchText)
        
        for entrySearchWidget in self.entrySearchWidgetList:
            if not entrySearchWidget.columnName == columnName:
                entrySearchWidget.clear()
        #clear the text in other search widgets 
    
        