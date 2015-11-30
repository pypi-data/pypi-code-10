import logging
from time import sleep

import requests
from requests.utils import quote
from bs4 import BeautifulSoup

from poogle.errors import PoogleRequestError, PoogleNoMoreResultsError
from poogle.containers import PoogleResultsPage

__author__     = "Makoto Fujimoto"
__copyright__  = 'Copyright 2015, Makoto Fujimoto'
__license__    = "MIT"
__version__    = "0.1"
__maintainer__ = "Makoto Fujimoto"


class Poogle(object):

    SEARCH_URL = 'https://www.google.com/search?q='

    def __init__(self, query, per_page=10, start_page=1, lazy=True, **kwargs):
        """
        Args:
            query(str):         The search query to execute.
            per_page(int):      The number of results to retrieve per page.
            start_page(int):    The starting page for queries.
            lazy(bool):         Don't execute the query until results are requested. Defaults to True.
            **kwargs:           Arbitrary keyword arguments, refer to the documentation for more information.

        Raises:
            ValueError: Raised if the supplied per_page argument is less than 1 or greater than 100
        """
        self._log = logging.getLogger('poogle')

        self._query        = query
        self._search_url   = self.SEARCH_URL + quote(query)

        if (per_page < 1) or (per_page > 100):
            raise ValueError('per_page must contain be an integer between 1 and 100')
        self._per_page     = per_page

        self._lazy         = lazy
        self._query_count  = 0
        self.total_results = 0

        self._results      = []
        self._current_page = start_page - 1
        self.last          = None

        self.strict = kwargs.get('strict', False)

        if not self._lazy:
            self.next_page()

    def next_page(self):
        """
        Get the next page of search results.

        Returns:
            PoogleResultsPage

        Raises:
            PoogleRequestError: Raised if an error occurs while executing the search query.
        """
        if self._query_count and not self.last.next_url:
            raise PoogleNoMoreResultsError('There are no more search results available')

        url = '{url}&num={n}&start={s}'.format(url=self._search_url, n=self._per_page,
                                               s=self._current_page * self._query_count)
        self._log.info('Executing search query: %s', url)

        # Execute the search query
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.RequestException as e:
            self._log.error('An error occurred when executing the search query: %s', str(e))
            raise PoogleRequestError(str(e))

        # Parse the search results page
        soup = BeautifulSoup(page.content, 'html.parser')
        page = PoogleResultsPage(self, soup)
        self.total_results = page.total_results

        self._current_page += 1
        self._query_count += 1
        self.last = page
        self._results.append((self._current_page, page))

        return page

    @property
    def query(self):
        return self._query

    @property
    def per_page(self):
        return self._per_page

    @per_page.setter
    def per_page(self, value):
        if self._query_count:
            self._log.warn('Attempted to change the per_page attribute after the query has already been executed')
            raise AttributeError('The per page attribute can not be changed after the search query has been executed')

        if (value < 1) or (value > 100):
            raise ValueError('per_page must contain be an integer between 1 and 100')

        self._per_page = value

    @property
    def results(self):
        """
        Concatenate results from all pages together and return

        Returns:
            list[poogle.containers.PoogleResult]
        """
        # If we're querying lazily, make sure we've fetched our initial results
        if self._lazy and not self._query_count:
            self._log.info('Executing query lazily')
            return self.next_page().results

        # Concatenate results from all pages together and return
        all_results = []
        for __, r in self._results:
            all_results += r.results

        return all_results

    def __repr__(self):
        return '<Poogle Search: {q!r}>'.format(q=self._query)


def google_search(query, results=10, pause=0.5):
    # Get the per page limit and ready our Poogle object
    per_page = min(results, 90) + 10
    poogle = Poogle(query, per_page)

    # Set a query limit to prevent infinite loops
    limit = int(results / 100) + 3
    query_count = 0

    query_results = []
    while len(query_results) < results:
        # Make sure we haven't exceeded our query limit
        if query_count >= limit:
            raise RuntimeError('Recursion error, exceeded query limit of %d with %d results', limit, len(query_results))

        # Pause if this is not our first query
        if pause and query_count:
            sleep(pause)

        try:
            query_results += poogle.next_page().results
        except PoogleNoMoreResultsError:
            # If we have no more results, break now
            break

        query_count += 1

    return query_results[:results]
