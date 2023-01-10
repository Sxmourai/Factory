from src.main.server import Server
from threading import Thread


server = Server(Server.LOCAL, port=9999)
Thread(target=server.run).start()
while True:
    cmd = input("> ")
    if cmd.lower() == "exit":
        server.exit()
    else:
        server.exec(cmd)
