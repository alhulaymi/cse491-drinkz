import app, db, recipes
import sys
import simplejson
from cStringIO import StringIO

  
def test_rpc_hello():
    method = 'hello'
    params = []
    id = 1
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = ('POST')
    dic = dict(method=method, params=params, id=id)
    s_input = simplejson.dumps(dic)
    environ['wsgi.input'] = StringIO(s_input)
    environ['CONTENT_LENGTH'] = len(s_input)
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('world') != -1, text
    print headers
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    
def test_rpc_add():
    method = 'add'
    params = [2,10]
    id = 1
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = ('POST')
    dic = dict(method=method, params=params, id=id)
    s_input = simplejson.dumps(dic)
    environ['wsgi.input'] = StringIO(s_input)
    environ['CONTENT_LENGTH'] = len(s_input)
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find("\"result\": 12") != -1, text
    print headers
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    
def test_rpc_convert_units_to_ml():
    method = 'convert_units_to_ml'
    params = ["13.5 liter"]
    id = 1
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = ('POST')
    dic = dict(method=method, params=params, id=id)
    s_input = simplejson.dumps(dic)
    environ['wsgi.input'] = StringIO(s_input)
    environ['CONTENT_LENGTH'] = len(s_input)
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    text_array = simplejson.loads(text)
    
    answer = text_array["result"]
    
    assert text.find("13500.0 ml") != -1, text
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    
def test_rpc_get_recipe_names():
    db._reset_db()
    recipe1 = recipes.Recipe('youth fountain martini', [('vermouth', '1.5 oz'),('elve tear','2 oz')])
    recipe2 = recipes.Recipe('godly vodka', [('mermaid tear', '1.5 oz'),('unicorn blood','2 oz')])
    db.add_recipe(recipe1)
    db.add_recipe(recipe2)
    
    method = 'get_recipe_names'
    params = []
    id = 1
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = ('POST')
    dic = dict(method=method, params=params, id=id)
    s_input = simplejson.dumps(dic)
    environ['wsgi.input'] = StringIO(s_input)    # looking for a socket? suuuuure, here's "one"
    environ['CONTENT_LENGTH'] = len(s_input)
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find("youth fountain martini") != -1, text
    assert text.find("godly vodka") != -1, text
 
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    
def test_rpc_get_liquor_inventory():
    db._reset_db()
    mfg1 = 'Uncle Herman\'s'
    mfg2 = 'Gray Goose'

    liquor1 = 'moonshine'
    liquor2 = 'vodka'

    type1 = 'blended scotch'
    type2 = 'unflavored vodka'

    amount1 = '1 liter'
    amount2 = '2 gallon'

    db.add_bottle_type(mfg1,liquor1,type1)
    db.add_bottle_type(mfg2,liquor2,type2)
    db.add_bottle_type(mfg1,liquor2,type2)
    db.add_bottle_type(mfg2,liquor1,type1)


    db.add_to_inventory(mfg1, liquor1, amount1)
    db.add_to_inventory(mfg2, liquor2, amount2)
    db.add_to_inventory(mfg1, liquor2, amount2)
    db.add_to_inventory(mfg2, liquor1, amount1)
    
    method = 'get_liquor_inventory'
    params = []
    id = 1
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = ('POST')
    dic = dict(method=method, params=params, id=id)
    s_input = simplejson.dumps(dic)
    environ['wsgi.input'] = StringIO(s_input)    # looking for a socket? suuuuure, here's "one"
    environ['CONTENT_LENGTH'] = len(s_input)
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find("[\"Uncle Herman's\", \"vodka\"]") != -1, text
    assert text.find("[\"Uncle Herman's\", \"moonshine\"]") != -1, text
    assert text.find("[\"Gray Goose\", \"vodka\"]") != -1, text
    assert text.find("[\"Gray Goose\", \"moonshine\"]") != -1, text
    
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
