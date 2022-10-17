import netmiko
import getpass
from netmiko import ConnectionHandler

def backup_config(running_config):
    running_config = session.send_command("show running-config")
    backup_file = open("backup_file.txt", "w+")
    backup_file.write(running_config)
    backup_file.close()
    
router_1 = {
    "device_type": "",
    "host": "192.168.1.1",
    "username": "",
    "password": "",
    "secret": ""
    }

def router_input():
	router_1["username"] = input("Please enter the username for the router: ")
	router_1["password"] = getpass.getpass("Please enter the password for the router: ")
	router_1["secret"] = getpass.getpass("Pease enter the secret password for the router: ")
router_input()
connected = False

while connected == False:
    connection_type = input("Would you like to telnet or ssh into the router?: ")
    backup = input("Would you like to create a backup of the running configs (yes/no)?: ")
    if connection_type == "telnet":
        router_1["device_type"] = "cisco_ios_telnet"
        valid = False
        while valid == False:
            try:
                session = netmiko.ConnectionHandler(**router_1)
                session.enable()
                valid = True
            except:
                print("Invalid credentials, try again:")
                router_input()
        running_config = session.send_command("show running-config")
        print(running_config)
        if backup == "yes":
            backup_config(running_config)
        else:
            break
        session.close()
        connected = True
        
        
    elif connection_type == "ssh":
        router_1["device_type"] = "cisco_ios"
        valid = False
        while valid == False:
            try:
                session = netmiko.ConnectionHandler(**router_1)
                session.enable()
                valid = True
            except:
                print("Invalid credentials, try again:")
        running_config = session.send_command("show running-config")
        print(running_config)
        if backup == "yes":
            backup_config(running_config)
        else:
            break
        session.send_command("exit")
        connected = True
       
        
        
        
    else:
        print("Invalid input, please try again")
print("You have succesfully created a backup of the config file to your local machine")