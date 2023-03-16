from flask import Flask, send_from_directory, request, render_template
import os.path
import miner

app = Flask(__name__)



games = []
playerNames = []

@app.route('/')
def start():
    return render_template("start.html")

@app.route('/newName')
def newName():
    return render_template("name.html").format("/newGame")

@app.route('/loadName')
def loadName():
    return render_template("name.html").format("/loadGame")
    
@app.route('/newGame')
def newGame():
    playerName = request.args['playerName']
    saves = checkSaves()
    if playerName.lower() in saves:
        print(playerName + " joined the game.")
        return render_template("errorNewName.html").format(playerName)
    else:
        game = miner.Miner(playerName)
        games.append(game)
        playerNames.append(playerName)
        game.save(playerName)
        print(playerName + " joined the game.")
        return render_template("game.html").format(inventoryDisplay(game.getInventory()), playerName)

@app.route('/rewrite')
def rewrite():
    playerName = request.args['playerName']
    game = miner.Miner(playerName)
    games.append(game)
    playerNames.append(playerName)
    game.save(playerName)
    print(playerName + " joined the game.")
    return render_template("game.html").format(inventoryDisplay(game.getInventory()), playerName)
    
@app.route('/loadGame')
def loadGame():
    playerName = request.args['playerName']
    if playerName in playerNames:
        return render_template("errorLoadName.html").format(playerName + "'s game file is already in use. If this is mistake, the game file must have been incorrectly exited.")
    game = miner.Miner(playerName)
    games.append(game)
    playerNames.append(playerName)
    print(playerName + " joined the game.")
    try:
        qN, q = game.load(playerName)
        game.fillQs(qN, q)
        print(game.minerSettings.getAutoSave())
        return render_template("game.html").format(inventoryDisplay(game.getInventory()), playerName)
    except Exception as e:
        return render_template("errorLoadName.html").format(playerName + "'s game file does not exist.\nError Code: " + str(e))

@app.route('/save')
def save():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    game.save(playerName)
    inventory = inventoryDisplay(game.getInventory())
    return render_template("gameSave.html").format(inventory, playerName)

@app.route('/home')
def home():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    print(game.minerSettings.getAutoSave())
    autoSave(playerName, game)
    return render_template('game.html').format(inventoryDisplay(games[0].getInventory()), playerName)

@app.route('/miningMode')
def miningMode():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    inventory = inventoryDisplay(game.getInventory())
    quarry = quarryDisplay(game.getQuarry())
    tools = toolsDisplay()
    autoSave(playerName, game)
    return render_template("mining.html").format(inventory, quarry, playerName, "", tools)

@app.route('/miningMode2')
def miningMode2():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    mineNum = request.args['mineNum']
    try:
        tool = request.args['tool']
        mats = game.mine(int(mineNum), tool)
        matsDisp = foundMatsDisplay(mats)
        inventory = inventoryDisplay(game.getInventory())
        quarry = quarryDisplay(game.getQuarry())
        tools = toolsDisplay()
        autoSave(playerName, game)
        return render_template("mining.html").format(inventory, quarry, playerName, matsDisp, tools)
    except:
        inventory = inventoryDisplay(game.getInventory())
        quarry = quarryDisplay(game.getQuarry())
        tools = toolsDisplay()
        autoSave(playerName, game)
        return render_template("mining.html").format(inventory, quarry, playerName, "", tools)

@app.route('/sellingMode')
def sellingMode():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    inventory = inventoryDisplay(game.getInventory())
    sellDisp = sellItemsDisplay(game.getInventory())
    matSell, matWorth = forSaleDisplay()
    for m in miner.materials:
        if game.getInventory()[m] !=0:
            sell = '<input class="game_input_submit" type="submit" name="submitSell" formaction="/sellingMode2" value="Sell"/>'
            sellAll = '<input class="game_input_submit" type="submit" name="submitSell" formaction="/sellingMode2" value="Sell All"/>'
            autoSave(playerName, game)
            return render_template("selling.html").format(inventory, playerName, "", sellDisp, matSell, matWorth, sell, sellAll)
    autoSave(playerName, game)
    return render_template("selling.html").format(inventory, playerName, "", sellDisp, matSell, matWorth, "", "")

