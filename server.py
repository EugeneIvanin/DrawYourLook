import web

urls = ("/.*", "hello")
app = web.application(urls, globals())
render = web.template.render('templates/')


class hello:
    name = 'Eugene'    
    return render.index(name)

if __name__ == "__main__":
    app.run()
