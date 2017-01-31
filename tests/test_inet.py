# -*- coding: utf-8 -*-
import pytest
import csv
import vcr

from inet.inet import Inet

@pytest.fixture(scope='session')
def temp_file(tmpdir_factory):
    headers = ['name', 'website', 'postal_code']
    rows = [('a', 'www.nesta.org.uk', ''),
            ('c', 'https://www.nesta.org.uk', '')]
    temporary_file = tmpdir_factory.mktemp('data').join('temp.csv')
    with open(str(temporary_file), 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    return temporary_file


@pytest.fixture(scope='session')
def director_file(tmpdir_factory):
    headers = ['name', 'website', 'postal_code']
    rows = [('J Gardiner Consulting', 'www.jgardiner.co.uk', 'CF35 6HE')]
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
        i = Inet(data_file=str(temp_file))
        rows = i.data
        assert len(rows) == 2
        assert rows['a'] == {'website': 'www.nesta.org.uk',
                             'postal_code': ''}

    def test_start_adds_iteration_key(self, temp_file):
        i = Inet(data_file=str(temp_file))
        data = i.data
        with pytest.raises(KeyError):
            data['a']['iteration']
        i.start(iterations=1)
        assert data['a']['iteration'] == 0

    def test_start_directors_search(self, director_file):
        i = Inet(data_file=str(director_file))
        i.start(iterations=1)
        v = i.data['J Gardiner Consulting']
        assert v['company_data'] is not None
        print(len(v['company_data']))
        assert v['company_data'][0]['company_number'] == '10554177'

if __name__ == '__main__':
    pytest.main()
