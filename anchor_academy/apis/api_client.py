import requests
import logging

class ApiClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
    
    def fetch_sessions(self, start_date=None, end_date=None):
        #payload parameters will be the key-value pairs from the actual PlayerMaker payload. 
        payload = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        #send an HTTP GET request to the Playermaker API
        #create a requests object called "req". We can now get all the information we need from this object
        req = requests.get(
            f"{self.base_url}/sessions",
            headers={"Authorization": f"Bearer{self.api_key}"},
            params= payload
        )
        logging.info(f"api request url:{req.url}")

        #Generate a JSON response from the request
        
        req.raise_for_status()
        req.json()

        