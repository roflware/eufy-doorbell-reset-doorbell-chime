import socket
import binascii
import time
import random

# Python 3 version

# Get the port to send data to with the lookup request

actor_id = binascii.hexlify(b"") # 40 character account number here
p2p_did = "HXUSCAM-123456-XXXXX" # 20 character P2P DID here with dashes and case sensitive
p2p_a,p2p_b,p2p_c = p2p_did.split('-', 3)
p2p_mod = (binascii.hexlify(bytes(p2p_a, encoding= 'utf-8')) + b"00000" + bytes(hex(int(p2p_b))[2:], encoding= 'utf-8') + binascii.hexlify(bytes(p2p_c, encoding= 'utf-8')))

DST_UDP_IP = "" # Homebase2 base station internal IP address
DST_UDP_PORT = 32108

HOST_UDP_IP = "" # host IP address where the script is run

rand_port = random.randrange(20000, 65535, 1)

HOST_UDP_PORT = rand_port

MESSAGE_LOOKUP = binascii.unhexlify('f13000020000')
MESSAGE_CHECK_CAM = binascii.unhexlify(b'f1410017' + p2p_mod + b'000000000000')

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

# Turn the digital chime on, then off

UDP_PORT = perm_addr

DIGITAL_CHIME_ON = binascii.unhexlify(b'f1d0009cd1000000585a5948ad06880000000100000000000000000005000000' + actor_id + b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
DIGITAL_CHIME_OFF = binascii.unhexlify(b'f1d0009cd1000001585a5948ad06880000000100000000000000000000000000' + actor_id + b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
SUCCESS_RECEIVED = binascii.unhexlify('ad0684')
#SESSION_END = binascii.unhexlify('f1f00000')

print("UDP target IP: %s" % DST_UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("Turning digital chime on: %s" % DIGITAL_CHIME_ON)

sock.sendto(DIGITAL_CHIME_ON, (DST_UDP_IP, UDP_PORT))

oneTimeOn = 1

while oneTimeOn:
    msg_received = sock.recv(65535)

    if SUCCESS_RECEIVED in msg_received:
        sock.sendto(DIGITAL_CHIME_OFF, (DST_UDP_IP, UDP_PORT))
        print("UDP target IP: %s" % DST_UDP_IP)
        print("UDP target port: %s" % UDP_PORT)
        print("Turning digital chime off: %s" % DIGITAL_CHIME_OFF)
        oneTimeOn = 0
