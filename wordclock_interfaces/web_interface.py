import web
from web import form
import threading

render = web.template.render('web_templates/')

my_form = form.Form(
 form.Button("btn", id="EVENT_BUTTON_LEFT", value="True", html="Left", class_="_left"),
 form.Button("btn", id="EVENT_BUTTON_RETURN", value="True", html="Return", class_="_return"),
 form.Button("btn", id="EVENT_BUTTON_RIGHT", value="True", html="Right", class_="_right"),
)

class index:
    def GET(self):
        form = my_form()
        return render.index(form, "Welcome")

    def POST(self):
        inp = web.input(id="EVENT_BUTTON_LEFT")
        form = my_form()
        return render.index(form, "Answer received")

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
        app = web.application(self.urls, globals())
        app.run()

    def _left(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_LEFT)

    def _return(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RETURN)

    def _right(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RIGHT)

