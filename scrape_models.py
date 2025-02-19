from scrape import ElementSelector


class WebPage:
    """ Represents a web page. """
    
    def __init__(self, name, url, html_content, **kwargs):
        """
        Initializes a WebPage object with specified attributes and any additional keyword arguments.

        Args:
            name (str): The name of the web page.
            url (str): The URL of the web page.
            html_content (str): The HTML content of the web page.
            **kwargs: Additional user-defined attributes, passed as key-value pairs.

        Example:
            page = WebPage(name='Example Page', url='https://example.com', html_content='<html>...</html>',
                           sub_urls=['https://example.com/news'], custom_attribute='Custom Value')
        """
        self.name = name
        self.url = url
        self.html_content = html_content

        # Dynamically assign any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def pretty_print_html(html_content, indent_size=4, initial_indent=0):
        """ Pretty prints the HTML content with indentation for better readability. 
        
        Args:
            html_content (str): The HTML content to print.
            indent_size (int, optional): The size of each indentation level. Defaults to 4.
            initial_indent (int, optional): The starting indentation level. Defaults to 0.
        
        Example:
            WebPage.pretty_print_html('<html><body>Hello</body></html>')
        """
        indent_level = initial_indent
        formatted_html = ''
        for char in html_content:
            if char == '<':
                formatted_html += '\n' + ' ' * indent_size * indent_level + char
                indent_level += 1
            elif char == '>':
                formatted_html += char
                indent_level = max(indent_level - 1, 0)
            else:
                if formatted_html.endswith('>'):
                    formatted_html += '\n' + ' ' * indent_size * indent_level + char
                else:
                    formatted_html += char

        print(formatted_html)




class NewsSite(WebPage):
    """Represents a news site."""

    def __init__(self, name, url, scraper, **kwargs):
        """
        Initialize a NewsSite object.

        Args:
            name (str): The name of the news site.
            url (str): The URL of the news site.
            scraper (WebScraper): The web scraper used for scraping.
            **kwargs: Additional user-defined attributes.

        Example:
            news_site = NewsSite(name='Example News Site', url='https://example.com', scraper=scraper, attr1='value1', attr2='value2')
        """
        super().__init__(name, url, scraper, **kwargs)
        self.scraper = scraper
        self.articles = []

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def scrape_articles(self, selector):
        """Scrapes articles from the news site based on the provided selector."""

        html_content = self.scraper.scrape(self.url, 'html')
        article_elements = ElementSelector.extract_elements(html_content, selector)
        self.articles = [Article(name="Article", url=self.url, scraper=self.scraper, html_content=element) for element
                         in article_elements]

    def scrape_articles2(self, selector):
        """Scrapes articles from the news site based on the provided selector."""
        html_content = self.scraper.scrape(self.url, 'html')
        article_elements = ElementSelector.extract_elements(html_content, selector)
        self.articles = [Article(name="Article", url=self.url, scraper=self.scraper, html_content=element) for element
                         in article_elements]

class Article(WebPage):
    """Represents an article on a news site."""
    def __init__(self, name, url, scraper, **kwargs):
        """
        Initialize an Article object.

        Args:
            name (str): The name of the article.
            url (str): The URL of the article.
            scraper (WebScraper): The web scraper used for scraping the article.
            **kwargs: Additional user-defined attributes.

        Example:
            article = Article(name='Example Article', url='https://example.com/article', scraper=scraper, custom_attr='value')
        """
        super().__init__(name, url, scraper=scraper, html_content="")
        self.scraper = scraper

        # Set user-defined attributes
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


class WebStore(WebPage):
    """Represents a web store."""

    def __init__(self, name, url, scraper, **kwargs):
        """
        Initialize a WebStore object.

        Args:
            name (str): The name of the web store.
            url (str): The URL of the web store.
            scraper (WebScraper): The web scraper used for scraping.
            **kwargs: Additional user-defined attributes.

        Example:
            web_store = WebStore(name='Example Web Store', url='https://example.com', scraper=scraper, attr1='value1', attr2='value2')
        """
        super().__init__(name, url, scraper, **kwargs)
        self.scraper = scraper
        self.products = []

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def scrape_products(self, selector):
        """Scrapes products from the web store based on the provided selector.

        Args:
            selector (str): The CSS selector or HTML tag for the product elements.

        Example:
            web_store = WebStore(name='Example Web Store', url='https://example.com', scraper=scraper)
            web_store.scrape_products(selector='.product-item')
        """
        html_content = self.scraper.scrape(self.url, 'html')
        product_elements = ElementSelector.extract_elements(html_content, selector)
        self.products = [Product(name="Product", url=self.url, scraper=self.scraper, html_content=element) for element in product_elements]


class Product(WebPage):
    """Represents a product on a webstore."""
    def __init__(self, name, url, scraper, **kwargs):
        """
        Initialize a Product object.

        Args:
            name (str): The name of the product.
            url (str): The URL of the product.
            scraper (WebScraper): The web scraper used for scraping the product.
            **kwargs: Additional user-defined attributes.

        Example:
            product = Product(name='Example Product', url='https://example.com/product', scraper=scraper, custom_attr='value')
        """
        super().__init__(name, url, "", scraper=scraper)
        self.scraper = scraper
        self.content = ""

        # Set user-defined attributes
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def scrape_description(self, html_content, selector='//div[@class="product-description"]'):
        """Scrapes the description of the product.

        Args:
            html_content (str): The HTML content of the product page.
            selector (str, optional): The XPath selector for the description element. Defaults to
                '//div[@class="product-description"]'.

        Example:
            product = Product(name='Product 1', url='https://www.example.com/product1', scraper=scraper)
            product.scrape_description(html_content)
            # OR
            product.scrape_description(html_content, selector='//div[@class="custom-description"]')
        """
        description_elements = ElementSelector.extract_elements(html_content, selector)
        if description_elements:
            self.description = ' '.join(element.text.strip() for element in description_elements)
