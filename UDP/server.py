import datetime
import time
from threading import Thread
import socket
from os import system
import sys


class monocell(Thread):

    def __init__(self,name):

        Thread.__init__(self)
        self.name = name

    def run(self):

        heart(self.name)


def speed_convert(recv_size):                           #for human-readable output

    calc = recv_size*8                                  # convert from byte to bit
    if calc > 1024:                                     # if > 1Kb
        if calc/1024 > 1024:                            # if > 1Mb
            return str(float(calc)/1024/1024) + " Mbps"

        else:
            return  str(float(calc)/1024) + " Kbps"
    else:
        return str(calc) + " bps"


def heart(name):

    global recv_size,UDP_IP,Client_info,speed_sum,count
    if name=="speed":
        while True:
            time.sleep(1)
            if recv_size == 4:                          # finish signal "done" size
                break
            if recv_size > 0:
                count  = count + 1                      # how many second after starting to record
            if count > start_measure and count < stop_measure: # record only in this period
                speed_sum = speed_sum + recv_size
            print speed_convert(recv_size)              # print realtime speed statistics for debugging
            recv_size = 0

    if name=="send":
        print "Uploading..."
        t = time.time()                                 # Start time
        while True:
            #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            sock.sendto(MESSAGE, Client_info)           # send garbage
            if time.time() - t > second:                # if sending for N seconds
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
            recv_size = recv_size + len(recv_data) + 42
            if len(recv_data) == 4:
                recv_size = 4
                break
        time.sleep(1)
        print "Client's upload test finish"
        print "Preparing for client's download"
        Client_info = addr
        #avg = speed_convert(speed_sum/(second-3))
        avg = speed_convert(speed_sum/period)
        print "Client's upload: " + avg
        for i in range(100):                   # send average speed statistic from sender
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
    UDP_IP = ""                                 # Symbolic name meaning all available interfaces
    UDP_PORT = 5005                             # Arbitrary non-privileged port
    Client_info = ""                            # to record client's information
    recv_size = 0
    speed_sum = 0
    count = 0
    start_measure = 4                           # what time to accumulate speed avg to $speed_sum
    stop_measure = 10                           # what time to stop accumulate speed avg
    period = stop_measure - start_measure - 1   # the time from $start_measure to $stop_measure
    MESSAGE = "Hello, World!" * 113             # payload
    if len(sys.argv) > 1:
        UDP_PORT = int(sys.argv[1])
    try:
        sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM)     # UDP
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
