import socket
import pyaudio
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


def main():
    p = pyaudio.PyAudio()
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.bind(('0.0.0.0', 20171))

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
    try:
        while True:
            data = stream.read(1024)
            cli.sendto(data, ('192.168.233.5', 20170))
            print(len(data))
            # stream.write(data, 1024)

    except KeyboardInterrupt:
        pass

    print("* done")

    stream.stop_stream()
    stream.close()

    p.terminate()


main()
