import random

################################################################################################################

#                                                   CLASSES

################################################################################################################
class Switch:
    def __init__(self, name):
        self.type = "switch"
        self.dev_name = name
        self.forwardingTable = {} # String: String ("00-00-00-00-10": "3")
        self.ports = [] # just to keep track of port connectivity
                
    def activate(self, *ports):
        self.ports = ports
        for port in self.ports:
            if port.type == "host":
                port.switch = self
                
    def getMessage(self, sender, hostAddress, message, destAddress):
        if hostAddress not in self.forwardingTable.keys():
            self.forwardingTable[hostAddress] = self.ports.index(sender)
        self.send(sender, hostAddress, message, destAddress)

    def send(self, sender, hostAddress, message, destAddress):
        if destAddress in self.forwardingTable.keys():
            self.ports[self.forwardingTable.get(destAddress)].getMessage(self, hostAddress, message, destAddress)
        else:
            self.broadcast(sender, hostAddress, message, destAddress)

    def broadcast(self, sender, hostAddress, message, destAddress):
        for port in self.ports:
            if port != sender:
                port.getMessage(self, hostAddress, message, destAddress)
    
class Host:
    def __init__(self, mac, name):
        self.type = "host"
        self.dev_name = name
        self.macAddress = mac
        self.switch = 0 # just to keep track of the switch port

    def send(self, hostAddress, message, destAddress):
        self.switch.getMessage(self, hostAddress, message, destAddress)

    def getMessage(self, switch, hostAddress, message, destAddress):
        if destAddress == self.macAddress:
            print "{} ({}) recieved: {}".format(self.dev_name, self.macAddress, message)
        else:
            print "{} ({}) recieved a message".format(self.dev_name, self.macAddress)

################################################################################################################

#                                               INITIATION

################################################################################################################

laptop0 = Host("00-00-00-00-00", "laptop0")
laptop1 = Host("00-00-00-00-01", "laptop1")
laptop2 = Host("00-00-00-00-02", "laptop2")
laptop3 = Host("00-00-00-00-03", "laptop3")
laptop4 = Host("00-00-00-00-04", "laptop4")
laptop5 = Host("00-00-00-00-05", "laptop5")
laptop6 = Host("00-00-00-00-06", "laptop6")
laptop8 = Host("00-00-00-00-08", "laptop8")
laptop9 = Host("00-00-00-00-09", "laptop9")
laptop10 = Host("00-00-00-00-10", "laptop10")
laptop11 = Host("00-00-00-00-11", "laptop11")
laptop12 = Host("00-00-00-00-12", "laptop12")
laptop13 = Host("00-00-00-00-13", "laptop13")
switch0 = Switch("switch0")
switch1 = Switch("switch1")
switch2 = Switch("switch2")
switch3 = Switch("switch3")
switch4 = Switch("switch4")
switch0.activate(laptop0,laptop1,laptop2,switch4)
switch1.activate(laptop3,laptop4,switch4,switch2)
switch2.activate(laptop5,laptop6,laptop9,switch3,switch1)
switch3.activate(laptop8,laptop10,laptop11,switch2)
switch4.activate(laptop12,laptop13,switch0,switch1)

hosts = [laptop0, laptop1, laptop2, laptop3, laptop4, laptop5, laptop6, laptop8, laptop9, laptop10, laptop11, laptop12, laptop13]
switches = [switch0, switch1, switch2, switch3, switch4]
macAddresses = ["00-00-00-00-00", "00-00-00-00-01", "00-00-00-00-02", "00-00-00-00-03", "00-00-00-00-04", "00-00-00-00-05", "00-00-00-00-06", "00-00-00-00-08", "00-00-00-00-09", "00-00-00-00-10", "00-00-00-00-11", "00-00-00-00-12", "00-00-00-00-13"]

################################################################################################################

#                                                   HELPERS

################################################################################################################

def printUpperBanner(i):
    print("-")*55
    print(" "*22 + "ITERATION {}".format(i))
    print("-")*55
    
def printLowerBanner():
    print
    print("-")*55
    print
    print
    
################################################################################################################

#                                                       RUN

################################################################################################################

def transfer(i, hostAddress, message, destAddress):
    for host in hosts:
        if host.macAddress == hostAddress:
            printUpperBanner(i)
            host.send(hostAddress, message, destAddress)
            printLowerBanner()
            
devices1 = ["00-00-00-00-12", "00-00-00-00-06", "00-00-00-00-02", "00-00-00-00-04"]
devices2 = ["00-00-00-00-05", "00-00-00-00-12", "00-00-00-00-06", "00-00-00-00-02"]
def run():
    for i in range(4):
        transfer(i, devices1[i], "HELLO. THIS IS THE MESSAGE", devices2[i])
        for switch in switches:
            f = open('FW_{}.txt'.format(switch.dev_name), 'a')
            f.write(" "*22 + "ITERATION {}".format(i) + "\n")
            f.write("-"*55 + "\n\n")
            f.write(" "*12 + "MACAddress" + " "*15 +"Port\n")
            for key, value in switch.forwardingTable.iteritems():
                f.write(" "*10 + "{}".format(key) + " "*12 +"Port {}\n".format(value))
            f.write("-"*55 + "\n\n\n")
            f.close
run()
