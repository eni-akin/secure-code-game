'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import sqlite3
import os
import re
import math
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            # creates a dummy database inside the folder of this challenge
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            # checks if tables already exist, which will happen when re-running code
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            # if tables do not exist, create them and insert dummy data
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                # inserts dummy data to the 'stocks' table, representing average price on date
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops:
    """Only fixed SQL statements reach SQLite; user values are bound separately."""

    def _execute(self, statement, parameters):
        Create()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'level-4.db')
        with sqlite3.connect(path) as connection:
            return connection.execute(statement, parameters).fetchall()

    def get_stock_info(self, stock_symbol):
        # Keep the exercise's display format; this text is never executed.
        display = "SELECT * FROM stocks WHERE symbol = '%s'" % stock_symbol
        res = "[METHOD EXECUTED] get_stock_info\n[QUERY] " + display + "\n"
        if any(char in stock_symbol for char in ";%&^!#-'"):
            return res + "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        rows = self._execute("SELECT * FROM stocks WHERE symbol = ?", (stock_symbol,))
        return res + ''.join("[RESULT] " + str(row) for row in rows)

    def get_stock_price(self, stock_symbol):
        display = "SELECT price FROM stocks WHERE symbol = '%s'" % stock_symbol
        res = "[METHOD EXECUTED] get_stock_price\n[QUERY] " + display + "\n"
        rows = self._execute("SELECT price FROM stocks WHERE symbol = ?", (stock_symbol,))
        return res + ''.join("[RESULT] " + str(row) + "\n" for row in rows)

    def update_stock_price(self, stock_symbol, price):
        if not isinstance(price, float) or not math.isfinite(price) or price < 0:
            raise ValueError("ERROR: stock price must be a nonnegative finite float")
        display = "UPDATE stocks SET price = '%d' WHERE symbol = '%s'" % (price, stock_symbol)
        self._execute("UPDATE stocks SET price = ? WHERE symbol = ?", (price, stock_symbol))
        return "[METHOD EXECUTED] update_stock_price\n[QUERY] " + display + "\n"

    def _read_request(self, query):
        # Compatibility adapter for the old API: accept only two read operations.
        # Never pass the supplied SQL string to execute/executescript.
        match = re.fullmatch(
            r"\s*SELECT\s+(price|\*)\s+FROM\s+stocks\s+WHERE\s+symbol\s*=\s*'([A-Za-z0-9.\-]{1,20})'\s*",
            query, flags=re.IGNORECASE)
        if match is None:
            raise ValueError("Only stock-price and stock-info lookups are allowed")
        column, symbol = match.groups()
        if column.lower() == 'price':
            return self._execute("SELECT price FROM stocks WHERE symbol = ?", (symbol,))
        return self._execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))

    def exec_multi_query(self, query):
        res = "[METHOD EXECUTED] exec_multi_query\n"
        for part in filter(None, query.split(';')):
            rows = self._read_request(part)
            res += "[QUERY]" + part + "\n"
            res += ''.join("[RESULT] " + str(row) + " " for row in rows)
        return res

    def exec_user_script(self, query):
        # The former arbitrary-script endpoint now accepts one read-only lookup.
        rows = self._read_request(query)
        res = "[METHOD EXECUTED] exec_user_script\n[QUERY] " + query + "\n"
        return res + ''.join("[RESULT] " + str(row) for row in rows)
