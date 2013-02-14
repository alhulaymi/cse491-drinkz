"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}

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
        _inventory_db[(mfg, liquor)] = add_two_amounts(amount, _inventory_db[(mfg, liquor)])
    else:
        _inventory_db[(mfg, liquor)] = amount

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
    final_amount = 0
    
    # go through the matching inventory
    for single_item in amounts:
        print single_item
        amount_string =single_item.split()[0]
        unit =single_item.split()[1]
        amount = float(amount_string)
        
        # Unit handling
        if(unit == "ml"):
            final_amount += amount
        elif(unit == "oz"):
            # 1 oz = 29.5735 ml
            final_amount += (amount*29.5735)
    
    # back to string and return
    return str(final_amount) + " ml"
    
def add_two_amounts(first,second):
    first_int = float(first.split()[0])
    f_unit = first.split()[1]
    second_int = float(second.split()[0])
    s_unit = second.split()[1]
    if(f_unit == "oz"):
        first_int = first_int * 29.5735
    if(s_unit == "oz"):
            second_int = second_int * 29.5735
    final_amount = first_int + second_int
    return str(final_amount)+" ml"


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l
