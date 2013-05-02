"""
Database functionality for drinkz information.

I chose set for recipe:
    
Why not list? Aside from the fact that your hint said not to, checking for duplication will take more work.
Why not dictionary? taking Rcipe objects, converting them to keys (by names) and value (list of tuples of ingredients) will require us to
                    convert them back to a Recipe objects as return value for some of the functions. Which means we need to import the
                    Recipe class. We don't want that. We don't want to import Recipe class into this file because we need to import this
                    file into recipes.py later. I could've used the names as keys and the actual recipes as values but that will be somewhat
                    of duplications.

 
"""


from cPickle import dump, load

import sqlite3

import os

import db,recipes

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

def Connect():
     connection = sqlite3.connect("drinkz.db")
     cursor = connection.cursor()
     return (connection, cursor)

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    
    (conn, c) = Connect()
    query = "DELETE FROM mfg_liq"
    c.execute(query)
    
    query = "DELETE FROM inventory"
    c.execute(query)
    
    query = "DELETE FROM types"
    c.execute(query)
    
    query = "DELETE FROM recipes"
    c.execute(query)
    
    conn.commit()
    conn.close()
    
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()

def save_db(filename):
    fp = open(filename, 'wb')
    tosave = (_recipes_db,_bottle_types_db, _inventory_db)
    
    
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _recipes_db,_bottle_types_db, _inventory_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_recipes_db,_bottle_types_db, _inventory_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
    
class DuplicateRecipeName(Exception):
    pass

def get_bottle_types():
    
    
    
    (conn,c) = Connect()
    query = "SELECT mfg,liquor,type FROM mfg_liq JOIN types ON ml_id=id"
    c.execute(query)
    rows = c.fetchall()
    #print rows
    print "about to print types"
    for n in rows:
        
        print n
    if rows is None:
        return []
    return list(rows)
    
    return list(_bottle_types_db)

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    (conn,c) = Connect()
    query = "INSERT INTO mfg_liq (mfg,liquor) VALUES (?,?)"
    c.execute(query,(mfg,liquor))
    id = c.lastrowid
    
    query = "INSERT INTO types VALUES (?,?)"
    c.execute(query,(id,typ))
    
    conn.commit()
    
    conn.close()
    
    #_bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    (conn,c) = Connect()
    query = "SELECT * FROM mfg_liq WHERE mfg=? and liquor=?"
    c.execute(query,(mfg,liquor))
    
    if not c.fetchone() is None:
        return True
    else:
        return False
    
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    id = getMfgLiqId(mfg,liquor)
    (conn, c) = Connect()
    newAmount =""
    if(id > 0):
        query = "SELECT amount FROM inventory where ml_id=?"
        c.execute(query,(id,))
        oldAmountt = c.fetchone()
        if oldAmountt is None:
            query = "INSERT INTO inventory VALUES (?,?)"
            c.execute(query,(id,amount))
            conn.commit()
            conn.close()
            return
        else:
            print "sup: "+str(oldAmountt)
            oldAmount = oldAmountt[0]
            newAmount = str(add_two_amounts(amount, oldAmount)) + " ml"
            
            query = "UPDATE inventory SET amount = ? WHERE ml_id = ?"
            c.execute(query,(newAmount,id))
            conn.commit()
            conn.close()
        return
        
    else:
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

def check_inventory(mfg, liquor):
    id = int(getMfgLiqId(mfg, liquor))
    if(id > 0):
        (conn, c) = Connect()
        c.execute("SELECT * FROM inventory WHERE ml_id = ?",(id,))
        if c.fetchone() is None:
            return False
        else:
            return True
    else:
        return False
        
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    # the result we will eventually return
    
    id = getMfgLiqId(mfg, liquor)
    
    (conn, c) = Connect()
    query = "SELECT amount FROM inventory WHERE ml_id = ?"
    
    c.execute(query, (id,))
    row = c.fetchone()
    if row is None:
        return 0.0
    amount = convert_to_ml(row[0])
    return amount
    return float(row[0].split()[0])
    
    if(c.rowcount == 0):
        return 0.0
    amount_tuple = c.fetchone()
    if not amount_tuple:
        return 0.0
    amount = amount_tuple[0]
    
    final_amount = float(_inventory_db[(mfg, liquor)].split()[0])
    return final_amount
    
    
