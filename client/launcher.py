import subprocess

process = []

for i in range(2):
    process.append(subprocess.Popen("python client_gui.py", creationflags=subprocess.CREATE_NEW_CONSOLE))

input("Enter to exit...")

while process:
    process.pop().kill()