# -*- coding: utf-8 -*-
import chwrapper


class CompaniesHouseClient():
    def __init__(self):
        self._ch = chwrapper.Search()

    def get_company_data(self, k, v):
        pc = v['postal_code']
        r = self._ch.search_companies(k, items_per_page=200)
        items = r.json()['items']
        c_numbers = []
        for item in items:
            if item['address'].get('postal_code') == pc:
                c_numbers.append(item['company_number'])
        return {'company_numbers': c_numbers}


ch_client = CompaniesHouseClient()
