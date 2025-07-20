# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies for sql execution
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    name = "team"


    # The `names` will receive no arguments.
    # This method returns a list of tuples
    # by calling 'query' method in sql_execution.py
    def names(self):
        
        # The SQL query will select
        # two columns:
        #   1. Team name
        #   2. Team id
        # This query returns 2-column data
        # for all teams in the database

        query_string = f"""
            select 
                {self.name}_name, {self.name}_id
            from
                {self.name}
            """
        
        results = super().query(query_string)
        return results
    

    def username(self, id):

        # SQL query:
        #   - Selects a team name
        #   - Filter with a WHERE clause
        #     to only return the team data for the given id
        query_string = f""" 
            select
                {self.name}_name
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
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        
        results = super().pandas_query(query_string)
        return results