#!/bin/python3
# Notas: No sistema de login falta por para criar o serviço.
import os
def network_adaptor():
    os.system("ip link show") # Para mostrar as plcas de rede
    option1 = input("Insira a placa de rede que pretende desligar / ligar\nOpção: ") 
    option2 = int(input("[1] - ligar\n[2] - desligar\nOpção: "))
    if option2 == 1:
        os.system(f"ip link set {option1} up")
        print("Placa ligada com Sucesso")
    elif option2 == 2:
        os.system(f"ip link set {option1} down")
        print("Placa Desligada com Sucesso")

def ping():
    ip = input("Insira o ip ou domínio: ")
    os.system(f"ping {ip} -c 4") # o menos -c 4 serve para limitar o ping a 4 tentativas

def services():
    option1 = int(input("Qual o serviço que pretende instalar?\n[1] - SFTP (Protocolo de transferência de arquivos)\n[2] - Firewall \nOpção:"))
    if option1 == 1: # Instalar o SFTP
        adduser_or_install = int(input("O que pretende fazer\n[1] - Instalar o serviço\n[2] - Adicionar utilizadores\n[3] - Ver utilizadores\nopção:"))
        if adduser_or_install == 1:
            os.system("apt install vsftpd") ## O && serve para so executar o proximo comando se o primeiro for concluido
            os.system("rm -r /etc/vsftpd.conf && cp /etc/Ubuntu_rootkit/src/services/sftp/vsftpd.conf  /etc/vsftpd.conf") ## rm -r para apgar o ficheiro criado na instalação ## cp para copiar o nosso ficheiro configurado para o serviço
            utilizador_1 = input("Insira o utilizador que prentede adicionar: ") # 
            os.system(f"echo {utilizador_1} >>/etc/vsftpd.chroot_list")
        elif adduser_or_install == 2:
            def add_user():
                    utilizador_2 = input("Novo Utilizador: ")
                    os.system(f"echo {utilizador_2} >>/etc/vsftpd.chroot_list")
                    op = int(input("Deseja adicionar outro utilizador?\n[1] - Sim\n[2] - Não\nOpção: "))
                    if op == 1:
                        add_user()
                    elif op == 2:
                        services()
            add_user()
        elif adduser_or_install == 3:
            os.system("cat /etc/vsftpd.chroot_list")
    elif option1 == 2:  # Firewall
        op1 = int(input("O que pretende fazer\n[1] - Desligar\Ligar Firewall\n[2] - Adicionar Portas\n[3] - Bloquear Porta\n[4] - Ver as portas\n[5] - Sair\nOpção: "))
        if op1 == 1:
            op2 = int(input("O que pretende fazer:\n[1] - Desligar a Firewall\n[2] - Ligar a Firewall\n[3] - Ver o Estado\n[4] - Sair\nOpção"))
            if op2 == 1:
                os.system("ufw disable")
            elif op2 == 2:
                os.system("ufw enable")
            elif op2 == 3:
                os.system("ufw status")
            elif op2 == 4:
                services()
        elif op1 == 2:
            op2 = int(input("Qual é a porta: "))
            op3 = input("Qual o protocolo  que pretende adicionar ex: tcp, udp\nOpção: ")
            os.system(f"ufw allow {op2}/{op3}")
        elif op1 == 3:
            op2 = int(input("Qual é a porta: "))
            op3 = input("Qual o protocolo  que pretende Bloquear ex: tcp, udp\nOpção: ")
            os.system(f"ufw deny {op2}/{op3}")
        elif op1 == 4:
            os.system("ufw status")
        elif op1 == 5:
            star_menu()

def star_menu(): 
    os.system("clear") # para limpar a tela
    option1 = int(input("Bem vindo\n\nIndique o que pretende fazer:\n"
                        "[1] - Ligar/Desligar placas de rede\n"
                        "[2] - Ping\n"
                        "[3] - Instalar Serviços\n"
                        "[0] - sair\n"
                        "Opção: "))
    match option1:
            case 1:
                network_adaptor()
                star_menu()
            case 2:
                ping()
                star_menu()
            case 3:
                services()
                star_menu()
            case 0:
                print("bye bye")
            case _:
                print("Invalido")
                star_menu()

def login():
    uid = os.getuid() # Verificar o UID do Utilizador Atual
    # O uid Serve para identificar utilizadores dentro do kernel por um valor inteiro designado por user identifier.
    if uid == 0:  # Verificar se o UID é igual a 0. 0 é o Uid do utilizador (Root)
        if os.path.isdir("/etc/Ubuntu_rootkit"): # Verificar se a pasta /etc/Ubuntu_rookit já esta criada com a biblioteca os
            star_menu()
        else:
            print("Serviço ainda não instalado")
            os.system("cd .. && mv ogrupo1/ /etc/Ubuntu_rootkit && cd /etc/Ubuntu_rootkit && chmod +x main.py && ./main.py") # Se não tiver irá criar a mesma :) o simbolo && serve para 
                                                                                                                                    #so executar o proximo comando se o primeiro for concluido com sucesso
            os.system("cp src/default/rootkit.service /usr/lib/systemd/system") # Esta linha serve copiar a configuração default para que consigamos utilizar o nosso script como um serviço
            os.system("echo 'alias rootkit=\"cd /etc/Ubuntu_rootkit && ./main.py\"' >> /etc/bash.bashrc")  # A ' \ ' barra invertida serve para que possamos usar caracteres especiais como por exemplo o &&
            os.system("shutdown -r now") 
    else:
        print("Têm de estar em root para poder usar o programa!")
login()

