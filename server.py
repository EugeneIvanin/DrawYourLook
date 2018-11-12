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
        
class filters:
    def GET(self):
        name = 'filters_page'
        return render.start(name)
   
        
class result:
    def GET(self):
        name = 'result_page'
        return render.start(name)
    

        
if __name__ == "__main__":
    app.run()
