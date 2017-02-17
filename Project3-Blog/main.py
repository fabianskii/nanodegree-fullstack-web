import jinja2
import webapp2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

secret = ''

def makeSecureVal(val):
	return '%s|%s' % (val, hmac.new(secret,val).hexdigest())

def checkSecureVal(secureVal):
	val = secureVal.split('|')[0]
	if secureVal == makeSecureVal(val):
		return val

class BlogMainHandler(webapp2.RequestHandler):
	def render_front(self, title = "", content = "", created = ""):
		blogPosts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
		self.render("bloglistposts.html", title = title, content = content, blogPosts = blogPosts)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def readSecureCookie(self,name):
		cookieVal = self.request.cookies.get(name)
		return cookieVal and checkSecureVal(cookieVal)

	def setSecureCookie(self, name, val):
		cookieVal = makeSecureVal(val)
		self.response.headers.addHeader(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookieVal))

	def login(self, user):
		self.setSecureCookie('userId',str(user.key()))	

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.readSecureCookie('user_id')
		self.user = uid and User.byId(int(uid))

class MainPage(BlogMainHandler):
	def get(self):
		str("hi")
		self.render_front()

	def post(self):
		username = self.request.get("username")
		pwd = self.request.get("pwd")
		user = User.login(username, pwd)
		if user:
			self.login(u)
			self.redirect('/blognewpost')
		else:
			self.render('/blog')

def makeSalt(length = 5):
	return ''.join(random.choice(letters) for x in xrange(length))

def makePwHash(name, pw, salt = None):
	if not salt:
		salt = makeSalt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (salt,h)

def validPw(name, password, h):
	salt = h.split('|')[0]
	return h == makePwHash(name, password, salt)

def usersKey(group = 'default'):
	return db.Key.from_path('users', group)

class User(db.Model):
	username = db.StringProperty(required = True)
	pwdHash = db.StringProperty(required = True)

	@classmethod
	def byId(cls, uid):
		return User.getById(uid)

	@classmethod
	def byName(cls, username):
		user = user.all().filter('name =',name).get()
		return user

	@classmethod
	def register(cls, username, pwd):
		pwHash = makePwHash(username, pwd)
		return User(username = username,
					pwHash = pwHash)

	@classmethod
	def login(cls, name, pwd):
		user = cls.byName(name)
		if user and validPw(username, pwd, user.pwHash):
			return user

class BlogPost(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

class BlogSinglePost(BlogMainHandler):
	def get(self, post_id):
		key = db.Key.from_path('BlogEntry', int(post_id))
		post = db.get(key)
		blogPost = []
		blogPost.append(post)
		self.render("bloglistposts.html", blogEntry = blogPost)

class BlogNewPost(BlogMainHandler):
	def get(self):
		if self.user:
			self.render("blognewpost.html")
		else:
			self.redirect("/blog")

	def post(self):
		title = self.request.get("title")
		content = self.request.get("content")

		if title and content:
			blogPost = blogPost(title = title, content = content)
			blogPost.put()
			self.redirect('/blog/%s' % str(blogPost.key().id()))

class RegisterForm(BlogMainHandler):
	def get(self):
		self.render("register.html")

	def post(self):
		self.username = self.request.get("username")
		self.password = self.request.get("pwd")

		params = dict(username = self.username)

		self.done()

	def done(self, *a, **kw):
		raise NotImplementedError

class Register(RegisterForm):
	def done(self):
		user = User.byName(self.username)
		if user:
			msg = 'That user already exists.'
			self.render('register.html')
		else:
			user = User.register(self.username, self.pwd)
			user.put()
			self.login(user)
			self.redirect('/blognewpost')

class Login(BlogMainHandler):
	def post(self):
		username = self.request.get('username')
		pwd = self.request.get('pwd')

		user = User.login(username, pwd)
		if user:
			self.login(u)
			self.redirect('/blognewpost')
		else:
			msg = 'Invalid login'
			self.render('index.html')

class Logout(BlogMainHandler):
	def get(self):
		self.logout()
		self.redirect('/blog')

app = webapp2.WSGIApplication([('/blog', MainPage),
								('/', MainPage),
								('/blognewpost', BlogNewPost),
								('/blog/([0-9]+)', BlogSinglePost),
								('/blog/register', RegisterForm)
	], debug=True)