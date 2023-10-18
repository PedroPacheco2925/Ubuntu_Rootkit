from SystemTools import *


class ServerTools(SystemTools):
    def __init__(self): #####david comentar
        super().__init__() #####david comentar
        self.welcome() #####david comentar

    def welcome(self):
        print('\nWelcome to Ubuntu Server Configuration Tools')

    def menu(self):
        print(f'\nTools:\n'
              f'[1] - Ping\n'
              f'[2] - Configure Network Adapters\n'
              f'[3] - Configure services\n'
              f'[4] - Return to main menu\n')

        option = int(input(f'Option: '))

        match option:
            case 1:
                super().ping();
            case 2:
                self.network_conf_menu();
            case 3:
                self.service_configuration_menu()
            case 4:
                return
            case _:
                print("Choose a valid option!")
        self.menu()

    def add_user_to_sftp():  # Criar a função Adicionar Utilizador
        user = input("Choose a name for your new user: ")  # Pedir o Utilizador ao Utilizador
        os.system(f"echo {user} >>/etc/vsftpd.chroot_list")  # Comando para adicionar o utilizador ao Serviço
        option = int(input("Do wish to add another user?\n"
                       "[1] - Yes\n"
                       "[2] - No\n"
                       "Option: "
                       ))  # Escolha do que pretende fazer

        if option == 1:
            add_user()
        elif option == 2:
            self.configure_sftp()

    def service_configuration_menu(self):
        option = int(input("Which service do you want to configure?\n"
                           "[1] - SFTP (Secure File Transfer Protocol)\n"
                           "[2] - Firewall \n"
                           "[3] - return to previous menu\n"
                           "Option:"
                           ))  # Escolher o serviço que pretende instalar

        return option

    def service_configuration(self):
        while True:
            option = self.service_configuration_menu()
            match option:
                case 1:
                    self.configure_sftp()
                case 2:
                    self.configure_firewall()
                case 3:
                    self.menu()
                    return
                case _:
                    print("Choose a valid option!")

            self.service_configuration_menu()

    def firewall_conf_menu(self):
        option = int(input(
            "Choose what you want to do...\n"
            "[1] - Configure Firewall Status\n"
            "[2] - Allow Port\n"
            "[3] - Denny Port\n"
            "[4] - Check Ports\n"
            "[5] - Return to previous menu\n"
            "Opção: "))  # Escolha do que pretende fazer na firewall

        return option

    def configure_firewall(self):
        while True:
            option = self.firewall_conf_menu()
            match option:
                case 1:
                    option = int(input("Choose what you want to do...\n"
                                       "[1] - Disable Firewall\n"
                                       "[2] - Enable Firewall\n"
                                       "[3] - Check Firewall Status\n"
                                       "[4] - Return to previous menu\n"
                                       "Option: "))  # Escolha do que pretende fazer na firewall
                    if option == 1:
                        os.system("ufw disable")  # Desligar a Firewall
                    elif option == 2:
                        os.system("ufw enable")  # Ligar a Firewall
                    elif option == 3:
                        os.system("ufw status")  # Ver o Estado da Firewall
                    elif option == 4:
                        Server.services(self)

                case 2:
                    port = int(input("Choose the port: "))  # Escolha da porta
                    protocol = input("Wich protocol do you want to add? ex: tcp, udp\n"
                                     "Option: ")  # Escolha do Protocolo
                    os.system(f"ufw allow {port}/{protocol}")  # Execução do comando
                case 3:
                    port = int(input("Choose the port: "))  # Escolha da porta
                    protocol = input("Wich protocol do you want to remove? ex: tcp, udp\n"
                                     "Option: ")  # Escolha do Protocolo
                    os.system(f"ufw deny {port}/{protocol}")  # Execução do comando
                case 4:
                    os.system("ufw status")  # Comando para ver o Estado da Firewall
                case 5:
                    self.menu()
                    return
                case _:
                    print("Choose a valid option!\n")

            self.firewall_conf_menu()

    def network_conf_menu(self):
        option = int(input("What do you wish to do?\n"
                           "1 - Turn Network adapters ON/OFF\n"
                           "2 - Configure network adapters\n"
                           "3 - Return to previous menu"
                           "Option: "
                           ))

        match option:
            case 1:
                self.manage_network_adaptor()
            case 2:
                self.conf_network_adapters()
            case 3:
                self.menu()
            case _:
                print("Choose a valid option!")

        self.network_conf_menu()

    def conf_network_adapters(self):
        static_ip = input(f'Insert the static IP for your server (e.g. 10.10.10.10/24): ')
        alt_dns = input(f'Insert alternative DNS (e.g. 8.8.8.8): ')

        nics = super().get_nics()

        ip_octets = static_ip.split('.')
        gateway = f'{ip_octets[0]}.{ip_octets[1]}.{ip_octets[2]}.254'

        ip_dns = static_ip.split('/')[0]

        conf_text = (f'network:\n'
                     f'  ethernets:\n'
                     f'    {nics[1]}:\n'
                     f'      dhcp4: true\n'
                     f'    {nics[2]}:\n'
                     f'      dhcp4: false\n'
                     f'      addresses:\n'
                     f'      - {static_ip}\n'
                     f'      routes:\n'
                     f'      - to: default\n'
                     f'        via: {gateway}\n'
                     f'      nameservers:\n'
                     f'        addresses: [{ip_dns},{alt_dns}]\n'
                     f'  version: 2\n')

        with open("/etc/netplan/00-installer-config.yaml", "w") as config_file:
            config_file.write(conf_text)

        os.system('netplan apply')
        os.system('ip a')

    def configure_sftp_menu(self):
        option = int(input("O que pretende fazer\n"
                           "[1] - Instalar o serviço\n"
                           "[2] - Adicionar utilizadores\n"
                           "[3] - Ver utilizadores\n"
                           "[4] - Return to previous menu\n"
                           "opção:"))  # Escolher o que pretende fazer

        return option

    def configure_sftp(self):
        option = self.configure_sftp_menu()
        if option == 1:
            os.system("apt install vsftpd")
            os.system("cp /Ubuntu_rootkit/src/services/sftp/vsftod.conf /etc/vsftpd.conf")  ## cp para copiar o nosso ficheiro configurado para o serviço
            self.add_user_to_sftp()
        elif option == 2:
            self.add_user_to_sftp()
        elif option == 3:
            os.system("cat /etc/vsftpd.chroot_list")  # Mostrar Todos os Utilizadores
        elif option == 4:
            return

        self.configure_sftp_menu()
