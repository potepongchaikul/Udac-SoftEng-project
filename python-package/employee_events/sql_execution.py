from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Define path variable: `db_path`
# This points to `employee_events.db` file. This directory
# will be subsequently used for establishing database connection
db_path = Path(__file__).parent / "employee_events.db"


# Define a `QueryMixin` class:
# This acts as add-on to the `QueryBase` class in
# query_base.py, by creating connection using `db_path`.
# 
# Methods:
# - `pandas_query`: Return results as Pandas dataframe
# - `query`: Return results as list of tuples

class QueryMixin:
    def pandas_query(self, query_string):
        connection = connect(db_path)
        result = pd.read_sql(query_string, connection)
        connection.close()
        return result

    def query(self, query_string):
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
 
# Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
