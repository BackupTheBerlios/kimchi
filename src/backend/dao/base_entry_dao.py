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
from backend.domain.entry import Entry
from backend.util import escapeSql

conn = None

def loadFromRow(row, ktable):
    
    entry = Entry()
    entry.id = row['id']
    for col in ktable.columns:
        setattr(entry, col.name, row[str(col.name)])
    
    return entry


def getAllEntries(ktable):

    list = []
    
    sql = 'SELECT * FROM %s' % (ktable.name, )
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor:
        entry = loadFromRow(row, ktable)
        list.append(entry)
        
    return list
    
    
def getEntry(ktable, id):
    
    sql = 'SELECT * FROM %s WHERE id = ?' % (ktable.name, )
    cursor = conn.cursor()
    cursor.execute(sql, (id, ))
    row = cursor.fetchone()
    entry = loadFromRow(row, ktable)
    
    return entry


def add(entry, ktable):
    
    entryColumns = ''
    entryValues = ''
    for col in ktable.columns:
        entryColumns += col.name + ', '
        value = escapeSql(getattr(entry, col.name))
        entryValues += '\'' + value + '\', '
    #remove last ', ' from both strings
    entryColumns = entryColumns[:-2]
    entryValues = entryValues[:-2]
    
    sql = 'INSERT INTO %s(%s) VALUES(%s)' % (ktable.name,
                                             entryColumns,
                                             entryValues)
    cursor = conn.cursor()
    cursor.execute(sql)
    entry.id=cursor.lastrowid
    
    """
    Insert values in the kindex table too    
    """
    for col in ktable.columns:
        value = escapeSql(getattr(entry, col.name))
        sql = 'INSERT INTO kindex(ktable_id, row_id, contents) VALUES(?, ?, ?)' 
        cursor.execute(sql, (ktable.id, entry.id, value))
    
    conn.commit()

def update(entry, ktable):
    
    params = ''
    for col in ktable.columns:
        value = escapeSql(getattr(entry, col.name))
        params += col.name + '=\'' + value + '\', '
    params = params[:-2]
    
    sql = "UPDATE %s SET %s WHERE id = ?" % (ktable.name,
                                             params)
    cursor = conn.cursor()
    cursor.execute(sql, (entry.id, ))
    
    """
    Update values in the kindex table too    
    First, remove index entries associated with this entry 
    """
    cursor.execute('DELETE FROM kindex WHERE ktable_id = ? AND row_id = ?', (ktable.id, entry.id))
    """
    Then insert new values in the kindex table     
    """
    for col in ktable.columns:
        value = escapeSql(getattr(entry, col.name))
        sql = 'INSERT INTO kindex(ktable_id, row_id, contents) VALUES(?, ?, ?)' 
        cursor.execute(sql, (ktable.id, entry.id, value))
    
    conn.commit()
    
    
def remove(entry, ktable):
    sql = 'DELETE FROM %s WHERE id = ?' % (ktable.name, )
    cursor = conn.cursor()
    cursor.execute(sql, (entry.id, ))
    cursor.execute('DELETE FROM kindex WHERE ktable_id = ? AND row_id = ?', (ktable.id, entry.id))
    
    conn.commit()
    
def getEntriesByFilter(ktable, columnName, filterText):
    
    list = []
    
    sql = 'SELECT * FROM %s WHERE %s LIKE \'%%%s%%\'' % (ktable.name,
                                                     columnName,
                                                     filterText)
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor:
        entry = loadFromRow(row, ktable)
        list.append(entry)
        
    return list
    
