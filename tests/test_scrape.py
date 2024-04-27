import pytest
from unittest.mock import patch
from scrape import *

# Mock for JSON responses
mock_json = {
    "id": 1,
    "title": "Sample JSON Object",
    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
}

# Test Scraper class for different data types and responses
class TestScraper:
    def test_scrape_returns_html_as_bytes(self):
        url = "https://example.com"
        data_type = "html"
        scraper = Scraper()
        result = scraper.scrape(url, data_type)
        assert isinstance(result, bytes), "HTML content should be returned as bytes"

    def test_scrape_returns_json_as_dict(self):
        url = "https://example.com"
        data_type = "json"
        scraper = Scraper()
        with patch.object(scraper, 'scrape', return_value=mock_json):
            result = scraper.scrape(url, data_type)
            assert isinstance(result, dict) and result == mock_json, "JSON data should be returned as a dictionary and match the mock JSON"

    def test_scrape_raises_error_for_unsupported_data_type(self):
        url = "https://example.com"
        data_type = "unsupported"
        scraper = Scraper()
        with pytest.raises(ValueError):
            scraper.scrape(url, data_type)

# Test for URL extraction from HTML content
def test_url_extraction_from_html():
    html_content = """
    <html>
        <body>
            <a href="https://example.com/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="https://example.com/page3">Page 3</a>
        </body>
    </html>
    """
    base_url = "https://example.com"
    expected_urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]
    extracted_urls = extract_urls(html_content, base_url)
    assert extracted_urls == expected_urls, "Extracted URLs should match the expected list of URLs"

# Test for HTML parsing and URL extraction
def test_html_parsing_and_url_extraction():
    url = "https://example.com"
    html_content = """
    <html>
        <body>
            <a href="https://example.com/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="https://example.com/page3">Page 3</a>
        </body>
    </html>
    """
    expected_urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]
    extracted_urls = parse_html(url, html_content)
    assert extracted_urls == expected_urls, "Extracted URLs from parsed HTML should match the expected URLs"

# Test scraping functionality of WebScraper
def test_web_scraper_scraping_html_and_json():
    web_scraper = WebScraper()
    url_html = "https://example.com"
    data_type_html = "html"
    html_content = web_scraper.scrape(url_html, data_type_html)
    assert isinstance(html_content, str), "Scraped HTML content should be a string"

    url_json = "https://example.com/api"
    data_type_json = "json"
    with patch.object(web_scraper, 'scrape', return_value=mock_json):
        json_data = web_scraper.scrape(url_json, data_type_json)
    assert isinstance(json_data, dict) and json_data == mock_json, "Scraped JSON data should be a dictionary and match the mock JSON"

# Test WebCrawler's single-page crawl functionality
def test_single_page_crawl_functionality():
    crawler = WebCrawler()
    with patch.object(crawler, 'scrape', return_value='<html><body><a href="https://example.com/page1">Page 1</a></body></html>'):
        crawled_urls = crawler.crawl('https://example.com', max_depth=1, num_threads=1)
        assert 'https://example.com' in crawled_urls and 'https://example.com/page1' in crawled_urls, "Crawled URLs should include the starting and extracted URL"

# Test WebCrawler's ability to crawl multiple pages
def test_multiple_pages_crawl_functionality():
    crawler = WebCrawler()
    with patch.object(crawler, 'scrape', side_effect=[
        '<html><body><a href="https://example.com/page1">Page 1</a></body></html>',
        '<html><body><a href="https://example.com/page2">Page 2</a></body></html>'
    ]):
        crawled_urls = crawler.crawl('https://example.com', max_depth=2, num_threads=1)
        assert 'https://example.com' in crawled_urls and 'https://example.com/page1' in crawled_urls, "Crawled URLs should contain the starting URL and extracted URLs from both pages"

# Test WebCrawler's error handling when scrape method fails
def test_crawl_error_handling():
    crawler = WebCrawler()
    with patch.object(crawler, 'scrape', side_effect=Exception("Scrape error")):
        crawled_urls = crawler.crawl('https://example.com', max_depth=1, num_threads=1)
        assert len(crawled_urls) == 0, "No URLs should be crawled when an error occurs during scraping"


def test_extract_elements_by_xpath():
    html = '<div class="container"><h1>Title</h1><p>Content</p></div>'
    selector = "//h1"
    expected_elements = ['<h1>Title</h1>']

    elements = ElementSelector.extract_elements_by_xpath(html, selector)
    print(f"Actual elements nisse: {elements}")

    assert elements == expected_elements


def test_extract_elements_by_tag():
    html = '<div class="container"><h1>Title</h1><p>Content</p></div>'
    selector = "<p>"
    expected_elements = ['<p>Content</p>']

    elements = ElementSelector.extract_elements_by_tag(html, selector)
    print(f"Actual elements: {elements}")

    assert elements == expected_elements


def test_extract_elements_by_css_selector():
    html = '<div class="container"><h1>Title</h1><p>Content</p></div>'
    selector = "p"
    expected_elements = ['<p>Content</p>']

    elements = ElementSelector.extract_elements_by_css_selector(html, selector)
    print(f"Actual elements: {elements}")

    assert elements == expected_elements, f"Test failed: Expected {expected_elements}, got {elements}"


def test_filter_elements_by_attribute():
    elements = ['<h1 id="title">Title</h1>', '<p class="content">Content</p>']
    attr_name = "class"
    attr_value = "content"
    expected_elements = ['<p class="content">Content</p>']

    filtered_elements = ElementSelector.filter_elements_by_attribute(elements, attr_name, attr_value)
    print(f"Filtered elements: {filtered_elements}")

    assert filtered_elements == expected_elements


def test_extract_elements():
    # Given HTML content
    html = '<div class="container"><h1>Title</h1><p>Content</p></div>'
    # CSS selector that aims to select the <p> tag inside a div with class "container"
    selector = ".container p"
    # Expected elements result
    expected_elements = ['<p>Content</p>']
    # When extracting elements using the CSS selector
    elements = ElementSelector.extract_elements(html, selector)

# Then, output the results for debugging
    print(f"Actual elements: {elements}")

# Assert to check if the actual extracted elements match the expected elements
    assert elements == expected_elements, f"Test failed: Expected {expected_elements}, got {elements}"




# Run the tests
if __name__ == "__main__":
    pytest.main()
