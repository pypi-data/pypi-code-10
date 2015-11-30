import re
import logging

from requests.utils import unquote
from yurl import URL

from poogle.errors import PoogleParserError, PoogleError, PoogleNoResultsError


class PoogleResultsPage(object):
    """
    Search results page container
    """
    def __init__(self, poogle, soup):
        """
        Args:
            poogle(poogle.Poogle):      The parent Poogle object
            soup(bs4.BeautifulSoup):    The search results page HTML soup.
        """
        self._log    = logging.getLogger('poogle.results_page')
        self._poogle = poogle
        self._soup   = soup
        self.results = []
        self.count   = 0

        self.total_results = 0
        self.number = 0

        self.prev_url = None
        self.next_url = None

        # Result counts aren't critical, so unless we want strict parsing, we should swallow any errors parsing them.
        try:
            self._parse_total_results_count()
        except PoogleError:
            if self._poogle.strict:
                raise

        self._parse_results()
        self._parse_page_number()

    def _parse_results(self):
        """
        Parse search results.
        """
        try:
            results = self._soup.find(id='search').ol.find_all('li', {'class': 'g'})
        except AttributeError as e:
            self._log.debug(e.message)
            raise PoogleNoResultsError('Your search - {q} - did not match any documents.'.format(q=self._poogle.query))

        for result in results:
            try:
                self.results.append(PoogleResult(self, result))
            except PoogleParserError:
                self._log.info('Skipping unparsable result')
                continue

        self.count = len(self.results)

    def _parse_total_results_count(self):
        """
        Parse the (estimated) total number of search results found.

        Raises:
            PoogleParserError:  Raised if the search results count could not be parsed for any reason.
        """
        # Get the raw result count string
        self._log.debug('Parsing total results count from the search results page')
        try:
            stats = self._soup.find(id='resultStats').text
        except Exception as e:
            self._log.warn('An error occurred while parsing the total results count: %s', e.message)
            raise PoogleParserError(e.message)
        self._log.debug('Results text matched: %s', stats)

        # Parse the result count
        match = re.match(r'^[\w\s]+?(?P<count>\d+(,\d+)*)[\w\s]+$', stats)
        if not match or not match.group('count'):
            self._log.error('Unrecognized total results format: %s', stats)
            raise PoogleParserError('Unrecognized total results format: {f}'.format(f=stats))

        self.total_results = int(match.group('count').replace(',', ''))
        self._log.info('Total results count successfully parsed: %d', self.total_results)

    def _parse_page_number(self):
        """
        Parse the current page number.

        Raises:
            PoogleParserError:  Raised if strict parsing is enabled and the page number could not be parsed.
        """
        foot = self._soup.find(id='foot')
        tds = foot.find_all('td')
        for td in tds:
            if not td.a and td.text.isdigit():
                self.number = int(td.text)
                self._log.info('Page number parsed: %d', self.number)
                break
        else:
            self._log.warn('Unable to parse the current page number')
            if self._poogle.strict:
                raise PoogleParserError('Unable to parse the current page number')

        # Get the previous / next page links.
        tds = foot.find_all('td')
        p_prev = tds[0].a
        if p_prev:
            self.prev_url = 'https://www.google.com{q}'.format(q=p_prev.get('href'))
            self._log.debug('Previous page URL: %s', self.prev_url)

        p_next = tds[-1].a
        if p_next:
            self.next_url = 'https://www.google.com{q}'.format(q=p_next.get('href'))
            self._log.debug('Next page URL: %s', self.next_url)

    def __len__(self):
        return self.count

    def __repr__(self):
        return '<PoogleResultsPage Container: Page {num!r}>'.format(num=self.number)


class PoogleResult(object):
    """
    Single search result container.
    """
    def __init__(self, page, soup):
        """
        Args:
            page(PoogleResultsPage):    The page this search result was found on
            soup(bs4.element.Tag):      The search result HTML soup
        """
        self._log = logging.getLogger('poogle.result')
        self._soup = soup
        self.page = page

        self.title = None
        self.url = None
        self.url_regex = re.compile(r'^/url\?q=(?P<url>.+)&sa=\w')

        self._parse_result()

    def _parse_result(self):
        """
        Parse search result data.

        Raises:
            PoogleParserError:  Raised if the result can not be parsed for any reason
        """
        self.title = self._soup.a.text
        self._log.info('Result title parsed: %s', self.title)

        # Make sure this is a valid result URL (and not a link to image results, as an example).
        href = self._soup.a.get('href')
        if not href.startswith('/url?'):
            raise PoogleParserError('Unrecognized URL format: %s', href)

        match = self.url_regex.match(href)
        if not match or not match.group('url'):
            self._log.error('Unable to parse search result URL: {h}'.format(h=href))
            raise PoogleParserError('Unable to parse search result URL: %s', href)

        url = unquote(match.group('url'))
        self.url = URL(url)
        self._log.info('Result URL parsed: %s', self.url)

    def __repr__(self):
        return '<PoogleResult Container: "{title!r}">'.format(title=self.title)

    def __unicode__(self):
        return '{title!r} :: {url!r}'.format(title=self.title, url=self.url)

    def __str__(self):
        return unicode(self).encode('utf-8')
