# Age-Domain-Scraper

## Installation
```bash
git clone https://github.com/faizdotid/Age-Domain-Scraper
cd Age-Domain-Scraper
pip3 instal bs4
pip3 install requests
pip3 install python-whois
pip3 install pandas
```

## Usage

You can use this script in the following ways:

```bash
# to check the values of the domains without making any changes
python3 yo.py --filters da=30 --check

# to apply the changes
python3 yo.py --filters da=30
```

## Filters

The filters allow you to narrow down the details you're interested in. The supported filters are:

- Domain Authority (da)
- Page Authority (pa)
- Domain Rating (dr)
- Citation Flow (cf)
- Age (age)
- Trust Flow (tf)
- Backlink (backlink)
- Referring Domains (referring_domains)

Each filter can be used with the `--filters` flag, followed by the filter and the value you're interested in. For example, if you're interested in domains with a Domain Authority of 30, you would use `--filters da=30`.

## Requirements

- Python3

This utility is easy to use and will provide you with valuable information about your or others' domains. Please ensure that Python3 is installed in your environment before proceeding.
