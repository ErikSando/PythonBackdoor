import socket

def get_ip():
    s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_temp.settimeout(0)
    
    try:
        s_temp.connect(("8.8.8.8", 80))
        ip = s_temp.getsockname()[0]
    
    except Exception:
        ip = '127.0.0.1'
    
    finally:
        s_temp.close()

    return ip

ip = get_ip()
port = 12345

thread_count = 0

s = socket.socket()

s.bind((ip, port))
s.listen(10)
s.settimeout(6)

class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection

        notif = self.connection.recv(2048)

        print("Connection Established:", address) # address[0] is ip
        print(notif.decode("utf-8"))

    def send(self, command):
        if command == "close":
            self.connection.close()
        
        if command == "exit" or command == "quit":
            self.connection.send("exit".encode())

        self.connection.send(command.encode())

        output = self.connection.recv(4096)
        
        if not output: return
        
        print(output.decode("utf-8"))

try_connect = True

def _help():
    print("=== HELP ===")
    print("[ip] [command]")
    print(" - Runs the command on the client with the specified ip address")
    print("connect")
    print(" - Attempts to form a connection (timeout of 6 seconds)")

def process_command(cmd):
    if not cmd: return

    args = cmd.split()
    ip = args[0]

    # checking if the first argument is a server command
    if ip == "connect":
        global try_connect
        try_connect = True
        return
    
    if ip == "help":
        _help()
        return

    if not ip in clients: return

    command = " ".join(args[1:])

    clients[ip].send(command)

clients = {}

def main_loop():
    global try_connect

    if try_connect:
        try_connect = False
        
        try:
            connection, address = s.accept()
            clients[address[0]] = ClientConnection(connection, address)
            
        except:
            print("Timed out")

    process_command(input("> "))

print("Use 'help' to understand how to use the CLI")
print("Waiting for first connection...")

while True:
    main_loop()
