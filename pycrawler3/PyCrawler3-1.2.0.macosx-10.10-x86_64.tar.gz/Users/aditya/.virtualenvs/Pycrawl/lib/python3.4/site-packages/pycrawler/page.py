import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor


class ContentExtractor:

    EXTRACTOR_DEFAULT = 'DefaultExtractor'
    EXTRACTOR_ARTICLE = 'ArticleExtractor'
    EXTRACTOR_ARTICLE_SENTENCES = 'ArticleSentencesExtractor'
    EXTRACTOR_KEEP_EVERTYHING = 'KeepEverythingExtractor'
    EXTRACTOR_KEEP_EVERTYHING_WITH_MIN_KWORDS = 'KeepEverythingWithMinKWordsExtractor'
    EXTRACTOR_LARGEST = 'LargestContentExtractor'
    EXTRACTOR_NUM_WORDS_RULES = 'NumWordsRulesExtractor'
    EXTRACTOR_CANOLA = 'CanolaExtractor'

    @staticmethod
    def extract(html, extractor_type):
        """Extract text content using several method from html

        :param html:
        :param extractor_type:
        :return:
        """
        return Extractor(extractor=extractor_type, html=html)


def extract_encoding(bs4):
    encoding = bs4.original_encoding

    if not encoding:
        # Find encoding from meta charset
        charset = bs4.select('meta[charset]')

        if charset.__len__() > 0:
            encoding = charset[0]['charset']

    return encoding


def extract_favicon(bs4):
    """Extracting favicon url from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of favicon urls
    """

    favicon = []

    selectors = [
        'link[rel="icon"]',
        'link[rel="Icon"]',
        'link[rel="ICON"]',
        'link[rel^="shortcut"]',
        'link[rel^="Shortcut"]',
        'link[rel^="SHORTCUT"]'
    ]

    for selector in selectors:

        icons = bs4.select(selector)

        if icons:

            for icon in icons:

                if icon.has_attr('href'):

                    favicon.append(icon['href'])

    return favicon


def extract_metas(bs4):
    """Extracting meta tags from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of meta tags
    """

    meta_tags = []

    metas = bs4.select('meta')

    for meta in metas:

        meta_content = {}

        meta_attrs = [
            'charset',
            'name',
            'content',
            'property',
            'http-equiv',
            'itemprop'
        ]

        for attr in meta_attrs:
            if meta.has_attr(attr):
                meta_content.update({attr: meta[attr]})

        meta_tags.append(meta_content)

    return meta_tags


def convert_invalid_url(url):
    """Convert invalid url with adding extra 'http://' schema into it

    :param url:
    :return:
    """
    regex_valid_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url if regex_valid_url.match(url) else 'http://{}'.format(url)


def extract_links(bs4):
    """Extracting links from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of links
    """

    unique_links = list(set([anchor['href'] for anchor in bs4.select('a[href]') if anchor.has_attr('href')]))

    # remove irrelevant link
    unique_links = [link for link in unique_links if link != '#']

    # convert invalid link with adding 'http' schema
    return [convert_invalid_url(link) for link in unique_links]


def extract_original_links(base_url, bs4):
    """Extracting links that contains specific url from BeautifulSoup object

    :param base_url: `str` specific url that matched with the links
    :param bs4: `BeautifulSoup`
    :return: `list` List of links
    """
    valid_url = convert_invalid_url(base_url)

    url = urlparse(valid_url)

    base_url = '{}://{}'.format(url.scheme, url.netloc)

    base_url_with_www = '{}://www.{}'.format(url.scheme, url.netloc)

    links = extract_links(bs4)

    result_links = [anchor for anchor in links if anchor.startswith(base_url)]

    result_links_www = [anchor for anchor in links if anchor.startswith(base_url_with_www)]

    return list(set(result_links + result_links_www))


def extract_css_links(bs4):
    """Extracting css links from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of links
    """

    links = extract_links(bs4)

    real_css = [anchor for anchor in links if anchor.endswith(('.css', '.CSS'))]

    css_link_tags = [anchor['href'] for anchor in bs4.select('link[type="text/css"]')
                     if anchor.has_attr('href')]

    return list(set(real_css+css_link_tags))


def extract_js_links(bs4):
    """Extracting js links from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of links
    """

    links = extract_links(bs4)

    real_js = [anchor for anchor in links if anchor.endswith(('.js', '.JS'))]

    js_tags = [anchor['src'] for anchor in bs4.select('script[type="text/javascript"]')
               if anchor.has_attr('src')]

    return list(set(real_js+js_tags))


