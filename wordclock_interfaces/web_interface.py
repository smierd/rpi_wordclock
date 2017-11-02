import web
import threading

render = web.template.render('wordclock_interfaces/web_templates/')

class index:
    def GET(self):
        return render.index("No button pressed yet.")

    def POST(self):
        return web.input().signal

class EvtInjector:
    def __init__(self, evtHandler):
        self.evtHandler = evtHandler

    def __call__(self, handler):
        eventId = web.input(signal="invalid")
        if eventId.signal != "invalid":
            self.evtHandler.setEvent(int(eventId.signal))
        return handler()

class CustomWebApp(web.application):
    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class web_interface(threading.Thread):

    def __init__(self, config, evtHandler):
        '''
        Initialization
        '''
        print('Setting up web interface')
        self.evtHandler = evtHandler

        # web.py specific initializations
        self.urls = ('/', 'index')

        # thread-specific initializations
        super(web_interface, self).__init__()
        self.daemon=True
        self.start()

    def run(self):
        app = CustomWebApp(self.urls, globals())
        app.add_processor(EvtInjector(self.evtHandler))
        app.run()

    def _left(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_LEFT)

    def _return(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RETURN)

    def _right(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RIGHT)

