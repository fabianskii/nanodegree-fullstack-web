import jinja2
import webapp2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'static/templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		css_url = url_for('static', filename='css/style.css')
		self.render("index.html", cssurl = cssurl)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)