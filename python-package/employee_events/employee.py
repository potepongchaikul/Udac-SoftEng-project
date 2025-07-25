# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Define a subclass of QueryBase
# called Employee
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    name = "employee"
    
    # The `names` will receive no arguments.
    # This method returns a list of tuples
    # by calling 'query' method in sql_execution.py
    def names(self):
        
        # The SQL query will select
        # three columns:
        #   1. The employee's first name
        #   2. The employee's last name
        #   3. The employee's id
        # This query returns 2-column data
        # for all employees in the database
        # containing their full name and their id
        query_string = f"""
            select 
                concat(first_name, " ",last_name) as full_name, 
                {self.name}_id
            from
                {self.name}
            """
        
        results = super().query(query_string)
        return results
    
    # The `username` method will receive:
    # `id` argument and return a list of tuples
    # from an sql execution
    def username(self, id):
        
        # SQL query:
        #   - Selects an employees full name
        #   - Filter with a WHERE clause
        #     to only return the full name of the employee
        #     with an id equal to the id argument
        query_string = f""" 
            select
                concat(first_name, " ",last_name) as full_name
            from
                {self.name}
            where
                {self.name}.{self.name}_id = {id}
            """
        results = super().query(query_string)
        return results


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    def model_data(self, id):
        query_string = f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """

        results = super().pandas_query(query_string)
        return results
