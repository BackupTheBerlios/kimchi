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
from ui.widget.DictionaryContainer import DictionaryContainer
from ui.widget.DictionarySelectorPanel import DictionarySelectorPanel
from ui.widget.GlobalSearchPanel import GlobalSearchPanel


class EditPanel(QSplitter):
    
    def __init__(self, appManager, parent = None):
        super(EditPanel, self).__init__(parent)
        
        self.config = appManager.configEngine.config
        self.appManager = appManager
        
        
                
        self.dictSelectorPanel = DictionarySelectorPanel(self.config, self)
#        self.globalSearchPanel = GlobalSearchPanel(self, appManager)
        self.dictContainerPanel = QStackedWidget(self)
        self.dictWidgets = {}
        
        
        for ktable in self.config.tables:
            dictContainer = DictionaryContainer(appManager, ktable)
            self.dictWidgets[ktable] = dictContainer
            self.dictContainerPanel.addWidget(dictContainer)
        
        """CONNECTIONS"""
        self.connect(self.dictSelectorPanel, SIGNAL('dictionarySelected'),
                     self.updateDictContainerPanel)
        
        # for saving the splitter state
        self.connect(self, SIGNAL('splitterMoved(int, int)'), self.updateEditPanelState)
        self.connect(self, SIGNAL('destroyed()'), self.mainPanelDestroyed)
        
        """ LAYOUT """
        self.setOrientation(Qt.Horizontal)
        
        self.leftSplitter = QSplitter()
        self.leftSplitter.setOrientation(Qt.Vertical)
        self.leftSplitter.addWidget(self.dictSelectorPanel)
#        self.leftSplitter.addWidget(self.globalSearchPanel)
        
        self.addWidget(self.leftSplitter)
        self.addWidget(self.dictContainerPanel)

        self.mainPanelState = None
        self.restoreEditPanelState()
        
        
    
    def updateDictContainerPanel(self, ktable):
        dictContainer = self.dictWidgets[ktable]
        self.dictContainerPanel.setCurrentWidget(dictContainer)
        
    def updateEditPanelState(self):
        self.mainPanelState = self.saveState()
        
    def saveEditPanelState(self):
        settings=QSettings()
        settings.setValue('EditPanel/State', QVariant(self.mainPanelState))
        
    def restoreEditPanelState(self):
        settings=QSettings()
        self.mainPanelState = settings.value('EditPanel/State').toByteArray() 
        self.restoreState(self.mainPanelState)
        
    def mainPanelDestroyed(self):
        self.saveEditPanelState()
        
        