@app.route('/sellingMode2')
def sellingMode2():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    rawListOfQtys = []
    listOfMats = []
    for m in miner.materials:
        if game.getInventory()[m] != 0:
            rawListOfQtys.append(request.args[m + "Qty"])
            listOfMats.append(m)
    listOfQtys = list(map(int, rawListOfQtys))
    query = request.args['submitSell']
    total = game.sell(query, listOfQtys, listOfMats)
    inventory = inventoryDisplay(game.getInventory())
    sellDisp = sellItemsDisplay(game.getInventory())
    matSell, matWorth = forSaleDisplay()
    for m in miner.materials:
        if game.getInventory()[m] !=0:
            sell = '<input class="game_input_submit" type="submit" name="submitSell" formaction="/sellingMode2" value="Sell"/>'
            sellAll = '<input class="game_input_submit" type="submit" name="submitSell" formaction="/sellingMode2" value="Sell All"/>'
            autoSave(playerName, game)
            return render_template("selling.html").format(inventory, playerName, totalEarnedDisplay(total), sellDisp, matSell, matWorth, sell, sellAll)
    autoSave(playerName, game)
    return render_template("selling.html").format(inventory, playerName, totalEarnedDisplay(total), sellDisp, matSell, matWorth, "", "")

@app.route('/buyingMode')
def buyingMode():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    forSale = itemsForSaleDisplay()
    priceItems, priceCounts = itemPricesDisplay()
    inventory = inventoryDisplay(game.getInventory())
    autoSave(playerName, game)
    return render_template("buying.html").format(inventory, playerName, "", forSale, priceItems)

@app.route('/buyingMode2')
def buyingMode2():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    DictOfQtys = {}
    for fs in miner.forSale:
        DictOfQtys[fs] = int(request.args[fs + "Qty"])
    items = game.buy(DictOfQtys)
    forSale = itemsForSaleDisplay()
    priceItems, priceCounts = itemPricesDisplay()
    inventory = inventoryDisplay(game.getInventory())
    autoSave(playerName, game)
    return render_template("buying.html").format(inventory, playerName, itemsBoughtDisplay(items), forSale, priceItems)

@app.route('/refinery')
def refinery():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    inventory = inventoryDisplay(game.getInventory())
    autoSave(playerName, game)
    return render_template("refinery.html").format(inventory, playerName, "")

@app.route('/refinery2')
def refinery2():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    mat = request.args['mat']
    qty = int(request.args['qty'])
    r = game.refine(qty, mat)
    inventory = inventoryDisplay(game.getInventory())
    autoSave(playerName, game)
    return render_template("refinery.html").format(inventory, playerName, refineDisplay(r, mat))

@app.route('/crafting')
def crafting():
    playerName = request.args['playerName']
    game = games[playerNames.index(playerName)]
    inventory = inventoryDisplay(game.getInventory())
    craftItems = itemCraftDisplay(game)
    recDisp = craftingRecipeDisplay(game)
    autoSave(playerName, game)
    return render_template('crafting.html').format(inventory, playerName, craftItems, "", recDisp)

@app.route('/crafting2')
def crafting2():
    playerName = request.args['playerName']
    toCraft = request.args['craftables']
    game = games[playerName.index(playerName)]
    craftedItem = game.craft(toCraft)
    cIDisp = craftedItemDisplay(craftedItem, toCraft)
    inventory = inventoryDisplay(game.getInventory())
    craftItems = itemCraftDisplay(game)
    recDisp = craftingRecipeDisplay(game)
    autoSave(playerName, game)
    return render_template('crafting.html').format(inventory, playerName, craftItems, cIDisp, recDisp)

