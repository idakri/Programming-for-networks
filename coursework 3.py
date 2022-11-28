import netmiko
import getpass
from netmiko import ConnectHandler
import concurrent.futures


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


def menu():
    print("-----------------------------------")
    print("What operation would you like to perform?")
    print("1 - Create a loopback interface on the host R1")
    print("2 - Configure a routing protocol on the host R1")
    print("3 - Configure multiple hosts with VLANS simultaneously")
    
    valid = False
    while valid == False:
        user_input = input("What would you like to perform (1/2/3)?: ")
        
        if user_input == "1":
            loopback()
            valid = True
        elif user_input == "2":
            routing_protocols()
            valid =True
        elif user_input == "3":
            session.disconnect()
            Vlan()
            valid = True
        else:
            print("Invalid input, Try again!")


def loopback():
    interface = input("Which loopback interface woould you like to set(1,2,3...)?:  ")
    loopback_interface = "interface loopback "+interface
    ip = input("What would you like to set the ip address and subnet mask to (x.x.x.x x.x.x.x)?: ")
    ip_address = "ip address"+ip
    loopback_commands = [loopback_interface, ip_address, "ip nat inside"]
    loopback_commands = ["interface looback 1", "ip address 192.168.1.2 255.255.255.0", "ip nat inside"]
    session.send_config_set(loopback_commands)
    print("You have successfully created a loopback interface on the host R1 with ip address and subnet mask "+ip)
    
    
def routing_protocols():
    valid = False
    while valid == False:
        user_input = input("Which routing protocol would you like to use (OSPF/EIGRP/RIP): ")
        if user_input == "OSPF":
            ospf_commands = ["router ospf 10", "network 192.168.1.0 0.0.0.255 area 0"]
            session.send_config_set(ospf_commands)
            print("You have successfully configured OSPF on the host R1")
            valid = True
        elif user_input == "EIGRP":
            eigrp_commands = ["router eigrp 100", "network 192.168.1.0", "no auto-summary"]
            session.send_config_set(eigrp_commands)
            print("You have successfully configured EIGRP on the host R1")
            valid = True
        elif user_input == "RIP":
            rip_commands = ["router rip", "version 2", "network 192.168.1.0"]
            session.send_config_set(rip_commands)
            print("You have successfully configured RIP on the host R1")
            valid = True
        else:
            print("Invalid input, try again:")
            
def vlan_configs(ip):
    if ip == "192.168.1.1":
        host = "host"
    elif ip == "192.168.1.2":
        host = "ip"
    
    R1_Vlan_config = []
    S1_Vlan_config = []
        
    device = {
        "device_type": "cisco_ios",
        host : ip,
        "username": "cisco",
        "password": "cisco",
        "secret": "class"
        }
    try:
        print("Connecting to IP: "+ip)
        session = netmiko.ConnectHandler(**device)
        session.enable
        print("Connected to IP: "+ip)
        if ip == "192.168.1.1":
            session.send_config_set(R1_Vlan_config)
            print("R1 was configured with Vlan settings")
            session.disconnect()
        elif ip == "192.168.1.2":
            session.send_config_set(S1_Vlan_config)
            print("S1 was configured with Vlan settings")
            session.disconnect()
    except:
        print("Doesnt work")

def Vlan():
    
    ip = ["192.168.1.1","192.168.1.2"]
    with concurrent.futures.ThreadPoolExecutor() as exe:
        results = exe.map(vlan_configs, ip)
    


connected = False
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
    
    session.disconnect()
    connected = True

