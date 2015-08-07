from django.db.models import Aggregate

from k2.utils.django.db.models.sql import aggregates as k2_aggregates_module

class IfnullSum(Aggregate):
    """IfnullSum aggregate definition sums col with 0 when no rows"""
    name = 'IfnullSum'
    def add_to_query(self, query, alias, col, source, is_summary):
        klass = getattr(k2_aggregates_module, self.name)
        aggregate = klass(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate
