import time
import yaml
import socket
from argparse import ArgumentParser

import jim

config = {
    'host': '127.0.0.1',
    'port': 8000,
    'buffersize': 1024
}

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)
parser.add_argument(
    '-ht', '--host', type=str, required=False,
    help='Sets server host'
)
parser.add_argument(
    '-p', '--port', type=int, required=False,
    help='Sets server port'
)

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

if args.host:
    config['host'] = args.host

if args.port:
    config['port'] = args.port


def make_request():
    ret = {'time': int(time.time())}
    request = input('request: ')
    ret['action'] = request
    if request == jim.ACTION_AUTHENTICATE:
        ret['account_name'] = input('account_name: ')
        ret['password'] = input('password: ')
    return ret


def send(sock, data):
    jim.send(sock, data)


def recv(sock, bufsize):
    ret = jim.recv(sock, bufsize)
    return ret


def handle_response(response):
    print(response)
    print('Client send data')


if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.connect((config.get('host'), config.get('port')))

        print('Client was started')

        data = make_request()
        send(sock, data)
        response = recv(sock, config.get('buffersize'))
        handle_response(response)

        sock.close()
    except KeyboardInterrupt:
        print('Client shutdown')
