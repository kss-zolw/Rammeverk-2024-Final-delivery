import requests
import concurrent.futures
from urllib.parse import urljoin
import re
import threading
import csv

from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    def scrape(url, data_type):
        """Use the requested URL to scrape data.
        Args:
            url (string): The URL to scrape.
            data_type (string): The type of data to scrape if it is html or json).

        Returns:
            bytes or dict: The scraped data.

        Raises:
            ValueError: If an unsupported data type is provided.
            Exception: If the request fails with a non-200 status code.
        """
        with requests.Session() as session:
            response = session.get(url)
            if response.status_code != 200:
                raise Exception(f"Request failed: status code {response.status_code}")

            if data_type == 'html':
                return response.content
            elif data_type == 'json':
                return response.json()
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
        
    @staticmethod
    def export_to_file(data, file_path, fields=None):
        """Exports the scraped data to a file.

    Args:
        data (bytes, str, list, or dict): The data to export.
        file_path (str): The path to the output file.
        fields (list, optional): The fields to include in the CSV output file. This is only used if data is a dict or list of dicts.

    Raises:
        ValueError: If the data type is unsupported or if fields are not provided for a dict.
    """
        if isinstance(data, bytes):
            data = data.decode('utf-8')  # Decode bytes to string assuming UTF-8 encoding

        if isinstance(data, str):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)  # Write string data directly to file
        elif isinstance(data, dict) or (isinstance(data, list) and all(isinstance(item, dict) for item in data)):
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if not fields:
                    if isinstance(data, dict):
                        fields = list(data.keys())  # Use dictionary keys as fields if not specified
                    elif isinstance(data, list):
                        fields = list(data[0].keys())  # Assume all dictionaries have the same structure
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                if isinstance(data, dict):
                    writer.writerow(data)  # Write a single dictionary to the CSV file
                else:
                    writer.writerows(data)  # Write a list of dictionaries to the CSV file
        else:
            raise ValueError("Invalid data type. Expected bytes, str, dict, or list of dicts.")


    @staticmethod
    def extract_text(element):
        """Extracts the text content from an HTML element."""
        soup = BeautifulSoup(element, 'html.parser')
        return soup.get_text(strip=True)


    @staticmethod
    def extract_attribute(element, attribute):
        """Extracts the value of the specified attribute from an HTML element."""
        soup = BeautifulSoup(element, 'html.parser')
        tag = soup.find()
        if tag and tag.has_attr(attribute):
            return tag[attribute]
        return ""


def extract_urls(html_content, base_url):
    """Extracts URLs from the HTML content.

    Args:
        html_content (str): The HTML content to extract URLs from.
        base_url (str): The base URL of the web page.

    Returns:
        list: A list of extracted URLs.
    """
    pattern = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1'
    urls = []

    for match in re.finditer(pattern, html_content):
        href = match.group(2)
        absolute_url = urljoin(base_url, href)
        urls.append(absolute_url)

    return urls


class WebScraper:
    """A web crawler for scraping and extracting URLs from web pages."""

    def __init__(self):
        self.scraper = Scraper()

    def scrape(self, url, data_type):
        """Scrapes data from a given URL.

        Args:
            url (str): The URL to scrape.
            data_type (str): The type of data to scrape ('html' or 'json').

        Returns:
            str or dict: The scraped data as a string (HTML) or a dictionary (JSON).

        Example:
            web_scraper = WebScraper()
            html_content = web_scraper.scrape('https://example.com', 'html')
            json_data = web_scraper.scrape('https://example.com/api', 'json')
        """
        content = self.scraper.scrape(url, data_type)
        if data_type == 'html':
            return content.decode('utf-8')  # Decode content into a string
        return content


def parse_html(url, html_content):
    """Parses the HTML content and extracts URLs.

           Args:
               url (str): The URL of the web page.
               html_content (str): The HTML content to parse.

           Returns:
               list: A list of extracted URLs.

           Example:
               crawler = WebCrawler()
               html_content = crawler.scrape('https://example.com')
               urls = crawler.parse_html('https://example.com', html_content)
               for url in urls:
                   print(url)
           """
    start_tag = '<a'
    end_tag = '</a>'
    href_attr = 'href='
    url_prefixes = ('http://', 'https://')

    urls = []

    while True:
        start_index = html_content.find(start_tag)
        if start_index == -1:
            break

        end_index = html_content.find(end_tag, start_index)
        if end_index == -1:
            break

        anchor_content = html_content[start_index:end_index]
        href_index = anchor_content.find(href_attr)
        if href_index == -1:
            continue

        href_start = anchor_content.find('"', href_index) + 1
        href_end = anchor_content.find('"', href_start)
        href = anchor_content[href_start:href_end]

        if href.startswith(url_prefixes):
            urls.append(href)
        else:
            absolute_url = urljoin(url, href)
            urls.append(absolute_url)

        html_content = html_content[end_index:]

    return urls


