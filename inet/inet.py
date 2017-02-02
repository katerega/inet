# -*- coding: utf-8 -*-

"""
Inet
----

Crawl a seed group of companies to find links and establish an Innovation
Network

"""

import csv
import logging
import os

from . import sources

# Configure logging to do nothing by default. Will begin
# logging if logging system configured by user"""

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Inet():
    """Control scrape behaviour and persist data

    Controls the scraping process, alternating between network
    discovery and scraping behavioural evidence. Initialise
    the seed list of data by passing the path of the csv
    file to the "data_file" keyword.

    Parameters
    ----------
    data_file: str, default None
        A valid path to the data file, which should be formatted as csv

    Returns
    -------
    Inet object

    Examples
    --------
    >>> i = inet.Inet(data_file='path/to/file.csv')
    """

    def __init__(self, data_file=None):
        if not data_file:
            raise AttributeError("No path to data_file supplied")

        # Naive check for file type based on extension
        if os.path.splitext(data_file)[-1].lower() == '.csv':
            # self.rows is a list of NamedTuples
            # corresponding to rows/headings
            logger.info("Loading data from {}".format(data_file))
            self.data = self._read_data_file(data_file)
        else:
            raise TypeError("Input file must be of type .csv")

        self.twitter_handler = sources.twitter_handler
        self.ops_client = sources.ops_client
        self.ch_client = sources.ch_client
        self.html_scraper = sources.html_scraper

    def _read_data_file(self, data_file):
        """Read in a data_file.

        Opens the file at path 'data_file' and reads in the file.
        Expects a header row.

        Parameters
        ----------
        data_file: string
            Path to input data file

        Returns
        -------
        List of NamedTuple objects with names corresponding
        to the headers in 'data_file'.
        """
        result = {}

        with open(data_file, 'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                result.setdefault(
                    row['name'],
                    {k: v for k, v in row.items() if k != 'name'})

        logger.info("Loaded data from {}".format(data_file))

        return result

    def _scrape_html(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                url = v['website']
                try:
                    v['html'] = self.html_scraper.scrape(url)
                    logger.info("Stored html for {}".format(url))
                except TypeError:
                    logger.warn("No html stored for {}".format(url))
                    v['html'] = None

    def _scrape_twitter_handles(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                url = v['website']
                try:
                    for html in v.get('html'):
                        v['twitter_handles'] = self.html_scraper.twitter_handles(html)  # noqa
                    logger.info("Found {} twitter handles in {}"
                                .format(len(v.get('twitter_handles', [])), url))  # noqa
                except TypeError:
                    logger.warn("No twitter handles stored for {}".format(url))
                    v['twitter_handles'] = None

    def twitter_followers(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                v['twitter_followers'] = self.twitter_handler.followers(v['twitter_handles'])  # noqa

    def twitter_following(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                v['twitter_following'] = self.twitter_handler.following(v['twitter_handles'])  # noqa

    def mutual_follows(self):
        for k, v in self.data.items():
            v['mutual_follows'] = {}
            if self.check_iteration(v.get('iteration')):
                for handle in v['twitter_followers']:
                    followers = v['twitter_followers'][handle]
                    following = v['twitter_following'][handle]
                    mutual_set = set(followers).intersection(following)
                    mutual_list = list(mutual_set)
                v['mutual_follows'][handle] = mutual_list

    def _get_company_data(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                v['company_data'] = self.ch_client.get_company_data(k, v)

    def _shared_directors(self):
        for k, v in self.data.items():
            if self.check_iteration(v.get('iteration')):
                self.data[k]['directors'] = self.ch_client.get_directors(k, v)

    def check_iteration(self, iteration):
        return iteration == self._iteration

    def start(self, iterations=1):
        """Start the iteration process.

        Starts the iteration process that expands the original seed
        data.

        Parameters
        ----------
        iterations: int, default 5
            Number of iterations to complete

        Returns
        -------
        None
        """
        logger.info("Starting data crawl. Number of iterations is {}"
                    .format(iterations))

        # Track what iteration node was added in
        for entry in self.data:
            self.data[entry]['iteration'] = 0

        for iteration in range(iterations):
            logger.info("Starting iteration {}".format(iteration))
            self._iteration = iteration
            self._scrape_html()
            self._scrape_twitter_handles()
            self._get_company_data()
            self._shared_directors()
            self.twitter_followers()
            self.twitter_following()
            self.mutual_follows()
