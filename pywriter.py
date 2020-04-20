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
iterations = os.environ.get('ITERATIONS')
junksize = os.environ.get('JUNKSIZE')

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]

def rand_name():
   name = ' '.join([name_words[random.randint(0, (len(name_words) - 1))] for i in range(2)])
   return name

def sql_connect():
    global sqlconn
    print("Connecting to SQL...")
    sqlconn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};server=%s;database=%s;uid=%s;pwd=%s' %
        ( sql_server, sql_db, sql_user, sql_pass ) )

def run_writer(times, junksize):
    global sqlconn

    print("Inserting records ...")

    x = 0
    while (x < int(times)):
        age = random.randint(1,101)
        name = rand_name()
        city = rand_name()
        junk = random.getrandbits(junksize)

        global sqlconn

        cursor = sqlconn.cursor()

        cursor.execute("INSERT INTO TestDB.dbo.Person (Name, Age, City, Junk) VALUES (?, ?, ?, ?)", (name, str(age), city, junk) )

        sqlconn.commit()
        x = x + 1



print("Environment Info")

print("DB Server: ", sql_server)
print("DB Database: ", sql_db)
print("DB User: ", sql_user)
print("DB Password: ", sql_pass)
print("Iterations per loop: ", iterations)

global sqlconn

sql_connect()

var = 1
while var == 1 :
    start = time.time()
    run_writer(iterations, junksize)
    end = time.time()
    print("Function took: ", (end - start))
