import pandas as pd
import csv, ast, psycopg2
import glob
import createHeaders, createDB

#Creates a database and stores tables for every CSV file in a folder;
#Uses the createDB and createHeaders to create these tables;
path = "C:\Users\SuWi\Documents\Project\Datasets\*.csv"
table_headers = {}
for filename in glob.glob(path):
    ind1 = filename.index('Datasets')
    ind2 = filename.index('.csv')
    shortname = filename[ind1+len('Datasets')+1:ind2]
    #open file
    f = open(filename, 'r')
    read = csv.reader(f)
    #create the headers for each file
    statement = createHeaders.currentHead(read,shortname) 
    table_headers[shortname] = statement
    f.close()
#print table_headers['HZ']
createDB.init_tables('june5.db',table_headers)



"""
Things to take care of:
    1. date/time in excel
        - look at var type: date_time, date
        - sunset, sunrise, total daylight time may need extra handling
    2. titles of file names
        - "shanghai.csv"?
        - what happens if theres duplicates "HZ" "HZ2"
    3. what happens if the database or table does not exist; or that they already exist? does it overwrite?
    4. check out how qlik can interact with sqlite
"""
