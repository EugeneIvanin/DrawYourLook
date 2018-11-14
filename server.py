#!/usr/bin/env python

import web

web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'

urls = ("/", "start",
        "/filters(.+)", "filters",
        "/result(.+)", "result")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)
session = web.session.Session(app, web.session.DiskStore('sessions'))


class start:
    def GET(self):
        web.header("Cache-Control", "no-cache, max-age=0, must-revalidate, no-store")
        return render.start()
        
class filters:
    def GET(self, url):
        web.header("Cache-Control", "no-cache, max-age=0, must-revalidate, no-store")
        return render.filters(url)
   
        
class result:
    def GET(self, filter_url):
        list_url_filter = filter_url.split('.zip', 1) 
        filter = list_url_filter[0]
        address = list_url_filter[1]
        
        url = "http://" + url
        after = subprocess.check_output(["bash", "script.sh", url, filter_url])
        # ловим ошибку 
        if not after.startswith('http'):
            after = '/static/PhLab1.jpg'
        address = after
        return render.result(address)
    
        
if __name__ == "__main__":
    app.run()
