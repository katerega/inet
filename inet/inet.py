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

    def _get_links_using_xpath(self, tree, xpath):
        return list(self._check_url_scheme(str(link)) for link in tree.xpath(xpath))

    def scrape_html(self,
                    url,
                    about=True,
                    about_xpath=None,
                    twitter_handles=True,
                    twitter_xpath=None):
        """Scrape the HTML of company websites."""

        # Xpath selector for hrefs that contain 'about'
        if about_xpath is None:
            # translate lowercases all upercase A B O U T chars
            about_xpath = ("//a[text()[contains(translate(., 'ABOUT', 'about')," +
                           "'about')]]/@href")

        if twitter_xpath is None:
            twitter_xpath = ("//a[contains(@href,'twitter.com')]/@href")

        page = requests.get(url)
        tree = html.fromstring(page.content)

        about_links = self._get_links_using_xpath(tree, about_xpath)
        twitter_links = self._get_links_using_xpath(tree, twitter_xpath)

        responses = {'about_html': [], 'twitter_links': []}
        for link in about_links:
            # Some links aren't qualified URLs in which case
            # Requests raises an error - we don't want those in the list
            try:
                page = requests.get(link)
                responses['about_html'].append(page)
            except requests.exceptions.InvalidURL as e:
                log.debug(e)

        [responses['twitter_links'].append(link) for link in twitter_links]

        return responses
