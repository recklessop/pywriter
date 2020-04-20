import os
import threading
import time
import pyodbc

sql_server = os.environ.get('DBSERVER')
sql_db = os.environ.get('DBDATABASE')
sql_user = os.environ.get('DBUSER')
sql_pass = os.environ.get('DBPASS')

def sql_connect():
    global sqlconn
    print("Connecting to SQL...")
    sqlconn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};server=%s;database=%s;uid=%s;pwd=%s' %
        ( sql_server, sql_db, sql_user, sql_pass ) )

def run_writer():
    print("Function Running...")

    global sqlconn

    cursor = sqlconn.cursor()
    cursor.execute('SELECT * FROM TestDB.dbo.Person')
    columns = [column[0] for column in cursor.description]
    print(columns)


    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))

    print(results)
    
    #cursor.execute('''
    #            INSERT INTO TestDB.dbo.Person (Name, Age, City)
    #            VALUES
    #            ('Bob',55,'Montreal'),
    #            ('Jenny',66,'Boston')
    #            ''')
    sqlconn.commit()



print("Environment Info")

print("DB Server: ", sql_server)
print("DB Database: ", sql_db)
print("DB User: ", sql_user)
print("DB Password: ", sql_pass)

global sqlconn

sql_connect()

var = 1
while var == 1 :
    start = time.time()
    run_writer()
    end = time.time()
    print("Function took: ", (end -start))
