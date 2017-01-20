# -*- coding: utf-8 -*-
import logging

import chwrapper

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CompaniesHouseClient():
    def __init__(self):
        self._ch = chwrapper.Search()

    def get_company_data(self, k, v):
        """Search companies house for the data"""
        try:
            pc = v['postal_code']
        except AttributeError:
            logger.warn("No postal code found for {}".format(k))
            return []

        r = self._ch.search_companies(k, items_per_page=200)
        items = r.json()['items']
        data = []

        for item in items:
            try:
                if item['address'].get('postal_code') == pc:
                    data.append(item)
            except AttributeError:
                logger.info("No address item for {}")
        return data


ch_client = CompaniesHouseClient()
