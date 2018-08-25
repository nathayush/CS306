import socket
import time
from tkinter import *
import sys

class Client:
    BUFFER_SIZE = 2000
    
    def __init__(self):
        self.host = ""
        self.port = 0
        
    def run(self):
        temp = ipEntry.get().split(":")
        self.host = temp[0]
        self.port = int(temp[1])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.host, self.port))
        
        for widget in frame.winfo_children():
            widget.destroy()
        k = Label(frame, text="Connected to {}:{}".format(self.host, self.port))
        k.pack(side=BOTTOM)
        print ("Getting tags...")
        tags = self.sock.recv(self.BUFFER_SIZE).decode()
        text = Label(frame, text="Tags on server: " + str(tags.replace("&", ", ")))
        text.pack()
        print ("Tags on server: " + str(tags.replace("&", ", ")))
        
    def send(self):
        for widget in frame1.winfo_children():
            widget.destroy()
        msg = tagEntry.get()
        if msg != "q":
            self.sock.send(msg.encode())
            events = self.sock.recv(self.BUFFER_SIZE).decode()
            if events != "":
                eventList = events.split("#&")
                text = Label(frame1, text="Received from server: ")
                text.pack()
                print ("Received from server:")
                i = 0
                for event in eventList:
                    i += 1
                    out = "{}. ".format(i) + event
                    text1 = Label(frame1, text=out)
                    text1.pack()
                    print ("{}. ".format(i) + event)
            else:
                text = Label(frame1, text="Nothing received from server.")
                text.pack()
                print ("Nothing received from server.")
            print ("")
        else:
            self.sock.close()
            root.quit()
    
root = Tk()
tcpClient = Client()

w = Label(root, text="Client Portal")
w.pack()

frame = Frame(root, width=300, height=300)
frame.pack()

ipLabel = Label(frame, text="Enter Server IP, port:")
ipLabel.pack(side=LEFT)
ipEntry = Entry(frame, bd =5)
ipEntry.insert(0, '127.0.1.1:1234')
ipEntry.pack(side=LEFT)
connectButton = Button(frame, text="Connect", command = tcpClient.run)
connectButton.pack(side=BOTTOM)

frame2 = Frame(root, width=300, height=200)
frame2.pack()
frame1 = Frame(root, width=300, height=200)
frame1.pack()

tagLabel = Label(frame2, text="Enter Tag (or q to quit):")
tagLabel.pack(side=LEFT)
tagEntry = Entry(frame2, bd =5)
tagEntry.pack(side=LEFT)
sendButton = Button(frame2, text="Send", command = tcpClient.send)
sendButton.pack(side=BOTTOM)

root.mainloop()