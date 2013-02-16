"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

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
        
    try:
        x = []
        n = 0
    except:
        print "that's weird! failed to assign values to simple variables. This just got serious"
        pass
        
    for line in new_reader:
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
