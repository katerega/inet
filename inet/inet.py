# -*- coding: utf-8 -*-
import csv
import os

from collections import namedtuple


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
                self.rows = []
                with open(data_file) as f:
                    f_csv = csv.reader(f)
                    headings = next(f_csv)
                    Row = namedtuple('Row', headings)
                    for r in f_csv:
                        row = Row(*r)
                        self.rows.append(row)
            else:
                raise TypeError("Input file must be of type .csv")
        else:
            raise AttributeError("No data_file path specified as a "
                                 "parameter to Inet object")
