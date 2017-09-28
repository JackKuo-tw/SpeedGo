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


def speed_convert(recv_size):    #for human-readable output

    calc = recv_size*8           # convert from byte to bit
    if calc > 1024:              # if > 1Kb
        if calc/1024 > 1024:     # if > 1Mb
            return str(float(calc)/1024/1024) + " Mbps"
        else:
            return  str(float(calc)/1024) + " Kbps"
    else:
        return str(calc) + " bps"


def heart(name):

    global recv_size,speed_sum,count
    if name=="speed":
        while True:
            time.sleep(1)                                       # pause for 1 second
            if recv_size == 4:                                  # finish signal "done" size
                break
            if recv_size > 0:
                count  = count + 1                              # how many second after starting to record
            if count > start_measure and count < stop_measure:  # record only in this period
                speed_sum = speed_sum + recv_size
            print speed_convert(recv_size)                      # print realtime speed statistics for debugging
            recv_size = 0

    if name=="receive":
            while 1:
                recv_data, addr = sock.recvfrom(2048)
                recv_size = recv_size + len(recv_data) + 42
                if len(recv_data) == 4:
                    recv_size = 4
                    break
            print "Client's upload test finish"
            print "###### download speed: " + speed_convert(speed_sum/period) + " ######"

    if name=="send":
        print "Uploading..."
        t = time.time()                                     # Start time
        while True:
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))        # send garbage
            if time.time() - t > second:                    # if sending for N seconds
                for i in range(5):
                    sock.sendto("done", (UDP_IP, UDP_PORT)) # send finish signal
                time.sleep(1)
                for i in range(5):
                    sock.sendto("done", (UDP_IP, UDP_PORT))
                break
        print "Upload test finish"
        recv_data, addr = sock.recvfrom(2048)          # receive average speed statistic from receiver
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
    UDP_IP = "10.21.20.174"                     # The default host
    UDP_PORT = 5005                             # port used by the server
    count = 0                                   # receive data for N seconds
    speed_sum = 0                               # accumulate every one second speed avg
    start_measure = 4                           # what time to accumulate speed avg to $speed_sum
    stop_measure = 10                           # what time to stop accumulate speed avg
    period = stop_measure - start_measure - 1   # the time from $start_measure to $stop_measure
    MESSAGE = "Hello, World!" * 113             # payload
    recv_size = 0
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
        send = monocell("send")
        send.start()
    except:
        print "internal error!"
        system("pause")


