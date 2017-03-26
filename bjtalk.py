import socket
import pyaudio
import sys
import json
from threading import Thread


# CHUNK = 1024
# WIDTH = 2
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5


def play(cli, stream):
    while True:
        data, addr = cli.recvfrom(4096)
        stream.write(data, 1024)


def bjtalk(cli_addr, serv_addr):

    p = pyaudio.PyAudio()
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.bind(cli_addr)

    # stream = p.open(format=p.get_format_from_width(WIDTH),
    stream = p.open(format=1,
                    channels=1,
                    rate=8000,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)

    print("* recording")

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    t = Thread(target=play, args=(cli, stream,))
    t.setDaemon(True)
    t.start()
    print('connect to {}'.format())
    try:
        while True:
            data = stream.read(1024)
            cli.sendto(data, serv_addr)
            # print(len(data))
            # stream.write(data, 1024)

    except KeyboardInterrupt:
        pass

    print("* done")

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    if len(sys.argv[1:]) <= 1:
        print('''{
    "listen":"0.0.0.0:20171",
    "server":"example.com:20170"
''')

    else:
        json_file = sys.argv[1]
        with open(json_file) as f:
            cfg = json.loads(f.read())

        cli_ip, cli_port_str = cfg['listen']
        serv_ip, serv_port_str = cfg['server']
        cli_addr = (cli_ip, int(cli_port_str))
        serv_addr = (serv_ip, int(serv_port_str))

        bjtalk(cli_addr, serv_addr)
