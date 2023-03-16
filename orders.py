import random

pluralItems = ['Ammo', 'Spurs']

class Orders:

    names = []
    items = []
    pluralItems = []
    namesInUse = []
    itemsInUse = []
    craftables = {}
    codex = {}
    worthRanges = {}
    craftingRecipes = []
    

    def __init__(self):
        self.names = ['Duane Wall', 'Alan Lott', 'Eddie Park', 'Earnest Merrill', 'Jeff Patrick', 'Bernard Ellis', 'Randall Roach', 'Angel Sweet', 'Brandon McClain', 'Brandon Wheeler', 'Patricia McBride', 'Lillian Irwin', 'Marie Mathews', 'Ella Blake', 'Tracey Livingston', 'Karla Patrick', 'Sherri Brewer', 'Stacey Kramer', 'Maya Sullivan', 'Alejandra Blair', 'Homer Wilkins', 'Daniel Baxter', 'Kent Franco', 'Gary Raymond', 'Kim Holloway', 'Derek Walls', 'Paul Sparks', 'Kristopher Conley', 'Max Skinner', 'Thomas Barr', 'Harriet Landry', 'Rosie Giles', 'Marian Dorsey', 'Joanne Morse', 'Loretta Christian', 'Christine Russell', 'Cassandra William', 'Tonya Hunter', 'Paige Nichols', 'Kaitlin Gilmore', 'Manuel Pierce', 'Eddie Miles', 'Joseph Hyde', 'Billie Davis', 'Daniel Hess', 'Carl Yates', 'Sergio Gentry', 'Duane Shepard', 'Daniel Yates', 'Tristan Hines', 'Elsie Huffman', 'Anita Peterson', 'Marie Terrell', 'Myrna Aguirre', 'Rachel Byers', 'Janet Mueller', 'Shawna Copeland', 'Courtney Nielsen', 'Naomi Morin', 'Dominique Fletcher', 'Donald Rhodes', 'Elmer Ryan', 'Neil Melton', 'Claude Ford', 'Jim Chambers', 'Harold Wright', 'Phillip Potter', 'Steven Hart', 'Brandon Collier', 'Damian Stein', 'Alice Roy', 'Daisy Carney', 'Deborah Lambert', 'Jane Norman', 'Doris Hutchinson', 'Dorothy Sweet', 'Angie Haney', 'Veronica Summers', 'Taylor Maldonado', 'Nancy Collier']

        self.craftables = {
            'Iron Pickaxe': '3;ri.2;w', 
            'Shovel': '1;ri.2;w',
            'Axe': '3;ri.2;w',
            'Iron Bucket': '3;ri',
            'Ammo': '1;ri.1;sd',
            'Spurs': '2;ri',
            'Ring': '1;rg',
            'Diamond Ring' : '1;rg.1;d',
            'Gold Necklace': '2;rg',
            'Skillet': '2;i'
            }
        
        self.codex = {
            'w':'Wood',
            's':'Stone',
            'c':'Coal',
            'i':'Iron',
            'g':'Gold',
            'd':'Diamond',
            'ri':'Refined Iron',
            'rg':'Refined Gold',
            'sd':'Stick of Dynamite',
            'bd':'Box of Dynamite',
        }

        self.worthRanges = {
            'Iron Pickaxe': [110, 125], 
            'Shovel': [50, 65],
            'Axe': [110, 125],
            'Iron Bucket': [100, 115],
            'Ammo': [140, 155],
            'Spurs': [70, 85],
            'Ring': [65, 80],
            'Diamond Ring' : [115, 130],
            'Gold Necklace': [120, 135],
            'Skillet': [30, 45]
        }

        self.craftingRecipes = [
            "Pickaxe - 3 Refined Iron, 2 Wood",
            "Shovel - 1 Refined Iron, 2 Wood",
            "Axe - 3 Refined Iron, 2 Wood",
            "Iron Bucket - 3 Refined Iron",
            "Ammo - 1 Refined Iron, 1 Stick of Dynamite",
            "Spurs - 2 Refined Iron",
            "Ring - 1 Refined Gold",
            "Diamond Ring - 1 Refined Gold, 1 Diamond",
            "Gold Necklace - 2 Refined Gold",
            "Skillet - 2 Iron"
            ]
        
    # Basic order maker
    def makeOrder(self):
        while True:     # Picks a name that is not being used so name can be used as a kind of primary key
            name = self.names[random.randint(1, len(self.names)) - 1]
            if name not in self.namesInUse:
                self.namesInUse.append(name)
                break
        while True:
            items = list(self.craftables.keys())
            item = items[random.randint(1, len(items)) - 1]
            if item not in self.itemsInUse:
                self.itemsInUse.append(item)
                break
        price = random.randint(self.worthRanges[item][0], self.worthRanges[item][1])
        statement = articleGrammer("needs", item)
        return [name, item, statement, price]

    def completeOrder(self, name):
        self.namesInUse.remove(name)

    def decodeIngreds(self, toCraft, inv):
        mqs = {}
        tc = self.craftables[toCraft]
        divCount = tc.count(".")
        if divCount != 0:
            ingreds = tc.split(".")
            for i in ingreds:
                qty, mat = i.split(";")
                mqs[self.codex[mat]] = int(qty)
        else:
            qty, mat = tc.split(";")
            mqs[self.codex[mat]] = int(qty)

        valid = True
        invKeys = list(inv.keys())
        
        print(invKeys)
        for m in mqs:
            print(m)
            if m not in invKeys or inv[m] < mqs[m]:
                valid = False
        
        if valid:
            for m in mqs:
                inv[m] -= mqs[m]
            inv[toCraft] += 1
            return articleGrammer("You crafted", toCraft)
        else:
            return articleGrammer("You do not have enough materials to make", toCraft)

def articleGrammer(stringy, item):
    firstLet = item[0]
    
    if item in pluralItems:
        return stringy + " " + item
    if firstLet.lower() in  ['a', 'e', 'i', 'o', 'u']:
        return stringy + " an " + item
    else:
        return stringy + " a " + item


# GETTERS/SETTERS ***************************************************

"""
_____________________________________
|    CRAFTING INGREDIENTS CODE      |
|-----------------------------------|
| stone             =    s          |
| coal              =    c          |
| iron              =    i          |
| gold              =    g          |
| diamond           =    d          |
| refined iron      =    ri         |
| refined gold      =    rg         |
| wood              =    w          |
| stick of dynamite =    sd         |
| box of dynamite   =    bd         |
|                                   |
| Example: 4 Coal, 2 Iron = 4;c.2;i |
|___________________________________|

"""