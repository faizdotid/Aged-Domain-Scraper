# main.py

import requests
import os
from helper.ExpiredDomains import ExpiredDomainExtractor
from helper.Semrush import Semrush
from helper.ExportExcel import DataFrameToExcel
import concurrent.futures

class Main:

    def __init__(self):
        self.session = None
        self.user_creds = {
            'username': 'ath123',
            'password': 'ath12345',
        }

    def start_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })

    def start_extractor(self):
        self.extractor = ExpiredDomainExtractor(self.session)
        self.extractor.set_user_credentials(self.user_creds['username'], self.user_creds['password'])
        self.extractor.authenticate_user()

    def start_semrush(self):
        self.semrush = Semrush(self.session)

    def save_output(self, data: list):
        df_to_excel = DataFrameToExcel('output.xlsx')
        df_to_excel.append_data_to_excel(data)

    def run(self):
        tld = input('Tld (enter for default): ')
        if tld == '':
            tld = 'combinedexpired'
        else:
            tld = 'expired' + tld
        start_page = int(input('Start page: '))
        end_page = int(input('End page: '))
        self.extractor.fetch_expired_domains(tld, start_page, end_page)
        expired_domains =  self.extractor.get_expired_domains()
        print(f'Found total {len(expired_domains)} domains')
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_result = {executor.submit(self.semrush.get_url_metrics, domain): domain for domain in expired_domains}
            for future in concurrent.futures.as_completed(future_result):
                result = future.result()
                if result is not None:
                    results.append(result)
        self.save_output(results)

q = Main()
q.start_session()
q.start_extractor()
q.start_semrush()
q.run()