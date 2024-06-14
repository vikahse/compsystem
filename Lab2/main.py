import sys
from icmplib import ping
import icmplib
import os
import ipaddress
import socket


def check_icmp_blocking(Address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((Address, 80))
        print(f"ICMP packets are allowed to reach the {Address} host")
    except Exception as e:
        print(f"ICMP packets to the {Address} host are blocked")
        sys.exit(1)
    finally:
        s.close()


def check_host_address(Address):
    try:
        ip = ipaddress.ip_address(Address)
        print(f"The host address {Address} is set correctly: {ip}")
    except ValueError:
        print(f"Is not an IPv4/IPv6 Address")


MaxBlockSize = int(os.getenv('MaxBlockSize', 1500))
MinBlockSize = int(os.getenv('MinBlockSize', 0))
Address = os.getenv('Address', 'www.abs.ru')

check_host_address(Address)
check_icmp_blocking(Address)

if MaxBlockSize < 0:
    print("The argument MaxBlockSize cannot be negative")
    sys.exit(1)

if MinBlockSize < 0:
    print("The argument MinBlockSize cannot be negative")
    sys.exit(1)

try:
    response = ping(Address, count=1, interval=0.1, privileged=False)
except icmplib.exceptions as e:
    print(f"Error: {e}")
    sys.exit(1)

LastMinBlockSize = MinBlockSize
LastMaxBlockSize = MaxBlockSize
Flag = False
BlockSize = MaxBlockSize // 2

while not Flag:
    try:
        response = ping(Address, count=1, payload_size=BlockSize, interval=0.1, privileged=False, timeout=0.5)
    except icmplib.exceptions as e:
        print(f'Error: {e}')
        sys.exit(1)
    if not response.is_alive:
        print(f"MTU = {BlockSize} is too large")
        LastMaxBlockSize = BlockSize
        if (LastMaxBlockSize - LastMinBlockSize) < 3:
            BlockSize -= 1
        else:
            BlockSize = LastMinBlockSize + ((LastMaxBlockSize - LastMinBlockSize) // 2)
    else:
        if LastMinBlockSize == BlockSize:
            Flag = True
        else:
            print(f"{BlockSize} can be increased")
            LastMinBlockSize = BlockSize
            BlockSize += (LastMaxBlockSize - LastMinBlockSize) // 2

print(f"Final MTU: {BlockSize}")
