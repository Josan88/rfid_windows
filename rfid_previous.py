import time
import socket
import mysql.connector
import functools

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost", user="rfid", passwd="softworld", database="stc"
)


# Create a cache decorator
def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in wrapper.cache:
            return wrapper.cache[key]
        else:
            result = func(*args, **kwargs)
            wrapper.cache[key] = result
            return result

    wrapper.cache = {}
    return wrapper


def sql_insert(mydb, epidString, timestamp):
    mycursor = mydb.cursor()
    sql = "INSERT INTO vehicle_logbook (epid, seen_datetime) VALUES (%s, %s)"
    val = (epidString, timestamp)
    mycursor.execute(sql, val)
    mydb.commit()

def sql_update(mydb, epidString, timestamp):
    mycursor = mydb.cursor()
    sql = "UPDATE rfid SET last_seen = %s WHERE epid = %s"
    val = (timestamp, epidString)
    mycursor.execute(sql, val)
    mydb.commit()
    
@cache
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


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ("192.168.2.139", 8010)

print("starting up on %s port %s" % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


# CRC check function
def crc16_calc(data, crc=0xFFFF, xorout=0):
    for i in range(len(data)):
        t = (crc >> 8) ^ data[i]
        t = t ^ t >> 4
        crc = (crc << 8) ^ (t << 12) ^ (t << 5) ^ (t)
        crc &= 0xFFFF
    return crc ^ xorout


def tagSearch(rawData):
    rawDataLength = len(rawData)
    i = 0
    while i < rawDataLength:
        if rawData[i] == 170 and rawData[i + 1] == 170:  # step 1
            tagLength = rawData[i + 3]  # step 2
            oneTag = rawData[
                i : i + tagLength + 3
            ]  # full tag bytes including crc bytes
            oneTagString = oneTag.hex()
            oneTagCheck = oneTag[: tagLength + 1]  # full tag bytes excluding crc bytes
            oneTagCrcBytes = oneTag[tagLength + 1 : tagLength + 3].hex()  # step 3
            crc16Check = hex(crc16_calc(oneTagCheck))[2:]

            if crc16Check == oneTagCrcBytes:
                epid = oneTag[
                    10:25
                ]  # Can be further improved - Will have issues with integrated reader (without antenna)
                epidString = epid.hex()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # Find the registered tag in mysql database
                # If tag is found, update the last_seen column
                # If tag is not found, insert the tag into the database
                resp = sql_select(mydb, epidString)
                if resp == True and epidString != "":
                    sql_update(mydb, epidString, timestamp)
                    sql_insert(mydb, epidString, timestamp)
                elif resp == False and epidString != "":
                    print("Tag not found")

            i += tagLength + 4  # step 4


while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()

    try:
        print("connection from", client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            tagSearch(data)

    finally:
        # Clean up the connection
        connection.close()
