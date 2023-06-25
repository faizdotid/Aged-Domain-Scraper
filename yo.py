import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
import whois

class DomainScraper:

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'}
    def __init__(self, filters, check: bool) -> None:
        self.domain_list = []
        self.filters = filters if filters is not None else {}
        self.check = check

    def is_domain_accessible(self, domain: str) -> bool:
        try:
            whois.whois(domain)
            return True
        except Exception:
            return False

    def parse_to_int(self, value: str):
        try:
            return int(value)
        except ValueError:
            return value

    def extract_domain_info(self, html_response: str):
        soup = BeautifulSoup(html_response, 'html.parser')
        domain_table = soup.find('tbody', class_='row-hover')

        if domain_table is None:
            print("No domain table found...")
            return

        domain_rows = domain_table.find_all('tr')
        for row in domain_rows:
            self.process_row(row)

    def process_row(self, row):
        td_elements = row.find_all('td')
        if len(td_elements) < 9:
            return

        domain_info = self.build_domain_info(td_elements)
        if self.is_domain_suitable(domain_info):
            if self.check:
                if not self.is_domain_accessible(domain_info['Domain']):
                    domain_info['Status'] = 'Available'
                else:
                    domain_info['Status'] = 'Not Available'
            self.domain_list.append(domain_info)

    def build_domain_info(self, td_elements):
        return {
            'Domain': 'http://' + td_elements[0].text,
            'Age': self.parse_to_int(td_elements[1].text),
            'DA': self.parse_to_int(td_elements[2].text),
            'PA': self.parse_to_int(td_elements[3].text),
            'DR': self.parse_to_int(td_elements[4].text),
            'CF': self.parse_to_int(td_elements[5].text),
            'TF': self.parse_to_int(td_elements[6].text),
            'Backlinks': self.parse_to_int(td_elements[7].text),
            'Referring Domains': self.parse_to_int(td_elements[8].text),
        }

    def is_domain_suitable(self, domain_info):
        for key, value in self.filters.items():
            formatted_key = key.replace('_', ' ').title() if '_' in key else key.upper()
            if formatted_key in domain_info and domain_info[formatted_key] <= value:
                return False
        return True

    def fetch_domain_data(self):
        url = 'https://www.seekahost.com/free-expired-domains-list/'
        try:
            response = requests.get(url, timeout=70, headers=self.header)
            if response.status_code == 200:
                self.extract_domain_info(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def export_to_excel(self):
        domain_df = pd.DataFrame(self.domain_list)

        with pd.ExcelWriter('domains.xlsx', engine='xlsxwriter', mode='w') as writer:
            domain_df.to_excel(writer, sheet_name='Sheet1', index=False)

            workbook = writer.book
            header_format = self.get_header_format(workbook)
            worksheet = writer.sheets['Sheet1']
            self.format_columns(domain_df, worksheet, header_format)
        print('Saved to domains.xlsx')

    def get_header_format(self, workbook):
        return workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#0000FF',
            'font_color': 'white',
            'border': 1,
            'align': 'center'
        })

    def format_columns(self, domain_df, worksheet, header_format):
        for col_num, value in enumerate(domain_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, len(value) * 2)
        worksheet.set_column(0, 0, 50)


def main(args):
    scraper = DomainScraper(args.filters, args.check)
    scraper.fetch_domain_data()
    scraper.export_to_excel()

class KeyValue(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        for kv in values.split(","):
            k,v = kv.split("=")
            my_dict[k] = int(v)
        setattr(namespace, self.dest, my_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape expired domains from seekahost.com')
    parser.add_argument('--filters', action=KeyValue, help='Filters to apply to the domain list (e.g. --filters PA=20,DA=30)')
    parser.add_argument('--check', action='store_true', default=False, help='Check if the domain is available')
    args = parser.parse_args()

    main(args)
