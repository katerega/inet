# -*- coding: utf-8 -*-
import csv
import logging
import os
import requests

from collections import namedtuple
from lxml import html
from urllib.parse import urlparse
from . import sources

"""Configure logging to do nothing by default. Will begin
logging if logging system configured by user"""

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Inet():
    """Inet class"""
    def __init__(self, data_file=None):
        # Naive check for file type based on extension
        # First check filepath is passed as a parameter
        if data_file is not None:
            # Then split off the extension using os
            ext = os.path.splitext(data_file)[-1].lower()
            # then check ends with .csv or .json
            if ext == '.csv':
                # List of NamedTuples corresponding to rows/headings
                self.rows = self._read_data_file(data_file)
            else:
                raise TypeError("Input file must be of type .csv")
        else:
            raise AttributeError("No data_file path specified as a "
                                 "parameter to Inet")

        # Access sources from this class
        self.twitter_client = sources.twitter_client
        self.ops_client = sources.ops_client
        self.ch_client = sources.ch_client

    def _check_url_scheme(self, url):
        if not urlparse(url).scheme:
            url = "http://" + url
        return url

    def _read_data_file(self, data_file):
        self.rows = []
        with open(data_file) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            return [Row(*r) for r in f_csv]

    def _scrape_html(self, url, about_xpath=None):
        """Use urls in the data to get company html - specifically
        the homepage, and the about page"""

        # Xpath selector for hrefs that contain 'about'
        if about_xpath is None:
            about_xpath = ("//a[text()[contains(translate(., 'ABOUT', 'about')," +
                           "'about')]]/@href")

        # Get the page using requests
        page = requests.get(url)
        # Convert to html from string
        tree = html.fromstring(page.content)
        # Select the 'about' links
        about_links = tree.xpath(about_xpath)
        # Validate the urls and append http if needed
        about_links = list(self._check_url_scheme(link) for link in about_links)
        # Create a list of the 'about' request.Response objects
        about_responses = []
        for link in about_links:
            # Some links aren't qualified URLs in which case
            # requests raises an error - we don't want those in the list
            try:
                page = requests.get(link)
                about_responses.append(page)
            except requests.exceptions.InvalidURL as e:
                log.debug(e)
        # return the list of response objects
        return about_responses
