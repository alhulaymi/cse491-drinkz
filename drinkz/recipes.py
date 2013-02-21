import db
class Recipe(object):
    def __init__(self,n = "",i = []):
        self.name = n;
        self.ingredients = i
    
    def need_ingredients(self):
        
        # the list we're hoping to return
        missing = []
        
        found = False
        
        # go through the ingredients
        for ing in self.ingredients:
            found = False
            # make a tuple to be added eventually
            need = (ing[0],db.convert_to_ml(ing[1]))
            
            original_needed_amount = need[1] # ignore this for a while, it will come in handy soon
            
            # now compare the ingredient type to the types we hve
            for type in db.get_bottle_types():
                
                
                # if we know such type exists and that type is in our inventory (by a mfg and a liquor)
                if (type[2] == need[0]) and db.check_inventory(type[0],type[1]):
                    #print "checking "+type[2]+" with mfg= "+type[0]+ " with liquor "+type[1]
                    # see how much liquor is available by that particular mfg and liquor
                    available_amount = db.get_liquor_amount(type[0],type[1])
                    
                    # if we have more than or equal amount of that liquor from that particular mfg and liquor
                    if (available_amount >= original_needed_amount):
                        #print "found it :)"
                        # then we're done here, let's move on to the next ingredient (break out of the current/types loop)
                        found = True
                        break
                        
                        
                    else:    # if the amount is not enough
                        
                        # how much is missing? (difference between what we need and what we have)
                        difference_amount =  original_needed_amount - available_amount
                       
                        # we will try to find the mfg and liquor with the minimum missing amount. Otherwise, just leave it alone.
                        # I know I could've used min() but this will make thins look simpler
                        if(difference_amount < need[1]):
                            #print "we will replace the current "+str(need[1])+" with the new differnece: "+str(difference_amount)
                            need = (need[0],difference_amount)
                        #else:
                            #print "we will not replace "+str(need[1])+" with the new difference "+str(difference_amount)
                            
            if(not found):
                 missing.append(need)
        return missing
                            
                    
            
        
    def out(self):
        print "Recipe is:"
        
        print self.name + " " + str(self.ingredients)
        
      
            
    def __cmp__(self,other):
        equal = True
        
        if self.name != other.name:
            return False
        
        if (len(self.ingredients) != len(other.ingredients)):
            return False
        
        for i in self.ingredients:
            print "should see something"
            print i
            if(not (self.ingredients in other.ingredients)):
                return False
        return True