#!/usr/bin/env python

import Engine
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from Models import Feed, Post, values

from urllib2 import urlopen as open
import feedparser

class MainPage(webapp.RequestHandler): #handles the / page
	def get(self):  #the page itself is generated here
		user = users.get_current_user()
		if user:
			values.values['user'] = user.nickname()
		 	Engine.getFeeds(user)
			values.values['feedLink'] = '/'
			self.response.out.write(template.render(
								'./Templates/main.html', values.values))
			
 		else:
			self.redirect('/login')

	def post(self):	#this will handle the Add Feed feature
		user = users.get_current_user()
		url = self.request.get('url')
		if not url:
			self.redirect('/')
		else:
			feed = Feed(url=url, owner=user)
			feed = Engine.makeFeed(feed)
			if feed != 0:
				feed = Engine.parseFeed(feed, user)
				feeds = Feed.gql("WHERE ownser = :owner", owner = user)
				self.redirect('/')			
			else:
				self.redirect('/')


class showFeed(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		Engine.getFeeds(user)
		key = self.request.get('feed')
		user = users.get_current_user()
		feeds = Feed.gql('WHERE owner = :owner', owner=user)
		for feed in feeds:
			key2 = str(feed.key())
			key = str(key)
			values.values['feed_title'] = feed.title
			values.values['feedLink'] = feed.link
			if key2 == key:
				posts =Post.gql("WHERE owner = :owner AND feed = :feed",
								owner = user, feed = feed)
				posts = posts.fetch(10)
				values.values['posts'] = posts
				self.response.out.write(template.render(
								'./Templates/main.html', values.values))


class DeleteFeed(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		ftd = self.request.get('feedtodelete')
		if ftd == '/':
			self.redirect('/')
		else:
			feeds = Feed.gql(
				"WHERE owner = :owner AND link = :link",
				owner=user, link = ftd)
			feeds = feeds.fetch(1)
			for feed in feeds:
				posts = Post.gql("WHERE owner = :owner AND feed = :feed",
							owner = user, feed = feed)
			posts = posts.fetch(1000)
			db.delete(posts)
			db.delete(feed)
			self.redirect('/')
		

		
class Login(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			self.redirect('/')
	
class Logout(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect(users.create_logout_url(self.request.uri))
		else:
			self.redirect('/')


class test(webapp.RequestHandler): # for testing purpose only
	def get(self):
		user = users.get_current_user()
		allfeeds = Feed.gql('WHERE owner = :owner', owner = user)
		allfeeds = allfeeds.fetch(1000)
		x = 0 
		for feed in allfeeds:
		
			post_newest = Post.gql("WHERE owner = :owner AND feed = :feed"
									" ORDER BY date DESC",
									owner = user, feed = feed)
			post_newest = post_newest.fetch(1)
			xml = open(feed.rsslink)
			xml = xml.read()
			k = feedparser.parse(xml)
			xmldate = Engine.parseDate(k.entries[0].date_parsed)
			date = post_newest[0].date
			if xmldate > date:
				
			
			
def main():
	app = webapp.WSGIApplication([
	('/', MainPage),
	('/feed', showFeed),
	('/deleteFeed', DeleteFeed),
	('/login', Login),
	('/logout', Logout),
	('/test', test),
	], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	




if __name__ == "__main__":
	main()