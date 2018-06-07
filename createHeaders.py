import csv, ast, psycopg2
import string

Error =  (ValueError, AssertionError,SyntaxError) 

def dataType(val, current_type):
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

def shortnameAdjust(shortname):
        """
        Used to find similar key words of named files
        """
        #dictionary of similar words
        stored = {'SH':['sh','shanghai','shang hai'],'BJ':['bj','beijing','bei jing'],'SZ':['sz','shenzhen','shen zhen'],
        'CD':['cd','chengdu', 'cheng du','chendu','chen du'], 'NJ':['nj','nanjing','nan jing', 'nan jin', 'nanjin'], 'HZ':[
        'hz','hangzhou', 'hang zhou'],'WH':['wh','wuhan','wu han']}

        short = str(shortname).lower()
        
        for key, value in stored.items():
            for word in value:
                if word in short:
                    return key
            
        return shortname

def currentHead(filename, shortname):
    """
    input:
        filename - an opened csv file 
    returns:
        statement - a string that emulates the sql command to creating a table according to the types from csv file
    """
    longest, headers, type_list = [], [], []
    
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
    
    #build statement
    short = shortnameAdjust(shortname)
    statement = 'create table  '+ short + ' ('
    for i in range(len(headers)):

        #handling edge cases
        headers[i] = headers[i].replace('(', " ")
        headers[i] = headers[i].replace(')', " ")
        headers[i] = headers[i].replace('.', " ")
        headers[i] = headers[i].lstrip().rstrip()
        headers[i] = headers[i].replace(' ', "_")
        headers[i] = headers[i].replace('__', "_")
        if '\xef\xbb\xbf' in headers[i]:
            headers[i] = headers[i][3:]

        #output the sql command line string    
        if type_list[i] == 'varchar':
            statement = (statement + '{} varchar({}),').format(headers[i].lower(), str(longest[i]))
        else:
            statement = (statement + '{} {}' + ',').format(headers[i].lower(), type_list[i])

    statement = statement[:-1] + ');'
    return statement



    