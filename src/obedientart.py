import tornado.ioloop
import tornado.web
import os
import sqlite3

app_dir = os.path.dirname(os.path.realpath(__file__))

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("userid", max_age_days=1)
        if not user_id:
            return None
        return user_id

class MainHandler(BaseHandler):
    def get(self):
        self.render(self.render(app_dir + "/public/index.html"))

class LoginHandler(BaseHandler):
    def get(self):
        self.render(self.render(app_dir + "/public/login.html"))

class RegistrationHandler(BaseHandler):
    def get(self):
        self.render(self.render(app_dir + "/public/register.html"))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/register", RegistrationHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/js/"}),
    ], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    login_url = "/login")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
