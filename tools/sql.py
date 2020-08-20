#!/usr/bin/python3

import os
import sys
import sqlite3
import json
from pathlib import Path
from os import listdir
from os.path import isfile, join

# 根據傳入暱稱搜尋對應 UID。
# -1 表示傳入暱稱直接找不到對照值，可以理解爲 7/23 04:46 之後的暱稱
# -2 表示有多個使用者同時使用過某個名字，同時快取時間為 undefined （遺失快取時間）
def searchUid(originName, cacheTime, userData, rawUserData):
    def find(name):
        if len(userData[name]) > 1:
            if cacheTime == "undefined":
                return -2

            for uid in userData[name]:
                index = [i for i, x in enumerate(
                    rawUserData[uid]["name"]) if x == name]

                # 針對重名
                for i in index:
                    if int(rawUserData[uid]["time"][i]) <= int(cacheTime) and int(rawUserData[uid]["time"][i+1]) > int(cacheTime):
                        return uid

                # 若還是找不到，那就再根據 timestamp
                i = 0
                length = len(rawUserData[uid]["time"])
                while i < length:
                    if i == length - 1 and int(cacheTime) > int(rawUserData[uid]["time"][i]):
                        return uid
                    elif int(cacheTime) >= int(rawUserData[uid]["time"][i]) and int(cacheTime) < int(rawUserData[uid]["time"][i+1]):
                        return uid

                    i += 1

        else:
            return userData[name][0]

    try:
        return find(originName)
    except:
        try:
            name = [n for n in userData if originName in n][0]
            return find(name)
        except:
            print(originName)
            return -1


def main():
    jsonData = []

    with open("./user.json", "r") as f:
        rawUserData = json.load(f)

    with open("./sorted.json", "r") as f:
        userData = json.load(f)

    for i in range(60, 86):
        d = f"../d/{i}"
        files = [f for f in listdir(d) if isfile(join(d, f))]

        for f in files:
            with open(f"../d/{i}/{f}", "r") as temp:
                data = json.load(temp)

            did = f.split(".")[0]
            cacheTime = data["cacheTime"]
            participant = []
            floors = []
            for floor in data["content"]:
                uid = searchUid(floor["author"], cacheTime,
                                userData, rawUserData)

                name = floor["author"]
                temp = {
                    "uid": uid,
                    "name": name
                }

                floors.append(temp)

                if uid not in participant:
                    participant.append(uid)

            # SQLite
            conn.execute("INSERT INTO allData(did, participant, floors, cacheTime) VALUES(?,?,?,?)", (did, json.dumps(
                participant, ensure_ascii=False), json.dumps(floors, ensure_ascii=False), cacheTime))

            # JSON
            temp = {
                "did": did,
                "participant": participant,
                "floors": floors,
                "cacheTime": cacheTime
            }
            jsonData.append(temp)

    with open("./search.json", "w") as f:
        json.dump(jsonData, f)


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
