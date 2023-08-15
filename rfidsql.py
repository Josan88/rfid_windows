import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="rfid",
    passwd="softworld",
    database="stc"
)

mycursor = mydb.cursor()


sql = "INSERT INTO vehicle_logbook (epid, seen_datetime) VALUES (%s, %s)"

val = ("1234567890", "2019-01-01 00:00:00")

mycursor.execute(sql, val)

mydb.commit()

print("1 record inserted, ID:", mycursor.lastrowid)
