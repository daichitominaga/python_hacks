#!/usr/bin/env python

import requests


def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = ""

with open("subdomains-wordlist.txt") as word_file:
    for line in word_file:
        word = line.strip()
        test_url = word + "." + target_url
        res = request(target_url)
        if res:
            print("[+] Discovered subdomain --> " + test_url)

with open("commont.txt") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        res = request(target_url)
        if res:
            print("[+] Discovered URL --> " + test_url)