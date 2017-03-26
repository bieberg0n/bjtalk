import socket
import time
import pprint
from struct import pack


# users = {
# ('127.0.0.1', 20170):233,
# ('127.0.0.2', 20170):234
# }

def addr_to_bytes(addr):
    ip, port = addr
    ip_bytes = b''.join([pack('B', int(i)) for i in ip.split('.')])
    port_bytes = pack('>H', port)
    return ip_bytes + port_bytes


def handle(data, addr, users, serv):
    addr_bytes = addr_to_bytes(addr)
    [serv.sendto(addr_bytes+data, user) for user in users if user != addr]
    return


def start_serv():
    users = dict()
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv.bind(('0.0.0.0', 20170))
    clock = int(time.time())

    try:
        while True:
            now = int(time.time())
            if now - clock > 5:
                users = {user: users[user] for user in users.keys()
                         if (now-users[user]) < 5}
                pprint.pprint(users)
                clock = now

            else:
                pass

            data, addr = serv.recvfrom(4096)
            users[addr] = now
            # print(addr, len(data))
            handle(data, addr, users, serv)
    except KeyboardInterrupt:
        print('Server exit.')


if __name__ == '__main__':
    start_serv()
