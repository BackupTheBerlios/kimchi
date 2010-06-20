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
from ui.widget.EntrySearchPanel import EntrySearchPanel
from ui.widget.EntryDisplayPanel import EntryDisplayPanel
from ui.widget.EntryTablePanel import EntryTablePanel

from ui.util import makeSplitterVisible



class DictionaryContainer(QSplitter):
    
    def __init__(self, appManager, ktable, parent = None):
        super(DictionaryContainer, self).__init__(parent)
        
#        self.setTitle(ktable.label)
        
        self.entryListPanel = EntryTablePanel(appManager, ktable)
        self.entrySearchPanel = EntrySearchPanel(appManager, ktable)
        self.entryDisplayPanel = EntryDisplayPanel(ktable) 
        
        """CONNECTIONS"""
        self.connect(self.entrySearchPanel, SIGNAL("searchTextChanged"),
                     self.entryListPanel.filterEntryList)

        self.connect(self.entryListPanel, SIGNAL('entrySelected'), self.entryDisplayPanel.update)
    
        """LAYOUT"""
        self.setOrientation(Qt.Horizontal)
        
        smallSplitter = QSplitter(Qt.Vertical)
        self.entrySearchPanel.setMaximumHeight(self.entrySearchPanel.minimumSizeHint().height())
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setWidget(self.entrySearchPanel)
        smallSplitter.addWidget(sa)
#        smallSplitter.addWidget(self.entrySearchPanel)
        
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setWidget(self.entryDisplayPanel)
        smallSplitter.addWidget(sa)

#        makeSplitterVisible(smallSplitter)
        
        
        self.addWidget(self.entryListPanel)
        self.addWidget(smallSplitter)
        
