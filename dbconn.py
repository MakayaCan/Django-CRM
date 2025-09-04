from django.db import connections
from django.db.utils import OperationalError

db_conn = connections['default']
try:
    db_conn.cursor()
    print("Database connection OK")
except OperationalError as e:
    print("Database connection failed")
    print(e)
