# -*- coding: utf-8 -*-
import pytest
import csv
import vcr

from inet.inet import Inet


@pytest.fixture(scope='session')
def temp_file(tmpdir_factory):
    headers = ['name', 'h1']
    rows = [('a', 'b'), ('c', 'd')]
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
        rows = inet.data
        assert len(rows) == 2
        assert rows['a'] == {'h1': 'b'}

    def test_start(self, temp_file):
        inet = Inet(data_file=str(temp_file))
        assert inet.start() is None


if __name__ == '__main__':
    pytest.main()
