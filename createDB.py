"""
This program creates an SQLite database and inserts the neccessary tables into it.
"""
import sqlite3
Error =  (ValueError, AssertionError, sqlite3.OperationalError) 


def overwrite_question (conn, create_table_sql):
    yes_list = ['yes','y','ok']

    #find table name
    now = str(create_table_sql)
    idx = now.index("(")
    table_name = now[len("create table"):idx].strip()
    #view the tables
    view_tables(conn, table_name, create_table_sql)

    Join = raw_input("Do you wish to overwrite the existing table? (Y,N) ").lower()

    if Join in yes_list:
        #perform overwtie
        
        new_statement = "drop table " + table_name + ";"
        c = conn.cursor()
        c.execute(new_statement)
        print "About to overwrite..."
        c.execute(create_table_sql)
        print "Table " + table_name + " overwritten."
    else:
       pass
def view_tables(conn, table_name,sql_term):
    """
    Used to compare the two tables schema
    """
    #PROBLEM HERE
    c = conn.cursor()
    Join = raw_input("Type 'old' to see existing table values, type 'new' to see new table schema, type 'q' to quit view or not view ").lower()
    if Join == "old":
        print "select * from " + table_name + ";"
        old = c.execute("select * from " + table_name + ";").fetchall()
        for row in old:
            print row 
        view_tables(conn, table_name, sql_term)
    elif Join == "new":
        print sql_term
        view_tables(conn, table_name, sql_term)
    elif Join == "q":
        pass
    else: 
        print "Please choose old, new, or no."
        view_tables(conn, table_name, sql_term)
    


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
        print  e
        
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
        #this happens usually when table already exists
        print str(e) + " or maybe there is a duplicate file"
        overwrite_question(conn,create_table_sql)
        

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
            create_table(conn,value)
    else:
        print("Error! cannot create the database connection.")
    pass
