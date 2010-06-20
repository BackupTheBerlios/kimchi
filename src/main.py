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

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui.MainWindow import MainWindow
from backend.config.Config import Config
from backend.ApplicationManager import ApplicationManager
from backend.config.ConfigEngine import ConfigEngine
from backend.domain.config.ktable import KTable
from ui.dialog.ConfigDialog import ConfigDialog
from backend.service.config_data_access_service import ConfigDataAccessService
from backend.domain.config.kcolumn import KColumn

import ui.resources

__version__ = '0.0.1'

styleSheet = '''

QSplitter::handle:vertical {
    border: 1px solid lightgray;
}
'''

def main():
    
    app = QApplication(sys.argv)
    app.setOrganizationName('Kimchi')
    app.setOrganizationDomain('kimchi.app')
    app.setApplicationName('Kimchi')
    app.setWindowIcon(QIcon(':/appIcon'))
    
    
    locale = QLocale.system().name()
#    locale = 'ro_RO'

    qtTranslator = QTranslator()
    if qtTranslator.load('qt_' + locale, ':/'):
        app.installTranslator(qtTranslator)
    appTranslator = QTranslator()
    if appTranslator.load('kimchi_' + locale, ':/'):
        app.installTranslator(appTranslator)
        
    
#    app.setStyleSheet(styleSheet)
    
    appManager = ApplicationManager()
    
    mainWindow = MainWindow(appManager)
    mainWindow.show()
    app.exec_()
    
    
main()
