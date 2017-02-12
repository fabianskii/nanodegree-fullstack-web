import jinja2
import webapp2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class BlogEntry(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
	def render_front(self, title = "", content = "", created = ""):
		blogEntry = db.GqlQuery("SELECT * FROM BlogEntry ORDER BY  created DESC")
		self.render("bloglist.html", title = title, content = content, blogEntry = blogEntry)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		content = self.request.get("content")

		if title and content:
			blog_entry = BlogEntry(title = title, content = content)
			blog_entry.put()
		self.write("thanks!")

class CreateArticle(Handler):
	def get(self):
		self.render("createarticle.html")

app = webapp2.WSGIApplication([('/', MainPage),('/createarticle', CreateArticle)

	], debug=True)