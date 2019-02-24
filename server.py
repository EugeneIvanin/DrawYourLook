#!/usr/bin/env python

import web
import subprocess
import sys
import os


web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'
        

urls = ("/", "start",
        "/filters(.*)", "filters",
        "/result(.*)", "result",
        "/process(.*)", "process",
       "/upload", "upload")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'filter_url': "", 'origin_url': ""})
    web.config._session = session
else:
    session = web.config._session

class upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        print(x, file=sys.stderr)
        print(x.myfile.filename, file=sys.stderr)
        filedir = 'C:\\Users\\Mvideo\\Desktop\\Hackathon\\app\\DrawYourLook' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            
            fout.write("HELLO!") # writes the uploaded file to the newly created file.

            fout.close() # closes the file, upload complete.
        raise web.seeother('/upload')


class start:
    def GET(self):
        return render.start()
        
class filters:
    def GET(self, url):
        if not session['origin_url'].startswith('http') or url != 'fromprocess':
            session['origin_url'] = "http://" + url
        return render.filters()



class process:
    def GET(self, filter_url):
        session['filter_url'] = filter_url
        return render.process("", "", "hidden", "", 'true')
        
class result:
    def GET(self, dummy_url):
     
        filter_url = session['filter_url']
        origin_url = session['origin_url']
        
        after = subprocess.check_output(["bash", "script.sh", origin_url, filter_url])
        # catch error
        if not after.startswith('http'):
            after = '/static/PhLab1.jpg'
        return render.process("", after, "", "hidden", 'false')

    
        
if __name__ == "__main__":
    app.run()
