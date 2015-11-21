'''
from pycrawl import crawler

# Execute variants
page = crawler.grab('http://www.pasarpanda.com')
page = crawler.from_file('file.html')
page = crawler.from_text("<html></html>")

# methods
page.html('#my_container') # get html content by given css selector
page.text('#my_container') # get text content by given css selector
page.images() # all images links

# information provided
page.title # page title
page.encoding # page encoding
page.language # text language of page
page.metas # list dictionary of meta
page.content # text content
page.copyright # copyright
page.links # all links on the site
page.original_links # all original links (the domain links are same as the requested page)
page.resource_links # all js & css links
page.js_links # all javascript links
page.css_links # all css links
page.favicon # favicon url
'''
from .http import HttpRequest
from .page import Page


class Crawler:

    @classmethod
    def grab(cls, url):

        content = HttpRequest.get(url)

        return Page(content, url=url)

    @classmethod
    def from_file(cls, abs_path):

        f = open(abs_path, 'r')

        content = f.read()

        f.close()

        return Page(content)

    @classmethod
    def from_text(cls, text):

        return Page(text)
