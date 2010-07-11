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

from ui.widget.MainPanel import MainPanel
from ui.dialog.ConfigDialog import ConfigDialog

from properties import APP_NAME, APP_ABOUT

import resources
import os
from datetime import datetime
from backend.service.storage_manager import appFilePath
from ui.dialog.FileDialogWithValidation import FileDialogWithValidation

class MainWindow(QMainWindow):
    
    def __init__(self, appManager, parent = None):
        super(MainWindow, self).__init__(parent)
        
        self.appManager = appManager
        
        self.resize(QSize(800,600))
        
        
        self.createMenu()
        self.createToolBar()
        
        self.mainPanel = None
        self.initMainPanel()
        
        self.setWindowTitle(APP_NAME)
        
        
        
        self.restoreMainWindowState()
        
    def initMainPanel(self):
        self.mainPanel = MainPanel(self.appManager)
        self.setCentralWidget(self.mainPanel)
        
        
    def saveMainWindowState(self):
        settings=QSettings()
        settings.setValue('MainWindow/Geometry', QVariant(self.saveGeometry()))
        settings.setValue('MainWindow/State', QVariant(self.saveState()))
        settings.setValue('Application/FontSize', QVariant(self.fontSize))
        
    def restoreMainWindowState(self):
        settings=QSettings()
        self.restoreGeometry(settings.value('MainWindow/Geometry').toByteArray())
        self.restoreState(settings.value('MainWindow/State').toByteArray())
        
        self.fontSize, ok = settings.value('Application/FontSize').toInt()
        if not ok:
            self.fontSize = qApp.font().pointSize()
        self.changeFontSize()
        
    def closeEvent(self,event):
        self.saveMainWindowState()
        
    
    def createAction(self, text, slot, shortcut = None, icon = None,
                     tip = None):
        
        action = QAction(text, self)
        self.connect(action, SIGNAL('triggered()'), slot)
        
        if icon is not None:
            action.setIcon(QIcon(":/%s" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        
        return action

    
    def createMenu(self):
        
        fileMenu = self.menuBar().addMenu(self.tr('&File'))
        
        fileQuitAction = self.createAction(self.tr('Ex&it'), self.close,
                "Alt+X", "filequit", self.tr('Close the application'))
        fileCreateBackupAction = self.createAction(self.trUtf8('Create backup'), self.createBackup)
        fileRestoreBackupAction = self.createAction(self.trUtf8('Restore backup'), self.restoreBackup)
        
        fileMenu.addAction(fileQuitAction)
        fileMenu.addAction(fileCreateBackupAction)
        fileMenu.addAction(fileRestoreBackupAction)
        
        
        optionsMenu = self.menuBar().addMenu("&Dictionaries")
        settingsAction = self.createAction("&Manage", 
                self.showConfigDialog, "Ctrl+M", 'dictionaryIcon')        
        optionsMenu.addAction(settingsAction)
        
        helpMenu = self.menuBar().addMenu('&Help')
        aboutAction = self.createAction('&About %s' % APP_NAME, self.helpAbout, 
                'Alt+A', 'appIcon')
        helpMenu.addAction(aboutAction)
        
        
    def createToolBar(self):
        toolBar = self.addToolBar('toolBar')
        toolBar.setObjectName('toolBar')
        
        chooseFontAction = self.createAction(self.trUtf8('Select font'),
                                self.chooseFont)
        increaseFontSizeAction = self.createAction(self.trUtf8('+'),
                                self.increaseFontSize)
        
        decreaseFontSizeAction = self.createAction(self.trUtf8('-'),
                                self.decreaseFontSize)
        
        toolBar.addAction(chooseFontAction)
        toolBar.addAction(increaseFontSizeAction)
        toolBar.addAction(decreaseFontSizeAction)
        
        
    def showConfigDialog(self):
        configDialog = ConfigDialog(self.appManager.configEngine.config, self)
        if configDialog.exec_():
            self.appManager.updateConfiguration(configDialog.config)
            self.initMainPanel()
            
    def helpAbout(self):
        QMessageBox.about(self, 'About %s' % APP_NAME,
                          APP_ABOUT)
        
    def createBackup(self):
        
        appFileName = self.appManager.appFileName
        appFilePath = self.appManager.appFilePath
        (name, ext) = appFileName.split('.')
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
        suggestedFileName = '%s-%s.%s' % (name, timestamp, ext)
        suggestedFolder = self.appManager.appStorageDir
        suggestedFilePath = suggestedFolder + os.sep + suggestedFileName
        
        fileDialog = FileDialogWithValidation(self, [appFilePath])
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.selectFile(suggestedFilePath)
        
        if fileDialog.exec_():
            choosenPath = fileDialog.selectedFiles()[0]
            self.appManager.createBackup(unicode(choosenPath))
    
    def restoreBackup(self):
        
        appFilePath = self.appManager.appFilePath
        
        suggestedFolder = self.appManager.appStorageDir
        
        fileDialog = FileDialogWithValidation(self, [appFilePath])
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.selectFile(suggestedFolder)
        
        if fileDialog.exec_():
            choosenPath = fileDialog.selectedFiles()[0]
            self.appManager.restoreBackup(unicode(choosenPath))
            
            
    def chooseFont(self):
#        print self.font()
        font, ok = QFontDialog.getFont(self.font(), self)
        if ok:
#            self.setFont(font)
            QApplication.setFont(font,'ResizableFont')
            
    def increaseFontSize(self):
        self.fontSize += 1
        self.changeFontSize()
    
    def decreaseFontSize(self):
        self.fontSize -= 1
        self.changeFontSize()
    
    def changeFontSize(self):
        font = qApp.font()
        font.setPointSize(self.fontSize)
        qApp.setFont(font, 'ResizableFont')    
        