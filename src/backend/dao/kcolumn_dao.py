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
from backend.domain.config.kcolumn import KColumn
conn = None

def loadFromRow(row):
    
    kcolumn = KColumn()
    kcolumn.id = row['id']
    kcolumn.ktableId = row['ktable_id']
    kcolumn.label = row['label']
    kcolumn.type = row['type']
    kcolumn.visible = (row['visible'] == 1) 
    
    return kcolumn

def getListByKTable(ktable):
    
    kcolumns = []
    
    sql = 'SELECT * FROM kcolumn WHERE ktable_id = ?'
    cursor = conn.cursor()
    cursor.execute(sql, (ktable.id, ))
    for row in cursor:
        kcolumn = loadFromRow(row)
        kcolumns.append(kcolumn)
        
    return kcolumns
    
def add(kcolumn):
    
    sql = 'INSERT INTO kcolumn(ktable_id, label, type, visible)\
        VALUES(?, ?, ?, ?)'
    cursor = conn.cursor()
    cursor.execute(sql, (kcolumn.ktableId, 
                         kcolumn.label, 
                         kcolumn.type, 
                         1 if kcolumn.visible else 0))
    kcolumn.id=cursor.lastrowid
    conn.commit()


def get(id):
    
    sql = 'SELECT * FROM kcolumn WHERE id = ?'
    cursor = conn.cursor()
    cursor.execute(sql, (id, ))
    row = cursor.fetchone()
    
    kcolumn = loadFromRow(row)
    
    return kcolumn


def update(kcolumn):
    
    sql = 'UPDATE kcolumn SET label = ?, ' + \
        'type = ?, ' + \
        'visible = ? ' + \
        'WHERE id = ? ' 
    cursor = conn.cursor()
    cursor.execute(sql, (kcolumn.label, 
                         kcolumn.type, 
                         1 if kcolumn.visible else 0,
                         kcolumn.id))
    conn.commit()
    
def remove(kcolumn):
    sql = 'DELETE FROM kcolumn WHERE id = ?'
    cursor = conn.cursor()
    cursor.execute(sql, (kcolumn.id, ))
    conn.commit()
    
def removeMultiple(kcolumns):
    for kcolumn in kcolumns:
        remove(kcolumn)
        
def removeByKTable(ktable):
    sql = 'DELETE FROM kcolumn WHERE ktable_id = ?'
    cursor = conn.cursor()
    cursor.execute(sql, (ktable.id, ))
    conn.commit()
    