import os
import threading
import time
import pyodbc
import random
import urllib.request
import string
from influxdb import InfluxDBClient

sql_server = os.environ.get('DBSERVER')
sql_db = os.environ.get('DBDATABASE')
sql_user = os.environ.get('DBUSER')
sql_pass = os.environ.get('DBPASS')
iterations = os.environ.get('ITERATIONS')
junksize = os.environ.get('JUNKSIZE')
global hostname
hostname = os.environ.get('HOSTNAME')

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]

def rand_name():
   name = ' '.join([name_words[random.randint(0, (len(name_words) - 1))] for i in range(2)])
   return name

def influx_connect():
    global influxclient
    print("Connecting to InfluxDB...")
    try:
        influxclient = InfluxDBClient(host='influxdb', port=8086, database='sqldata')
    
    except:
        print("Unable to connect to InfluxDB")
        return
    
    influxclient.create_database("sqldata")


def sql_connect():
    global sqlconn
    print("Connecting to SQL...")
    sqlconn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};server=%s;database=%s;uid=%s;pwd=%s' %
        ( sql_server, sql_db, sql_user, sql_pass ) )

def randomString(stringLength=junksize):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def run_writer(times, junksize):
    global sqlconn
    global json_body
    global hostname

    print("Inserting records ...")

    junk = randomString(junksize)
    x = 0
    while (x < int(times)):
        age = random.randint(1,101)
        name = rand_name()
        city = rand_name()

        start = time.time()

        cursor = sqlconn.cursor()
        cursor.execute("INSERT INTO TestDB.dbo.Person (Name, Age, City, Junk) VALUES (?, ?, ?, ?)", (name, str(age), city, str(junk)) )
        sqlconn.commit()

        end = time.time()
        elapsed = (end - start)

        result = { 
            "measurement": "writelatency",
            "tags": { 
                "writer": hostname 
                },
            "time": time.time_ns(),
            "fields": { 
                "duration": elapsed 
                }
            }

        json_body.append(result)

        x = x + 1



print("Environment Info")

print("DB Server: ", sql_server)
print("DB Database: ", sql_db)
print("DB User: ", sql_user)
print("DB Password: ", sql_pass)
print("Iterations per loop: ", iterations)
print("Junksize (KiloBytes): ", int(junksize))

global sqlconn
global influxclient
global json_body

sql_connect()
influx_connect()

var = 1
while var == 1 :

    json_body.clear()

    run_writer(iterations, int(junksize))

    influxclient.write_points(json_body, database='sqldata', time_precision='n', batch_size=10000, protocol='json')