import web

web.config.debug = False

urls = ("/", "start",
        "/filters(.+)", "filters",
        "/result(.+)", "result")

app = web.application(urls, globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'filter': 0})


class start:
    def GET(self):
        return render.start()

    def POST(self):
        url = web.input()
        raise web.seeother('/filters')
        
class filters:
    def GET(self, url):
        return render.filters(url)
   
        
class result:
    def GET(self):
        return render.start()
    

        
if __name__ == "__main__":
    app.run()
