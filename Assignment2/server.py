import socket
from threading import Thread, Timer
from datetime import date
from datetime import datetime
import sys
from scraper.scraper import webdata


class ClientThread(Thread):
 
    def __init__(self, ip, port, conn, tagsList, eventList):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print ("New server socket thread started for " + ip + ":" + str(port) + "\n")
        self.tagsList = tagsList
        self.eventList = eventList
        flat_list = list(set([item for sublist in self.tagsList for item in sublist]))
        self.conn.send("&".join(flat_list).encode())

    def run(self):
        while True :
            tag = self.conn.recv(2048).decode()
            if not tag:
                break
            print ("Server received data:", tag)
            sending = ""
            for sublist in self.tagsList:
                if tag in sublist:
                    index = self.tagsList.index(sublist)
                    event, date = self.eventList[index]
                    sending = sending + event + " (" + date + ")#&"
            sending = sending[:-2]
            self.conn.send(sending.encode())
            print ("\nServer is listening...")
        print ("Socket closed for " + ip + ":" + str(port) + "\n")
        self.conn.close()

    
def Main():
    TCP_IP = socket.gethostbyname(socket.gethostname())
    print(TCP_IP)
    TCP_PORT = int(sys.argv[1])
    BUFFER_SIZE = 20
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))
    threads = []
    
    def getData():
        print ("Updating events...")
        data = webdata()
        tagsList = data.tagsList
        eventList = data.eventList
        print ("Events updated.\n")
        return (tagsList, eventList)
    tagsList, eventList = getData()

    while True:
        tcpServer.listen(4)
        print ("Server is listening..." )
        (conn, (ip,port)) = tcpServer.accept()
        newthread = ClientThread(ip, port, conn, tagsList, eventList)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

if __name__ == '__main__':
    Main()
