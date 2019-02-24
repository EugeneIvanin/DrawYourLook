#!/usr/bin/env python

import web
from web import form

import subprocess
import sys
import os

import requests 

web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'
        

urls = ("/", "start",
        "/filters(.*)", "filters",
        "/result(.*)", "result",
        "/process(.*)", "process",
       "/upload", "upload",
       "/get_result", "get_result")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'filter_url': "", 'origin_url': ""})
    web.config._session = session
else:
    session = web.config._session


myform = form.Form( 
    form.Textbox("Enter URL:", 
        form.notnull,
        form.Validator('Не должно быть пустой строкой', lambda x: str(x) != ''))) 

class get_result:
    def GET(self):
        user_data = web.input(img={})['img'] 
        sys.stderr.write(user_data)
        return render.get_result()
        


class upload:
    def GET(self): 
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form)

    def POST(self): 
        form = myform() 
        if not form.validates(): 
            return render.formtest(form)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            str_url = form["Enter URL:"].value
            r = requests.get(str_url)
            with open("get_data.xlsx",'wb') as f:
                    f.write(r.content) 
            return render.get_result()
        
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


