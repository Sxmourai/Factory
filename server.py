from src.server.server import Server
from threading import Thread


server = Server("localhost")
Thread(target=server.run).start()
try:
    while True:
        cmd = input("> ")
        if cmd.lower() == "exit":
            server.exit()
        else:
            server.exec_input(cmd)
except KeyboardInterrupt:
    server.exit()