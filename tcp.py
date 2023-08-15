import socket

# A list of detected filtered and unique epid for each tags
epidList = []

# Create a TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8010))
server.listen(1)

print("Waiting for connection")


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
                if (
                    epidString not in epidList and epidString != ""
                ):  # hardcoded to ignore heartbeat signal
                    epidList.append(epidString)
                    print(epidList)
            i += tagLength + 4


while True:
    connection, address = server.accept()
    print("Connected")
    data = connection.recv(1024)
    tagSearch(data)
