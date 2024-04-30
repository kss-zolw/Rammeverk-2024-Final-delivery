import pytest
from unittest.mock import MagicMock
from unittest.mock import Mock
from scrape_models import *

@pytest.fixture
def scraper_mock():
    return MagicMock()


###
# Explaniation: The test_class_initialization_and_attribute_assignment function is a parametrized test that tests the initialization of the WebPage,
# NewsSite, Article, and WebStore classes. The test checks if the attributes are correctly assigned to the objects.
# The test_class_initialization_and_attribute_assignment function is parametrized with the class_type and attrs parameters,
# which define the class to be tested and the attributes to be assigned to the object, respectively.
# The test iterates over the class_type and attrs parameters and creates an object of the specified class with the provided attributes.
# The test then asserts that the attributes of the object match the expected values.
@pytest.mark.parametrize(
    "class_type, attrs",
    [
        (WebPage, {"name": "Page", "url": "https://test.no", "html_content": "<html>...</html>",
                   "attr1": "value1", "attr2": "value2"}),
        (NewsSite, {"name": "News Site", "url": "https://test.no", "scraper": scraper_mock,
                    "attr1": "value1", "attr2": "value2"}),
        (Article, {"name": "Article", "url": "https://test.no/article", "scraper": scraper_mock,
                   "attr1": "value1", "attr2": "value2", "html_content": "<html>...</html>"}),
        (WebStore, {"name": "Web Store", "url": "https://test.no", "scraper": scraper_mock,
                    "attr1": "value1", "attr2": "value2"}),
    ]
)
def test_class_initialization_and_attribute_assignment(class_type, attrs):
    obj = class_type(**attrs)
    for attr_name, attr_value in attrs.items():
        assert getattr(obj, attr_name) == attr_value

def test_web_page_html_formatting(scraper_mock, capsys):
    html_content = "<html>...</html>"
    page = WebPage(name="Example Page", url="https://test.no", html_content=html_content)
    with capsys.disabled():
        page.pretty_print_html(html_content)  

def test_news_site_article_scraping():
    scraper_mock = Mock()
    scraper_mock.scrape.return_value = "<html><div class='article'>Article 1</div><div class='article'>Article 2</div></html>"
    news_site = NewsSite(name="Example News Site", url="https://test.no", scraper=scraper_mock)
    selector = ".article"
    news_site.scrape_articles(selector)
    for article in news_site.articles:
        print(article.name)
    assert len(news_site.articles) == 2
    assert news_site.articles[0].name == "Article"
    assert news_site.articles[0].url == "https://test.no"
    assert news_site.articles[0].scraper == scraper_mock

def test_article_html_formatting(scraper_mock, capsys):
    html_content = "<html>...</html>"
    article = Article(name="Test Article", url="https://test.no/article", scraper=scraper_mock, html_content=html_content)
    with capsys.disabled():
        article.pretty_print_html(html_content)

def test_web_store_product_scraping(scraper_mock):
    selector = ".product-item"
    web_store = WebStore(name="Example Web Store", url="https://test.no", scraper=scraper_mock)
    scraper_mock.scrape.return_value = "<html><div class='product-item'>Item 1</div><div class='product-item'>Item 2</div></html>"
    web_store.scrape_products(selector)
    assert len(web_store.products) == 2
    assert web_store.products[0].name == "Product"
    assert web_store.products[0].url == "https://test.no"
    assert web_store.products[0].scraper == scraper_mock
