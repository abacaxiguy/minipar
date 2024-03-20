import socket
import threading

sock = None
conn = None
addr = None

def _start(host='localhost', port=12345):
    global sock
    global conn
    global addr
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        conn, addr = sock.accept()

        # print(f"Server escutando em {host}:{port}")
    except:
        pass

# def start():
#     threading.Thread(target=_start).start()

def send(message):
    global conn
    conn.send(message.encode('utf-8'))

def receive(host='localhost', port=12345):
    global conn
    global sock

    sock.connect((host, port))
    return sock.recv(1024).decode('utf-8')

def calc(expression):
    operation, value1, value2 = expression.split(',')
    if operation == '+':
        return int(value1) + int(value2)
    elif operation == '-':
        return int(value1) - int(value2)
    elif operation == '*':
        return int(value1) * int(value2)
    elif operation == '/':
        return int(value1) / int(value2)

    return 'Operação inválida'