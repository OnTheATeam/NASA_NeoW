from astropy.time import Time

from datetime import date
import datetime
import requests

class Asteroids:
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.api_endpoint = 'https://api.nasa.gov/neo/rest/v1/feed'

    def get_asteroids_today(self):
        asteroid_list = []

        today_str = str(date.today())
        params = {'start_date' : today_str,
                'end_date' : today_str,
                'api_key' : self.api_key}
        
        get_request = requests.get(url = self.api_endpoint, params = params)
        json_resp = get_request.json()

        neos = json_resp['near_earth_objects']
    
        # Since we only supplied one date, we only expect one date in response
        date_key = list(neos.keys())[0]

        for neo in neos[date_key]:
            name = neo['name']

            # Let's convert TDB time to UTC time using Astropy
            close_approach_epoch = datetime.datetime.strptime(neo['close_approach_data'][0]['close_approach_date_full'], '%Y-%b-%d %H:%M')
            close_approach_epoch = Time(close_approach_epoch, scale='tdb')
            close_approach_epoch = str(close_approach_epoch.tt)

            miss_miles = neo['close_approach_data'][0]['miss_distance']['miles']
            diameter_miles = neo['estimated_diameter']['miles']['estimated_diameter_max']
            url = neo['nasa_jpl_url']
            asteroid_list.append((name, close_approach_epoch, miss_miles, diameter_miles, url))

        return asteroid_list