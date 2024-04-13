import pytest

from webscraper_framework.core.scraper import BasicScraper

def test_fetch_page():
    scraper = BasicScraper("http://example.com")
    page_content = scraper.fetch_page()
    assert page_content is not None

