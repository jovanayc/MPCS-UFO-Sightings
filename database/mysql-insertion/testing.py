import mysql.connector as mysc
from mysql.connector import errorcode

# remember to fill in with your own pwd!
config = {
    'user':     'root',
    'password': 'porcu555',
    'host':     'localhost',
    'database': 'UFO',
}

try:
    cnx    = mysc.connect(**config)
    cursor = cnx.cursor()
except mysc.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("check username and pwd")
    else:
        print(err)
    exit(1)

cursor.execute("SELECT MAX(SightingID) AS max_id FROM Sightings;")
max_id = cursor.fetchone()[0]
print(max_id)
max_id += 1