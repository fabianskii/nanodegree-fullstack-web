from flask_assets import Bundle, Environment
from .. import basic-bloc

bundles = {
	'home_css' : Bundle(
		'css/style.css',
		output = 'gen/style.css'		
		)
}

assets = Environment(app)
assets.register(bundles)