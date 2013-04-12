"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes                    # import from local package

# I know lots of "try" but the HW pages specified I should have a try for each individual line

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    #reader = csv.reader(fp)
    try:
        new_reader = data_reader(fp)
    except:
        print "failed to process the file using your fancy new function"
        pass
        
    x = []
    n = 0

    for line in new_reader:
        if len(line) != 3:
            print "not correct format in one line"
            continue
            
        try:
            (mfg, name, typ) = line
        except:
            print "failed to assign values from a line to a three-value tuple (types). Check your format"
            pass
        n += 1
        
        try:
            db.add_bottle_type(mfg, name, typ)
        except:
            print "something went wrong while trying to add a bottle type in while loading types"
            pass

    return n
    
def load_recipes(fp):
    """
    Loads in data of the form recipes from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of recipes loaded
    """
    #reader = csv.reader(fp)
    try:
        new_reader = data_reader(fp)
    except:
        print "failed to process the file using your fancy new function"
        pass
        
    n = 0

        
    for line in new_reader:
        #The format should be: name,ingredient, amount unit,ingredient, amount unit,..etc thus we should have at least 3 items
        if len(line)%2 == 0:
            print "not correct format in one line"
            pass
        
        if len(line) == 0:
            pass
            
       # try:
        ingredients_list = []
        i=1
        recipe_name = line[0]
        while i < len(line):
            
            temp_ing = (line[i].lstrip(),line[i+1].lstrip())
            print "temp_ing: "+str(temp_ing)
            ingredients_list.append(temp_ing)
            
            
            
            i = i + 2
       # except:
        #    print "failed to assign values from a line to a recipe list of ingredients tuples"
         #   pass
        
        print "list: "+str(ingredients_list)
        try:
            recipe = recipes.Recipe(recipe_name,ingredients_list)
            db.add_recipe(recipe)
        except:
            print "something went wrong while trying to add a recipe in while recipes"
            pass
        
        n += 1

    return n

def data_reader(fp):
    
    try:
        reader = csv.reader(fp)
    except:
        print "failed to open the provided file"
        pass
        
    for line in reader:
        
        try:
            if not line:
                continue
        except:
            print "fatal error while detecting empty line"
            pass
        
        #print "line: "+str(line)
        
        #if len(line) != 3:
            #continue
            
        try:
            if line[0].startswith('#'):
                continue
        except IndexError:
            print "index error raised while trying to read line in CSV"
        except:
            print "error reading a line"
            pass
        
        try:    
            yield line
        except:
            print "failed to yeild the generated value"
            pass

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    
        
    try:
        new_reader = data_reader(fp)
    except:
            print "failed to process the file using your fancy new function"
            pass
    try:
        x = []
        n = 0
    except:
        print "that's weird! failed to assign values to simple variables. This just got serious"
        pass
        
    for line in new_reader:
        if len(line) != 3:
            print "not correct format in one line"
            pass
        try:
            (mfg, name, amount) = line
        except:
            print "failed to assign values from a line to a three-value tuple (amounts). Check your format"
            pass
        n += 1
        try:
            db.add_to_inventory(mfg, name, amount)
        except:
            print "something went wrong while trying to add a bottle type in while loading types"
            pass

    return n
