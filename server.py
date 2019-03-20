#!/usr/bin/env python

import web
import subprocess
from client_opeapi import ClientOpeapi
from daemon import runner


web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'

class MyApplication(web.application):
 
    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

urls = ("/", "start",
        "/filters(.*)", "filters",
        "/result(.*)", "result",
        "/process(.*)", "process")

app = MyApplication(urls, globals())
render = web.template.render('templates/', cache = False)


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'filter_url': "", 'origin_url': "", 'after': ""})
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
        api = ClientOpeapi('dd23c729867efed20328bf3a8b7e9f23', '857165871a491e1ebc72b1abb2415606')
        if filter_url == 'blue_pink.zip':
                template_name = '1001185'
        elif filter_url == 'comic.zip':
                template_name = '1001186'
        elif filter_url == 'pop_art_light.zip':
                template_name = '1001187'
        elif filter_url == 'stereo.zip':
                template_name = '1001188'
                
        try:
            after = api.template_process(origin_url, template_name)
        except:
            after = '/static/PhLab1.jpg'
        session['after'] = after
        after = session['after']
        # after = subprocess.check_output(["bash", "script.sh", origin_url, filter_url])
        # catch erro
        return render.result("", after, "", "hidden", 'false')

    
        
if __name__ == "__main__":
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()

