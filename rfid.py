import time
import socket

# Create a list to store dictionary of scanned tags and timestamps
tagDataList = []

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

                # Check if the tag has been scanned before
                if epidString in [d["epid"] for d in tagDataList]:
                    # If yes, update the timestamp
                    for d in tagDataList:
                        if d["epid"] == epidString:
                            d["timestamp"] = timestamp
                elif (
                    epidString not in [d["epid"] for d in tagDataList]
                    and epidString != ""
                ):
                    # If no, add the tag to the list
                    tagDataList.append({"epid": epidString, "timestamp": timestamp})

                print(tagDataList)

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
