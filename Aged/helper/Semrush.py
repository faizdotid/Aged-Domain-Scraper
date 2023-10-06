# helper/Semrush.py

import requests
import json
import sys
import whois
import time

class Semrush:
    USERNAME = 'mozscape-c400337ba7'
    PASSWORD = '272edc64ff57f002b64551e2ea3b5de'
    BASE_URL = 'https://lsapi.seomoz.com/v2/url_metrics'

    def __init__(self, session: requests.Session):
        self.session = session
    
    def get_url_metrics(self, url: str):
        data = {'targets': [url]}
        try:
            response = self.session.post(self.BASE_URL, data=json.dumps(data), auth=(self.USERNAME, self.PASSWORD), timeout=70)
            if response.status_code == 200:
                return self.parse_response_content(response.text)
            elif "limit reached." in response.text:
                print('Limit reached for {} account'.format(self.USERNAME))
                sys.exit()
            elif "Too Many Requests" in response.text:
                print('Too Many Requests wait for 5 seconds')
                time.sleep(5)
                self.get_url_metrics(url)
            else:
                print('Error: {}'.format(response.text))
        except KeyboardInterrupt:
            user_choice = input('Do you want to exit? (y/n): ')
            if user_choice.lower() == 'y':
                sys.exit()
            else:
                self.get_url_metrics(url)
        except Exception as e:
            print(e)
            return None
    
    def check_domain_availability(self, domain: str):
        try:
            whois.whois(domain)
            return False
        except Exception:
            return True

    def parse_response_content(self, content: str):
        json_content = json.loads(content)['results'][0]
        metrics = {
            'Domain': 'http://' + json_content['root_domain'],
            'DA': json_content['domain_authority'],
            'PA': json_content['page_authority'],
            'SS': json_content['spam_score'],
        }
        if self.check_domain_availability(json_content['root_domain']):
            metrics['Status'] = 'Available'
        else:
            metrics['Status'] = 'Not Available'
        return metrics