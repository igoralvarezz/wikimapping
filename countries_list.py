import sqlite3
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

# Ignore SSL certificate errors when connecting
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

page_url = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'

# Connect to the SQLite database file and create a cursor
database = sqlite3.connect('country_list.sqlite')
db_cursor = database.cursor()

# creates the database schema to store the countries list
db_cursor.executescript(
''' DROP TABLE IF EXISTS Country;

CREATE TABLE Country(
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    url     TEXT UNIQUE)
'''
)

# connect to wikipedia and download the HTML
html = urllib.request.urlopen(page_url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
content = soup.find_all(id='content')[0]

# grab countries table data
table = content.select('h2 > span#List_of_states')[0].parent.next_sibling.next_sibling
rows = table.find_all('span', {'class': 'flagicon'})

country_list = []
country_count = 0

for country in rows:
    if country != None:
        atag = country.next_sibling
        try:
            country_name = atag.contents[0]
            country_link = atag['href']

            # insert country and URL into the database
            db_cursor.execute(
            '''INSERT OR IGNORE INTO Country (name, url) VALUES (?,?)''',
            (country_name, country_link)
            )
            country_count += 1

        except:
            continue

# save changes to the database 
database.commit()
