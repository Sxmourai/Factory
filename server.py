from src.server.server import Server
from threading import Thread


server = Server(Server.LOCAL)
Thread(target=server.run).start()
while True:
    cmd = input("> ")
    if cmd.lower() == "exit":
        server.exit()
    else:
        server.exec_input(cmd)
