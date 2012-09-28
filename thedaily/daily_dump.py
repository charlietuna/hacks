import sqlite3
import BeautifulSoup

if __name__ == "__main__":
	conn = sqlite3.connect("thedaily.sqlite")
	cursor = conn.cursor()

	cursor.execute("select url, content from stories")
	
	for url, content in cursor:
		print url
