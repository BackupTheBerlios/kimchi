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
from backend.domain.search_result_entry import SearchResultEntry

conn = None

def loadFromRow(row, ktableId):
    
    entry = SearchResultEntry()
    entry.ktableId = ktableId
    entry.id = row['id']
    for i in range(1, len(row)):
        if row[i]:
            entry.addValue(row[i])
    
    return entry


def getEntries(ktableId, entryIds):
    
    list = []
    
    rowIdsStr = '('
    for entryId in entryIds:
        rowIdsStr += str(entryId) + ', '
    rowIdsStr = rowIdsStr[:-2]
    rowIdsStr += ')'
     
    sql = 'SELECT * FROM %s WHERE id IN %s' % ('ktable_' + str(ktableId),
                                                rowIdsStr)
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor:
        entry = loadFromRow(row, ktableId)
        list.append(entry)
        
    return list
    
