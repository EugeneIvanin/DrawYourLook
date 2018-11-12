import web

web.config.debug = False

urls = ("/", "start",
        "/filters", "filters",
        "/result(.+)", "result")

app = web.application(urls, globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'filter': 0})


class start:
    def GET(self):
        return render.start()
    
    def POST(self):
        url = web.input()
        raise web.seeother('/filters', url)

        
class filters:
    def GET(self):
        return render.filters()
   
        
class result:
    def GET(self):
        name = 'result_page'
        return render.result(name)
    

        
if __name__ == "__main__":
    app.run()
