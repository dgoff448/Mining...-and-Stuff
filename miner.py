import os
import random
import orders
import settings

materials = ["Stone", "Coal", "Iron", "Gold", "Diamond", "Refined Iron", "Refined Gold"]    # Used in init
lowerMats = ["stone", "coal", "iron", "gold", "diamond", "refined iron", "refined gold"]
matWorth = [1, 5, 10, 25, 50, 30, 55]
materialsRange = [[1, 45], [46, 70], [71, 85], [86, 95], [96, 100]]
# Stone - 45%
# Coal - 25%
# Iron - 15%
# Gold - 10%
# Diamond - 5%
nonMats = ["Money", "Pickaxe", "Stick of Dynamite", "Box of Dynamite", "Wood"] # Used in init
forSale = ["New Quarry", "Pickaxe", "Stick of Dynamite", "Box of Dynamite", "Wood"]
forSaleCosts = [50, 50, 75, 125, 5]


class Miner:
    

    playerName = ""
    quarryNums = []
    quarry = []
    inventory = {}
    orderTickets = []
    ords = ""
    craftables = []

    def __init__(self, playerName):
        self.playerName = playerName
        self.newQuarry()

        a = len(nonMats)
        b = len(forSale)
        c = len(forSaleCosts)
        if not (a == b & a == c & b == c):
            raise Exception("ERROR: Array Lengths Do Not Match!")
        
        for n in nonMats:
            self.inventory[n] = 0

        self.inventory["Pickaxe"] = 50

        for m in materials:
            self.inventory[m] = 0

        self.ords = orders.Orders()
        # initial filling of orders
        for i in range(0, 3 - len(self.orderTickets)):
                self.orderTickets.append(self.ords.makeOrder())

        cra = []
        for c in self.ords.craftables:
            cra.append(c)
        self.craftables = cra

        for c in self.craftables:
            self.inventory[c] = 0

        # init settings.py
        self.minerSettings = settings.Settings()

    """
    Save Formatting:
    ------------------
    [inventoryItem0]:[inventoryItemAmt0]&[inventoryItem1]:[inventoryItemAmt1]& . . . & [inventoryItem_]:[inventoryItemAmt_]*\n
    [quarryNum0],[quarryNum1], . . . ,[quarryNum_]*\n
    [quarry0],[quarry1], . . . ,[quarry_]*\n
    [orderName0]:[orderItem0]:[orderStatement0]:[orderAmt0]& . . . &[orderName_]:[orderItem_]:[orderStatement_]:[orderAmt_]*\n
    AutoSave:[autoSaveBool]
    """
    def save(self, playerName):
        name = playerName.lower()
        try:
            with open("saves/" + name + ".txt", 'w') as f:
                # Inventory
                for i in self.inventory:
                    if (list(self.inventory.keys()))[-1] != i:
                        f.write(str(i) + ":" + str(self.inventory[i]) + "&")
                    else:
                        f.write(str(i) + ":" + str(self.inventory[i]))
                # f.write("*")
                f.write('\n')
                # Quarry Nums
                for i in range(0, len(self.quarryNums)):
                    if i != len(self.quarryNums) - 1:
                        f.write(str(self.quarryNums[i]) + ",")
                    else:
                        f.write(str(self.quarryNums[i]))
                # f.write("*")
                f.write('\n')
                # Quarry
                for i in range(0, len(self.quarry)):
                    if i != len(self.quarry) - 1:
                        f.write(str(self.quarry[i]) + ",")
                    else:
                        f.write(str(self.quarry[i]))
                # f.write("*")
                f.write('\n')
                # Orders
                for i in range(0, len(self.orderTickets)):
                    for t in range(0, len(self.orderTickets[i])):
                        if t != len(self.orderTickets[i]) - 1:
                            f.write(str(self.orderTickets[i][t]) + ":")
                        else:
                            f.write(str(self.orderTickets[i][t]))
                    if i != len(self.orderTickets) - 1:
                        f.write("&")
                # f.write("*")
                f.write('\n')
                # Settings
                f.write("AutoSave:")
                print(self.minerSettings.getAutoSave())
                f.write(str(self.minerSettings.getAutoSave()))

            return "Game Saved"
        except:
            return "Saving Error"

    def load(self, playerName):
        name = playerName.lower()
        with open("saves/" + name + ".txt", 'r') as f:
            inp = f.readlines()
            print(len(inp))
            print(inp)
            inp1 = []
            for i in inp:
                inp1.append(i.strip('\n'))
            inventoryRaw, QNRaw, QRaw, OrdersRaw, SettingsRaw = inp1[0], inp1[1], inp1[2], inp1[3], inp1[4]
            print(inp1)

            # Inventory
            inv = inventoryRaw.split("&")
            for i in inv:
                key, val = i.split(":")
                self.inventory[key] = int(val)

            # Orders
            self.orderTickets.clear()
            orderTicks = OrdersRaw.split("&")
            self.ords.namesInUse.clear()
            for o in orderTicks:
                name, item, statement, amt = o.split(":")
                self.orderTickets.append([name, item, statement, amt])
                self.ords.namesInUse.append(name)

            # Quarry Nums
            qNList = list(map(int, QNRaw.split(",")))

            # Quarry
            qList = list(map(int, QRaw.split(",")))

            # Settings
            label, boolean = SettingsRaw.split(":")        # Structure needs to change when more settings added
            if boolean == "True":
                b = True
            else:
                b = False
            self.minerSettings.setAutoSave(b)
        print(qNList)
        print(qList)
        return qNList, qList

    def fillQs(self, qN, q):
        self.quarry.clear()
        self.quarryNums.clear()
        for i in qN:
            self.quarryNums.append(i)
        for i in q:
            self.quarry.append(i)

    def newQuarry(self):
        self.quarry.clear()
        self.quarryNums.clear()
        for i in range(0, 100):
            self.quarry.append(random.randint(1, 100))
            self.quarryNums.append(i+1)

    def initQuarry(self):
        for i in range(0, 100):
            self.quarry.append(random.randint(1, 100))
            self.quarryNums.append(i+1)

    def getMatName(self, mat):
        if mat <= 50:
            matName = materials[0]
        elif mat <= 70:
            matName = materials[1]
        elif mat <= 85:
            matName = materials[2]
        elif mat <= 95:
            matName = materials[3]
        elif mat <= 100:
            matName = materials[4]
        else:
            matName = "Dirt"
        return matName

    def addToInv(self, matName):
        if matName in self.inventory:
                self.inventory[matName] += 1
        else:
            self.inventory[matName] = 1
    
    def mine(self, num, tool):
        matNames = []
        if tool == "Pickaxe" and self.inventory["Pickaxe"] > 0:
            try:
                mat = self.quarry.pop(self.quarryNums.index(num))
            except Exception as e:
                print(e)
                return ["Your pickaxe is not strong enough for this section."]
            self.quarryNums.remove(num)
            matName = "null"
            self.inventory["Pickaxe"] -= 1
            matName = self.getMatName(mat)

            self.addToInv(matName)
            matNames.append(matName)
            if self.inventory["Pickaxe"] == 0:
                return matNames
            else:
                return matNames
        elif tool == "Stick of Dynamite" and self.inventory["Stick of Dynamite"] > 0:
            foundMats = []
            low = num - 4
            high = num + 5
            if self.quarryNums.index(num) <= 5:
                low = 0
                high = 9
            elif self.quarryNums.index(num) >= len(self.quarryNums) - 6:
                # print("2") # for testing
                low = len(self.quarryNums) - 10
                high = len(self.quarryNums) - 1

            for i in range(low, high + 1):
                try:
                    mat = self.quarry.pop(low)
                    self.quarryNums.pop(low)
                    foundMats.append(self.getMatName(mat))
                    # print(i + 1, "- Success") # for testing
                except Exception as e:
                    # print(i, "- Error", e) # for testing
                    pass
                stringy = "You collected "

            self.inventory["Stick of Dynamite"] -= 1
            for f in foundMats:
                self.addToInv(f)
                matNames.append(f)

            return matNames
        elif tool == "Box of Dynamite" and self.inventory["Box of Dynamite"] > 0:
            foundMats = []
            low = num - 9
            high = num + 10
            if self.quarryNums.index(num) <= 10:
                low = 0
                high = 19
                # print("1") # for testing
            elif self.quarryNums.index(num) >= len(self.quarryNums) - 10:
                # print("2") # for testing
                low = len(self.quarryNums) - 20
                high = len(self.quarryNums) - 1

            for i in range(low, high + 1):
                try:
                    mat = self.quarry.pop(low)
                    self.quarryNums.pop(low)
                    foundMats.append(self.getMatName(mat))
                    # print(i + 1, "- Success") # for testing
                except Exception as e:
                    # print(i, "- Error", e) # for testing
                    pass
                stringy = "You collected "

            self.inventory["Box of Dynamite"] -= 1
            for f in foundMats:
                self.addToInv(f)
                matNames.append(f)

            return matNames

    def refine(self, qty, mat):
        coalRefined = ["Iron", "Gold"]

        fuelNeeded = {"Iron": 2, "Gold": 4} # val = Coal count
        if mat in coalRefined:
            if qty < 0:
                return "Invalid Qty: cannot be negative"
            if mat == "":
                return "You have not picked a material to refine."
            if mat in list(self.inventory.keys()) and qty <= self.inventory[mat] and self.inventory["Coal"] >= (qty * fuelNeeded[mat]): # look to see if mats exist and if they exist in that qty
                # true - remove mats and fuel from inventory/ add refined mats/ return descr string
                self.inventory[mat] -= qty
                self.inventory["Coal"] -= (fuelNeeded[mat] * qty)
                self.inventory["Refined " + mat] += qty
                if qty == 1:
                    return "You refined 1 " + mat + " ingot."
                else:
                    return "You refined " + str(qty) + " " + mat + " ingots."
            elif mat not in list(self.inventory.keys()):
                return "You do not have any" + str(mat)
            elif self.inventory[mat] == 0:
                return "You do not have any" + mat
            elif self.inventory["Coal"] < (qty * fuelNeeded[mat]):
                return "You do not have enough fuel."
            elif self.inventory[mat] < qty:
                return "You do not have" + str(qty) + mat + "s."
        else:
            return "Bruh"

    def sell(self, query, listOfQtys, listOfMats):
        q = query.split(" ")
        if query == "Sell All":
            total = 0
            # for i in list(self.inventory.keys()):
            for i in range(0, len(listOfMats)):
                if i not in nonMats and i not in self.craftables:
                    worth = (self.inventory[listOfMats[i]] * matWorth[materials.index(listOfMats[i])])
                    self.inventory["Money"] += worth
                    total += worth
                    self.inventory[listOfMats[i]] = 0
        elif query == "Sell":
            total = 0
            for i in range(0, len(listOfMats)):
                if listOfMats[i] in list(self.inventory.keys()) and listOfQtys[i] > 0:
                    if listOfQtys[i] <= self.inventory[listOfMats[i]]:
                        worth = (listOfQtys[i] * matWorth[materials.index(listOfMats[i])])
                        self.inventory["Money"] += worth
                        total += worth
                        self.inventory[listOfMats[i]] -= listOfQtys[i]
        elif len(q) == 3:
            worth = (self.inventory[q[2]] * matWorth[materials.index(q[2])])
            self.inventory["Money"] += worth
            total = worth
            self.inventory[q[2]] = 0
        return total

    def buy(self, Dict):
        boughtItems = []
        for d in Dict:
            i = forSale.index(d)
            if d == "New Quarry":
                if Dict[d] > 0:     # Qty > 0
                    if self.inventory["Money"] >= forSaleCosts[i]:
                        self.inventory["Money"] -= forSaleCosts[i]
                        self.newQuarry()
                        boughtItems.append("New Quarry")
            elif d == "Pickaxe":
                if Dict[d] > 0:     # Qty > 0
                    if self.inventory["Money"] >= forSaleCosts[i]:
                        self.inventory["Money"] -= forSaleCosts[i]
                        self.inventory["Pickaxe"] = 50 # reset durability
                        boughtItems.append("Pickaxe")
            elif d in forSale:
                if Dict[d] > 0:     # Qty > 0
                    for j in range(0, Dict[d]):
                        if self.inventory["Money"] >= forSaleCosts[i]:
                            self.inventory["Money"] -= forSaleCosts[i]
                            self.inventory[d] += 1
                            boughtItems.append(d)

        return boughtItems

    def craft(self, toCraft):
        return self.ords.decodeIngreds(toCraft, self.getInventory())

    def fillOrders(self):
        c = len(self.orderTickets)
        if c < 3:
            for i in range(0, 3 - len(self.orderTickets)):
                self.orderTickets.append(self.ords.makeOrder())

    def completeOrder(self, orderName):
        order = ""
        for o in self.getOrders():
            if o[0] == orderName:
                order = o
                break
        if order == "":
            raise Exception("ERROR: Order name is not found in player's list of orders.")
        # Check inventory
        if o[1] in list(self.inventory.keys()):
            if self.inventory[o[1]] > 0:
                self.inventory[o[1]] -= 1
                self.inventory["Money"] += int(o[3])
                self.ords.completeOrder(orderName)
                self.orderTickets.remove(o)
                self.fillOrders()
                return "You earned $" + str(o[3]) + "!"
            else:
                return "You do not have the item needed for this order."
        else:
            return "You do not have the item needed for this order."
                

# Getters/ Setters *****************************************************************************************

    def getInventory(self):
        return self.inventory

    def setInventory(self, key, val):
        self.inventory[key] = self.inventory[key] + val

    def getQuarry(self):
        return self.quarryNums

    def getOrders(self):
        return self.orderTickets
