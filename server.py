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

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

host, port = config.get('host'), config.get('port')


def send(sock, data):
    jim.send(sock, data)


def recv(sock, bufsize):
    ret = jim.recv(sock, bufsize)
    return ret

def make_response(request):
    ret = {'response': jim.RESPONSE_WRONG_REQUEST, 'time': int(time.time())}
    action = request['action']
    if action == jim.ACTION_AUTHENTICATE:
        response = jim.RESPONSE_WRONG_AUTH
        ret['response'] = response
        if response == jim.RESPONSE_OK:
            ret['alert'] = 'Необязательное сообщение/уведомление'
        elif response == jim.RESPONSE_WRONG_AUTH:
            ret['error'] = 'This could be "wrong password" or "no account with that name"'
        elif response == jim.RESPONSE_CONFLICT:
            ret['error'] = 'Someone is already connected with the given user name'
    return ret

if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.listen(5)

        print(f'Server started with {host}:{port}')

        while True:
            client, address = sock.accept()
            client_host, client_port = address
            print(f'Client was detected {client_host}:{client_port}')

            request = recv(client, config.get('buffersize'))
            data = make_response(request)
            send(client, data)
            client.close()
    except KeyboardInterrupt:
        print('Server shutdown')
