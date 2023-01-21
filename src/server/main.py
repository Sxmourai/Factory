import sys
import os
from time import sleep
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from server import Server


server = Server(Server.LOCAL)
server.run()
# while True:
#     cmd = input("> ")
#     if cmd == "exit":
sleep(2)
server.exit()
#     else: server.exec_input(cmd)