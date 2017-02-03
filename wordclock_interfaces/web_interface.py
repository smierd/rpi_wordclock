import web
from web import form
import threading

render = web.template.render('web_templates/')
button_resp = "temp"

my_form = form.Form(
 form.Button("btn", id="Search planet", value="ipfact", html="Find Target", class_="ipfact"),
 form.Button("btn", id="Lock on Target", value="lockta", html="Select planet to target", class_="lockta"),
 form.Button("btn", id="Destroy all humans", value="deshum", html="Destroy all humans", class_="deshum"),
 form.Button("submit", type="submit", description="Register")
)

class index:
    def GET(self):
        form = my_form()
        return render.index(form, button_resp)

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

