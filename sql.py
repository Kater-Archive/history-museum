#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('reports.sqlite3')
print("成功連接資料庫")

c = conn.cursor()

c.execute(
    ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='allData' '''
)
if c.fetchone()[0] == 1:
    print('資料表已存在，開始記錄')
else:
    print('資料表不存在，先建表')

    conn.execute(
        '''
        CREATE TABLE reports
        (
            id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
            did             INTEGER     NOT NULL,
            participant     INTEGER     NOT NULL
        );
        '''
    )

conn.commit()
conn.close()