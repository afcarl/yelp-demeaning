import json
import pandas as pd
import yelp
import requests
import parsehoods
# get neighborhoods

def find_place_in_hood(hood,place):
	hood = hood.replace(' ','+')
	place = place.replace(' ','+')
	yelpie = yelp.yelp_api()
	s_url = yelpie.request_url('http://api.yelp.com/v2/search?term=' + place + '&location=' + hood)
	req = requests.get(s_url)
	if req.status_code == 200:
		json_req = req.json()
		if 'total' in json_req:
			if json_req['total'] > 0:
				businesses = json_req['businesses']
				ids, ratings = [],[]
				for business in businesses:
						if business['name'].lower().replace(' ','').find(place.replace('+','').lower()) > -1:
							ids.append(business['id'])
							ratings.append(business['rating'])
				return [ids,ratings]
		else:
			return None
	else:
		return None

	

def get_ratings_in_city(place,city,hoods):

	hoods = hoods.loc[hoods.city == city,'hood']
	ids,ratings = [],[]
	for hood in hoods:
		results = find_place_in_hood(hood+' ' + city,place)
		if results is not None:
			hood_ids,hood_ratings = results
			ids.append(hood_ids)
			ratings.append(hood_ratings)

	# make a list of lists just a list
	ids = sum(ids,[])
	ratings = sum(ratings,[])

	df = pd.DataFrame({'id':ids,'ratings':ratings})
	df = df.drop_duplicates(cols = 'id')
	return df

hoods_df = parsehoods.getcities()
SF_test = get_ratings_in_city('starbucks','San Francisco',hoods_df)

