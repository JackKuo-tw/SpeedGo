import datetime
import time
from threading import Thread
import socket
from os import system
import sys


class monocell(Thread):

    def __init__(self,name):

        Thread.__init__(self)
        self.birthTime = datetime.datetime.now()
        self.name = name

    def run(self):

        heart(self.name)


def speed_convert(data):

    calc = data*8
    if calc > 1024:
        if calc/1024 > 1024:
            return str(float(calc)/1024/1024) + " Mb"

        else:
            return  str(float(calc)/1024) + " Kb"
    else:
        return str(calc) + " bytes"


def heart(name):

    global data,UDP_IP,Client_info,avg_speed,count
    if name=="speed":
        while True:
            time.sleep(1)
            if data == 4:
                break
            if data > 0:
                count  = count + 1
            if count > 4 and count <10:
                avg_speed = avg_speed + data
            print speed_convert(data)
            data = 0

    if name=="send":
        print "Uploading..."
        t = time.time()
        while True:
            #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            sock.sendto(MESSAGE, Client_info)
            if time.time() - t > second:
                for i in range(5):
                    sock.sendto("done", Client_info)
                time.sleep(1)
                for i in range(5):
                    sock.sendto("done", Client_info)
                time.sleep(1)
                for i in range(5):
                    sock.sendto("done", Client_info)
                break
        print "Upload test finish"

    if name=="receive":
        print "Waiting for Upload test..."
        count = 0
        while 1:
            recv_data, addr = sock.recvfrom(2048)
            #print len(recv_data)
            data = data + len(recv_data) + 42
            if len(recv_data) == 4:
                data = 4
                break
        time.sleep(1)
        print "Client's upload test finish"
        print "Preparing for client's download"
        Client_info = addr
        #avg = speed_convert(avg_speed/(second-3))
        avg = speed_convert(avg_speed/5)
        print "Client's upload: " + avg
        for i in range(100):
            sock.sendto(avg, Client_info)
        time.sleep(1)
        for i in range(50):
            sock.sendto(avg, Client_info)
        time.sleep(4)
        print UDP_IP
        try:
        #    speed = monocell("speed")
            send = monocell("send")

        #    speed.start()
            send.start()
        except:
            print "internal error!"
            system("pause")    

if __name__ == "__main__":
    second = 10
    UDP_IP = ""       # Symbolic name meaning all available interfaces
    UDP_PORT = 5005            # Arbitrary non-privileged port
    Client_info = ""
    data = 0
    avg_speed = 0
    count = 0
    MESSAGE = "Hello, World!" * 113
    if len(sys.argv) > 1:
        UDP_PORT = int(sys.argv[1])
    try:
        sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))
        try:
            speed = monocell("speed")
            receive = monocell("receive")

            speed.start()
            receive.start()
        except:
            print "internal error!"
    except:
        print "socket error"



