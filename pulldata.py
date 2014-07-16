import json
import oauth2
import requests

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
	
r = request_url('http://api.yelp.com/v2/search?term=food&location=San+Francisco',auth_dict)
