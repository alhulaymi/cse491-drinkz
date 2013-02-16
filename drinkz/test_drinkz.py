"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

# neat data 
testTypesData1 = "./test-data/bottle-types-testing-data-1.txt"

# nasty data
testTypesData2 = "./test-data/bottle-types-testing-data-2.txt"

# neat data 
testAmountsData1 = "./test-data/bottle-amounts-testing-data-1.txt"

# nasty data
testAmountsData2 = "./test-data/bottle-amounts-testing-data-2.txt"

from . import db, load_bulk_data


# this will test under the assumption that all amounts are in ml
def test_sum_amount_uniform():
    mfg = "Johnnie Walker"
    liqur = "Black Label"
    first_amount = "1 ml"
    second_amount = "1 ml"
    
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory(mfg, liqur, first_amount)
    db.add_to_inventory(mfg, liqur, second_amount)
    
    total_amount = db.get_liquor_amount(mfg,liqur)
    
    print "uniform amount adding method failed"
    print total_amount
    assert total_amount == 2.0
    
    
# this will test some amounts by oz and some by ml
def test_sum_amount_diverse():
    mfg = "Johnnie Walker"
    liqur = "Black Label"
    first_amount = "1 ml"
    second_amount = "1 oz"
    
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory(mfg, liqur, first_amount)
    db.add_to_inventory(mfg, liqur, second_amount)
    
    total_amount = db.get_liquor_amount(mfg,liqur)
    
    print "diverse amount adding method failed"
    print "check this out: " + str(total_amount)
    assert total_amount == 30.5735
    

def test_load_bulk_bottle_types_1():
    testTypesData1
    filed = open(testTypesData1,"r")
    n = load_bulk_data.load_bottle_types(filed)
    filed.close()
    print "failed to read neat types data"
    assert 1==n
 
def test_load_bulk_bottle_types_2():   
    testTypesData2
    file2 = open(testTypesData2,"r")
    m = load_bulk_data.load_bottle_types(file2)
    file2.close()
    print "failed to read nasty types data"
    assert 2==m
    
def test_load_bulk_bottle_amounts_1():
    
    #prepare
    testAmountsData1
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    
    #read
    filed = open(testAmountsData1,"r")
    n = load_bulk_data.load_inventory(filed)
    filed.close()
    
    #check
    print "failed to read neat amounts data "
    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert 1==n
 
def test_load_bulk_bottle_amounts_2():   
    
    #prepare
    testAmountsData2
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    #read
    filed = open(testAmountsData2,"r")
    n = load_bulk_data.load_inventory(filed)
    filed.close()
    
    #check
    print "failed to read nasty amounts data"
    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert 2==n


def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_script_load_bottle_amounts_1():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-amounts-data-1.txt', 'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x
