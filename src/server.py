import socket
import threading

class Server:
    def __init__(self):
        self.sock = None
        self.conn = None
        self.addr = None

    def _start(self, host='localhost', port=12345):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            self.sock.listen(1)
            # print(f"Server escutando em {host}:{port}")
        except:
            pass

    def start(self):
        threading.Thread(target=self._start).start()

    def send(self, message, conn=None):
        if conn == None:
            self.conn, self.addr = self.sock.accept()
            self.conn.send(message.encode('utf-8'))
            return self.conn
        else:
            conn.send(message.encode('utf-8'))

    def receive(self, host='localhost', port=12345, conn=None):
        if conn == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

            response = self.sock.recv(1024).decode('utf-8')
            return {'response': response, "conn": self.sock}
        else:
            response = conn.recv(1024).decode('utf-8')
            return {'response': response, "conn": self.sock}

    def calc(self, expression):
        operation, value1, value2 = expression.split(',')
        print('Cálculo realizado com sucesso!')
        if operation == '+':
            return int(value1) + int(value2)
        elif operation == '-':
            return int(value1) - int(value2)
        elif operation == '*':
            return int(value1) * int(value2)
        elif operation == '/':
            return int(value1) / int(value2)

        return 'Operação inválida'