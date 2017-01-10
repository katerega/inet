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

from collections import namedtuple
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
            self.rows = self._read_data_file(data_file)
        else:
            raise TypeError("Input file must be of type .csv")

        self.twitter_client = sources.twitter_client
        self.ops_client = sources.ops_client
        self.ch_client = sources.ch_client
        self.html_scraper = sources.html_scraper

    def _read_data_file(self, data_file):
        """Read in data_file

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
        self.rows = []
        with open(data_file) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            return [Row(*r) for r in f_csv]
