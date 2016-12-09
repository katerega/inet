# -*- coding: utf-8 -*-
import epo_ops


class OpsClient(epo_ops.RegisteredClient):
    """Wraps the epo_ops Client and RegisteredClient classes"""

    def __init__(self,
                 key,
                 secret,
                 accept_type='JSON',
                 middlewares=None,):
        super().__init__(key,
                         secret,
                         accept_type,
                         middlewares)

    def applicant_search(self,
                         search_term,
                         range_begin=1,
                         range_end=25,
                         constituents=None):
        cql = 'pa={}'.format(search_term)
        return self.published_data_search(cql,
                                          range_begin,
                                          range_end,
                                          constituents)

    def inventor_search(self,
                        search_term,
                        range_begin=1,
                        range_end=25,
                        constituents=None):
        cql = 'in={}'.format(search_term)
        return self.published_data_search(cql,
                                          range_begin,
                                          range_end,
                                          constituents)
