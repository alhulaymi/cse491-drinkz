
class Recipe:
    def __init__(self,n = "",i = []):
        self.name = n;
        self.ingredients = i
    
    def need_ingredients(self):
        return 0
        
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