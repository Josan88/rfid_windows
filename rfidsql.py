import mysql.connector
import time

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost", user="rfid", passwd="softworld", database="stc"
)


def sql_insert(mydb, epidString, timestamp):
    mycursor = mydb.cursor()
    sql = "INSERT INTO vehicle_logbook (epid, seen_datetime) VALUES (%s, %s)"
    val = (epidString, timestamp)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def sql_update(mydb, epidString, timestamp):
    mycursor = mydb.cursor()
    sql = "UPDATE rfid SET last_seen = %s WHERE epid = %s"
    val = (timestamp, epidString)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record updated.")


def sql_select(mydb, epidString):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM rfid WHERE epid = %s"
    val = (epidString,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if myresult:
        return True
    else:
        return False


if __name__ == "__main__":
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if sql_select(mydb, "e2806995000050009125b19cacb500"):
        sql_update(mydb, "e2806995000050009125b19cacb500", timestamp)
    else:
        sql_insert(mydb, "e2806995000050009125b19cacb500", timestamp)
