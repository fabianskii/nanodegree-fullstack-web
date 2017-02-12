import jinja2
import webapp2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	def render_front(self, title = "", content = "", created = ""):
		blogEntry = db.GqlQuery("SELECT * FROM BlogEntry ORDER BY created DESC LIMIT 10")
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

class BlogEntry(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class BlogEntryHandler(Handler):
	def get(self, post_id):
		key = db.Key.from_path('BlogEntry', int(post_id))
		post = db.get(key)
		blogEntry = []
		blogEntry.append(post)
		self.render("bloglist.html", blogEntry = blogEntry)

class CreateArticle(Handler):
	def get(self):
		self.render("createarticle.html")

	def post(self):
		title = self.request.get("title")
		content = self.request.get("content")

		if title and content:
			blog_entry = BlogEntry(title = title, content = content)
			blog_entry.put()
			self.redirect('/blog/%s' % str(blog_entry.key().id()))

app = webapp2.WSGIApplication([('/blog', MainPage),
								('/createarticle', CreateArticle),
								('/blog/([0-9]+)', BlogEntryHandler)

	], debug=True)