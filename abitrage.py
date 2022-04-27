from asyncore import write
import json
import requests
from AlbionItem import AlbionItem

class AbitrageBot():
    URL = "https://www.albion-online-data.com/api/v2/stats/prices/{0}?locations=Caerleon,Lymhurst,Bridgewatch,Fort%20Sterling"
    ITEMDATA = "ItemData.json"
    ITEMNAMES = "ItemNames.json"
    ITEMSTORAGE = "ItemStorage.json"

    def __init__(self) -> None:
        self.bestitems = []
        self.running = False
        self.filter = ("UNIQUE")
        # get item data
        with open(self.ITEMNAMES, "r+", encoding='utf-8') as file:
            self.item_names = json.load(file)

        # get weight data
        with open(self.ITEMDATA, "r+", encoding='utf-8') as file:
            self.item_data = json.load(file)

    def main_loop(self):
        self.running = True
        self.fetch_data()

    def create_request(self, url):
        req = requests.get(url)
        # validate request
        while(req.status_code == 429):
            req = requests.get(url)

        if req.status_code == 200:
            # return request data
            return req.json()

    def get_item_data(self, current_item : AlbionItem):
        weightFound = False
        shortname = current_item.GetName()
        if "@" in shortname:
            shortname = shortname[:len(shortname) -2]

        for category in self.item_data:
            if weightFound:
                break
            for itemdata in self.item_data[category]:
                if weightFound:
                    break
                if shortname == itemdata["@uniquename"]:
                    # item found
                    current_item.SetCategory(itemdata["@shopcategory"])
                    try:
                        current_item.SetWeight(float(itemdata["@weight"]))
                        weightFound = True
                    except:
                        current_item.SetWeight(float(0.001))
                        weightFound = True
        return current_item

    def fetch_data(self):
        items = []
        # every item
        for item in self.item_names:

            if not self.running:
                break

            current_item = AlbionItem(item["UniqueName"])

            # filter for itemgroups
            if current_item.GetName().startswith(self.filter):
                continue

            current_item = self.get_item_data(current_item)

            # create request 
            jsonData = self.create_request(self.URL.format(current_item.GetName()))
            #jsonData = self.create_request(self.URL.format("T5_ARMOR_CLOTH_SET1@1"))


            current_city = "Bridgewatch"
            city = {}
            item_citys = []
            item_qualitys = []
            # every quality peer item
            for item in jsonData:
                if item["city"] != current_city:
                    if len(item_qualitys) > 0:
                        # only add city to item if it has a quality
                        city = {item["city"]: item_qualitys}
                        item_citys.append(city)
                    #cleanup for 
                    current_city = item["city"]
                    item_qualitys = []
                if item["sell_price_min"] > 0 and item["buy_price_max"] > 0:
                    # only add quality to item if it has prices
                    quality = { "quality": item["quality"], "sell": item["sell_price_min"], "buy": item["buy_price_max"]}
                    item_qualitys.append(quality)
                    
            if len(item_citys) > 1:
                # only add item to item if it has citys
                raw_item = {"name": current_item.GetName(), "category:": current_item.GetCategory(), "weight": current_item.GetWeight(), "citys": item_citys}
                items.append(raw_item)

        with open(self.ITEMSTORAGE, "w", encoding='utf-8') as file:
            json.dump(items, file)


obj = AbitrageBot()

obj.main_loop()
