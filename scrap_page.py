import sqlite3
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import json
import datetime

# connect to country_list database and create a cursor
country_database = sqlite3.connect('country_list.sqlite')
country_db_cursor = country_database.cursor()

# get the list of countries and save to country_list
country_list = []
country_db_cursor.execute('SELECT name, url  FROM country')

for country in country_db_cursor:
    country_list.append([country[0],country[1]])


# connect to page database file and create a cursor
database = sqlite3.connect('page.sqlite')
db_cursor = database.cursor()

# create the database schema to store the page content
db_cursor.executescript(
''' DROP TABLE IF EXISTS Page;

    CREATE TABLE Page(
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title   TEXT UNIQUE,
        url     TEXT UNIQUE,
        content TEXT UNIQUE,
        links   TEXT,
        refs    TEXT)
'''
)


# Ignore SSL certificate errors when connecting
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

page_url = input('Enter the URL of the Wikipedia page to be scanned: ')

# parse the input URL
try:
    page_url_info = urlparse(page_url)
    # print(page_url)
except:
    print('Error parsing the URL')
    quit()

# Check if it is a page of the english version of Wikipedia
if (page_url_info.scheme == 'http' or page_url_info.scheme == 'https') and (page_url_info.netloc != 'en.wikipedia.org'):
    print('Sorry, for now it works only with english wikipedia pages (https://en.wikipedia.org/**)')
    quit()

# connect to wikipedia and download the HTML
html = urllib.request.urlopen(page_url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
content = soup.find_all(id='content')[0]
page_title = soup.find(id='firstHeading').text
time_now = datetime.datetime.now()

print(time_now)

# find all country links and country names inside the page content
link_list = []
country_ref_count = 0
country_ref_list = []
country_name_count = 0
country_name_list = []

print('Page:', page_title)
print('\n============= LINK RESULTS ================')

for p in content.find_all('p'):
    a = p.find_all('a')
    # grab only the links which have a title attribute (to avoid refference links and such)
    for link in a:
        try:
            link_title = link['title']
            url = link['href']
        except:
            continue

        # check if name of country is present in link title and the url is pointing to a country page in wikipedia
        for country in country_list:
            country_check = "(\\b|\\n)"+country[0]+"(\\b|\\n|\\.|\,)"
            if re.search(country_check, link_title):
                if country[1] == url:
                    country_ref_count += 1
                    country_ref_list.append(link_title)

for item in country_ref_list:
    print(item)

print('============= NAMES RESULTS ================')

for country in country_list:
    for item in content.find_all(string=re.compile('\\b(' + country[0] + ')\\b')):
        # print(item, type(item))
        country_name = re.findall(re.compile('\\b(' + country[0] + ')\\b'), item)
        for occ in country_name:
            country_name_list.append(occ)
            country_name_count += 1


# count the occurrence of countries names and links in the article and how many times each country appeared

country_set = []
for item in country_name_list:
    country_set.append(item)
for item in country_ref_list:
    country_set.append(item)
country_set = set(country_set)
countries_data = {
    'countries': {},
    'countriesUrls':{},
    'article':{}
}
for country in country_set:
    print(country + ':', country_ref_list.count(country) + country_name_list.count(country))

    countries_data['countries'][country] = country_ref_list.count(country) + country_name_list.count(country)



print('=============================')
print('Number of different countries in the article =', len(country_set))
print('Number of country refferences in the article =', country_ref_count + country_name_count)

#check which country appeared the most and how many times
most_mentions = 0
most_mentioned = ''
for country in countries_data['countries']:
    if countries_data['countries'][str(country)] > most_mentions:
        most_mentions = countries_data['countries'][str(country)]
        most_mentioned = country

print('Most Mentioned country was', most_mentioned, 'with', most_mentions, 'mention(s)')

# save info to the database
db_cursor.execute(
'''INSERT INTO Page (title, url, content, links, refs) VALUES (?,?,?,?,?)''',
(page_title, str(page_url), str(content), str(country_ref_list), str(country_name_list))
)

database.commit()

# Remove tags from first paragraph (description)
try:
    first_paragraph = content.find_all(class_='shortdescription')[0].text
except:
    first_paragraph = content.find_all('p')[0]
    for i in range (5):
        if (len(first_paragraph.text) < 5) or ('coordinates' in first_paragraph.text.lower() ):
            first_paragraph = content.find_all('p')[i+1]
        else:
            break

    def remove_tags(paragraph):
        for data in paragraph(['sup', '.reference']):
            # Remove tags
            data.decompose()
        # return data by retrieving the tag content
        text = ' '.join(paragraph.stripped_strings)

        return text
    first_paragraph = remove_tags(first_paragraph)


#save the info to the JSON file to generate visualization
for country in country_list:
    countries_data['countriesUrls'][country[0]] = 'https://en.wikipedia.org/' + country[1]

countries_data['article']['url'] = page_url
countries_data['article']['title'] = page_title
countries_data['article']['date'] = str(time_now.day) + '/' + str(time_now.month) + '/' + str(time_now.year) + '|' + str(time_now.hour) + ':' + str(time_now.minute)
countries_data['article']['description'] = first_paragraph
countries_data['article']['num_countries'] = len(country_set)
countries_data['article']['num_mentions'] = country_ref_count + country_name_count
countries_data['article']['most_mentions'] = most_mentions
countries_data['article']['most_mentioned'] = most_mentioned

with open('countries_data.json', 'w', encoding='utf-8') as f:
    json.dump(countries_data, f, ensure_ascii=False, indent=4)


# print(content.find_all('p')[0])
