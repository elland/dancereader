from google.appengine.ext import db
from Models import Post, Feed, values
from urllib2 import urlopen as open
from BeautifulSoup import BeautifulSoup as soup
from feedparser import parse as feedparse
import re
import datetime

def getFeeds(user):
	feeds = Feed.gql("WHERE owner = :owner", owner=user)
	feeds = feeds.fetch(100)
	values.values['feeds'] = feeds

def checkHTTP(url):
	test = re.search('http://', url)
	if test == None:
		url = 'http://' + url
	return(url)	
	
	
def makeLink(url):
	url = checkHTTP(url)
	test = re.search('http://www.', url)
	if test:
		url = url.strip('http:/www.')
	else:
		test = re.search('http://', url)
		if test:
			url =url.strip('http://')
	return(url)
	
	
def checkRepeated(url):
	feeds  = db.GqlQuery(
		"SELECT * FROM Feed WHERE url = :url", url=url)
	feeds = feeds.fetch(1)
	if feeds:
		return(True)
	else:
		return(False)
		
		
def makeFeed(feed):
	feed.link = makeLink(feed.url)
	feed.url = checkHTTP(feed.url)
	test = checkRepeated(feed.url)
	if test == True:
		return(0)
	return(feed)


def linkTrim(url):
	url = checkHTTP(url)
	test = re.search('http://www.', url)
	if test:
		url = url.strip('http:/www.')
	else:
		test = re.search('http://', url)
		if test:
			url =url.strip('http://')
	test = re.search('/.*?', url)
	if test:
		url = url.split('/')
		url = url[0]
	return(url)
	
	
def parseFeed(feed, user):
	index = open(feed.url) # gets html index
	index = index.read() # continues
	
	soupd = soup(index)  # parse the hml with BeautifulSoup
	
	rsslink = soupd.findAll('link',   #this little mess will get the
				type="application/rss+xml")  #rss link
	if rsslink == '[]':
		rsslink = soupd.findAll('link',
		 		type="application/rdf+xml") # or rdf
	elif rsslink == '[]':
		rsslink = soupd.findAll('link', 
				type="application/atom+xml") # or atom
	rsslink = str(rsslink) 					#and put to a string

	
	#no need to understand this as none will ever comprehend RegExp
	# a hint, it strips the link out of the html tag
	link = re.search('href=".*?"', rsslink)
	if link == 0:
		link = link.group()
		link = re.search('HREF=".*?"', rsslink)
		link = link.strip('HREF=')
		link = str(link)
		link = link.strip('""')
	elif link == 0:
		print 'erro, linha 94 engine.py, link para rss n encontrado!'
	else:
		link = link.group()
		link = str(link)
		link = link.strip('href=')
		link = link.strip('""')
	feed.rsslink = link #we will need to store this, for updates
	# now some more fun, getting the real thing, xml content
	#from the link we have
	xml = open(link)
	xml = xml.read()
	#time to parse it with FeedParser
	k = feedparse(xml)
	feed.title = k.feed.title
	feed.put()
	# now let's parse the posts one-by-one
	for x in range(len(k.entries)): 
		
		p = str(x)
		post = Post(url = k.entries[x].link,
				owner=user)
		#now that the post model is set, let us play!
		#ugly but necessary:
		if k.entries[x].has_key('author') is True:
		          post.author = k.entries[x].author + ' sings '
		else:
		   post.author ='Anonymous'
		if k.entries[x].has_key('category') is True:
			post.category =' on '+ k.entries[x].category
		else:
			post.category = ''
		if k.entries[x].has_key('date_parsed') is True:
			date = parseDate(k.entries[x].date_parsed)
			post.date = date
			
		if k.entries[x].has_key('summary') is True:
			post.summary = k.entries[x].summary
		else:
			post.summary = 'No private dancing, cowboy...'

		if k.entries[x].has_key('title') is True:
			post.title = k.entries[x].title

		if len(post.title) == 0:
			post.title = "Untitled"
		
		post.feed = feed.key()
		post.put()
		
	return(feed)


def parseDate(pdate):
	date = datetime.datetime(
		pdate[0], pdate[1], pdate[2], pdate[3], pdate[4], pdate[5])
	return date
	
	
# now the important part, gettin up to date, dance it!

def update():
	allfeeds = Feed.gql('')
	allposts = Post.gql('')
	
	
	
