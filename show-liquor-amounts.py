import drinkz.db

drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
drinkz.db.add_bottle_type('Johnnie Walker', 'White Label', 'blended scotch')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 oz')
drinkz.db.add_to_inventory('Johnnie Walker', 'White Label', '1 oz')
drinkz.db.add_to_inventory('Johnnie Walker', 'White Label', '2 oz')

# So we won't list the same type twice when we calcualte the amount
done_types =[]

print 'Manufacturer\tLiquor\t\t\tAmount'
print '------------\t------\t\t\t------'
for mfg, liquor in drinkz.db.get_liquor_inventory():
    
    # check if we did it before
    if((mfg,liquor) in done_types):
        continue
    # if not, calculate the amount, show the the info, and add it as done
    else:
        amount = drinkz.db.get_liquor_amount(mfg, liquor)
        print '%s\t%s\t\t%s' % (mfg, liquor, amount)
        done_types.append((mfg,liquor))