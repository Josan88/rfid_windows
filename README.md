# Python RFID program
A brief description of the project.

# Installation
Instructions on how to install the project.

# Usage
This script is used to read RFID tags and store the data in a MySQL database. It listens for incoming data on a TCP/IP socket and processes the data to extract RFID tag information. The script then checks if the tag is registered in the MySQL database. If the tag is registered, the script updates the last_seen column for the tag and inserts a new record into the car_logbook table. If the tag is not registered, the script logs the event and continues listening for incoming data.

The script also updates the last_seen column for the RFID reader in the rfid_reader table whenever it receives a specific message from the reader.

The script uses a configuration file (config.yaml) to specify the server IP address, server port, and MySQL database connection details.

The script also creates a system tray icon that allows the user to view the log file and exit the script.

Functions:
- connect_to_database(): Connects to the MySQL database and returns a connection object.
- insert_record(mydb, epidString, timestamp, client_address): Inserts a new record into the car_logbook table.
- update_record(mydb, epidString, timestamp, client_address): Updates the last_seen column for a registered RFID tag.
- update_reader(mydb, timestamp, client_address): Updates the last_seen column for the RFID reader.
- select_record(mydb, epidString): Checks if a record exists in the registered_rfid table for a given RFID tag.
- crc16_calc(data, crc=0xFFFF, xorout=0): Calculates the CRC16 checksum for a given data string.
- process_tag(mydb, tag, client_address): Processes a single RFID tag and updates the database if necessary.
- on_connect(icon): Callback function that is called when the system tray icon is clicked. Starts listening for incoming data on the TCP/IP socket.

# License
The license under which the project is released.

# Credits
