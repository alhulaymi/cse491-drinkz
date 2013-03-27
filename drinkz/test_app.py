import app, db, recipes
import urllib

def test_recipes():
    db._reset_db()
    recipe1 = recipes.Recipe('vodka martini', [('vermouth', '1.5 oz')])

    recipe2 =  recipes.Recipe('vomit inducing martini', [('blended scotch',
                                                          '2 oz'),
                                                         ('unflavored vodka',
                                                          '1.5 oz')])

    db.add_recipe(recipe1)
    db.add_recipe(recipe2)
    
    environ = {}
    environ['PATH_INFO'] = '/recipes'
    
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('vodka martini') != -1, text
    assert text.find('vomit inducing martini') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'