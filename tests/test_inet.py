# -*- coding: utf-8 -*-
import pytest
import csv
import vcr

from inet.inet import Inet


@pytest.fixture(scope='session')
def temp_file(tmpdir_factory):
    headers = ['header1', 'header2']
    rows = [('AA', 'BB'), ('CC', 'DD')]
    temporary_file = tmpdir_factory.mktemp('data').join('temp.csv')
    with open(str(temporary_file), 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    return temporary_file


class TestInet():
    """Test the Inet class functions as expected"""
    def test_no_data_file(self):
        with pytest.raises(AttributeError):
            Inet(data_file=None)

    def test_wrong_file_type(self, tmpdir):
        with pytest.raises(TypeError):
            p = tmpdir.mkdir("sub").join("temp.txt")
            p.write("content")
            Inet(data_file=str(p))

    def test_read_csv(self, temp_file):
        inet = Inet(data_file=str(temp_file))
        rows = inet.rows
        assert len(rows) == 2
        assert rows[0].header1 == 'AA'
        assert rows[0].header2 == 'BB'
        assert rows[1].header1 == 'CC'
        assert rows[1].header2 == 'DD'

        with pytest.raises(AttributeError):
            assert rows[0].header3 == 'AA'

    @vcr.use_cassette('fixtures/vcr_cassettes/scrape_html.yaml')
    def test_scrape_html(self, temp_file):
        inet = Inet(data_file=str(temp_file))
        responses = inet.scrape_html('http://www.nesta.org.uk')
        keys = responses.keys()
        assert 'about_html' in keys
        assert 'twitter_links' in keys
        assert responses['about_html'][0].url == 'http://www.nesta.org.uk/about-us'
        assert len(responses['about_html']) == 1
        assert len(responses['twitter_links']) == 2
        assert responses['twitter_links'][0] == 'http://twitter.com/nesta_uk'

    @vcr.use_cassette('fixtures/vcr_cassettes/htnl_scrape_custom_xpath.yaml')
    def test_custom_about_xpath(self, temp_file):
        inet = Inet(data_file=str(temp_file))
        about_xpath = "//a[contains(@href,'twitter.com')]/@href"
        responses = inet.scrape_html('http://www.nesta.org.uk',
                                     about_xpath=about_xpath)
        assert len(responses['about_html']) == 2
        assert len(responses['twitter_links']) == 2
        assert responses['twitter_links'][0] == 'http://twitter.com/nesta_uk'
        assert responses['about_html'][0].url == 'https://twitter.com/nesta_uk'

if __name__ == '__main__':
    pytest.main()
