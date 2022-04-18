class AlbionItem:

    def __init__(self, name):
        self.name = name
        self.quality = -1
        self.profit = -1

    def __repr__(self):
        return "Name: " + self.name + " Quality: " + str(self.quality) + " Profit: " + str(self.profit)
        
    def SetName(self, name):
        self.name = name

    def GetName(self) -> str:
        return self.name

    def SetQuality(self, quality):
        self.quality = quality

    def GetQuality(self) -> int:
        return self.quality

    def SetProfit(self, profit):
        self.profit = profit

    def GetProfit(self) -> int:
        return self.profit
