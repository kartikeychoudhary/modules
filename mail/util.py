import configparser
import getpass
import os

CURRENT_PATH = os.getcwd()

def createFile(config):
    username = input("Enter the username\n")
    password = getpass.getpass(prompt='Password: ', stream=None)
    config['CREDENTIALS'] = {'username':username, 'password':password}
    with open('config.ini', 'w') as file:
        config.write(file)


def loadCredentials():
    config = configparser.ConfigParser()
    if not os.path.exists(CURRENT_PATH+"/config.ini"):
        createFile(config)
    else:
        try:
            config.read('config.ini')
            
            username = config['CREDENTIALS']['username']
            password = config['CREDENTIALS']['password']

            return [username,password]
        except:
            print("credentials file is corrupted or not found")
            print("Creating new Entries..")
            createFile(config)