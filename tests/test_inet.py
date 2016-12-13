# -*- coding: utf-8 -*-
import pytest
import csv

from inet.inet import Inet


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

    def test_read_csv(self, tmpdir):
        headers = ['header1', 'header2']
        rows = [('AA', 'BB'), ('CC', 'DD')]
        temp_file = tmpdir.mkdir("sub").join("temp.csv")
        with open(str(temp_file), 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)
        inet = Inet(data_file=str(temp_file))
        rows = inet.rows
        assert len(rows) == 2
        assert rows[0].header1 == 'AA'
        assert rows[0].header2 == 'BB'
        assert rows[1].header1 == 'CC'
        assert rows[1].header2 == 'DD'

        with pytest.raises(AttributeError):
            assert rows[0].header3 == 'AA'

if __name__ == '__main__':
    pytest.main()
