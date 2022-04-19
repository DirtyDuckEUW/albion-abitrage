import json
import requests
import time
from AlbionItem import AlbionItem

BESTITEMS = []
DEBUG = False
COUNTER = 0

def AddItem(new_item: AlbionItem):
    new_item_added = False
    if len(BESTITEMS) >= 10:
        SortProfit()
        print("Least profit: " + str(BESTITEMS[-1].GetProfit()))
        print("New profit:   " + str(new_item.GetProfit()))
        if new_item.GetProfit() > BESTITEMS[-1].GetProfit():
            BESTITEMS.pop()
            BESTITEMS.append(new_item)
            new_item_added = True
    else:
        BESTITEMS.append(new_item)
        new_item_added = True

    if new_item_added:
        SortProfit()
        print("----------------------------")
        print("New item added!")
        print(new_item)
        print("----------------------------")

def SortProfit():
    BESTITEMS.sort(key=lambda x: x.profit, reverse=True)
    
# get item data
items = open('items.json', "r+", encoding='utf-8')
data = json.load(items)
items.close()

# get item data
items = open('itemsweigth.json', "r+", encoding='utf-8')
weightData = json.load(items)
items.close()

# every item
for item in data:
    COUNTER += 1
    weightFound = False
    current_item = AlbionItem(item["UniqueName"])

    # filter for itemgroups
    if current_item.GetName().startswith(("T1", "T2", "T3")):
        continue

    shortname = current_item.GetName()
    if "@" in shortname:
        shortname = shortname[:len(shortname) -2]

    for category in weightData:
        if weightFound:
            break
        for weightitem in weightData[category]:
            if weightFound:
                break
            if shortname == weightitem["@uniquename"]:
                try:
                    current_item.SetWeight(float(weightitem["@weight"]))
                    weightFound = True
                except:
                    current_item.SetWeight(float(1))
                    weightFound = True




    # create request
    url = "https://www.albion-online-data.com/api/v2/stats/prices/{0}?locations=Caerleon,Lymhurst".format(
        current_item.GetName())
    req = requests.get(url)

    while(req.status_code == 429):
        print("------------------------------------")
        print("Waiting for api to recharge...")
        print("Checked items: " + str(COUNTER))
        print("---------Current best items---------")
        for item in BESTITEMS:
            print(item)
        time.sleep(30)
        req = requests.get(url)

    if req.status_code == 200:
        # get request data
        jsonData = req.json()

        best_profit_peer_quality = 0

        # every quality peer item
        for quality in range(0, int(len(jsonData) / 2)):
            caerleaonItem = jsonData[quality]
            lymhurstItem = jsonData[quality + int(len(jsonData) / 2)]

            # lym buy
            # car sell
            if lymhurstItem["buy_price_max"] > 0 and caerleaonItem["sell_price_min"] > 0:
                # calculate profit
                profit =  lymhurstItem["buy_price_max"] - caerleaonItem["sell_price_min"]
                weightProfit = round(profit / current_item.GetWeight(), 2)
                current_item.SetProfit(weightProfit)

                if current_item.GetProfit() < best_profit_peer_quality:
                    continue

                best_profit_peer_quality = current_item.GetProfit()
                current_item.SetQuality(quality + 1)
                #add new best item
                AddItem(current_item)
                
print("-----FINISHED-----")
SortProfit()
print(BESTITEMS)
