import socket, _thread

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
address = (ip, port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

def wait_for_clients(arg):
    while True:
        try:
            data, address = s.recvfrom(1024)
            client_msg = data.decode("utf-8")
            split_msg = client_msg.split()

            # Client notifying server
            if split_msg[0].lower() == "client":
                send_msg = True
                if address[0] in client_addresses: send_msg = False
                client_addresses[address[0]] = address
                if send_msg: print("New connection (" + address[0] + "): " + client_msg)
                continue

            # Command output
            print(client_msg)
        
        except:
            pass

def _help():
    print("=== HELP ===")
    print("[ip] [command]")
    print(" - Runs the command on the client with the specified ip address")

def process_command(cmd):
    if not cmd: return

    args = cmd.split()
    ip = args[0]

    # checking if the first argument is a server command
    if ip == "help":
        _help()
        return

    if not ip in client_addresses: return

    command = " ".join(args[1:])
    s.sendto(command.encode("utf-8"), client_addresses[ip])

client_addresses = {}

def main_loop():
    _thread.start_new_thread(wait_for_clients, (0,))
    process_command(input(""))

print("Use 'help' to understand how to use the CLI")
print("Waiting for first connection...")

while True:
    main_loop()