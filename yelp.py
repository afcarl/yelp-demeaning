import oauth2
# get neighborhoods

class yelp_api(object):

	def __init__(self, config_file = 'yelp.config'):

		credentials = json.load(open(config_file))
		yelp_consumer_key = credentials['consumer_key']
		yelp_consumer_secret = credentials['consumer_secret']
		yelp_token = credentials['token']
		yelp_token_secret = credentials['token_secret']

		self.auth_dict = {
			'consumer_key': yelp_consumer_key,
			'consumer_secret': yelp_consumer_secret,
			'token': yelp_token,
			'token_secret': yelp_token_secret
			}



	def self.request_url(self,url):
		consumer = oauth2.Consumer(self.auth['consumer_key'], self.auth['consumer_secret'])
		oauth_request = oauth2.Request('GET', url, {})
		oauth_request.update(
		    {
		        'oauth_nonce': oauth2.generate_nonce(),
		        'oauth_timestamp': oauth2.generate_timestamp(),
		        'oauth_token': self.auth['token'],
		        'oauth_consumer_key': self.auth['consumer_key']
		    }
		)
		# print auth_token
		token = oauth2.Token(key=self.auth['token'], secret = self.auth['token_secret'])
		oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
		signed_url = oauth_request.to_url()

		return signed_url