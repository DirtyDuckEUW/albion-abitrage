import json
import requests
import time
from AlbionItem import AlbionItem
from operator import attrgetter

BESTITEMS = []
DEBUG = False

def AddItem(new_item: AlbionItem):
    new_item_added = False
    if len(BESTITEMS) >= 10:
        SortProfit()
        if new_item.GetProfit() > BESTITEMS[-1].GetProfit():
            BESTITEMS.pop()
            BESTITEMS.append(new_item)
            new_item_added = True
    else:
        BESTITEMS.append(new_item)
        new_item_added = True

        print("----------------------------")
        print("New item added!")
        print(new_item)
        print("----------------------------")
    if DEBUG and new_item_added:
        SortProfit()
        print("Items: " + str(len(BESTITEMS)))
        for item in BESTITEMS:
            print(item)


def SortProfit():
    print("---------SORTING---------")
    BESTITEMS.sort(key=lambda x: x.profit, reverse=True)
    
# get item data
f = open('items.json', "r+", encoding='utf-8')
data = json.load(f)
f.close()

# every item
for item in data:
    current_item = AlbionItem(item["UniqueName"])

    if not current_item.GetName().startswith("T4"):
        continue

    # create request
    url = "https://www.albion-online-data.com/api/v2/stats/prices/{0}?locations=Caerleon,Lymhurst".format(
        current_item.GetName())
    req = requests.get(url)

    while(req.status_code == 429):
        print("Waiting for api to recharge...")
        time.sleep(10)
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
                current_item.SetProfit(lymhurstItem["buy_price_max"] - caerleaonItem["sell_price_min"])

                if current_item.GetProfit() < best_profit_peer_quality:
                    continue

                best_profit_peer_quality = current_item.GetProfit()
                current_item.SetQuality(quality + 1)
                print(current_item)
                #add new best item
                AddItem(current_item)
                
print("-----FINISHED-----")
SortProfit()
print(BESTITEMS)
