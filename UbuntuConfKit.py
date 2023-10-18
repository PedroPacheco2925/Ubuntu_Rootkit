# apt install pip
# pip install psutil
# To run on ubuntu server:
#       - MAKE SURE ONE OF THE NETWORK ADAPTARS IS IN BRIDGED MODE
#       - Check ssh status: systemctl status ssh
#           - If stopped: systemctl start ssh
#           - If not installed: apt install ssh
#       - Open powershell on project directory (windows)
#       - copy (using scp) from windows to the IP of the virtual machine:
#               - scp project.tar <user>@<IP>:<Destination folder>
#       - Go to dir on virtual machine and run:
#               - python3 UbuntuConfiKit.py

from ClientTools import *
from ServerTools import *


def main_menu():
    option = int(input(f'[1] - Configure an Ubuntu Server\n'
                       f'[2] - Configure an Ubuntu Client\n'
                       f'[3] - Quit\n'
                       f'Option: '))
    return option


while True:
    option = main_menu()
    match option:
        case 1:
            ubuntu_server = ServerTools()
            ubuntu_server.menu()
        case 2:
            ubuntu_client = ClientTools()
            ubuntu_client.menu()
        case 3:
            print("Thanks for playing... Goodbye!")
            exit()
        case _:
            print("Choose a valid option!\n")
