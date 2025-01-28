from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import requests
import time


link = 'https://www.billboard.com/charts/hot-100/'

# Gets the information from the website

hot100_req = requests.get(link)

# Injests the html into a BeautifulSoup object

hot100_soup = BeautifulSoup(hot100_req.content)

# Selects the song titles from the website

hot100_songs = hot100_soup.select(
  ".o-chart-results-list-row-container .o-chart-results-list__item #title-of-a-story"
)

len(hot100_songs)

# Creates a range object to iterate over

song_range = range(0, len(hot100_songs))

# Gets the text from the song titles. 
# This is a pain, but you will have to 
# do this a lot with BeautifulSoup.
# Easy enough with list comprehension.

hot100_songs = [hot100_songs[x].text for x in song_range]

# List comprehension is a bit more readable than a for loop
# and works like this: [expression for item in iterable]

# Just using some list comprehension to clean up the text

hot100_songs = [re.sub('\t|\n', '', hot100_songs[x]) for x in song_range]

# Now I can put those into a DataFrame

pd.DataFrame({'song': hot100_songs})

# FOR NEXT TIME!

execution_link = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'

exec_req = requests.get(execution_link)

exec_soup = BeautifulSoup(exec_req.content)

statement_links = exec_soup.select('a[href*="last"]')

statement_range = range(0, len(statement_links))

statement_links = ["https://www.tdcj.texas.gov/death_row/" + statement_links[x].get('href') for x in statement_range]

link = statement_links[0]

statements = []

for link in statement_links:
  time.sleep(np.random.uniform(0,.5,1)[0])

  statement_req = requests.get(url=link)

  statement_soup = BeautifulSoup(statement_req.content)
  
  last_statement = statement_soup.select('p.bold:nth-last-of-type(3) ~ p')
  
  last_statement = [last_statement[x].text for x in range(0, len(last_statement))]
  
  last_statement = "".join(last_statement)
  
  statements.append(last_statement)
  

