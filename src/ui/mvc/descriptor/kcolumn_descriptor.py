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
from backend.domain.config.kcolumn import SMALL_TEXT, BIG_TEXT

properties = [u'Label', u'Type', u'Visible']

typesByCode = {
               SMALL_TEXT: u'Small Text',
               BIG_TEXT: u'Big Text'}

typesByValue = {
                u'Small Text': SMALL_TEXT,
                u'Big Text': BIG_TEXT}

    
def getValue(kcolumn, index):
    if properties[index] == u'Label':
        return kcolumn.label
    elif properties[index] == u'Type':
        return typesByCode[kcolumn.type]
    elif properties[index] == u'Visible':
        return 'Yes' if kcolumn.visible else 'No'
    else:
        raise Exception, 'No such index property for kcolumn: index %d' % index
    
def setValue(kcolumn, index, value):
    if properties[index] == u'Label':
        kcolumn.label = unicode(value)
    elif properties[index] == u'Type':
        kcolumn.type = typesByValue[unicode(value)]
    elif properties[index] == u'Visible':
        kcolumn.visible = (value == 'Yes')
    else:
        raise Exception, 'No such index property for kcolumn: index %d' % index
    
def columnCount():
    return len(properties)

def header(index):
    return properties[index]

def property(index):
    return properties[index]
