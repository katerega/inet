# -*- coding: utf-8 -*-
import pytest
import vcr

from inet.sources.html_scraper import html_scraper, HtmlScraper


class TestHtmlScrape():
    html_scraper = html_scraper

    def test_url_validity(self):
        assert 'http://www.ok.com' == self.html_scraper.check_url_scheme('http://www.ok.com')

    def test_scheme_gets_prepended(self):
        assert 'http://www.ok.com' == self.html_scraper.check_url_scheme('www.ok.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/htnl_scrape_custom_xpath.yaml')
    def test_custom_about_xpath(self):
        about_xpath = "//a[contains(@href,'twitter.com')]/@href"
        about_html = html_scraper.scrape('http://www.nesta.org.uk',
                                         about_xpath=about_xpath)
        assert len(about_html) == 3

    @vcr.use_cassette('fixtures/vcr_cassettes/no_twitter_xpath')
    def test_no_twitter_xpath(self):
        twitter_xpath = ("//a[text()[contains(translate(., 'ABOUT', " +
                         "'about'), 'about')]]/@href")
        about_html = html_scraper.scrape('https://www.nesta.org.uk')

        assert 'www.nesta.org.uk' in str(about_html[0]).split('/')
        assert len(about_html) == 2

    def test_html_scraper_object(self):
        assert isinstance(html_scraper, HtmlScraper)
