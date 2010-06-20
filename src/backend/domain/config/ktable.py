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

class KTable(object):
    
    def __init__(self, label = u''):
        self.id = None
        self.label = label
        
        self._columns = []
        
    @property
    def columns(self):
        return self._columns
    
    @columns.setter
    def columns(self, newColumns):
        self._columns = newColumns
#        self.populateColumnNames()
    
    def addColumn(self, column):
        self._columns.append(column)

            
    @property
    def columnsNames(self):
        colNames = []
        for col in self._columns:
            colNames.append(col.name)
    
        return colNames
    
    @property
    def columnsLabels(self):
        colLabels = []
        for col in self._columns:
            colLabels.append(col.label)
            
        return colLabels
            
    @property
    def name(self):
        return u'ktable_' + str(self.id)
    
    def __unicode__(self):
        return '(%s)' % (self.label, )
    
    def __str__(self):
        return self.__unicode__()
    
    
    
