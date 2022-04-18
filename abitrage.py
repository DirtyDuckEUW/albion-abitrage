import json
import requests
import time

f = open('items.json', "r+", encoding='utf-8')
data = json.load(f)
f.close()

bestItemProfit = 0
bestItemName = ""

for item in data:
    name = item["UniqueName"]

    if not name.startswith("T4"):
        continue

    url = "https://www.albion-online-data.com/api/v2/stats/prices/{0}?locations=Caerleon,Lymhurst".format(
        name)
    req = requests.get(url)

    while(req.status_code == 429):
        print("Waiting for api to recharge...")
        time.sleep(30)
        req = requests.get(url)

    if req.status_code == 200:
        jsonData = req.json()

        bestQualityProfit = 0
        bestQualityId = 0
        for id in range(0, int(len(jsonData) / 2)):
            caerleaonItem = jsonData[id]
            lymhurstItem = jsonData[id + int(len(jsonData) / 2)]

            if lymhurstItem["buy_price_max"] > 0 and caerleaonItem["sell_price_min"] > 0:
                profit = lymhurstItem["buy_price_max"] - \
                    caerleaonItem["sell_price_min"]
                print("{0}, Q: {1}, P: {2}".format(name, id + 1, profit))
                if profit > bestQualityProfit:
                    bestQualityId = id
                    bestQualityProfit = profit

        if bestQualityProfit > bestItemProfit:
            bestItemName = name + " " + str(bestQualityId)
            bestItemProfit = bestQualityProfit
            # lym buy
            # car sell
print("----------------------------")
print(bestItemName)
print(str(bestItemProfit))
