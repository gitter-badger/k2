from django.db.models.sql.aggregates import *

class IfnullSum(Aggregate):
    sql_function = 'SUM'
    sql_template = 'IFNULL(%(function)s(%(field)s),0)'