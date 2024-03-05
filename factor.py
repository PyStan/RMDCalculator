import psycopg2
import pandas as pd
from sqlalchemy import create_engine
#
class Factor:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    #     spouse_age default is Life Expectancy Factor because if spouses age is not provided/ or needed this is the paramenter needed to query database
    def all_tables(self, age, table, spouse_age="Life Expectancy Factor"):
        conn = psycopg2.connect(database="rmd tables", user="postgres", password="", host="localhost", port="5433")
        cur = conn.cursor()
        cur.execute(f'SELECT "{spouse_age}" FROM "{table}" WHERE "Age" = %s;', (int(age),))
        result = cur.fetchone()

        if result is not None:
            value_to_retrieve = result[0]
            return value_to_retrieve
        else:
            return "ERROR while retrieving value in the tables"

        cur.close()
        conn.close()