class WebCrawler:
    """A web crawler for scraping and extracting URLs from web pages."""

    def __init__(self):
        self.visited_urls = set()
        self.queue = []

    def crawl(self, url, max_depth=3, num_threads=5):
        """Crawl the web starting from a given URL.

        Args:
            url (str): The starting URL to crawl.
            max_depth (int, optional): The maximum depth to crawl. Defaults to 3.
            num_threads (int, optional): The number of threads to use for concurrent crawling. Defaults to 5.

        Returns:
            list: A list of crawled URLs.

        Example:
            crawler = WebCrawler()
            crawled_urls = crawler.crawl('https://example.com', max_depth=2, num_threads=10)
            for url in crawled_urls:
                print(url)
        """
        crawled_urls = []
        visited_urls = set()
        queue = [(url, 0)]
        active_threads = 0
        active_threads_lock = threading.Lock()

        def crawl_worker():
            nonlocal active_threads
            with active_threads_lock:
                active_threads += 1


            while True:
                try:
                    current_url, depth = queue.pop(0)
                except IndexError:
                    break

                if depth > max_depth:
                    continue

                if current_url in visited_urls:
                    continue

                visited_urls.add(current_url)
                print(f"Crawling {current_url} at depth {depth}")

                try:
                    html_content = self.scrape(current_url, 'html')
                    parsed_urls = extract_urls(html_content, current_url)
                    crawled_urls.append(current_url)

                    for parsed_url in parsed_urls:
                        queue.append((parsed_url, depth + 1))
                except Exception as e:
                    print(f"Error occurred while crawling {current_url}: {str(e)}")

            with active_threads_lock:
                active_threads -= 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            while queue:
                with active_threads_lock:
                    if active_threads < num_threads:
                        executor.submit(crawl_worker)

        return crawled_urls

    def scrape(self, url, data_type):
        web_scraper = WebScraper()
        return web_scraper.scrape(url, data_type)


class ElementSelector:
    """ Class to extract elements from HTML content based on different selectors. """

    @staticmethod
    def extract_elements(html, selector):
        """Determines the method of extraction based on the type of selector."""
        if selector.startswith("//"):
            # Extract using XPath-like syntax (if you want to implement this, consider using lxml)
            return ElementSelector.extract_elements_by_xpath(html, selector)
        elif selector.startswith("<"):
            # Extract using direct HTML tag
            return ElementSelector.extract_elements_by_tag(html, selector)
        else:
            # Extract using CSS-like syntax
            return ElementSelector.extract_elements_by_css_selector(html, selector)


    @staticmethod
    def extract_elements_by_xpath(html, selector):
        """Extracts elements using a simulated XPath selector."""
        tag = selector.split("//")[1]
        pattern = rf"<{tag}[^>]*>.*?</{tag}>"
        elements = re.findall(pattern, html, re.DOTALL)
        return elements

    @staticmethod
    def extract_elements_by_tag(html, selector):
        # Assuming direct tag use without angle brackets
        tag = selector.strip('<>')
        soup = BeautifulSoup(html, 'html.parser')
        return [str(element) for element in soup.find_all(tag)]

    @staticmethod
    def extract_elements_by_css_selector(html, selector):
        soup = BeautifulSoup(html, 'html.parser')
        selected_elements = soup.select(selector)
        # Convert elements back to string for comparison in tests
        return [str(element) for element in selected_elements]

    @staticmethod
    def filter_elements_by_attribute(elements, attr_name, attr_value):
        """Filters a list of HTML elements, returning only those that have a specific attribute with a specified value.

        Args:
            elements (list of str): HTML elements to filter.
            attr_name (str): The attribute name to filter by.
            attr_value (str): The attribute value to match.

        Returns:
            list of str: Filtered HTML elements.
        """
        filtered_elements = []
        for element in elements:
            soup = BeautifulSoup(element, 'html.parser')
            for tag in soup.find_all(attrs={attr_name: attr_value}):
                filtered_elements.append(str(tag))

        return filtered_elements

    @staticmethod
    def extract_urls(html_content, base_url):
        """Extracts URLs from the HTML content.

        Args:
           html_content (str): The HTML content to extract URLs from.
            base_url (str): The base URL of the web page.

        Returns:
            list: A list of extracted URLs.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []

        for tag in soup.find_all('a', href=True):
            href = tag['href']
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)

        return urls
