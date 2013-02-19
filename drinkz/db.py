"""
Database functionality for drinkz information.

Dictionaries and sets are faster in search.
Sets pro: mathematical operations (i.e. intersection, union)
Dictionaries pro: look up by key.
 I chose dictionaries for easier and safer coding


"""

import recipes

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

def get_bottle_types():
    return list(_bottle_types_db)

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    if((mfg, liquor) in _inventory_db):
        _inventory_db[(mfg, liquor)] = str(add_two_amounts(amount, _inventory_db[(mfg, liquor)])) + " ml"
    else:
        _inventory_db[(mfg, liquor)] = str(add_two_amounts("0 ml",amount)) + " ml"

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."

    
    # the result we will eventually return
    
    final_amount = float(_inventory_db[(mfg, liquor)].split()[0])
    return final_amount
    
    
def add_two_amounts(first,second):
    final_amount = convert_to_ml(first) + convert_to_ml(second)
    return final_amount


def get_liquor_inventory_with_amounts():
    for (m, l) in _inventory_db:
            yield m, l,_inventory_db[(m,l)] 

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l


# Input r: recipe object
# Output: False if a recipe with the same name exists
#         True otherwise
def add_recipe(r):
    if(r.name in list(_recipes_db.keys())):
        return False
    else:
        _recipes_db[r.name] = r.ingredients
        return True
    
#Input: string
#Output: Recipe object or false if it doesn't exist 
def get_recipe(name):
    if(name in list(_recipes_db.keys())):
        return recipes.Recipe(name,_recipes_db[name])
    else:
        return False
    

def get_all_recipes():
    all = []
    for key in _recipes_db:
        all.append(get_recipe(key))
    return all
 
#
# input string
# output float 
def convert_to_ml(amount):
    amount_f = float(amount.split()[0])
    unit = amount.split()[1]
    
    if(unit == "oz"):
    
        return amount_f*29.5735
    
    elif(unit == "gallon"):
    
        return amount_f*3785.41
    
    elif(unit == "liter"):
    
        return amount_f*1000
    
    elif(unit == "ml"):
    
        return amount_f
    