import netmiko
import getpass
from netmiko import ConnectHandler
import difflib


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

def compare_configs():
    finish = False
    while finish == False:
        print("----------------------------------------------------------------")
        print("What would you like to compare:")
        print("1 - The startup and running config of the router?")
        print("2 - The running config of the router and a backup saved on a local machine?")
        print("3 - Exit")
        running_config = session.send_command("show running-config")
        startup_config = session.send_command("show startup-config")
        
        user_input = input("Which would you like to comapare (1/2) or exit(3)?: ")
        
        if user_input == "1":
        
            diff = difflib.ndiff(running_config.splitlines(keepends=True), startup_config.splitlines(keepends=True))
            changes = [l for l in diff if l.startswith('+ ') or l.startswith('- ')]
            for c in changes:
                print(c)
                
        elif user_input == "2":
            
            with open("router_backup.txt") as f:
                backup_config = f.readlines()
            string = ""
            string = string.join(backup_config)
            
            diff = difflib.ndiff(running_config.splitlines(keepends=True), string.splitlines(keepends=True))
            changes = [l for l in diff if l.startswith('+ ') or l.startswith('- ')]
            for c in changes:
                print(c)
            f.close()
        
        elif user_input == "3":
            finish = True
    
    

while connected == False:
    print("You are connecting to the router via ssh")

    
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
    print("You have successfully connected to the router via SSH")
    compare_configs()
    session.disconnect()
    connected = True
    
