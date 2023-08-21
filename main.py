import time
import socket
import mysql.connector
import logging
import pystray
from PIL import Image
import subprocess
import yaml


# Connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host=config["sql"]["db_host"],
        user=config["sql"]["db_user"],
        passwd=config["sql"]["db_password"],
        database=config["sql"]["db_name"],
    )


# Insert a new record into the database
def insert_record(mydb, epidString, timestamp, client_address):
    sql = "INSERT INTO car_logbook (epid, car_seen_datetime, reader_ip) VALUES (%s, %s, %s)"
    val = (epidString, timestamp, client_address[0])
    with mydb.cursor() as mycursor:
        mycursor.execute(sql, val)
        mydb.commit()


# Update an existing record in the database
def update_record(mydb, epidString, timestamp, client_address):
    sql = "UPDATE registered_rfid SET car_lastseen = %s, reader_ip = %s WHERE epid = %s"
    val = (timestamp, client_address[0], epidString)
    with mydb.cursor() as mycursor:
        mycursor.execute(sql, val)
        mydb.commit()


# Update reader last seen in the database
def update_reader(mydb, timestamp, client_address):
    sql = "UPDATE rfid_reader SET reader_lastseen = %s WHERE reader_ip = %s"
    val = (timestamp, client_address[0])
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


# CRC check function
def crc16_calc(data, crc=0xFFFF, xorout=0):
    for i in range(len(data)):
        t = (crc >> 8) ^ data[i]
        t = t ^ t >> 4
        crc = (crc << 8) ^ (t << 12) ^ (t << 5) ^ (t)
        crc &= 0xFFFF
    return crc ^ xorout


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
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Find the registered tag in mysql database
        # If tag is found, update the last_seen column
        # If tag is not found, insert the tag into the database
        resp = select_record(mydb, epidString)

        if epidString != "":
            if resp == True:
                update_record(mydb, epidString, timestamp, client_address)
                update_reader(mydb, timestamp, client_address)
                insert_record(mydb, epidString, timestamp, client_address)
                logging.info("Tag found")

            elif resp == False:
                logging.info("Tag not found")


def on_connect(icon):
    icon.visible = True
    with connect_to_database() as mydb:
        while True:
            try:
                # Receive data from the client
                data = connection.recv(1024)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if data.hex() == "aaaaff06c10215e8a2":
                    update_reader(mydb, timestamp, client_address)
                    logging.info("Reader last seen updated")
                elif data:
                    rawDataLength = len(data)
                    i = 0
                    while i < rawDataLength:
                        if data[i] == 170 and data[i + 1] == 170:
                            process_tag(mydb, data[i:], client_address)
                            i += data[i + 3] + 4
                        else:
                            i += 1

            except socket.timeout:
                logging.error("Receive timed out")
                connection.close()
                exit()

            except Exception as e:
                logging.error("Error: %s", e)
                connection.close()
                exit()


if __name__ == "__main__":
    # Clear log file
    open("rfid.log", "w").close()

    logging.basicConfig(
        filename="rfid.log", level=logging.INFO, format="%(asctime)s %(message)s"
    )

    # Load config file
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Create a tray icon
    image = Image.open("rfid-icon.jpg")

    # Create a menu that pops up when the tray icon is clicked
    # The menu has two options: View log and Exit
    menu = pystray.Menu(
        pystray.MenuItem(
            "View log",
            lambda: (subprocess.Popen(["notepad.exe", "rfid.log"])),
        ),
        pystray.MenuItem(
            "Exit",
            lambda: (
                connection.close(),
                logging.info("Connection closed"),
                icon.stop(),
            ),
        ),
    )

    # Create the tray icon
    icon = pystray.Icon("RFID Reader", image, "RFID Reader", menu)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout period on the socket
    sock.settimeout(5)

    # Bind the socket to the port
    server_address = (config["server_ip"], config["server_port"])

    logging.info("Starting up on %s port %s" % server_address)
    
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    while True:
        try:
            connection, client_address = sock.accept()
            break
        except socket.timeout:
            logging.error("Reader connection timed out")

    logging.info("Connection from %s", client_address)

    # Start the tray icon
    icon.run(on_connect)
