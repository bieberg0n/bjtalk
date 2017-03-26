import socket
import time
import pprint


# users = {
# ('127.0.0.1', 20170):233,
# ('127.0.0.2', 20170):234
# }

def handle(data, addr, users, serv):
    [serv.sendto(data, user) for user in users if user != addr]
    return


def start_serv():
    users = dict()
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv.bind(('0.0.0.0', 20170))
    clock = int(time.time())

    while True:
        now = int(time.time())
        if now - clock > 60:
            users = {user: users[user] for user in users.keys() if (now-users[user]) < 60}
            pprint.pprint(users)
            clock = now

        else:
            pass

        data, addr = serv.recvfrom(4096)
        users[addr] = now
        print(addr, len(data))
        handle(data, addr, users, serv)


if __name__ == '__main__':
    start_serv()
