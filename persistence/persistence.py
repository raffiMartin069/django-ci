import psycopg2
from django.db import connection, ProgrammingError
import re

from utils.commons import Logger


class Database:
    
    @staticmethod
    def validators(query, data, fetch_one=False):
        if not isinstance(fetch_one, bool):
            raise ValueError("fetch_one must be a boolean value")
        
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        
        if data is not None and not isinstance(data, list):
            raise ValueError("data must be a list")
        
        return True

    @staticmethod
    def execute_query(query, fetch_one, data=None):
        """
        Execute a query and return a single result.
        Args:
            query (_type_): Add your query string here.
            fetch_one (_type_): boolean valus must be specified to indicate if the query will return a single result or multiple results.
            data (_type_, optional): Add your data here. Defaults to None. The format should be a list
        Raises:
            e: This will raise an exception if the query is invalid.
        Returns:
            _type_: This will return a single or multiple result.
        """

        is_valid = Database.validators(query, data, fetch_one)

        if not is_valid:
            raise ValueError("Invalid parameters")

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                result = cursor.fetchone() if fetch_one else cursor.fetchall()
            return result
        except Exception as e:
            connection.rollback()
            Logger.error(f"Error during query execution: {e}")
            raise e
        
    @staticmethod
    def insert(query, data):
        """
        Insert a record.
        Args:
            query (_type_): Add your query string here.
            data (_type_): Add your data here. The format should be a list
        Raises:
            e: This will raise an exception if the query is invalid.
        Returns:
            _type_: This will return a single or multiple result.
        """
        is_valid = Database.validators(query, data, False)
        
        if not is_valid:
            raise ValueError("Invalid parameters")
        
        try:
            
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
                result = cursor.lastrowid
                
        except Exception as e:
            connection.rollback()
            error_message = re.sub(r'CONTEXT.*', '', str(e), flags=re.DOTALL).strip()
            raise Exception(error_message)
        
        return result