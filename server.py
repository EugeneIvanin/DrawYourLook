#!/usr/bin/env python

import web
import subprocess

web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'

urls = ("/", "start",
        "/filters(.*)", "filters",
        "/result(.*)", "result",
        "/process(.*)", "process")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'filter_url': "", 'origin_url': ""})
    web.config._session = session
else:
    session = web.config._session


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
        # if not after.startswith('http'):
         #   after = '/static/PhLab1.jpg'
        return render.process("", after, "", "hidden", 'false')

    
        
if __name__ == "__main__":
    app.run()
