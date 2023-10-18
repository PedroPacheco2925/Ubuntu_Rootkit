from SystemTools import *


class ClientTools(SystemTools):
    def __init__(self):
        super().__init__()
        self.welcome()

    def welcome(self):
        print('\nWelcome to Ubuntu Client Configuration Tools')
