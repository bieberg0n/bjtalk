import socket
import pyaudio
import sys
import json
import queue
from struct import unpack
from threading import Thread


# CHUNK = 1024
# WIDTH = 2
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5


def play(q):
    p = pyaudio.PyAudio()
    stream = p.open(format=1,
                    channels=1,
                    rate=22050,
                    # input=True,
                    output=True,
                    frames_per_buffer=1024)
    while True:
    #     data, addr = cli.recvfrom(4096)
        data = q.get()
        stream.write(data, 1024)


def record(cli, serv_addr, stream):
    while True:
        data = stream.read(1024)
        cli.sendto(data, serv_addr)


def get_addr_from_data(bytes_):
    # print(bytes_)
    # ip = '.'.join([str(unpack('B', i)) for i in bytes_[:4]])
    ip = '.'.join([str(i) for i in bytes_[:4]])
    # print(ip)
    port = unpack('>H', bytes_[4:])
    return (ip, port)


def bjtalk(cli_addr, serv_addr):

    p = pyaudio.PyAudio()
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.bind(cli_addr)

    # stream = p.open(format=p.get_format_from_width(WIDTH),
    stream = p.open(format=1,
                    channels=1,
                    rate=22050,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)

    print('connect to {}'.format(serv_addr))
    t = Thread(target=record, args=(cli, serv_addr, stream,))
    t.setDaemon(True)
    t.start()

    print("* recording")
    queues = dict()
    while True:
        data, _ = cli.recvfrom(4102)
        addr_bytes, data = data[:6], data[6:]
        addr = get_addr_from_data(addr_bytes)

        if queues.get(addr):
            queues[addr].put(data)

        else:
            print('{} incoming'.format(addr))
            q = queue.Queue()
            t = Thread(target=play, args=(q, ))
            t.setDaemon(True)
            t.start()
            queues[addr] = q
            queues[addr].put(data)

    print("* done")

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    if len(sys.argv[1:]) < 1:
        print('''{
    "listen":"0.0.0.0:20171",
    "server":"example.com:20170"
}''')

    else:
        json_file = sys.argv[1]
        with open(json_file) as f:
            cfg = json.loads(f.read())

        cli_ip, cli_port_str = cfg['listen'].split(':')
        serv_ip, serv_port_str = cfg['server'].split(':')
        cli_addr = (cli_ip, int(cli_port_str))
        serv_addr = (serv_ip, int(serv_port_str))

        bjtalk(cli_addr, serv_addr)
