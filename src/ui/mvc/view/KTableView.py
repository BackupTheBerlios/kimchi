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

class KTableView(QListView):
    
    def __init__(self, parent = None):
        super(KTableView, self).__init__(parent)
        
#        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        

    def selectionChanged(self, selected, deselected):
        super(KTableView, self).selectionChanged(selected, deselected)
        
        if not selected.indexes():
            return
        
        firstSelectedIndex = selected.indexes()[0]
        if firstSelectedIndex.isValid():
            selectedTable = self.model().getTableByIndex(firstSelectedIndex)
            self.emit(SIGNAL('tableSelected'), selectedTable)
        
#        print selectedTableId
#        if ok and selectedTableId > 0:
#            selectedTable = self.model().getTById(selectedEntryId)
#            self.emit(SIGNAL('entrySelected'), selectedEntry)
#        else:
#            print 'Invalid selection'
#        print 'selectionChanged %d' % selectedEntryId
    
