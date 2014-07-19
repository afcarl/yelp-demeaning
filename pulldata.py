import json
import oauth2
import requests
import re
import pandas as pd
# get neighborhoods

def city_generator(text):
	areas = [] # list of dicts with key country, city, hood
	status = 'start' # start looking for a country
	hood_re = re.compile('<li>([A-z\s]*)</li>')
	city_state_re = re.compile(r'<li>([A-z\s\.\-]*),(.*)')
	for ii,line in enumerate(text):
		if status == 'start':
			is_start = line.find('hahastartnow')
			if is_start > -1:
				status = 'country'
			continue
		if status == 'country':
			country_idx = line.find('<li>')
			if country_idx > -1:
				country = line[country_idx+4:]
				print country
				status = 'city'
			continue
		if status == 'city':
			city_idx = line.find('<li>')
			if city_idx > -1:
				if country != 'USA':
					city = line[city_idx+4:]
					state = ''
					status = 'hood'
				else:
					city_match = city_state_re.search(line)
					if city_match is not None:
						city,state = city_match.group(1),city_match.group(2).strip()
					if (city == 'New York') & (state == 'NY'):
						status = 'borough'
			if line == '</ul>':
				status = 'country'
			continue
		if status == 'hood':
			hood_match = hood_re.search(line)
			if hood_match is not None:
				hood = hood_match.group(1)
				yield {'country':country, 'city': city, 'state': state, 'hood': hood}
			if line == '</ul>':
				status = 'city'
			continue
		if status == 'borough':
			borough_idx = line.find('<li>')
			if borough_idx > -1:
				borough = line[borough_idx+4:]
				status = 'borough_hood'
			if line == '</ul>':
				status = 'city'
			continue
		if status == 'borough_hood':
			hood_match = hood_re.search(line)
			if hood_match is not None:
				borough_hood = hood_match.group(1)
				yield {'country':country, 'city': city, 'state': state, 'borough': borough,'borough_hood': borough_hood}
			if line == '</ul>':
				status = 'borough'
			continue


with open('neigborhoods.html') as f:
	hoods_html = f.read()

hoods_text = [ line.strip() for line in re.split(r'[\n]',hoods_html) if line]

df = pd.DataFrame(city_generator(hoods_text))

hoods_html = BeautifulSoup(open('neigborhoods.html'))
hood_list = hoods_html.find(id="hood_list")
countries_data = hood_list.find_all('li',recursive=False)
countries = [area.contents[0].replace('\n','').strip() for area in countries_data]

credentials = json.load(open('yelp.config'))
yelp_consumer_key = credentials['consumer_key']
yelp_consumer_secret = credentials['consumer_secret']
yelp_token = credentials['token']
yelp_token_secret = credentials['token_secret']

auth_dict = {
	'consumer_key': yelp_consumer_key,
	'consumer_secret': yelp_consumer_secret,
	'token': yelp_token,
	'token_secret': yelp_token_secret
	}



def request_url(url,auth):
	consumer = oauth2.Consumer(auth['consumer_key'], auth['consumer_secret'])
	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update(
	    {
	        'oauth_nonce': oauth2.generate_nonce(),
	        'oauth_timestamp': oauth2.generate_timestamp(),
	        'oauth_token': auth['token'],
	        'oauth_consumer_key': auth['consumer_key']
	    }
	)
	# print auth_token
	token = oauth2.Token(key=auth['token'], secret = auth['token_secret'])
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
	signed_url = oauth_request.to_url()
	req = requests.get(signed_url)
	return req
	
s_url = request_url('http://api.yelp.com/v2/search?term=food&location=San+Francisco',auth_dict)

req = requests.get(s_url)

json_req = req.json()
