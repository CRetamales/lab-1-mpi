import psycopg2
from psycopg2 import extras
"""
This class is responsible for creating the database and the table, inserting data into the table, and fetching data from the table.
"""
class Database:
    """
    This function is the constructor of the class.
    Input: 
        - dbname as <class 'str'> with
        - user as <class 'str'> with
        - password as <class 'str'> with
        - host as <class 'str'> with
        - port as <class 'str'> with
    Output: Nothing
    """
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        # Connect to the database to create it
        self.connection = psycopg2.connect(user=user, password=password, host=host, port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.dbname = dbname
        self.create_db()
        self.connection.close()
        # Connect to the database to create the table
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        self.create_table()


    """
    This function is responsible for creating the database.
    Input: Self object
    Output: Nothing
    """
    def create_db(self):
        try:
            create_db_command = f"""
            CREATE DATABASE {self.dbname}
            """
            self.cursor.execute(create_db_command)
        except psycopg2.errors.DuplicateDatabase:
            pass

    """
    This function is responsible for creating the table.
    Input: Self object
    Output: Nothing
    """
    def create_table(self):
        create_table_command = """
        CREATE TABLE IF NOT EXISTS temperatures (
            station VARCHAR(255),
            temp_min DOUBLE PRECISION,
            temp_max DOUBLE PRECISION,
            temp_mean DOUBLE PRECISION
        )
        """
        self.cursor.execute(create_table_command)

    """
    This function is responsible for inserting data into the table.
    Input: 
        - station as <class 'str'> with
        - temp_min as <class 'float'> with
        - temp_max as <class 'float'> with
        - temp_mean as <class 'float'> with
    Output: Nothing
    """
    def insert_data(self, station, temp_min, temp_max, temp_mean):
        insert_command = """
        INSERT INTO temperatures (station, temp_min, temp_max, temp_mean)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_command, (station, temp_min, temp_max, temp_mean))

    """
    This function is responsible for fetching data from the table.
    Input: Self object
    Output: <class 'list'> with the data fetched
    """
    def fetch_data(self):
        self.cursor.execute("SELECT * FROM temperatures")
        return [dict(row) for row in self.cursor.fetchall()]

    """
    This function is responsible for closing the connection to the database.
    Input: Self object
    Output: Nothing
    """
    def close(self):
        self.connection.close()

