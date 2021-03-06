import tornado.ioloop
import tornado.web
import os
import sqlite3
import bcrypt
import tornado_mysql
import ConfigParser
import torndb
import uuid
import json
import time

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

        curr_userid = self.get_current_user()
        is_uploader = True if curr_userid == userid else False

        images = [x['id']
                for x in json.loads(FileHelpers.get_images(curr_userid, userid)) if x['id'] != None]

        self.render(app_dir + "/public/homepage.html",
            username=user.name, images=images, is_uploader=is_uploader)

    def post(self):
        contents = self.get_argument('contents', None)
        imageid = self.get_argument('imageid', None)
        if not contents or not imageid:
            raise tornado.web.HTTPError(401)

        image = db.get("SELECT * from pics WHERE id=%s LIMIT 1", imageid)
        if not image:
            raise tornado.web.HTTPError(404)

        comments = db.query("SELECT * from comments WHERE pic_id=%s ORDER BY time_stamp ASC", imageid)
        if comments:
            if len(comments) > 10:
                old_id = comments[0].id
                db.execute("DELETE FROM comments WHERE id = %s", old_id)

        db.execute("INSERT INTO comments (pic_id, time_stamp, contents) VALUES (%s, %s, %s)", imageid, time.time(), contents)
        self.redirect("/user/" + str(image.user_id))

class ImageHandler(BaseHandler):
    def get(self):
        global db
        imageid = self.get_argument('imageid', None)
        image = db.get("SELECT * from pics WHERE id=%s LIMIT 1", imageid)
        if not image:
            raise tornado.web.HTTPError(403)

        file = open(app_dir + "/public/images/" + image.file_path, 'r')
        self.write(file.read())

    @tornado.web.authenticated
    def post(self):
        imageinfo = self.request.files['image'][0]
        private = self.get_argument('private', None)
        if not imageinfo:
            raise tornado.web.HTTPError(401)

        if len(imageinfo['body']) > 250000:
            raise tornado.web.HTTPError(403, reason="File size too big! Images must be smaller than 250k")

        userid = self.get_current_user()

        file_path = imageinfo['filename']
        basename = os.path.basename(file_path)

        #insert the file record into the database
        is_private = 0
        if private == "on":
            is_private = 1
        imageid = str(uuid.uuid4())
        db.execute("INSERT INTO pics (id, file_path, private, user_id) VALUES (%s, %s, %s, %s)", imageid, file_path, is_private, userid)
        self.write(imageid)

        #Save file to the filesystem, if it doesn't already exist
        if not os.path.exists(basename):
            fh = open(app_dir + "/public/images/" + basename, 'w')
            fh.write(imageinfo['body'])

class CommentHandler(BaseHandler):
    def get(self):
        imageid = self.get_argument('imageid', None)
        if not imageid:
            raise tornado.web.HTTPError(401)
        comments = db.query("SELECT * from comments WHERE pic_id=%s ORDER BY time_stamp DESC LIMIT 10", imageid)
        if comments:
            self.write('<table>')
            for sublist in comments:
                self.write('  <tr>')
                self.write('    <td>' + sublist.contents)
                self.write('  </tr>')
            self.write('</table>')

class LoginHandler(BaseHandler):
    def get(self):
        self.render(app_dir + "/public/login.html")

    def post(self):
        username = self.get_argument('user', None)
        password = self.get_argument('password', None)

        if not username or not password:
            raise tornado.web.HTTPError(401)

        global db
        user = db.get("SELECT * from users WHERE name=%s LIMIT 1", username)

        if not user:
            raise tornado.web.HTTPError(403)

        if bcrypt.hashpw(password.encode('utf-8'), user.hash.encode('utf-8')) == user.hash:
            self.set_secure_cookie("userid", str(user.id), httponly=True, expires_days=1)
        else:
            raise tornado.web.HTTPError(403)

        self.redirect('/user/' + str(user.id))
        return

class FileHelpers(object):
    @staticmethod
    def get_images(userid, queried_user_id):
        #Scrub out private file ids for security
        if queried_user_id != userid:
            images = db.query("SELECT IF (private = 1, NULL, id) AS id, file_path, private from pics WHERE user_id=%s", queried_user_id)
        else:
            images = db.query("SELECT * from pics WHERE user_id=%s", queried_user_id)
        return json.dumps(images)

class ListFilesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        queried_user_id = self.get_argument('userid', None)
        if not queried_user_id:
            raise tornado.web.HTTPError(401)

        userid = self.get_current_user()

        images = FileHelpers.get_images(userid, queried_user_id)

        self.write(images)

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
        (r"/user", UserHandler),
        (r"/images", ImageHandler),
        (r"/comments", CommentHandler),
        (r"/listfiles", ListFilesHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": app_dir + "/public/js/"}),
    ], cookie_secret=secure_cookie_key,
    login_url = "/login")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
