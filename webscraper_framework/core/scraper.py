import requests
from bs4 import BeautifulSoup

class BasicScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, path=""):
        """ Fetches a web page and returns its content """
        try:
            response = requests.get(f"{self.base_url}/{path}")
            response.raise_for_status()  # Ensures we notice bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {self.base_url}/{path}: {e}")
            return None
        

    def parse_html(self, html_content, parser='html.parser'):
        """ Parses HTML content and returns a BeautifulSoup object """
        return BeautifulSoup(html_content, parser)


    def scrape(self, path="", parser='html.parser'):
        """ Fetches and parses a webpage """
        html_content = self.fetch_page(path)
        if html_content:
            return self.parse_html(html_content, parser)
        return None
