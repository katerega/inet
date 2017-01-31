# -*- coding: utf-8 -*-

"""
inet.sources.html_scraper
-------------------------

Provides the HtmlScraper class, which contains
methods for scraping websites for relevant information

"""

import logging
import requests

from lxml import html
from lxml.etree import XMLSyntaxError
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class HtmlScraper():
    """Provides html scraping methods for data discovery.

    Returns
    -------
    HtmlScraper object

    Examples
    --------
    >>> HtmlScraper = inet.sources.html_scraper.HtmlScraper()
    """

    def check_url_scheme(self, url):
        """Check URL validity."""
        if not urlparse(url).scheme:
            url = "http://" + url
        return url

    def get_links_using_xpath(self, tree, xpath):
        """Extract elements from tree using xpath."""
        return list(self.check_url_scheme(str(link)) for
                    link in tree.xpath(xpath))

    def request_url(self, url):
        """Wrap a requests.get() method in exception handlers."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as e:
            logger.debug(e)
        except requests.exceptions.TooManyRedirects as e:
            logger.debug(e)
        except requests.exceptions.InvalidURL as e:
            logger.debug(e)
        except requests.exceptions.HTTPError as e:
            logger.debug(e)

    def scrape(self, url, about=True, about_xpath=None):
        """Scrape the HTML of company websites.

        Search the html returned by the address specified in 'url'. Extracts
        HTML from any about pages that are present. Also extracts twitter
        handles from the html.

        Parameters
        ----------
        url: string
            A string representing the url of the site to be scraped
        about: Boolean, default True
            Set to False if about pages shouldn't be scraped.
        about_xpath: string, default None
            Custom xpath. If not supplied a preset xpath is used that
            extracts hrefs from occurences of 'about' in <a> elements

        Returns
        -------
        Dictionary of form {'about_html: []', 'twitter_links': []} where
        'about_html' is a list of html documents from the scrape, and
        'twitter_links' is a list of twitter handle links found in the html.
        """
        if about_xpath is None:
            about_xpath = ("//a[text()[contains(translate(., 'ABOUT', " +
                           "'about'), 'about')]]/@href")

        url = self.check_url_scheme(url)
        responses = []
        try:
            page = self.request_url(url)
            responses.append(page.content)
            tree = html.fromstring(page.content)
        except AttributeError as e:
            # Invalid url or no data returned
            logger.debug(e)
            return None
        except XMLSyntaxError as e:
            logger.debug(e)
        except:
            logger.debug()

        about_links = self.get_links_using_xpath(tree, about_xpath)
        for link in about_links:

            try:
                page = self.request_url(link)
            except requests.exceptions.InvalidSchema:
                logger.info("No schema for link {}".format(link))
                page = []

            if page:
                responses.append(page.content)

        logger.info("Found {} about pages in {}".format(len(responses), url))
        return responses

    def twitter_handles(self, html_str, twitter_xpath=None):
        """Search an html tree for twitter links."""
        if twitter_xpath is None:
            twitter_xpath = ("//a[contains(@href,'twitter.com')]/@href")

        tree = html.fromstring(html_str)
        return self.get_links_using_xpath(tree, twitter_xpath)


html_scraper = HtmlScraper()
