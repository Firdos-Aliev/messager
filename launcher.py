import subprocess

PROCESS = []

PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

for i in range(2):
    PROCESS.append(subprocess.Popen('python client.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

input("Press to kill all process...")
while PROCESS:
    proc = PROCESS.pop()
    proc.kill()
