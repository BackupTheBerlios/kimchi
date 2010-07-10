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
        
        self.entryTablePanel = EntryTablePanel(appManager, ktable)
        self.entrySearchPanel = EntrySearchPanel(appManager, ktable)
        self.entryDisplayPanel = EntryDisplayPanel(ktable) 
        
        
        
    
        """LAYOUT"""
        self.setOrientation(Qt.Horizontal)
        
        self.smallSplitter = QSplitter(Qt.Vertical)
        self.entrySearchPanel.setMaximumHeight(self.entrySearchPanel.minimumSizeHint().height())
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setWidget(self.entrySearchPanel)
        self.smallSplitter.addWidget(sa)
#        smallSplitter.addWidget(self.entrySearchPanel)
        
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setWidget(self.entryDisplayPanel)
        self.smallSplitter.addWidget(sa)

#        makeSplitterVisible(smallSplitter)
        
        
        self.addWidget(self.entryTablePanel)
        self.addWidget(self.smallSplitter)
        
        # select the first row in the table if exists
        self.entryTablePanel.selectEntryAtIndex(0)
        
        # variables used to save and restore 
        # this views splitters position
        self.mainSplitterState = QByteArray()
        self.smallSplitterState = QByteArray()
        
        self.mainSplitterStateId = 'DictionaryContainer%d/MainSplitterState' % (ktable.id)
        self.smallSplitterStateId = 'DictionaryContainer%d/SmallSplitterState' % (ktable.id)
        
        self.restoreWidgetState()
        
        """CONNECTIONS"""
        self.connect(self.entrySearchPanel, SIGNAL("searchTextChanged"),
                     self.entryTablePanel.filterEntryList)
        self.connect(self.entryTablePanel, SIGNAL('entrySelected'), self.entryDisplayPanel.update)
        
        # for saving the splitters state
        self.connect(self, SIGNAL('splitterMoved(int, int)'), self.updateMainSplitterState)
        self.connect(self.smallSplitter, SIGNAL('splitterMoved(int, int)'), self.updateSmallSplitterState)
        self.connect(self, SIGNAL('destroyed()'), self.onWidgetDestroy)
         
        
        
    '''Methods used to save and restore splitter positions
    '''    
    def updateMainSplitterState(self):
        self.mainSplitterState = self.saveState()
        
    def updateSmallSplitterState(self):
        self.smallSplitterState = self.smallSplitter.saveState()
        
    def saveWidgetState(self):
        settings=QSettings()
        settings.setValue(self.mainSplitterStateId, QVariant(self.mainSplitterState))
        settings.setValue(self.smallSplitterStateId, QVariant(self.smallSplitterState))
    
    def restoreWidgetState(self):
        settings=QSettings()
        
        self.mainSplitterState = settings.value(self.mainSplitterStateId).toByteArray()
        self.restoreState(self.mainSplitterState)

        self.smallSplitterState = settings.value(self.smallSplitterStateId).toByteArray()
        self.smallSplitter.restoreState(self.smallSplitterState)
        
    def onWidgetDestroy(self):
        self.saveWidgetState() 
            
