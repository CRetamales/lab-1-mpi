import psycopg2
from psycopg2 import extras

class Database:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.create_table()

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

    def insert_data(self, station, temp_min, temp_max, temp_mean):
        insert_command = """
        INSERT INTO temperatures (station, temp_min, temp_max, temp_mean)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_command, (station, temp_min, temp_max, temp_mean))

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM temperatures")
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        self.connection.close()

