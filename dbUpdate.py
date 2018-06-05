import sqlite3, csv,ast,glob, copy

Error =  (ValueError, AssertionError) 
def dataType(val, current_type):
    """
    This function is a series of if else statements that tests what var type each row should actually be.
    """
    try:
        # Evaluates numbers to an appropriate type, and strings an error
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar'
    except SyntaxError:
        return 'varchar'
    if type(t) in [int, long, float]:
        if (type(t) in [int, long]) and current_type not in ['float', 'varchar']:
           # Use smallest possible int type
            if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
                return 'smallint'
            elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                return 'int'
            else:
                return 'bigint'
        if type(t) is float and current_type not in ['varchar']:
           return 'decimal'
    else:
        return 'varchar'
def dataTypeMain(filename, shortname):
    """
    input:
        filename - an opened csv file 
    returns:
        type_list - a list that outlines every row's var_type
        longest - the longest length of every row
    """
    longest, headers, type_list = [], [], []
    types = []
    for row in filename:
        if len(headers) == 0:
            headers = row
            for col in row:
                longest.append(0)
                type_list.append('')
        else:
            for i in range(len(row)):
                # NA is the csv null value
                if type_list[i] == 'varchar' or row[i] == 'NA':
                    pass
                else:
                    var_type = dataType(row[i], type_list[i])
                    type_list[i] = var_type
            if len(row[i]) > longest[i]:
                longest[i] = len(row[i])
        types.extend(type_list)
    return type_list, longest
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

def update_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.executescript(create_table_sql)
        #c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_statement(tbname, listValue, type_list):
    """
    Creates a list of actual string command to insert values
    """
    
    all_statements = []
    for i in range(1, len(listValue)):
        statement = "insert into " + tbname + " values ("
        for item in range(len(listValue[i])):
            if type_list[item] != 'varchar':
                statement = statement + listValue[i][item] + ", "  
            else:
                statement = statement + "'" + listValue[i][item] + "', "

        statement = statement[:len(statement)-2]
        statement += ");"
        all_statements.append(statement)
    
    return all_statements

def insert_statements(dbname,tbname,listValue,type_list):

    database = 'C:\\sqlite\\' + dbname
    conn = create_connection(database)
    insertedList = create_statement(tbname, listValue, type_list)
    if conn is not None:
        for statement in insertedList:
            update_table(conn,statement)
    else:
        print("Error! cannot create the database connection.")
    pass

def main(dbname):

    #runs through every csv file in a folder 
    path = "C:\\Users\\SuWi\\Documents\\Project\\Datasets\\*.csv"
    for filename in glob.glob(path):
        ind1 = filename.index('Datasets')
        ind2 = filename.index('.csv')

        #tbname gets the initial of each city; used to identify table names
        tbname = filename[ind1+len('Datasets')+1:ind2]

        #open file
        f = open(filename, 'r')
        read = csv.reader(f)
        type_list, longest = dataTypeMain(read,tbname)

        #open new file because old one will get written over
        f2 = open(filename, 'r')
        read2 = csv.reader(f2)
        listValue = list(read2)
        
        insert_statements(dbname, tbname,listValue,type_list)
        f.close()
        f2.close()
    pass

main('june5.db')