import tornado.ioloop
import tornado.web
import os
import sqlite3
import bcrypt

app_dir = os.path.dirname(os.path.realpath(__file__))
db = sqlite3.connect(app_dir + '/../database.db')

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

    def post(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)
        if not user or not password:
            raise tornado.web.HTTPError(401)

        global db
        cursor = db.cursor()
        packaged = (user, ) #no idea why you have to do this
        cursor.execute("SELECT * from users WHERE name=? LIMIT 1", packaged)
        row = cursor.fetchone()
        if not row:
            raise tornado.web.HTTPError(402)

        username = row[1]
        passhash = row[2]

        password = password.encode('utf-8')
        if passhash == bcrypt.hashpw(password, passhash.encode('utf-8')) and username == user:
            self.set_secure_cookie("userid", user, httponly=True, expires_days=1)
        else:
            raise tornado.web.HTTPError(403)

class RegistrationHandler(BaseHandler):
    def get(self):
        self.render(self.render(app_dir + "/public/register.html"))

    def post(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password1', None)
        if not user or not password:
            raise tornado.web.HTTPError(401)

        global db
        cursor = db.cursor()
        packaged1 = (user, ) #no idea why you have to do this

        #Does the user already exist?
        cursor.execute("SELECT * from users WHERE name=? LIMIT 1", packaged1)
        row = cursor.fetchone()
        if row:
            raise tornado.web.HTTPError(403)

        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        packaged2 = (user, hashed, ) #no idea why you have to do this
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, hash) VALUES (?, ?)", packaged2)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/register", RegistrationHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/css/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/images/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/js/"}),
    ], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    login_url = "/login")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
