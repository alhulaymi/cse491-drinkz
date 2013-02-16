"""
Database functionality for drinkz information.

Dictionaries and sets are faster in search.
Sets pro: mathematical operations (i.e. intersection, union)
Dictionaries pro: look up by key.
 I chose dictionaries for easier and safer coding


"""

import drinkz.recipes.py

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

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
        print "just added into " + str(_inventory_db[(mfg, liquor)])
    else:
        _inventory_db[(mfg, liquor)] = str(add_two_amounts("0 ml",amount)) + " ml"
        print "just added into " + str(_inventory_db[(mfg, liquor)])

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for key in _inventory_db:
        if key[0] == mfg and key[1] == liquor:
            amounts.append(_inventory_db[key])
    
    # the result we will eventually return
    
    final_amount = float(_inventory_db[(mfg, liquor)].split()[0])
    print "final amount: " + str(final_amount)
    return final_amount
    
    # go through the matching inventory
    for single_item in amounts:
        print single_item
        amount_string =single_item.split()[0]
        print amount_string
        unit =single_item.split()[1]
        print unit
        amount = float(amount_string)
        
        # Unit handling
        if(unit == "ml"):
            final_amount += amount
        elif(unit == "oz"):
            # 1 oz = 29.5735 ml
            final_amount += (amount*29.5735)
    
    # back to string and return
    return final_amount
    
def add_two_amounts(first,second):
    first_float = float(first.split()[0])
    f_unit = first.split()[1]
    second_float = float(second.split()[0])
    s_unit = second.split()[1]
    
    if(f_unit == "oz"):
        first_float = first_float * 29.5735
    elif(f_unit == "gallon"):
        first_float = first_float * 3785.41
        
    if(s_unit == "oz"):
            second_float = second_float * 29.5735
    elif(s_unit == "gallon"):
            second_float = second_float * 3785.41
            
    final_amount = first_float + second_float
    print "first: " + first + " second: " + second + " = " + str(final_amount)
    return final_amount


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l


# Input r: recipe object
# Output: False if a recipe with the same name exists
#         True otherwise
def add_recipe(r):
    if(r.name in list(_recipes_db.keys()):
        return false
    else:
        _recipes_db[r.name] = r.ingredients
    return True
    
#Input: string
#Output: list of tuples  
def get_recipe(name):
    if(name in list(_recipes_db.keys()):
        return []
    else:
        return _recipes_db[name]
    

def get_all_recipes():
    all = {}
    for key in _recipes_db:
        all[key] = _recipes_db
        
    return all
