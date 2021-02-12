import socket
import binascii
import time
import random

# Get the port to send data to with the lookup request

account_number = binascii.hexlify("") # 40 character account number here
p2p_did = binascii.hexlify("") # 23 character P2P DID here

DST_UDP_IP = "" # Homebase2 base station internal IP address
DST_UDP_PORT = 32108

HOST_UDP_IP = "" # host IP address where the script is run

rand_port = random.randrange(20000, 65535, 1)

HOST_UDP_PORT = rand_port

MESSAGE_LOOKUP = binascii.unhexlify('f13000020000')
MESSAGE_CHECK_CAM = binascii.unhexlify('f1410017' + p2p_did)

MESSAGE_PING = binascii.unhexlify('f1e00000')
MESSAGE_PONG = binascii.unhexlify('f1e10000')

print("UDP target IP: %s" % DST_UDP_IP)
print("UDP target port: %s" % DST_UDP_PORT)
print("Sending lookup request to determine port: %s" % MESSAGE_LOOKUP)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST_UDP_IP, HOST_UDP_PORT))

sock.sendto(MESSAGE_LOOKUP, (DST_UDP_IP, DST_UDP_PORT))

data, addr = sock.recvfrom(65535) # buffer size is 65535 bytes
print(addr[1])

perm_addr = addr[1]

sock.sendto(MESSAGE_CHECK_CAM, (DST_UDP_IP, perm_addr))

UDP_PORT = perm_addr

MESSAGE_OFF = binascii.unhexlify('f1d0009cd1000000585a5948a706880000000100000000000000000000000000' + account_number + '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
MESSAGE_ON = binascii.unhexlify('f1d0009cd1000001585a5948a706880000000100000000000000000001000000' + account_number + '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
SUCCESS_OFF = binascii.unhexlify('a70684')
SESSION_END = binascii.unhexlify('f1f00000')

# Send the off signal to the doorbell

print("UDP target IP: %s" % DST_UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("Turning doorbell off: %s" % MESSAGE_OFF)

sock.sendto(MESSAGE_OFF, (DST_UDP_IP, UDP_PORT))

oneTimeOn = 1

while oneTimeOn:
    msg_received = sock.recv(65535)

    if SUCCESS_OFF in msg_received:

        # Send the on signal to the doorbell
        sock.sendto(MESSAGE_ON, (DST_UDP_IP, UDP_PORT))
        print("UDP target IP: %s" % DST_UDP_IP)
        print("UDP target port: %s" % UDP_PORT)
        print("Turning doorbell on: %s" % MESSAGE_ON)
        oneTimeOn = 0
        time.sleep(2) # this can vary -- honestly, you can probably just remove the SESSION_END if it's giving you too much trouble. It will eventually give up anyway
        sock.sendto(SESSION_END, (DST_UDP_IP, UDP_PORT))
