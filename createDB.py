"""
This program creates an SQLite database and inserts the neccessary tables into it.
"""
import sqlite3
Error =  (ValueError, AssertionError) 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def init_tables(dbname, statement_dict):
    """
    dbname -- should be something like file.db
    
    This function is diff from create_tables.
    create_tables actually creates the tables while init_tables takes input the dictionary of string statements to create these tables
    """
    database = 'C:\sqlite\\' + dbname
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        for key,value in statement_dict.items():
            print "here", value
            create_table(conn,value)
    else:
        print("Error! cannot create the database connection.")
    pass