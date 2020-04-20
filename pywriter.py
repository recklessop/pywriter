import os
import threading
import time
import pyodbc
import random
import urllib.request

sql_server = os.environ.get('DBSERVER')
sql_db = os.environ.get('DBDATABASE')
sql_user = os.environ.get('DBUSER')
sql_pass = os.environ.get('DBPASS')

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]
one_name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])


def rand_name():
   name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
   return name

def sql_connect():
    global sqlconn
    print("Connecting to SQL...")
    sqlconn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};server=%s;database=%s;uid=%s;pwd=%s' %
        ( sql_server, sql_db, sql_user, sql_pass ) )

def run_writer(name, age, city):
    print("Inserting - Name: {}, Age: {}, City: {}") % (name, str(age), city)

    global sqlconn

    #cursor = sqlconn.cursor()
    #cursor.execute('SELECT * FROM TestDB.dbo.Person')
    #columns = [column[0] for column in cursor.description]
    #print(columns)


    #results = []
    #for row in cursor.fetchall():
    #    results.append(dict(zip(columns, row)))

    #print(results)

    cursor.execute("INSERT INTO TestDB.dbo.Person (Name, Age, City) VALUES (?, ?, ?)", (name, str(age), city) )

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

    age = random.randint(1,101)
    name = rand_name()
    city = rand_name()

    start = time.time()
    run_writer(name, age, city)
    end = time.time()
    print("Function took: ", (end - start))
