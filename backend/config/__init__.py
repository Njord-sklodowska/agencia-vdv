import pymysql
pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.can_return_columns_from_insert = False
DatabaseWrapper.can_return_rows_from_bulk_insert = False