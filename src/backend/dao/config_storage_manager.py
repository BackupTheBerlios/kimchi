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
KTABLE_TABLE_NAME = 'ktable'
KCOLUMN_TABLE_NAME = 'kcolumn'
KINDEX_TABLE_NAME = 'kindex'

SQL_FOR_CREATE_KTABLE = '''CREATE TABLE IF NOT EXISTS ktable ( 
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    label VARCHAR NOT NULL
)'''

SQL_FOR_CREATE_KCOLUMN = '''CREATE TABLE IF NOT EXISTS kcolumn (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ktable_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    type INTEGER NOT NULL DEFAULT (0),
    visible INTEGER NOT NULL DEFAULT (1),
    seq_number INTEGER NOT NULL DEFAULT (0)
)'''

SQL_FOR_CREATE_KINDEX = '''CREATE TABLE IF NOT EXISTS kindex ( 
    id INTEGER NOT NULL PRIMARY KEY, 
    ktable_id INTEGER NOT NULL,
    row_id INTEGER NOT NULL,
    contents TEXT NOT NULL
)'''

def createConfigTables(conn):
    createDBTable(conn, KTABLE_TABLE_NAME, SQL_FOR_CREATE_KTABLE)
    createDBTable(conn, KCOLUMN_TABLE_NAME, SQL_FOR_CREATE_KCOLUMN)
    createDBTable(conn, KINDEX_TABLE_NAME, SQL_FOR_CREATE_KINDEX)
    
def createDBTable(conn, tableName, sqlForCreate):
    
    try:    
        
#        """check to see if the table already exists"""
#        rs = conn.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = '%s'" % (tableName, ))
#        r = rs.fetchone()
#        
#        if r is None:
#            """table doesn't exists yet, we are creating it now"""
        conn.execute(sqlForCreate)
        
        
    except Exception, e:
        print e

