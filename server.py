import web

web.config.debug = False

urls = ("/", "start",
        "/filters(.+)", "filters",
        "/result(.+)", "result")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)
session = web.session.Session(app, web.session.DiskStore('sessions'))


class start:
    def GET(self):
        return render.start()
        
class filters:
    def GET(self, url):
        return render.filters(url)
   
        
class result:
    def GET(self, filter_url):
        list_url_filter = filter_url.split('.zip', 1) 
        filter = list_url_filter[0]
        url = list_url_filter[1]
        return render.result(url, filter)
    

        
if __name__ == "__main__":
    app.run()
