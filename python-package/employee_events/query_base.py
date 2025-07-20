# Import any dependencies needed to execute sql queries
from sqlite3 import connect
from pathlib import Path
import pandas as pd
from .sql_execution import QueryMixin

# Subclass `QueryMixin` to exploit the inherited `query` and 
# `pandas_query` methods.
class QueryBase(QueryMixin):
    
    # `name`: Class attribute 
    # Set to empty string, but can be overwritten by its 
    # subclass, e.g. Employeee or Team.
    name = ""

    # `names`: Method
    # Set to empty list, but can be overwritten by its 
    # subclass, e.g. Employeee or Team.
    def names(self):
        return []

    # The `event_counts` will exploit the inherited 
    # `pandas_query` method to:
    #     - Inner join `name` (a table) with employee_events
    #     - Query positive events and negative events
    #     - Filter employee_events data by the `id`
    #     - Group and Order those by `event_date`
    #     - Returns a pandas dataframe
    # Ref: (from questions posted in 'Knowledge' forum): 
    #     `name`: Table name ("employee" or "team")
    #     `id`: This id is the specific employee or team ID you want to filter the results for.     
    def event_counts(self, id):
        
        query_string = f"""
            select 
                event_date as Day,
                sum(positive_events) as positive_events, 
                sum(negative_events) as negative_events
            from 
                {self.name} inner join employee_events
            on 
                employee_events.{self.name}_id = {self.name}.{self.name}_id
            where
                {self.name}.{self.name}_id = {id}
            group by
                event_date
            order by 
                event_date
            """
        results = super().pandas_query(query_string)
        return results

    # The `notes` method will retrieve `note_date`
    # and `note` columns filtered by the provided `id`.
    # The result is provided as a Pandas dataframe.
    def notes(self, id):

        query_string = f"""
            select 
                {self.name}_id as `{self.name} ID`,
                note_date as `Note date`, 
                note as `Description`
            from
                notes
            where
                {self.name}_id = {id}
            """
        results = super().pandas_query(query_string)
        return results
    