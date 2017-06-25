import requests
import json

from django.shortcuts import render
from django.http import HttpResponse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException
)

from .models import Movie 

# Create your views here.
def crawl_movie_details_from_imdb(movie_id):
    """
    Crawl the movie data from the IMDb site using the id.
    """
    # Create the driver object
    browser = webdriver.PhantomJS('./phantomjs')
    # browser = webdriver.Chrome()

    # Request for the IMDB homepage.
    browser.get('http://imdb.com/title/' + movie_id)

    # Get the name of the movie 
    try:
        name = browser.find_element_by_xpath('//h1[@itemprop="name"]').text
    except NoSuchElementException:
        name = ''

    # Get the duration of the movie 
    try:
        duration = browser.find_element_by_xpath('//time[@itemprop="duration"]').text
    except NoSuchElementException:
        duration = ''

    # Get the genres of the movie 
    try:
        movie_genres = browser.find_elements_by_xpath('//span[@itemprop="genre"]')
        genres = ','.join([genre.text for genre in movie_genres])
    except NoSuchElementException:
        genres = ''

    # Get the IMDb rating of the movie 
    try:
        rating = browser.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
    except NoSuchElementException:
        rating = ''

    # Get the description of the movie 
    try:
        description = browser.find_element_by_xpath('//div[@itemprop="description"]').text
    except NoSuchElementException:
        description= ''

    # Get the stars of the movie 
    try:
        movie_stars = browser.find_elements_by_xpath('//span[@itemprop="actors"]')
        stars = ''.join([star.text for star in movie_stars])
    except NoSuchElementException:
        stars = ''

    # Get the year of the movie
    try:
        year = browser.find_element_by_xpath('//span[@id="titleYear"]/a').text
    except NoSuchElementException:
        year = ''

    # Get the director of the movie
    try:
        director = browser.find_element_by_xpath('//span[@itemprop="director"]/a').text
    except NoSuchElementException:
        director = ''

    # Get the writer of the movie
    try:
        writer = browser.find_element_by_xpath('//span[@itemprop="creator"]/a').text
    except NoSuchElementException:
        writer = ''

    return {
        'data': {
            'movie_id': movie_id,
            'name': name,
            'year': year,
            'duration': duration,
            'rating': rating,
            'writer': writer,
            'description': description,
            'stars': stars,
            'genre': genres,
            'director': director
        }
    }

def get_movie(request, movie_id):
    """
    Retrieve the movie having the given id from the local database.
    If not present in the local database, retrieve it from the IMDb database.
    """
    # Search for the movie in the local database
    #
    try:
        movie = Movie.objects.get(movie_id=movie_id)

        # Get the details about the movie
        response = movie.get_details()
    except Movie.DoesNotExist:
        # Get the movie details from IMDb site
        response = crawl_movie_details_from_imdb(movie_id)

        # Insert the movie details into the database
        Movie.add(response)

    return HttpResponse(json.dumps(response))

def index(request):
    pass

def search(request):
    """
    Get the request, extract the search string, search the IMDb database 
    either via api or web crawling and return the results.
    """
    # Get the method to be used for searching.
    method = request.GET.get('method')

    # Get the search string parameter from the request query strings.
    search_string = request.GET.get('search_string')
    print(search_string)

    results = []

    # Perform search only if length of string is greater than zero.
    if len(search_string):
        # Search the IMdb database for the given search string
        if method == 'api':
            results = search_movies_via_api(search_string)
        elif method == 'wc':
            results = search_movies_by_WC(search_string)

    return HttpResponse(json.dumps({
        'data': results
    }))


def search_movies_by_WC(search_string):
    """
    Search for the movie in the IMDb Database by Web Crawling.
    """
    # Create the driver object
    browser = webdriver.PhantomJS('./phantomjs')
    # browser = webdriver.Chrome()

    # Request for the IMDB homepage.
    browser.get('http://imdb.com')

    try:
        # Get the search bar element
        navbar_query_elem = browser.find_element_by_id('navbar-query')

        # Input the search string into the search bar
        navbar_query_elem.send_keys(search_string)

        # Wait until the search result is loaded into the Source
        wait(browser, 60).until(lambda x: len(browser.find_elements_by_xpath('//div[@id="navbar-suggestionsearch"]/a')))

        # browser.implicitly_wait(30)
        # links = [link.get_attribute('href') 
        
        # Get the list of search result elements
        navbar_suggestionsearch_elements = browser.find_elements_by_xpath('//div[@id="navbar-suggestionsearch"]/a')

        results = []

        # Iterate through the list and extract the necessary details 
        for link in navbar_suggestionsearch_elements[:-1]:
            href = link.get_attribute('href')
            values = link.text.split('\n') # find_element_by_xpath('//div[@id="navbar-suggestionsearch"]/a[' + str(i) + ']/div/span[1]').text
            print(values)

            # Filter only the movies and Tv Series
            splitted_url = href.split('/')
            print(splitted_url)
            if 'title' in splitted_url:
                movie_id = splitted_url[splitted_url.index('title') + 1]

                results.append({
                    'id': movie_id,
                    'l': values[0],
                    'detail': values[1]
                })
    except (NoSuchElementException, StaleElementReferenceException) as e:
        pass

    return results 

def search_movies_via_api(search_string):
    """
    Search for the movie in the IMDb Database by Web Crawling.
    """
    # Make the search string to lowercase
    search_string = search_string.lower()

    # Send the request to the api.
    URL = 'https://v2.sg.media-imdb.com/suggests/' + search_string[0] + '/' +\
            search_string + '.json'

    # Get the json response
    resp = requests.get(URL)

    # Response data.  
    # Response data is in jsonp format
    resp_data = resp.text

    # Format the string from jsonp to json format.
    # Returned data is of format, imdb${str: search_string}({dict: response_data})
    str_data = resp_data[(6 + len(search_string)):].strip(")")

    # Convert the string to json 
    json_data = json.loads(str_data)

    # Retrieve the result if any result is returned else return empty list
    data = json_data['d'] if 'd' in json_data else [] 

    # Filter only the movies
    results = [item for item in data if 'q' in item]

    return results
