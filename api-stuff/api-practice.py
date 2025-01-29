import pandas as pd
import requests

# Pull link and headers from inspect on website
link = 'https://www.swimcloud.com/api/splashes/top_times/?dont_group=false&event=1200&eventcourse=Y&gender=M&page=1&region=countryorganisation_usacollege&season_id=28'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language":  "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "x-csrftoken": "8d9KfH8bPeHBNyb61fafDlrLrXXxHDf3",
    "Referer": "https://www.swimcloud.com/times/?dont_group=false&event=1200&gender=M&page=1&region=countryorganisation_usacollege&season_id=28&team_id&year"
}

# Make request to API and convert to JSON
request = requests.get(link, headers=headers)
swim_data = request.json()

# Inspect results
swim_data.keys()
swim_data['results'][0]
swim_data.get('results')[0].get('split').get('splittimes')

# Normalize data and pull out name, split, and overall times
results = pd.json_normalize(swim_data['results'])
results[['display_name', 'split.splittimes', 'eventtime']]

# If I want to iterate through multiple pages of the API, I can use a for loop:
top_300 = pd.DataFrame()
for i in range(1, 7):
	link=f'https://www.swimcloud.com/api/splashes/top_times/?dont_group=false&event=1200&eventcourse=Y&gender=M&page={i}&region=countryorganisation_usacollege&season_id=28'
	request=requests.get(link, headers=headers)
	swim_data=request.json()
	results=pd.json_normalize(swim_data['results'])
	top_300=pd.concat([top_300, results[['display_name', 'split.splittimes', 'eventtime', 'dateofswim']]], ignore_index=True)

print(top_300)

# Try new data
link = 'https://sumersports.com/wp-content/uploads/data/def_pers_tendency.json'