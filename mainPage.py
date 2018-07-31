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
    if statement!=None:
        table_headers[shortname] = statement
    f.close()

createDB.init_tables('final_data.db',table_headers)




"""
Notes:
    1. Pros and Cons of Uploading All Data/New Data:
        - history snapshot
    2. Need to change the 

#Used to query dates
select * from BJ where time_recorded > datetime('2018-06-11 14:04:20');

DataBase
1. Similar names taken care of
2. Dates taken care of
3. same existing tables done
4. updating asks for erasing, allows view ---> check 5
5. now data uploads all data again. providing historical snapshot
6. csv file names that do not fit the 7 cities will not be added; shows the printed text on the terminal
"""
