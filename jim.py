import json

# --- Actions ---
ACTION_PRESENCE = 'presence'
ACTION_PRОBE = 'prоbe'
ACTION_MSG = 'msg'
ACTION_QUIT = 'quit'
ACTION_AUTHENTICATE = 'authenticate'
ACTION_JOIN = 'join'
ACTION_LEAVE = 'leave'

# --- Responses ---
# 1xx

# 2xx
RESPONSE_OK = 200

# 3xx

# 4xx
RESPONSE_WRONG_REQUEST = 400
RESPONSE_WRONG_AUTH = 402
RESPONSE_CONFLICT = 409


# 5xx


def send(sock, data):
    sock.send(json.dumps(data).encode())


def recv(sock, bufsize):
    bytes_response = sock.recv(bufsize)
    return json.loads(bytes_response.decode())
