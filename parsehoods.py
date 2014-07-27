import re
import pandas as pd

def getcities(input_file='neigborhoods.html'):

	def city_generator(text):
		areas = [] # list of dicts with key country, city, hood
		status = 'start' # start looking for a country
		hood_re = re.compile(r'<li>(.+)</li>')
		city_state_re = re.compile(r'<li>([A-z\s\.\-]*),(.*)')
		aus_city_state_re = re.compile(r'<li>([A-z0-9]*)\s(.+)')
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
					status = 'city'
				continue
			if status == 'city':
				city_idx = line.find('<li>')
				if city_idx > -1:
					if country == 'Australia':
						city_match = aus_city_state_re.search(line)
						if city_match is not None:
							city,state = city_match.group(1),city_match.group(2).strip()
							status = 'hood'
							continue
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
						else:
							status = 'hood'
							
						continue
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


	with open(input_file) as f:
		hoods_html = f.read()

	hoods_text = [ line.strip() for line in re.split(r'[\n]',hoods_html) if line]

	df = pd.DataFrame(city_generator(hoods_text))

	return df