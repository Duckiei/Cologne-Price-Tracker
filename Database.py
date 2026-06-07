# ------------------- IMPORT STATEMENTS -------------------#
import sqlite3
import pandas
import datetime

# ------------------- FUNCTIONS / METHODS -------------------#


# Adds a cologne to be tracked into the Database
def setDB(title, price, quantity, url):
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()

    # If that cologne isn't being tracked already, then create a table for it, otherwise don't
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{title}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Price REAL,
        Quantity INTEGER,
        DateScraped TEXT,
        URL TEXT
    )""")

    # Add data points to under that colognes table
    cursor.execute(
        f"""INSERT INTO "{title}" (Price, Quantity, DateScraped, URL) VALUES (?,?,?,?)""",
        (
            price,
            quantity,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            url,
        ),
    )

    # Close everything
    conn.commit()
    cursor.close()
    conn.close()


# Uses pandas library to get the contents of a table as a DataFrame (Price date graph)
def getPriceDateDF(table):
    conn = sqlite3.connect("colognePriceTracker.db")
    dataFrame = pandas.read_sql_query(
        f'''SELECT Price,DateScraped FROM "{table}"''', conn
    )
    conn.close()

    return dataFrame


# Dataframe for quantity date graph
def getQuantityDateDF(table):
    conn = sqlite3.connect("colognePriceTracker.db")
    dataFrame = pandas.read_sql_query(
        f'''SELECT Quantity,DateScraped FROM "{table}"''', conn
    )
    conn.close()

    return dataFrame


# Gets all of the tables within the database
def getTables():
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()
    tables = []

    cursor.execute('''SELECT * FROM sqlite_master WHERE type="table"''')
    tablesTemp = cursor.fetchall()

    for tableTuple in tablesTemp:
        if not (tableTuple[1] == "sqlite_sequence"):
            tables.append(tableTuple[1])

    cursor.close()
    conn.close()

    return tables


# Returns the URL of tracked fragrance
def getURL(title):
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT URL FROM "{title}" LIMIT 1""")
    url = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return url


# Delete a table
def removeTable(title):
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()

    cursor.execute(f'''DROP TABLE IF EXISTS "{title}"''')

    conn.commit()
    cursor.close()
    conn.close()


# Get most recent quantity that was scraped from database
def getLatestQuantity(title):
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()

    cursor.execute(
        f"""SELECT Quantity FROM "{title}" ORDER BY DateScraped DESC LIMIT 1"""
    )
    latestQuantity = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return latestQuantity


# Get most recent price that was scraped from database
def getLatestPrice(title):
    conn = sqlite3.connect("colognePriceTracker.db")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT Price FROM "{title}" ORDER BY DateScraped DESC LIMIT 1""")
    latestPrice = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return latestPrice


# ------------------- TESTING -------------------#
