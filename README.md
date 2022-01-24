# wikimapping
Wikimapping is a simple python webscrapping script (using URLlib and BeautifulSoup 4 among other libraries) to get all the countries mentioned in any given Wikipedia article and display them in an HTML page with an interactive svg map (drawn using Topojson and D3.js JavaScript libraries and World Atlas' TopoJSON) aside some textual and tabular information. 
Once scrapped, the Python script stores all the article's information locally using an SQLite database to avoid multiple calls to Wikipedia during the building of the page.

This is my capstone project for the [Python For Everybody Specialization](https://www.coursera.org/specializations/python).

## Basic functionalities:
- Scrap the content of a Wikipedia article (english only for now), using the scrap_page.py script.
- List all the countries mentioned in the article (with or without hyperlinks) and how many times each one was mentioned.
- Get the basic information about the article scrapped (title, short-description, first paragraph, date/time of scrapping, total number of countries mentioned and total number of mentions for each and all countries together).
- Saves the info to an SQLite database and to a Json file.
- Generates a simple HTML/JS page to display the info
- Draws a simple interactive SVG World Map to display the countries and how many time they were mentioned in the article (using Topojson and D3.js).
