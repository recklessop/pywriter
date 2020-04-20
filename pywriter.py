import os
import threading

def run_writer():
    threading.Timer(5.0, run_writer).start()
    print("Function Running...")

print("Environment Info")

print("DB User: ", os.environ.get('DBUSER'))
print("DB Password: ", os.environ.get('DBPASS'))
print("DB Server: ", os.environ.get('DBSERVER'))


run_writer()
