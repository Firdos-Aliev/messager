import subprocess
from time import sleep

process = []

process.append(subprocess.Popen("python server/server.py", creationflags=subprocess.CREATE_NEW_CONSOLE))

sleep(4)
for i in range(2):
    process.append(subprocess.Popen("python client/client_gui.py", creationflags=subprocess.CREATE_NEW_CONSOLE))

input("Enter to exit...")

while process:
    process.pop().kill()
