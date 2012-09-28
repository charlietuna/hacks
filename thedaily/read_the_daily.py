#!/usr/bin/python
# coding=utf8

import urllib
import json
import re
import httplib2
import sqlite3

search_point = "http://search.twitter.com/search.json"

re_url = re.compile(ur"(?P<url>https?://[^\s\”]+/[^\s\.\&@\”\)\,]+)")
#re_url = re.compile("(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,?]))")

def find_url(text):
	m = re_url.search(text)
	if m:
		return m.group("url")
	return None

def expand_url(url):
	h = httplib2.Http()
	try:
		resp, content = h.request(url)
		return resp["content-location"], content
	except:
		print url
		print resp.status
		print resp
		print resp["content-location"]
		raise

def search_twitter(term):
	url = search_point + "?" + urllib.urlencode(dict(q=term, rpp=100))
	data = urllib.urlopen(url).read()
	obj = json.loads(data)

	for result in obj["results"]:
		yield result
		
	count = 0

	while obj["next_page"]:
		url = search_point + obj["next_page"]
		data = urllib.urlopen(url).read()
		obj = json.loads(data)
		for result in obj["results"]:
			yield result
#		count += 1
#		if count > 2:
#			break

if __name__ == "__main__":
	conn = sqlite3.connect("thedaily.sqlite")
	cursor = conn.cursor()
	
	cursor.execute("create table if not exists short_urls (shorturl TEXT PRIMARY KEY, url TEXT)")
	cursor.execute("create table if not exists stories (url TEXT PRIMARY KEY, content TEXT)")

	def do_story(url):
		pass
#		print url

	def sql_shorturl(shorturl):
		cursor.execute("select url from short_urls where shorturl=?", (shorturl,))
		value = cursor.fetchone()
		if value is None:
			return None
		return value[0]

	def sql_story(url):
		cursor.execute("select content from stories where url=?", (url,))
		value = cursor.fetchone()
		if value is None:
			return None
		return value[0]
		
	def daily_url(url):
		return url.startswith("http://thedaily.com/page") or url.startswith("http://www.thedaily.com/page")

	def canonify_daily_url(url):
		if url.startswith("http://thedaily.com/page"):
			url = url.replace("http://thedaily.com/page", "http://www.thedaily.com/page")
		m = re.match(r"^([^\?]+)", url)
		if m:
			url = m.group(1)
		return url

	for result in search_twitter("thedaily.com/page"):
		orig_url = find_url(result["text"])
		url = ""
		
		if not orig_url:
			continue

		if daily_url(orig_url):
			url = orig_url
		else:
			url = sql_shorturl(orig_url)
			if not url:
				print "new short url: ", orig_url
				try:
					url, content = expand_url(orig_url)
				except:
					print "error expanding: ", url, orig_url
					continue
				
				cursor.execute("insert into short_urls values(?, ?)", (orig_url, url))
				conn.commit()

		if daily_url(url):
			url = canonify_daily_url(url)
			print url
			if sql_story(url) is None:
				print "new story: " + url
				try:
					url, content = expand_url(url)
				except:
					print "error fetching: ", url
					continue
				cursor.execute("insert into stories values(?, ?)", (url, content.decode("utf-8")))
				conn.commit()

		do_story(url)

	conn.close()
