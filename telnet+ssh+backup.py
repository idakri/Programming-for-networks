import netmiko
import getpass
from netmiko import ConnectHandler

def backup_config(running_config):
    running_config = session.send_command("show running-config")
    backup_file = open("backup_file.txt", "w+")
    backup_file.write(running_config)
    backup_file.close()
    print("You have successfully created a backup of the config file to your local machine")
    
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
                session = netmiko.ConnectHandler(**router_1)
                session.enable()
                valid = True
            except:
                print("Invalid credentials, try again:")
                router_input()
        running_config = session.send_command("show running-config")
        print(running_config)
        if backup == "yes":
            backup_config(running_config)
            print("You have successfully connected to the router via Telnet")
        else:
            print("You have successfully connected to the router via Telnet")
            break
        
        session.disconnect()
        connected = True
        
        
    elif connection_type == "ssh":
        router_1["device_type"] = "cisco_ios"
        valid = False
        while valid == False:
            try:
                session = netmiko.ConnectHandler(**router_1)
                session.enable()
                valid = True
            except:
                print("Invalid credentials, try again:")
                router_input()
        running_config = session.send_command("show running-config")
        print(running_config)
        if backup == "yes":
            backup_config(running_config)
            print("You have successfully connected to the router via SSH")
        else:
            print("You have successfully connected to the router via SSH")
            break
        session.disconnect()
        connected = True
        
    else:
        print("Invalid input, please try again")
        
        
        
