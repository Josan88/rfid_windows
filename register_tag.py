import mysql.connector
import yaml
import socket


# Connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host=config["sql"]["db_host"],
        user=config["sql"]["db_user"],
        passwd=config["sql"]["db_password"],
        database=config["sql"]["db_name"],
    )


# Register a new tag in the database
def register_tag(mydb, epidString):
    sql = "INSERT INTO registered_rfid (epid) VALUES (%s)"
    val = (epidString,)
    with mydb.cursor() as mycursor:
        mycursor.execute(sql, val)
        mydb.commit()


# Check if a record exists in the database
def select_record(mydb, epidString):
    sql = "SELECT * FROM registered_rfid WHERE epid = %s"
    val = (epidString,)
    with mydb.cursor() as mycursor:
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            return True
        else:
            return False


# Process a single tag
def process_tag(mydb, tag, client_address):
    tagLength = tag[3]
    oneTag = tag[: tagLength + 4]
    oneTagCheck = oneTag[: tagLength + 1]
    oneTagCrcBytes = oneTag[tagLength + 1 : tagLength + 3].hex()
    crc16Check = hex(crc16_calc(oneTagCheck))[2:]

    if crc16Check == oneTagCrcBytes:
        epid = oneTag[10:25]
        epidString = epid.hex()

        if select_record(mydb, epidString):
            print("Tag already registered")
        else:
            register_tag(mydb, epidString)
            print("Tag registered")
    else:
        print("CRC check failed")


# CRC check function
def crc16_calc(data, crc=0xFFFF, xorout=0):
    for i in range(len(data)):
        t = (crc >> 8) ^ data[i]
        t = t ^ t >> 4
        crc = (crc << 8) ^ (t << 12) ^ (t << 5) ^ (t)
        crc &= 0xFFFF
    return crc ^ xorout


if __name__ == "__main__":
    # Load config
    with open("config.yaml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (config["server_ip"], config["server_port"])
    print("Starting up on %s port %s" % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Connect to the database
    mydb = connect_to_database()

    while True:
        # Wait for a connection
        print("Waiting for a connection")
        connection, client_address = sock.accept()
        try:
            print("Connection from", client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                if data:
                    tag = bytearray(data)
                    process_tag(mydb, tag, client_address)
                else:
                    print("No more data from", client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()