@app.route('/orders')
def orders():
    playerName = request.args['playerName']
    game = games[playerName.index(playerName)]
    print(game.orderTickets)
    print(game.ords.namesInUse)
    inventory = inventoryDisplay(game.getInventory())
    orderTicketsDisp = ordersDisplay(game.getOrders())
    autoSave(playerName, game)
    return render_template('orders.html').format(inventory, playerName, orderTicketsDisp,"")

@app.route('/orders2')
def orders2():
    playerName = request.args['playerName']
    orderName = request.args['orderName']
    game = games[playerName.index(playerName)]
    print(game.orderTickets)
    print(game.ords.namesInUse)
    result = completeOrder(orderName, game)
    inventory = inventoryDisplay(game.getInventory())
    orderTicketsDisp = ordersDisplay(game.getOrders())
    autoSave(playerName, game)
    return render_template('orders.html').format(inventory, playerName, orderTicketsDisp, result)

@app.route('/settings')
def settings():
    playerName = request.args['playerName']
    game = games[playerName.index(playerName)]
    print(game.minerSettings.getAutoSave())
    checkSave1 = "checked" if game.minerSettings.getAutoSave() else ""
    checkSave2 = "" if game.minerSettings.getAutoSave() else "checked"
    autoSave(playerName, game)
    return render_template("settings.html").format(playerName, checkSave1, checkSave2)

@app.route('/settings2')
def settings2():
    playerName = request.args['playerName']
    game = games[playerName.index(playerName)]
    autoSaveResult = request.args['autoSave']
    game.minerSettings.setAutoSave(True) if autoSaveResult == "On" else game.minerSettings.setAutoSave(False)
    checkSave1 = "checked" if game.minerSettings.getAutoSave() else ""
    checkSave2 = "" if game.minerSettings.getAutoSave() else "checked"
    autoSave(playerName, game)
    return render_template("settings.html").format(playerName, checkSave1, checkSave2)

@app.route('/quit')
def quit():
    playerName = request.args['playerName']
    games.remove(games[playerNames.index(playerName)])
    print(playerName + " quit the game.")
    playerNames.remove(playerName)
    return render_template("quit.html")



def checkSaves():
    saves = []
    dir = list(os.listdir("saves"))
    for d in dir:
        saveName, ext = d.split(".")
        saves.append(saveName)
    return saves

def inventoryDisplay(inv):
    stringy = ""
    for i in inv:
        if i == "Money":
            stringy += "<label class='game_label' >" + i + ": </label><label class='game_label'>$" + str(inv[i]) + "</label>\n<br>\n<br>\n"
        elif i == "Pickaxe":
            addon = "0"
            if inv[i] > 40:
                addon = "* * * * *"
            elif inv[i] > 30:
                addon = "* * * *"
            elif inv[i] > 20:
                addon = "* * *"
            elif inv[i] > 10:
                addon = "* *"
            elif inv[i] > 0:
                addon = "*"
            else:
                addon = "<i>broken</i>"
            if addon == "<i>broken</i>":
                stringy += "<img src='static/css/img/Broken Pickaxe.png' alt='' width='32' height='32' style='padding: 0px 10px 0px 0px;'><label class='game_label'>" + i + ": </label><label class='game_label'>" + addon + "</label>\n<br>\n<br>\n"
            else:
                stringy += "<img src='static/css/img/Pickaxe.png' alt='' width='32' height='32' style='padding: 0px 10px 0px 0px;'><label class='game_label'>" + i + ": </label><label class='game_label'>" + addon + "</label>\n<br>\n<br>\n"
        elif inv[i] != 0:
            stringy += "<img src='static/css/img/" + i + ".png' alt='" + i + "' width='32' height='32' style='padding: 0px 10px 0px 0px;'><label class='game_label'>" + i + ": </label><label class='game_label'>" + str(inv[i]) + "</label>\n<br>\n<br>\n"
    return stringy

