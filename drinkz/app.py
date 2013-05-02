#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import cgi, cgitb
import jinja2
cgitb.enable(display=0, logdir="/path/to/logdir")
import os
import uuid
from Cookie import SimpleCookie

import db, recipes
import load_bulk_data


usernames = {}




def load_db_file(file_name):
    db.load_db(file_name)


def printMenu():
    menu = """
    <h2> Menu </h2>
    <a href='/'>Home</a></br>
    
    <h3> Show </h3>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    
    <h3> Add </h3>
    <a href='add_recipe_form'>Recipes</a></br>
    <a href='add_inventory_form'>Inventory</a></br>
    <a href='add_type_form'>Liquor Types</a></br>
        
        
    
    <h3> Other </h3>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='upload'>Upload Data</a></br>
    
    </br>
    <a href='logout'>Log Out</a>
    """
    
    return menu
    


dispatch = {
    '/login' : 'login',
    '/logout' : 'logout',
    '/gate' : 'gate',
    '/' : 'index',
    '/recipes' : 'recipes',
    '/error' : 'error',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_types',
    '/convert_result' : 'convert_result',
    '/convert_to_ml' : 'convert_form',
    '/rpc'  : 'dispatch_rpc',
    '/upload' : 'upload_file_form',
    '/upload_file_script' : 'upload_file_script',
    '/add_type_form' : 'add_type_form',
    '/add_type_script' : 'add_type_script',
    '/add_recipe_form' : 'add_recipe_form',
    '/add_recipe_script_first' : 'add_recipe_script_first',
    '/add_recipe_script_second' : 'add_recipe_script_second',
    '/add_inventory_form' : "add_inventory_form",
    '/add_inventory_script' : "add_inventory_script",
    '/add_inventory_script' : "add_inventory_script"
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def load_bulk_data_types(self,file_name):
        return load_bulk_data.load_bottle_types(file_name)

    def load_bulk_data_inventory(self,file_name):
        return load_bulk_data.load_inventory(file_name)
        
    def load_bulk_data_recipes(self,file_name):
            return load_bulk_data.load_recipes(file_name)
        
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
        
    def load_db_file(self, file_name):
        db.load_db(file_name)
        
    def buildHtmlPage(self,title,head,body):
        
        
        vars = dict(script = head, title = title, body = body, sidebar = printMenu())
        
        #return page
        loader = jinja2.FileSystemLoader('../templates')
        env = jinja2.Environment(loader=loader)
        filename = "page.html"
        template = env.get_template(filename)
        return_value = template.render(vars)
        #print return_value
        return str(return_value)
            
    def index(self, environ, start_response):
        
        data = """
                <input type=\"button\" onclick=\"legalNotice()\" value=\"Legal Note\" />"""
        #data = data + printMenu()
        script = """
                <script>
                function legalNotice()
                {
                    alert('Minions and hellhounds might seek remedies for services provided here');
                }
                </script>
             """
         
        data = self.buildHtmlPage("Main Page",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
    
    def login(self, environ, start_response):
        data = """
            <html>
            <head>
                
            </head>
            <body>
                <form action='/gate'>
                    Name: <input type='text' name='name'> </br>
                    Password: <input type='password' name='password'>
                    <input type='submit' value='login'>
                </form>
            </body>
            </html>
        """
        start_response('200 OK', list(html_headers))
        return [data]
        
    def gate(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        password = results['password'][0]
        content_type = 'text/html'
        
        # authentication would go here -- is this a valid username/password,
        # for example?
        if name != "Hassan" or password != "hassan":
            headers = list(html_headers)
            headers.append(('Location', '/login'))
            start_response('302 Found', headers)
            return ["Redirect to home page, be patient goddammit!!!"]
            
        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to home page, be patient goddammit!!!"]
        
    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/login'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /login pgae ..."]
        
    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = """

        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Name</th><th>Ingredients</th><th>Are we missing anything?</tr>
        """
        for recipe in db.get_all_recipes():
            data = data + "<tr><td> "+ recipe.name +"</td><td><table cellpadding =\"5\">"
            for item in recipe.ingredients:
                data = data + "<tr><td>"+ item[0] +"</td><td> " + item[1] +" </td></tr>"
            data = data + "</table></td><td>"
            
            missing = recipe.need_ingredients()
            if(missing):
                data = data + "we're missing some stuff, call Mikey"
            else:
                data = data + "nope, we're good to go, call Mikey"
            
            print data + "</td></tr>"
        data = data + "</table>"

        menu = printMenu()
        
        #data = data + menu
        data = self.buildHtmlPage("Recipes","",data)
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = """
        <div class='info'>
        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Manfacturer</th><th>Liquor</th><th>Amount</th></tr>
        """
        for item in db.get_liquor_inventory_with_amounts():
            data = data + "<tr><td> "+ item[0] +" </td><td> "+item[1]+" </td><td> "+item[2]+" </td></tr>"
        data = data + "</table></div>"
        
        #data = data + printMenu()
        data = self.buildHtmlPage("Inventory","",data)
        start_response('200 OK', [('Content-type', content_type)])
        return [data]
        
    def liquor_types(self, environ, start_response):
        content_type = 'text/html'
        data = """
        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Manfacturer</th><th>Liquor</th><th>Type</th></tr>
        """
        for item in db.get_bottle_types():
            data = data + "<tr><td> %s </td><td> %s </td><td> %s </td></tr>" % item
        
        data = data + "</table>"
        
        #data = data + printMenu()
        data = self.buildHtmlPage("Liquor Types","",data)
        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def convert_form(self, environ, start_response):
        data = form()
        script = """
                    <script>
                    function askAboutSoul()
                    {
                        alert('Your soul will be owed to Satan in return for this dark dark knowledge');
                    }
                    </script>
                 """
        data = self.buildHtmlPage("Conversion Witchcraft",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
        
    def upload_file_form(self, environ, start_response):
        data = """
        <form action='upload_file_script' enctype='multipart/form-data' method='POST'>
        input file of data: <input type='file' name='file'></br>
        Contents of file: </br>
        <input type='radio' name='file_type' value='types' checked> Liquor Types </br>
        <input type='radio' name='file_type' value='inventory'> Cabinet Inventory </br>
        <input type='radio' name='file_type' value='recipes'> Recipes List </br>
        <input type='submit' value='upload'>
        </form>
        """
        script = ""
        data = self.buildHtmlPage("Data File",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def upload_file_script(self, environ, start_response):
        data = ""
        
        script = ""
        #http://stackoverflow.com/questions/530526/accessing-post-data-from-wsgi
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=post_env)
        
        
        fileitem = form["file"]
        
        destination_file_location = ""
        print form["file_type"].value
        
        if form["file_type"].value == "types":
            destination_file_location = "db_types_data.txt"
        elif form["file_type"].value == "inventory":
            destination_file_location = "db_inventory_data.txt"
        elif form["file_type"].value == "recipes":
            destination_file_location = "db_recipes_data.txt"
        

        data = ""
        
        
        if fileitem.file:
            destination_file = open(destination_file_location,"w")
            # It's an uploaded file; count lines
            linecount = 0
            while 1:
                line = fileitem.file.readline()
                if not line: break
                destination_file.write(line)
                linecount = linecount + 1
            destination_file.close()
        
        fp = open(destination_file_location)
        
        if form["file_type"].value == "types":
             items = self.load_bulk_data_types(fp)
        elif form["file_type"].value == "inventory":
             items = self.load_bulk_data_inventory(fp)
        elif form["file_type"].value == "recipes":
             items = self.load_bulk_data_recipes(fp)

        fp.close()
        
        data = data + str(items) + " items added </br>"
        
        data = data + "file recieved, proccssed and saved as " + destination_file_location
        #data = data + printMenu()
        
        data = self.buildHtmlPage("File received ",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def convert_result(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        ml_amount = db.convert_to_ml(results['amount'][0])

        content_type = 'text/html'
        data = "Amount entered: %s:" % (str(ml_amount)+" ml")
        
        #data = data + printMenu()
        data = self.buildHtmlPage("The Witch Has Spoken","",data)
        start_response('200 OK', list(html_headers))
        return [data]
    
    def add_type_form(self, environ, start_response):
        data = """
        <form action='add_type_script'>
        <table>
        <tr>
        <th>Manufacturer:</th> <td><input type='text' name='mfg'></td>
        </tr>
        <tr>
        <th>Liquor:</th> <td><input type='text' name='liquor'></td>
        </tr>
        <tr>
        <th>Type:</th> <td><input type='text' name='type'></td>
        </tr>
        </table>
        <input type='submit' value='Add'>
        </form>
        """
        script = ""
        data = self.buildHtmlPage("Add Bottle Type Form",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def add_type_script(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        type = results['type'][0]
        
        db.add_bottle_type(mfg,liquor,type)
        

        content_type = 'text/html'
        
        data = "Added Bottle type: " +type+ " of " + liquor + " made by "+mfg
        #data = data + printMenu()
        data = self.buildHtmlPage("One more type","",data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def add_inventory_form(self, environ, start_response):
        data = """
        <form action='add_inventory_script'>
        <table>
        <tr>
        <th>Manufacturer:</th> <td><input type='text' name='mfg'></td>
        </tr>
        <tr>
        <th>Liquor:</th> <td><input type='text' name='liquor'></td>
        </tr>
        <tr>
        <th>Amount:</th> <td><input type='text' name='amount'>i.e. 13.2 oz</td>
        </tr>
        </table>
        <input type='submit' value='Add'>
        </form>
        """
        script = ""
        data = self.buildHtmlPage("Add Bottle To Inventory Form",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
    
    def add_recipe_form(self, environ, start_response):
        data = """
        <form action='add_recipe_script_first'>
        <table>
        <tr>
        <th>How many ingredients in the recipe?</th> <td><input type='text' name='no_ingredients'></td>
        </tr>
        </table>
        <input type='submit' value='Next>>'>
        </form>
        """
        script = ""
        data = self.buildHtmlPage("Add Recipe Form 1",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def add_recipe_script_first(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        print results['no_ingredients'][0]
        ingredients = int(results['no_ingredients'][0]);
        
        
        data = """
        <form action='add_recipe_script_second'>
        <input type='text' placeholder='Recipe Name' name='recipe_name'>
        <table>
        <tr>"""
        for i in range(ingredients):
            data = data + "<th>Drink: </th><td><input type='text' name='no_ingredients"+str(i)+ """' value='drink'></td>
                             <th>Amount: </th><td><td><input type='text' value='0 ml' name='amount"""+str(i) +"'></td>"
            data = data + "</tr>"
        
        data = data +"""
        </table>
        """
        
        data = data + " <input type='hidden' name='no_ing' value='"+str(ingredients)+"""'>
        <input type='submit' value='Add'>
        </form>
        """
        script = ""
        data = self.buildHtmlPage("Add Recipe Form 2",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def add_recipe_script_second(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        no_ing = int(results['no_ing'][0]);
        ingredients = []
        
        for i in range(no_ing):
            drink = results['no_ingredients'+str(i)][0]
            amount = results['amount'+str(i)][0]
            
            ingredients.append((drink,amount))
            
        recipe = recipes.Recipe(results['recipe_name'][0],ingredients)
        
        try:
            db.add_recipe(recipe)
            data = "Added Recipe Successfully"
        except db.DuplicateRecipeName:
            data = "Recipe with name "+ results['recipe_name'][0] +"already exists"
            
        
        script = ""
        data = self.buildHtmlPage("Add Recipe Form 2",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
        
    def add_inventory_script(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        amount = results['amount'][0]
        
        try:
            db.add_to_inventory(mfg,liquor,amount)
            data = "Added "+amount+" for "+liquor+" made by "+mfg
        except db.LiquorMissing:
            data = "Failed to find this type!"
            
            

        content_type = 'text/html'
        
        
        #data = data + printMenu()
        data = self.buildHtmlPage("Inventory Item Addition","",data)
        start_response('200 OK', list(html_headers))
        return [data]
    
    ##### RPC API ########################################################################
    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                #print "wsgi: "
                #print environ['wsgi.input'].read(length)
                #print "-=-=-=-"
                body = environ['wsgi.input'].read(length)
                #print "body::: "+body
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])
                #print "response: "+response
                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
        
    def rpc_convert_units_to_ml(self, amount):
        return str(db.convert_to_ml(amount))+" ml"
        
    def rpc_get_recipe_names(self):
        return str(db.get_all_recipes_names())

    def rpc_get_liquor_inventory(self):
        inventories = db.get_liquor_inventory()
        inventory_list = []
        for inventory in inventories:
            inventory_list.append((inventory[0],inventory[1]))
        return inventory_list
        
    def rpc_add_inventory(self,mfg,liquor,amount):
        try:
            db.add_to_inventory(mfg,liquor,amount)
            data = "Added "+amount+" for "+liquor+" made by "+mfg
        except db.LiquorMissing:
            data = "Failed to find this type!"
        return data
        
    def rpc_add_bottle_type(self,mfg,liquor,type):
        db.add_bottle_type(mfg,liquor,type)
        return "Added One Bottle Type"
        
    def rpc_add_recipe(self, name, ingredients):
        db.add_recipe(recipes.Recipe(name,ingredients))
        return "Added One Recipe"
    
def form():
    return """
<form action='convert_result'>
How much liq... I mean fun you've got? <input type='text' name='amount' placeholder='amount unit' size='20'>
<input type='submit' onclick='askAboutSoul()' value='Sell Your Soul'>
</form>
"""



if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/login" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
