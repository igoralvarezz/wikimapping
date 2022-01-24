# wikimapping
Wikimapping is a simple python webscrapping script (using URLlib and BeautifulSoup 4 among other libraries) to get all the countries mentioned in any given Wikipedia article and display them in an HTML page with an interactive svg map (drawn using Topojson and D3.js JavaScript libraries and World Atlas Project's JSON) aside some textual and tabular information. 
Once scrapped, the Python script stores all the article's information locally using an SQLite database to avoid multiple calls to Wikipedia during the building of the page.

This is my capstone project for the [Python For Everybody Specialization](https://www.coursera.org/specializations/python).
