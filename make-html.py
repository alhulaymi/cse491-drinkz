#! /usr/bin/env python

import os

from drinkz import db,recipes

# Populating the db

recipe1 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                            ('vermouth', '1.5 oz')])
                                            
recipe2 =  recipes.Recipe('vomit inducing martini', [('orange juice',
                                                      '6 oz'),
                                                     ('vermouth',
                                                      '1.5 oz')])

mfg1 = 'Uncle Herman\'s'
mfg2 = 'Gray Goose'

liquor1 = 'moonshine'
liquor2 = 'vodka'

type1 = 'blended scotch'
type2 = 'unflavored vodka'

amount1 = '5 liter'
amount2 = '1 gallon'

db.add_recipe(recipe1)
db.add_recipe(recipe2)

db.add_bottle_type(mfg1,liquor1,type1)
db.add_bottle_type(mfg2,liquor2,type2)
db.add_bottle_type(mfg1,liquor2,type2)
db.add_bottle_type(mfg2,liquor1,type1)


db.add_to_inventory(mfg1, liquor1, amount1)
db.add_to_inventory(mfg2, liquor2, amount2)
db.add_to_inventory(mfg1, liquor2, amount2)
db.add_to_inventory(mfg2, liquor1, amount1)

###


try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

###

fp = open('html/index.html', 'w')



print >>fp, """

<a href='recipes.html'>Recipes</a></br>
<a href='inventory.html'>Inventory</a></br>
<a href='liquor_types.html'>Liquor Types</a></br>

"""

fp.close()

###

fp = open('html/recipes.html', 'w')

print >>fp,"""

<table border=\"1\" cellpadding =\"5\">
<tr><th>Name</th><th>Ingredients</th></tr>
"""
for recipe in db.get_all_recipes():
    print >>fp,"<tr><td> %s </td><td><table cellpadding =\"5\">" % recipe.name
    for item in recipe.ingredients:
        print >>fp, "<tr><td> %s </td><td> %s </td></tr>" % item
    print >>fp,"</table></td></tr>"


print >>fp,"""
</table>
"""



print >>fp, """

<a href='index.html'>Home</a></br>
<a href='inventory.html'>Inventory</a></br>
<a href='liquor_types.html'>Liquor Types</a></br>

"""

fp.close()

###

fp = open('html/inventory.html', 'w')
print >>fp,"""
<table border=\"1\" cellpadding =\"5\">
<tr><th>Manfacturer</th><th>Liquor</th><th>Amount</th></tr>
"""
for item in db.get_liquor_inventory_with_amounts():
    print >>fp,"<tr><td> %s </td><td> %s </td><td> %s </td></tr>" % item

print >>fp,"""
</table>
"""
print >>fp, """
</br>
<a href='index.html'>Home</a></br>
<a href='recipes.html'>Recipes</a></br>
<a href='liquor_types.html'>Liquor Types</a></br>

"""


fp.close()

###

fp = open('html/liquor_types.html', 'w')

print >>fp,"""
<table border=\"1\" cellpadding =\"5\">
<tr><th>Manfacturer</th><th>Liquor</th><th>Type</th></tr>
"""
for item in db.get_bottle_types():
    print >>fp,"<tr><td> %s </td><td> %s </td><td> %s </td></tr>" % item

print >>fp,"""
</table>
"""
print >>fp, """
</br>
<a href='index.html'>Home</a></br>
<a href='recipes.html'>Recipes</a></br>
<a href='inventory.html'>Inventory</a></br>

"""
fp.close()
