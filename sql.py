#!/usr/bin/python3

import os
import sys
import sqlite3
import json
from pathlib import Path
from os import listdir
from os.path import isfile, join

def searchUid(name, allData):
    pass

def main():
    allName = {}
    with open("./user.json", "r") as f:
        userData = json.load(f)

    for i in range(60, 86):
        d = f"./d/{i}"
        files = [f for f in listdir(d) if isfile(join(d, f))]
        
        for f in files:
            with open(f"./d/{i}/{f}", "r") as temp:
                data = json.load(temp)
            
            for key, value in userData.items():
                for name in value["name"]:
                    if name in allName:
                        if key not in allName[name]:
                            allName[name].append(key)
                    else:
                        allName[name] = [key]

    with open("./sorted.json", "w") as f:
        json.dump(allName, f, ensure_ascii=False)


conn = sqlite3.connect('search.sqlite3')
print("成功連接資料庫")

c = conn.cursor()

c.execute(
    ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='allData' '''
)
if c.fetchone()[0] == 1:
    print('資料表已存在，開始記錄')
    main()

else:
    print('資料表不存在，先建表')

    conn.execute(
        '''
        CREATE TABLE allData
        (
            id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
            did             INTEGER     NOT NULL,
            participant     TEXT        NOT NULL,
            floors          TEXT        NOT NULL,
            cacheTime       INTEGER     NOT NULL
        );
        '''
    )

    main()

conn.commit()
conn.close()