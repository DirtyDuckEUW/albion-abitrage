class AlbionItem:

    def __init__(self, name):
        self.name = name
        self.quality = -1
        self.profit = -1
        self.category = ""
        self.weight = 9999

    def __repr__(self):
        return "Name: " + self.name + " Quality: " + str(self.quality) + " Profit: " + str(self.profit) + " Weight: " + str(self.weight)
        
    def SetName(self, name):
        self.name = name

    def GetName(self) -> str:
        return self.name

    def SetQuality(self, quality):
        self.quality = quality

    def GetQuality(self) -> int:
        return self.quality

    def SetCategory(self, category):
        self.category = category

    def GetCategory(self) -> str:
        return self.category

    def SetWeight(self, weight):
        self.weight = weight

    def GetWeight(self) -> float:
        return self.weight

    def SetCity(self, city):
        self.city = city

    def GetCity(self) -> str:
        return self.city