def extract_resource_links(bs4):
    """Extracting resource links such as .js and .css from BeautifulSoup object

    :param bs4: `BeautifulSoup`
    :return: `list` List of resource links
    """

    return extract_js_links(bs4) + extract_css_links(bs4)


def extract_images(bs4, lazy_image_attribute=None):
    """If lazy attribute is supplied, find image url on that attribute

    :param bs4:
    :param lazy_image_attribute:
    :return:
    """

    # get images form 'img' tags
    if lazy_image_attribute:

        images = [image[lazy_image_attribute] for image in bs4.select('img') if image.has_attr(lazy_image_attribute)]

    else:

        images = [image['src'] for image in bs4.select('img') if image.has_attr('src')]

    # get images from detected links
    image_links = [link for link in extract_links(bs4) if link.endswith(('.jpg', '.JPG', '.png', '.PNG', '.gif', '.GIF'))]

    # get images from meta content
    image_metas = [meta['content'] for meta in extract_metas(bs4)
                   if 'content' in meta
                   if meta['content'].endswith(('.jpg', '.JPG', '.png', '.PNG', '.gif', '.GIF'))]

    return list(set(images + image_links + image_metas))


def extract_canonical(bs4):
    """Extracting canonical url

    :param bs4:
    :return:
    """

    link_rel = bs4.select('link[rel="canonical"]')

    if link_rel.__len__() > 0:

        if link_rel[0].has_attr('href'):

            return link_rel[0]['href']

    return None


class Page:

    def __init__(self, content, url=None):

        self.__url = url

        self.__original_content = content

        self.__bs4 = BeautifulSoup(content, 'html.parser')

        self._encoding = None

        self._canonical_url = None

        self._title = None

        self._favicon = None

        self._language = None

        self._metas = None

        self._content = None

        self._links = None

        self._original_links = None

        self._resource_links = None

        self._js_links = None

        self._css_links = None

    @property
    def encoding(self):

        if not self._encoding:

            self._encoding = extract_encoding(self.__bs4)

        return self._encoding

    @property
    def canonical_url(self):

        if not self._canonical_url:

            self._canonical_url = extract_canonical(self.__bs4)

        return self._canonical_url

    @property
    def title(self):

        if not self._title:

            self._title = self.__bs4.select('title')[0].get_text()

        return self._title

    @property
    def favicon(self):

        if not self._favicon:

            self._favicon = extract_favicon(self.__bs4)

        return self._favicon

    @property
    def language(self):

        if not self._language:

            result = self.__bs4.select('html')

            if result:

                if result[0].has_attr('lang'):

                    self._language = result[0]['lang']

        return self._language

    @property
    def metas(self):

        if not self._metas:

            self._metas = extract_metas(self.__bs4)

        return self._metas

    @property
    def content(self):

        if not self._content:

            self._content = ContentExtractor.extract(
                html=str(self.__bs4),
                extractor_type=ContentExtractor.EXTRACTOR_ARTICLE
            ).getText()

        return self._content

    @property
    def links(self):

        if not self._links:

            self._links = extract_links(self.__bs4)

        return self._links

    @property
    def original_links(self):

        if not self._original_links and self.__url:

            self._original_links = extract_original_links(self.__url, self.__bs4)

        return self._original_links

    @property
    def resource_links(self):

        if not self._resource_links:

            self._resource_links = extract_resource_links(self.__bs4)

        return self._resource_links

    @property
    def js_links(self):

        if not self._js_links:

            self._js_links = extract_js_links(self.__bs4)

        return self._js_links

    @property
    def css_links(self):

        if not self._css_links:

            self._css_links = extract_css_links(self.__bs4)

        return self._css_links

    @property
    def bs4(self):

        return self.__bs4

    def images(self, lazy_attr=None):
        """Get Images url

        :param lazy_attr: `str` set this if you wanna get custom img url attribute
        :return: `list` list of image urls
        """
        return extract_images(self.__bs4, lazy_image_attribute=lazy_attr)

    def html(self, selector):
        """Return html result that executed by given css selector

        :param selector: `str` css selector
        :return: `list` or `None`
        """

        result = self.__bs4.select(selector)

        return [str(r) for r in result] \
            if result.__len__() > 1 else \
            str(result[0]) if result.__len__() > 0 else None

    def text(self, selector):
        """Return text result that executed by given css selector

        :param selector: `str` css selector
        :return: `list` or `None`
        """

        result = self.__bs4.select(selector)

        return [r.get_text() for r in result] \
            if result.__len__() > 1 else \
            result[0].get_text() if result.__len__() > 0 else None

    def raw(self, selector):
        """Return a beautifulsoup result object by given css selector

        :param selector:
        :return:
        """
        return self.__bs4.select(selector)
