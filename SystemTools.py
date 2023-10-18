import os

import psutil


class SystemTools:

    def welcome(self):
        pass

    def ping(self):
        op = input("Insert IP or domain name: ")
        os.system(f"ping {op} -c 4 ")  # o menos -c 4 serve para limitar o ping a 4 tentativas

    def get_nics(self):
        return list(psutil.net_if_addrs().keys())

    def manage_network_adaptor(self):  # Criar a função para fazer alterações da placa de rede
        os.system("ip a")  # Para mostrar as plcas de rede
        nic = input("Insert the network adapter name to turn ON/OFF\n"
                    "Option: ")  # Escolher a placa de rede
        option = int(input("[1] - Turn ON\n"
                           "[2] - Turn OFF\n"
                           "Option: "))  # Escolher o que pretendes fazer
        if option == 1:
            return_code = os.system(f"ip link set {nic} up")  # Função para ligar a placa de rede
            if return_code == 0:
                print("NIC turned ON successfully")  # Mensagem de confirmação
            else:
                print("ERROR! Status not changed!")
        elif option == 2:
            return_code = os.system(f"ip link set {nic} down")  # Função para Desligar a placa de rede
            if return_code == 0:
                print("NIC turned OFF successfully")  # Mensagem de confirmação
            else:
                print("ERROR! Status not changed")
