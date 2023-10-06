# helper/ExpiredDomains.py

import requests
from bs4 import BeautifulSoup
import sys

class ExpiredDomainExtractor:
    BASE_URL = 'https://member.expireddomains.net'

    def __init__(self, session: requests.Session):
        self.session = session
        self.expired_domains = []
    
    def get_expired_domains(self):
        return self.expired_domains
    
    def set_user_credentials(self, username, password):
        self.username = username
        self.password = password

    def authenticate_user(self):
        login_data = {
            'login': self.username,
            'password': self.password,
            'redirect_to_url': '/home'
        }
        
        try:
            login_response = self.session.post(f'{self.BASE_URL}/login/', data=login_data)
            
            if 'Your account was disabled' in login_response.text:
                print('Your account was disabled')
                sys.exit()
                
            elif self.username in login_response.text:
                print('Login Success')
                
            else:
                print('Login Failed')
                sys.exit()
                
        except Exception as e:
            print(e)
            sys.exit()

    def extract_domain_names(self, html_content, page_number):
        soup = BeautifulSoup(html_content, 'html.parser')
        domain_elements = soup.find_all('a', class_='namelinks')
        
        print(f'Found {len(domain_elements)} domains in page {page_number + 1}')
        
        return [domain.get('title') for domain in domain_elements]

    def fetch_expired_domains(self, tld='combinedexpired', start_page=1, end_page=25):
        for page_number in range(start_page - 1, end_page):
            url = f'{self.BASE_URL}/domains/{tld}/?start={page_number * 25}'
            try:
                page_response = self.session.get(url)
                
                if 'You have reached the maximum [pages] limit' in page_response.text:
                    print('You have reached the maximum [pages] limit')
                    break
                    
                else:
                    domain_names = self.extract_domain_names(page_response.text, page_number)
                    self.expired_domains.extend(domain_names)
                    
            except KeyboardInterrupt:
                user_choice = input('Continue grab ? (y/n): ')
                if user_choice.lower() != 'y':
                    break
            except Exception as e:
                print(e)