import tornado.ioloop
import tornado.web
import os
import sqlite3
import bcrypt
import tornado_mysql
import ConfigParser
import torndb

app_dir = os.path.dirname(os.path.realpath(__file__))

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("userid", max_age_days=1)
        if not user_id:
            return None
        return user_id

class MainHandler(BaseHandler):
    def get(self):
        self.render(app_dir + "/public/index.html")

class UserHandler(BaseHandler):
    def get(self, userid):

        global db
        user = db.get("SELECT * from users WHERE id=%s LIMIT 1", userid)
        if not user:
            raise tornado.web.HTTPError(403)

        self.render(app_dir + "/public/homepage.html", username=user.name)

class LoginHandler(BaseHandler):
    def get(self):
        self.render(app_dir + "/public/login.html")

    def post(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)
        if not user or not password:
            raise tornado.web.HTTPError(401)

        global db
        row = db.get("SELECT * from users WHERE name=%s LIMIT 1", user)
        if not row:
            raise tornado.web.HTTPError(403)

        userid = row.id
        username = row.name
        passhash = row.hash

        password = password.encode('utf-8')
        if passhash == bcrypt.hashpw(password, passhash.encode('utf-8')) and username == user:
            self.set_secure_cookie("userid", user, httponly=True, expires_days=1)
        else:
            raise tornado.web.HTTPError(403)
        self.redirect('/user/' + str(userid))
        return

class RegistrationHandler(BaseHandler):
    def get(self):
        self.render(app_dir + "/public/register.html")

    def post(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password1', None)
        if not user or not password:
            raise tornado.web.HTTPError(401)

        global db
        #Does the user already exist?
        rows = db.get("SELECT * from users WHERE name=%s LIMIT 1", user)
        if rows:
            raise tornado.web.HTTPError(403)

        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        db.execute("INSERT INTO users (name, hash) VALUES (%s, %s)", user, hashed)
        self.redirect('/login')
        return


def make_app():

    config = ConfigParser.RawConfigParser()
    config.read(app_dir + '/settings.cfg')
    secure_cookie_key = config.get('server', 'secure_cookie_key')
    db_url = config.get('database', 'url')
    db_username = config.get('database', 'username')
    db_password = config.get('database', 'password')
    global db
    db = torndb.Connection(db_url, "obedientart", user=db_username, password=db_password)

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/register", RegistrationHandler),
        (r"/user/([^/]+)", UserHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/css/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/images/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/js/"}),
    ], cookie_secret=secure_cookie_key,
    login_url = "/login")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