def add_two_amounts(first,second):
    final_amount = convert_to_ml(first) + convert_to_ml(second)
    return final_amount


def get_liquor_inventory_with_amounts():
    (conn,c) = Connect()
    query = "SELECT mfg,liquor,amount FROM mfg_liq JOIN inventory ON ml_id=id"
    c.execute(query)
    rows = c.fetchall()
    for row in rows:
            yield row[0],row[1],row[2]
            #yield m, l,_inventory_db[(m,l)]
    conn.close()

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    (conn,c) = Connect()
    query = "SELECT mfg,liquor FROM mfg_liq"
    c.execute(query)
    rows = c.fetchall()
    for row in rows:
            yield row[0],row[1]
            
    #for (m, l) in _inventory_db:
    #   yield m, l
    
#Input: string
#Output: Recipe object or false if it doesn't exist 
def get_recipe(name):
    listRecipes = []
    (conn,c) = Connect()
    query = "SELECT type,amount FROM recipes WHERE name = ?"
    c.execute(query,(name,))
    if(int(c.rowcount) == 0):
        return False
    
    rows = c.fetchall()
    ingredients = []
    for row in rows:
        ingredients.append((row[0],row[1]))
        
        r = recipes.Recipe(name,ingredients)
        return r
    
    
    for row in rows:
        listRecipes.append(row[0])
    for i in range(len(listRecipes)):
        #print type(name)
        #print type(listRecipes[i].name)
        query = "SELECT type,amount FROM recipes WHERE name = ?"
        c.execute(query, listRecipes[i])
        rows = c.fetchall()
        for row in rows:
            ingredients.append((row[0],row[1]))
            
            r = recipes.Recipe(name,ingredients)
            
        if name == listRecipes[i].name:
            return listRecipes[i]
    return False
    
# Input r: recipe object
# Output: False if a recipe with the same name exists
#         True otherwise
def add_recipe(r):
    if(not get_recipe(r.name)):
        values = []
        (conn, c) = Connect()
        for ing in r.ingredients:
            values.append((r.name,ing[0],ing[1]))
        print "VALUES for add recipe: "+str(values)
        query = "INSERT INTO recipes VALUES (?,?,?)"
        c.executemany(query,values)
        print "CCCOUNT: "+str(c.rowcount)
        conn.commit()
        
        c.execute("SELECT * FROM recipes")
        res = c.fetchone()
        
        conn.close()
        #_recipes_db.add(r)
        return True
    err = "Duplicate recipe: name '%s'" % r.name
    raise DuplicateRecipeName(err)
    #return False
    

def get_all_recipes():
    
    (conn, c) = Connect()
    query = "SELECT * FROM recipes ORDER BY name"
    c.execute(query)
    rows = c.fetchall()
    all = []
    name = ""
    ings = []
    tmp_name=""
    
    
    for row in rows:
        tmp_name = row[0]
        print "***************"
        print row
        print "&&&&&&&&&&&&&&&&&"
        if name == "":
            name = tmp_name
        if tmp_name == name:
            ings.append((row[1],row[2]))
        else:
            print "Done with one show rec"
            print "NAME: "+name
            print "INGS: "+str(ings)
            r = recipes.Recipe(name, ings)
            all.append(r)
            name = tmp_name
            ings = [(row[1],row[2])]
    if name != "":        
        r = recipes.Recipe(name, ings)
        all.append(r)
    
    return all

def get_all_recipes_names():
    
    
    (conn, c) = Connect()
    query = "SELECT DISTINCT name FROM recipes"
    c.execute(query)
    rows = c.fetchall()
    all = []
    for row in rows:
        all.append(row[0])
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
    
        return amount_f*1000.0
    
    elif(unit == "ml"):
    
        return amount_f
        
def getMfgLiqId(mfg,liq):
    (conn,c) = Connect()
    query = "SELECT id FROM mfg_liq WHERE mfg=? and liquor=?"
    c.execute(query,(mfg,liq))

    result = c.fetchone()
    if not result is None:
        return int(result[0]) 
    else:
        return 0

    
