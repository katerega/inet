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

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Inet():
    """Inet class that controls scrape behaviour and persists any data."""
    def __init__(self, data_file=None):
        if not data_file:
            raise AttributeError("No path to data_file supplied")
        # Naive check for file type based on extension
        if os.path.splitext(data_file)[-1].lower() == '.csv':
            # self.rows is a list of NamedTuples
            # corresponding to rows/headings
            self.data = self._read_data_file(data_file)
        else:
            raise TypeError("Input file must be of type .csv")

        self.twitter_client = sources.twitter_client
        self.ops_client = sources.ops_client
        self.ch_client = sources.ch_client
        self.html_scraper = sources.html_scraper

    def _read_data_file(self, data_file):
        """Read in data_file.

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
        # Used to create valid identifiers from strings
        result = {}
        with open(data_file, 'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                result.setdefault(
                    row['name'],
                    {k: v for k, v in row.items() if k != 'name'})
        return result

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

        # Create an iteration key
        # This will record what iteration the data
        # was added in
        for entry in self.data:
            self.data[entry]['iteration'] = 0

        for x in range(iterations):
            for k, v in self.data.items():
                url = v['website']
                v['html'], v['twitter_handles'] = self.html_scraper.scrape(url)
                v['company_data'] = self.ch_client.get_company_data(k, v)






























