#! /usr/bin/env python

import os

from drinkz import db,recipes

# Populating the db

db.load_db("bin/db.txt")


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
<tr><th>Name</th><th>Ingredients</th><th>Are we missing anything?</tr>
"""
for recipe in db.get_all_recipes():
    print >>fp,"<tr><td> %s </td><td><table cellpadding =\"5\">" % recipe.name
    for item in recipe.ingredients:
        print >>fp, "<tr><td> %s </td><td> %s </td></tr>" % item
    print >>fp,"</table></td><td>"
    
    missing = recipe.need_ingredients()
    if(missing):
        print >>fp,"we're missing some stuff, call Mikey"
    else:
        print >>fp,"nope, we're good to go, call Mikey"
    
    print >>fp,"</td></tr>"


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
