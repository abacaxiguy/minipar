import socket

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 12345))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print('Conectado em', self.addr)
    
    def send(self, message):
        self.conn.send(message.encode('utf-8'))
    
    def receive(self):
        return self.conn.recv(1024).decode('utf-8')