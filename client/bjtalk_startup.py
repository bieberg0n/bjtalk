import json
import bjtalk

json_file = 'bjtalk.json'


def main(json_file):
    with open(json_file) as f:
        cfg = json.loads(f.read())

    cli_ip, cli_port_str = cfg['listen'].split(':')
    serv_ip, serv_port_str = cfg['server'].split(':')
    cli_addr = (cli_ip, int(cli_port_str))
    serv_addr = (serv_ip, int(serv_port_str))

    bjtalk.bjtalk(cli_addr, serv_addr)


main(json_file)