def foundMatsDisplay(mats):
    stringy = ""
    for i in range(len(mats) - 1, -1, -1):
        stringy += "<label class='game_label'>You found " + mats[i] + " !</label><img src='static/css/img/" + mats[i] + ".png' alt='" + mats[i] + "' width='32' height='32' style='padding: 0px 10px 0px 10px;'>\n<br>\n"
    return stringy

def totalEarnedDisplay(total):
    return "<label class='game_label'>You earned $" + str(total) + "!</label>"

def itemsBoughtDisplay(items):
    stringy = ""
    forSale = miner.forSale
    itemCounts = []
    for fs in forSale:
        itemCounts.append(0)

    for i in items:
        itemCounts[forSale.index(i)] += 1

    for i in range(0, len(forSale)):
        if itemCounts[i] != 0:
            stringy += "<label class='game_label'>"+ str(itemCounts[i]) + " " + forSale[i] +"</label><img src='static/css/img/" + forSale[i] + ".png' alt='" + forSale[i] + "' width='32' height='32' style='padding: 0px 10px 0px 10px;'>\n<br>"
    return stringy

def quarryDisplay(quarryNums):
    stringy = ""
    n = 0
    for i in range(0, (len(quarryNums) // 10)):
        for j in range(0, 10):
            numStr = str(i) + str(j)
            num = int(numStr)
            stringy += "<button class='button_quarry' style='width: 50px;' name='mineNum' value='" + str(quarryNums[num]) + "' formaction='/miningMode2'>" + str(quarryNums[num]) + "</button>\n"
            n = num
        stringy += "</tr></br>"
    if (len(quarryNums) % 10) != 0:
        stringy += "<tr>"
        for i in range(n + 1, len(quarryNums)):
            stringy += "<button class='button_quarry' style='width: 50px;' name='mineNum' value='" + str(quarryNums[i]) + "' formaction='/miningMode2'>" + str(quarryNums[i]) + "</button>\n"
        stringy += ""
    return stringy

def toolsDisplay():
    stringy = ""
    inventory = games[0].getInventory()
    for i in inventory:
        if i in miner.nonMats and i != "Money":
            if inventory[i] != 0:
                stringy += "<img src='static/css/img/" + i + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
                if i == "Pickaxe":
                    stringy += """
                    <input type="radio" value="{0}" name="tool" checked="checked">
                    <label class='game_label'>{0}</label>
                    <br>
                    """.format(i)
                else:
                    stringy += """
                    <input type="radio" value="{0}" name="tool">
                    <label class='game_label'>{0}</label>
                    <br>
                    """.format(i)
    if stringy == "":
        return "<label class='game_label'>You have no tools.</label>"
    else:
        return stringy

def refineDisplay(s, mat):
    return "<label class='game_label'>" + s + "</label><img src='static/css/img/Refined " + mat + ".png' alt='Refined " + mat + "' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"

def forSaleDisplay():
    stringy1 = ""
    stringy2 = ""
    mats = miner.materials
    worth = miner.matWorth

    for m in mats:
        stringy1 += "<img src='static/css/img/" + m + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy1 += "<label class='game_label'>" + m + " - $" + str(miner.matWorth[mats.index(m)]) + "</label>\n<br>\n<br>\n"
    
    # for w in worth:
    #     if w < 10:
    #         stringy2 += "<label class='game_label'>$ " + str(w) + "</label>\n<br>\n<br>\n"
    #     else:
    #         stringy2 += "<label class='game_label'>$ " + str(w) + "</label>\n<br>\n<br>\n"
    return [stringy1, stringy2]

def sellItemsDisplay(inventory):
    stringy = ""
    mats = miner.materials
    worth = miner.matWorth

    for i in range(0, len(mats)):
        m = mats[i]
        if inventory[m] != 0:
            w = str(worth[i])
            stringy += "<img src='static/css/img/" + m + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
            stringy += "<label class='game_label'>" + m + "</label>\n"
            stringy += "<label class='game_label' style='text-align: right;'>Qty: </label>\n"
            stringy += "<input class='game_number_input' type='number' value='0' name='" + m + "Qty' style='width: 50px;' align='right'>\n"
            stringy += "<button class='game_button_small' formaction='/sellingMode2' name='submitSell' value='Sell All " + m + "' style='font-size: 15px;'>Sell All</button>\n<br>\n<br>\n"
    return stringy

def itemsForSaleDisplay():
    forSale = miner.forSale
    stringy = ""

    for fs in forSale:
        stringy += "<img src='static/css/img/" + fs + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy += "<label class='game_label'>" + fs + "</label>\n"
        stringy += "<label class='game_label'style='text-align: right;'>Qty: </label>\n"
        stringy += "<input class='game_number_input' type='number' value='0' name='"+ fs + "Qty' style='width: 50px;' align='right'>\n<br>\n<br>\n"

    return stringy

def itemPricesDisplay():
    stringy1 = ""
    stringy2 = ""
    forSale = miner.forSale
    prices = miner.forSaleCosts

    for fs in forSale:
        stringy1 += "<img src='static/css/img/" + fs + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy1 += "<label class='game_label'>" + fs + " - $" + str(prices[forSale.index(fs)]) + "</label>\n<br>\n<br>\n"
    
    # for p in prices:
    #     if p < 10:
    #         stringy2 += "<label class='game_label'>$ " + str(p) + "</label>\n<br>\n<br>\n"
    #     else:
    #         stringy2 += "<label class='game_label'>$ " + str(p) + "</label>\n<br>\n<br>\n"
    # return [stringy1, stringy2]
    return [stringy1, '']

def itemCraftDisplay(game):
    stringy = ""
    for c in game.craftables:
        stringy += "<input type='radio' name='craftables' value='" +  c + "'>"
        stringy += "<img src='static/css/img/" + c + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy += "<label class='game_label'>" + c + "</label>\n<br>\n"

    return stringy

def craftedItemDisplay(stringy, toCraft):
    return "<label class='game_label'>" + stringy + "</label><img src='static/css/img/" + toCraft + ".png' alt='" + toCraft + "' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"

def craftingRecipeDisplay(game):
    stringy = ""
    for c in game.ords.craftingRecipes:
        glob = c.split(" ")
        if glob[1] != "-":
            stringy += "<img src='static/css/img/" + glob[0] +  " " + glob[1] + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        else:
            stringy += "<img src='static/css/img/" + glob[0] + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy += "<label class='game_label'>" + c + "</label>\n<br>\n<br>\n"
    return stringy

def ordersDisplay(listy):
    stringy = ""
    for ticket in listy:
        stringy += "<div>\n"
        stringy += "<img src='static/css/img/" + ticket[1] + ".png' alt='' width='32' height='32' style='padding: 0px 10px 0px 10px;'>"
        stringy += "<label class='game_label'>" + ticket[0] + " " + ticket[2] + ". ($" + str(ticket[3]) + ")</label>"
        stringy += "<label>\t\t</label><button class='game_button_small' style='font-size: 15px' type='submit' formaction='/orders2' name='orderName' value='" + ticket[0] + "'>Complete</button>\n<br>\n<br>\n"
        stringy+= "</div>\n"
    return stringy

def completeOrder(orderName, game):
    return "<label class='game_label'>" + game.completeOrder(orderName) + "</label>"




def autoSave(playerName, game):
    game.save(playerName) if game.minerSettings.getAutoSave() else ""
    

# Launch the local web server
if __name__ == "__main__":
    # app.run(host='localhost', debug=True)
    app.run(host='0.0.0.0', port=3000, debug=True)