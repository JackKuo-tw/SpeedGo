import datetime
import time
from threading import Thread
import socket
import psutil
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

    global data,avg_speed,count
    if name=="speed":
        while True:
            time.sleep(1)
            if data == 4:
                break
            if data > 0:
                count  = count + 1
            if count > 4 and count < 10:
                avg_speed = avg_speed + data
            print speed_convert(data)
            data = 0

    if name=="receive":
            while 1:
                recv_data, addr = sock.recvfrom(2048)
                #print recv_data
                #print len(recv_data)
                data = data + len(recv_data) + 42
                if len(recv_data) == 4:
                    data = 4
                    break
            print "Client's upload test finish"
            #print "###### download speed: " + speed_convert(avg_speed/(second-3)) + " ######"
            print "###### download speed: " + speed_convert(avg_speed/5) + " ######"

    if name=="send":
        print "Uploading..."
        t = time.time()
        while True:
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            if time.time() - t > second:
                for i in range(5):
                    sock.sendto("done", (UDP_IP, UDP_PORT))
                time.sleep(1)
                for i in range(5):
                    sock.sendto("done", (UDP_IP, UDP_PORT))
                break
        print "Upload test finish"
        recv_data, addr = sock.recvfrom(2048)
        print "###### upload speed: " + recv_data + " ######"
        time.sleep(4)
        print "Waiting for download test..."
        try:
            speed = monocell("speed")
            receive = monocell("receive")

            speed.start()
            receive.start()
        except:
            print "internal error!"
            
if __name__ == "__main__":
    second = 10
    UDP_IP = "10.21.20.174"
    UDP_PORT = 5005
    count = 0
    avg_speed = 0
    MESSAGE = "Hello, World!" * 113
    data = 0
    if len(sys.argv) > 1:
        UDP_IP = sys.argv[1]
    if len(sys.argv) > 2:
        UDP_PORT = int(sys.argv[2])
    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    try:
        try:
            sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        except:
            print "connection refuse"
    #    speed = monocell("speed")
        send = monocell("send")

    #    speed.start()
        send.start()
    except:
        print "internal error!"
        system("pause")


