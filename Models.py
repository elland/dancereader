from google.appengine.ext import db
from google.appengine.api import users

class values(object):
	posts = db.StringProperty()
	feeds = db.StringProperty()
	feed_title = db.StringProperty()
	feedLink = db.StringProperty()
	values = {
			'posts': posts, 'feeds': feeds,
			'feed_title': feed_title, 'feedLink': feedLink}
	
class Feed(db.Model):
	owner = db.UserProperty()
	url = db.StringProperty(required=True)
	link = db.StringProperty()
	title = db.StringProperty()
	
	
class Post(db.Model):
	owner = db.UserProperty()
	url = db.StringProperty(required=True)
	title = db.StringProperty()
	author = db.StringProperty()
	summary = db.TextProperty()
	category = db.StringProperty()
	modified = db.StringProperty()
	feed = db.ReferenceProperty(Feed, collection_name='feed')


