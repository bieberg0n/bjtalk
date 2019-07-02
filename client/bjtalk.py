#!/usr/bin/env python3

"""bjtalk.py
Usage:
  bjtalk.py (-s <SERVER>) (-p <SERVER_PORT>) (-u <USERNAME>)

Examples:
  bjtalk.py -s 'example.com' -p '27010' -u 'Tom'

Options:
  -h --help       Show this screen
  -s SERVER       server
  -p SERVER_PORT  server port
  -u USERNAME
"""

import time
import socket
import queue
from threading import Thread
from docopt import docopt
import pyaudio


def log(*args):
    print(*args)


class BjtalkClient:
    def __init__(self, serv_addr, username):
        # ('127.0.0.1', 27010)
        self.serv_addr = serv_addr
        self.username = username
        self.c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.c.bind(('0.0.0.0', 27011))
        self.q = queue.Queue()
        p = pyaudio.PyAudio()
        self.buf_len = 512
        self.stream = p.open(
            format=p.get_format_from_width(2),
            channels=1,
            rate=22500,
            input=True,
            output=True,
            frames_per_buffer=self.buf_len)

    def ping(self):
        while True:
            self.c.sendto(b'ping' + self.username.encode(), self.serv_addr)
            time.sleep(2)

    def record(self):
        while True:
            data = self.stream.read(self.buf_len)
            self.c.sendto(data, self.serv_addr)
            # self.q.put(data)

    def play(self, data):
        # time.sleep(1)
        self.stream.write(data, self.buf_len)

    def run(self):
        Thread(target=self.ping).start()
        Thread(target=self.record).start()

        while True:
            data, _ = self.c.recvfrom(2048)
            # data = self.q.get()
            if data.startswith(b'ping'):
                log(data[4:])

            else:
                # self.play(data)
                Thread(target=self.play, args=(data,)).start()


def main():
    args = docopt(__doc__)
    serv = args.get('-s').strip('\'\"')
    port = int(args.get('-p'))
    name = args.get('-u').strip('\'\"')

    serv_addr = (serv, port)
    cli = BjtalkClient(serv_addr, name)
    cli.run()


if __name__ == '__main__':
    main()