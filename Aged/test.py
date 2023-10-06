from bs4 import BeautifulSoup
import requests

for i in range(0, 25, 500):
    url = 'https://www.expireddomains.net/expired-domains/?start=' + str(i)
    response = requests.get(url)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('td', class_='field_domain')
    print(links)
    for link in links:
        link = link.find('a').get('title')
        with open('domains.txt', 'a') as f:
            f.write(link + '\n')
