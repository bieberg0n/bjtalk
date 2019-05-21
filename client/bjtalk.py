import time
import socket
import queue
from threading import Thread
import pyaudio


def log(*args):
    print(*args)


class BjtalkClient:
    def __init__(self, serv_addr):
        # ('127.0.0.1', 27010)
        self.serv_addr = serv_addr
        self.c = socket.socket(2, 2)
        self.q = queue.Queue()
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=p.get_format_from_width(1),
            channels=1,
            rate=22500,
            input=True,
            output=True,
            frames_per_buffer=256)

    def ping(self):
        while True:
            self.c.sendto(b'pinga', self.serv_addr)
            time.sleep(2)

    def record(self):
        while True:
            data = self.stream.read(256)
            self.c.sendto(data, self.serv_addr)
            # self.q.put(data)
            # return data

    def play(self, data):
        self.stream.write(data, 256)

    def run(self):
        Thread(target=self.ping).start()
        # Thread(target=self.record).start()

        while True:
            data, _ = self.c.recvfrom(2048)
            # data = self.record()
            # data = self.q.get()
            if data.startswith(b'ping'):
                log(data[4:])

            else:
                self.play(data)
                # Thread(target=self.play, args=(data,)).start()


def main():
    # c = socket.socket(2, 2)
    # c2 = socket.socket(2, 2)
    # c.sendto(b'ping', ('127.0.0.1', 27010))
    # c2.sendto(b'ping', ('127.0.0.1', 27010))
    # c2.sendto(b'test', ('127.0.0.1', 27010))
    # while True:
    #     log(c.recvfrom(512))
    serv_addr = ('127.0.0.1', 27010)
    cli = BjtalkClient(serv_addr)
    cli.run()


if __name__ == '__main__':
    main()