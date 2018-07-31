"""
This program is to record and control the times dbUpdate runs.
"""
import sqlite3
import getpass
import dbUpdate
from sqlite3 import Error

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

def record_table(conn, sql_script):
    """ update a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.executescript(sql_script)

        #only calls dbUpdate if it's not updated that day already
        dbUpdate.main('final_data.db')
    except Error as e:
        print(e)
        print 'Data has already been uploaded once today. Cannot auto upload again.'

#executing script
def main(dbname,table_name):
    user = getpass.getuser()
    database = 'C:\\sqlite\\' + dbname
    conn = create_connection(database)
    sql_script = 'insert into ' + table_name + " values(date('now','localtime'), \'" + user + "\')" 
    record_table(conn,sql_script)

main('final_data.db','updates_ran')