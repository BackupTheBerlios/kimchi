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

from backend.util import escapeSql



def indexData(conn, config):
    print 'indexing...'
    
    readCursor = conn.cursor()
    writeCursor = conn.cursor()
    
    # delete everithing from kindex table
    writeCursor.execute('DELETE FROM kindex')
    
    for ktable in config.tables:
        indexTable(ktable, readCursor, writeCursor)
        
    conn.commit()
    readCursor.close()
    writeCursor.close()
    
#    x = 10
#    y = 5
#    while True:
#        z = x * y
#        x += 1
#        y += 1
#        if x > 100 and y > 150:
#            x = 1;
#            y = 1;
#        print 'x = %d, y = %d, z = %d' % (x, y, z)

def indexTable(ktable, readCursor, writeCursor):
    
    
    rs = readCursor.execute('SELECT * FROM %s' % (ktable.name, ))
    while True:
        row = rs.fetchone()
        if row is None:
            break
        rowId = row[0]
        for i in range(1, len(row)):
            if row[i]:
                sql = 'INSERT INTO kindex(ktable_id, row_id, contents) VALUES(%d, %d, \'%s\')' % (ktable.id, rowId, escapeSql(row[i]))
                writeCursor.execute(sql)


