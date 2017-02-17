import os
import hashlib
import hmac
import re


import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 
				'templates')
jinja_env = jinja2.Environment(
			loader = jinja2.FileSystemLoader(template_dir),
            autoescape = True)

secret = 'shouldbearandomthing'

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class BlogHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		return render_str(template, **params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class BlogFront(BlogHandler):
	def get(self):
		self.render('blogfront.html')

### implementation of posts goes here
class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("post.html", p = self)
		
class PostPage(BlogHandler):
	def get(self, post_id):
		key = db.Key.from_path('Post', int(post_id))
		post = db.get(key)

		if not post:
			self.error(404)
			return

		self.render("permalink.html", post = post)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

### registration
class Signup(BlogHandler):
	def get(self):
		self.render("signup-form.html")

	def post(self):
		have_error = False
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')

		params = dict(username = self.username)

		if not valid_username(self.username):
			params['error_username'] = "That's not a valid username"
			have_error = True
		if not valid_password(self.password):
			params['error_password'] = "That was not a valid password"
			have_error = True
		elif self.password != self.verify:
			params['error_verify'] = "Your passwords did not match!"
			have_error = True
		if have_error:
			self.render('signup-form.html', **params)
		else:
			self.done
	def done(self, *a, **kw):
		raise NotImplementedError

class Register(Signup):
	def done(self):
		u = User.by_name(self.username)
		if u:
			msg = 'That user already exists.'
			self.render('signup-form.html', error_username = msg)
		else:
			u = User.register(self.username, self.password)
			u.put()
			self.login(u)
			self.redirect('/blog')

### Login
class Login(BlogHandler):
	def get(Self):
		self.render('login-form.html')

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		u = User.login(username, password)
		if u:
			self.login(u)
			self.redirect('/blog')
		else:
			msg = 'Invalid login'
			self.render('login-form.htmnl', error = msg)


app = webapp2.WSGIApplication([('/', BlogFront),
								('/blog', BlogFront),
								('/login', Login),
								('/signup', Register)
								])
