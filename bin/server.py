import _mypath
import sys
from cStringIO import StringIO

DBFile = "db.txt"

from drinkz import app

from drinkz.app import SimpleApp

import random, socket
port = random.randint(8000, 9999)


app.load_db_file(DBFile)
#httpd = make_server('', port, app)
print "Serving on port %d..." % port
print "Try using a Web browser to go to http://%s:%d/" % \
	  (socket.getfqdn(), port)
#httpd.serve_forever()
while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname(), port))
    sock.listen(5)
    
    
    
    while 1:
        print "Waiting ..."
        (clientsocket, address) = sock.accept()
        print str(address) + " connected"
        
        
        request = ""
        
        print "Waiting ..."
        request = request + clientsocket.recv(1024)
       
        print "<<<< Request Start: "
        print request
        print "Request End >>>>>"
        request = request.lstrip()
        request_all_list = request.splitlines()
        request_list = request_all_list[0].split(' ')
        if len(request_list) < 2:
            clientsocket.send("First line is not long enough")
            continue
        request_type, local_URL = request_list[0],request_list[1]
        environ = {}
        request_source_list = local_URL.split("?")
        if len(request_source_list) > 1:
            request_formdata = request_source_list[1]
            environ['QUERY_STRING'] = request_formdata
            #print "=======Form: "+request_formdata
            
        if len(request_source_list) > 0:
            request_source = request_source_list[0]
            #print "=======Page: "+request_source
            
        if len(request_source_list) == 0:
            request_source = "/"
        
        #request_type = request.strip(' ',1)[0]
        if request_type == "POST":
            s_input = request_all_list[-1]
            #print "===POST: "+s_input
            environ['wsgi.input'] = StringIO(s_input)
            environ['CONTENT_LENGTH'] = len(s_input)
            #clientsocket.send("Only GET requests please!")
            #continue
        
        
        environ['PATH_INFO'] = request_source
        environ['REQUEST_METHOD'] = (request_type)
        
        d = {}
        def my_start_response(s, h, return_in=d):
            d['status'] = s
            d['headers'] = h
        
        app_obj = app.SimpleApp()    
        results = app_obj(environ, my_start_response)
        #print "results:"+str(results)
        if request_type == "POST":
            text = "".join(results)
        else:
            text = "HTTP/1.0 "+d['status']+" \n"
            for header in d['headers']:
                text = text + (header[0]+": "+header[1]+" \n")
            text = text + "".join(results)
        #text = text.join(results)
        #print text
        #clientsocket.send(str(len(text)))
        #print "TEXT:  "+text
        clientsocket.send(text)
        clientsocket.close()
                