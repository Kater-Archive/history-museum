import json


rawData = ""
with open("Kater Analyze - query.tsv", "r") as f:
    rawData = f.read().split("\n")

all = {}
index = 0
while index < len(rawData):
    if index == 0:
        index += 1
        continue

    user = rawData[index].split("\t")
    
    uid = user[0]
    name = user[1]
    regTime = user[2]
    jsonStr = user[3]
    
    nameHistory = []
    timeHistory = [regTime]

    if(jsonStr == "null"):
        nameHistory.append(name)
    else:
        jsonData = json.loads(jsonStr)
        
        for j in jsonData:
            # nameHistory, timeHistory in json (key: value)
            for n, t in j.items():
                nameHistory.append(n)
                timeHistory.append(t)
        
        nameHistory.append(name)

    all[uid] = {
        "name": nameHistory,
        "time": timeHistory
    }
            
    index += 1

with open('user.json', 'w') as f:
    json.dump(all, f, ensure_ascii=False)