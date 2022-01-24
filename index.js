const svg = d3.select('svg')
const projection = d3.geoNaturalEarth1();
const pathGenerator = d3.geoPath().projection(projection);
const g = svg.append('g')

//
let jsonData = {};
let jsonKeys = [];

// Main Function
let main = {};
main.run = (url) => {
  let req = new XMLHttpRequest();
  req.open('GET', url);

  req.onload = ()=>{
    if (req.status == 200) {
      data = req.response
      jsonData = JSON.parse(data);

      utils.buildMap(jsonData)

    }
    else {
      console.log('error with', req.status);
    }

    req.onerror = (err) =>{
      console.log('Network Error with', url,':', err)
    }
  }
  req.send()
};

// Utils Functions
let utils = {};
utils.buildMap = (jsonData) => {
  // console.log(jsonData['Germany']);
  let mapwidth = 950, mapheight = 600;
  svg.call(d3.zoom()
      .scaleExtent([1, 7])
      .translateExtent([[0, 0], [mapwidth, mapheight]])
      .on("zoom", zoomed));

  function zoomed({transform}) {
    g.attr("transform", transform);
  }

  d3.json('./assets/countries-50m.json').then(data => {
    const countries = topojson.feature(data, data.objects.countries);
    jsonKeys = Object.keys(jsonData.countries);
    typeof(g.selectAll('path'));

    g.selectAll('path')
    .data(countries.features)
      .enter().append('path')
        .attr('d', pathGenerator)
        .attr('class', d => {
          let curr_country = d.properties.name;
          check = utils.checkCountry(curr_country);
          if (check > -1){
            return 'country selected'
          }
          else {
            return 'country'
          }
        })
        .attr('country', d => {
          let curr_country = d.properties.name;
          check = utils.checkCountry(curr_country);
          if (check > -1){
            return curr_country
          }
          else {
            return ''
          }
        })
      .append('title')
        .text(d => {
          let curr_country = d.properties.name;
          let titleDesc;
          check = utils.checkCountry(curr_country);
          if (check < 0){
            return d.properties.name
          }

          else if (jsonData.countries[d.properties.name] == '1') {
            titleDesc = new String(d.properties.name + '\nMentioned ' + jsonData.countries[d.properties.name]+ ' time in the article.');
          } else {
            titleDesc = new String(d.properties.name + '\nMentioned ' + jsonData.countries[d.properties.name]+ ' times in the article.');
          }
          return titleDesc
        });
  });
  utils.buildPage(jsonData);
};
utils.checkCountry = (country) => {
  return jsonKeys.indexOf(country)
};
utils.buildPage = (jsonData) => {
  let articleTitle = document.querySelector('#article-title'),
      articleDate = document.querySelector('#article-date'),
      articleDescription = document.querySelector('#article-description'),
      articleTotalCountries = document.querySelector('#number-country'),
      articleTotalMentions = document.querySelector('#number-mention'),
      articleMostMentions = document.querySelector('#most-mentions'),
      articleMostMentioned = document.querySelector('#most-mentioned'),
      articlePlaceholderMostMentioned = document.querySelector('#placeholder-most-mentioned'),
      articleDescTitle = document.querySelector('#desc-title')

      dbTitle = jsonData.article.title,
      dbDate = jsonData.article.date,
      dbUrl =  jsonData.article.url,
      dbDescription = jsonData.article.description,
      dbNumCountries = jsonData.article.num_countries,
      dbNumMentions = jsonData.article.num_mentions
      dbMostMentions = jsonData.article.most_mentions,
      dbMostMentioned = jsonData.article.most_mentioned


  articleTitle.text = dbTitle;
  articleTitle.href = dbUrl;
  articleDate.textContent = dbDate;
  articleDescription.textContent = dbDescription;
  articleDescTitle.textContent = dbTitle;
  articleDescTitle.href = dbUrl;
  articleMostMentioned.href = jsonData.countriesUrls[dbMostMentioned]

  // construct the total number of countries mentions phrase
  if (dbNumMentions > 1 && dbNumCountries > 1){
    articleTotalMentions.textContent = 'All the countries together were mentioned ' + dbNumMentions.toString() + ' times total';
  } else if (dbNumMentions == 1 && dbNumCountries == 1) {
    articleTotalMentions.textContent = 'The country was mentioned 1 time only.';
  } else if (dbNumMentions > 1 && dbNumCountries == 1){
    articleTotalMentions.textContent = 'The country was mentioned ' + dbNumMentions.toString() + ' times total';
  }

  // Construct the number of countries mentioned
  if (dbNumCountries > 1) {
    articleTotalCountries.textContent = 'a total of ' + dbNumCountries.toString() + ' countries'
  } else if (dbNumCountries < 1) {
    articleTotalCountries.textContent = 'no country '
  } else {
    articleTotalCountries.textContent = 'only 1 country '
  }

  // construct the most metioned country and mention number phrases
  if (dbMostMentions > 0) {

    articlePlaceholderMostMentioned.textContent = 'The most mentioned country was '
    articleMostMentions.textContent = ' with ' + dbMostMentions + ' mentions total';
    articleMostMentioned.textContent = dbMostMentioned
  }
// table construction
  let dbTable = jsonData.countries,
      articleTable = document.querySelector('#article-results'),
      jsonKeys = Object.keys(jsonData.countries);

  jsonKeys.forEach((country, index) => {
    table_country_name = document.createTextNode(country);
    table_country_mentions = document.createTextNode(dbTable[country]);
    table_country_anchor = document.createElement('a');
    table_country_anchor.href = jsonData.countriesUrls[country];
    table_country_anchor.target = '_blank';
    table_country_anchor.appendChild(table_country_name);

    tr = articleTable.insertRow(-1);
    tr.insertCell(0).appendChild(table_country_anchor);
    tr.insertCell(1).appendChild(table_country_mentions);
  });
  // Sort the table by default alphabetically by name of the country
  utils.sortTable(0)

};
utils.sortTable = (n) => {
  var table;
  table = document.querySelector("table");
  var rows, i, x, y, count = 0;
  var switching = true;

  // Order is set as ascending
  var direction = "ascending";

  // Run loop until no switching is needed
  while (switching) {
      switching = false;
      var rows = table.rows;

      //Loop to go through all rows
      for (i = 1; i < (rows.length - 1); i++) {
          var Switch = false;

          // Fetch 2 elements that need to be compared
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];

          // Check the direction of order
          if (direction == "ascending") {

              // Check if 2 rows need to be switched
              if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase())
                  {
                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
              }
          } else if (direction == "descending") {

              // Check direction
              if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase())
                  {
                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
              }
          }
      }
      if (Switch) {
          // Function to switch rows and mark switch as completed
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;

          // Increase count for each switch
          count++;
      } else {
          // Run while loop again for descending order
          if (count == 0 && direction == "ascending") {
              direction = "descending";
              switching = true;
          }
      }
  }
}
main.run('./countries_data.json')
