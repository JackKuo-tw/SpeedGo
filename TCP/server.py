import datetime
import time
from threading import Thread
import socket
from os import system
import sys


class multi(Thread):

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
    global recv_size,Client_info,speed_sum,count,conn,period,start_measure,stop_measure,brake
    if name=="speed":
        while True:
            time.sleep(1)
            if recv_size == 4:               # finish signal "done" size
                break
            if recv_size > 0:
                count  = count + 1           # how many second after starting to record
            if count > start_measure and count <= stop_measure:  # record only in this period
                speed_sum = speed_sum + recv_size
            print speed_convert(recv_size)   # print realtime speed statistics for debugging
            recv_size = 0

    if name=="send":
        print "Uploading..."
        garbage = "Hello, World!" * 112            # payload
        t = time.time()                            # Start time
        while True:
            conn.sendto(garbage,Client_info)       # send garbage
            if time.time() - t > second:           # if sending for N seconds
                time.sleep(7)                      # wait for retransmission
                conn.sendto("done",Client_info)    # send finish signal
                break
        print "Client's download test finish"
        time.sleep(2)
        conn.close()
        brake = 0

    if name=="receive":
        conn, Client_info = s.accept()
        print 'Connected by', Client_info # client's IP address and port number
        while 1:
            recv_recv_size = conn.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if len(recv_recv_size) == 4 and recv_recv_size=="done":    # finish signal from sender
                recv_size = 4
                break
        time.sleep(1)
        print "Client's upload test finish"
        print "Preparing for client's download"
        avg = speed_convert(speed_sum/period)
        print "Client's upload: " + avg
        conn.sendto(avg, Client_info)    # send average speed statistic from sender
        time.sleep(2)
        try:
            send = multi("send")
            send.start()
        except:
            print "internal error!"

if __name__ == "__main__":
    HOST = ''                 
    PORT = 50007             
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    brake = 0
    while 1:
        if brake ==1:
            time.sleep(1)
            continue
        time.sleep(1)
        second = 10
        Client_info = ""          # to record client's information
        recv_size = 0             # receive recv_size size
        speed_sum = 0             # accumulate every one second speed avg
        count = 0                 # receive data for N seconds
        conn = ""
        start_measure = 4         # what time to accumulate speed avg to $speed_sum
        stop_measure = 9          # what time to stop accumulate speed avg
        period = stop_measure - start_measure  # the time from $start_measure to $stop_measure
        MESSAGE = "Hello, World!" * 113
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(1)
            recv_size = 0
            brake = 1
            try:
                speed = multi("speed")
                receive = multi("receive")

                speed.start()
                receive.start()
            except:
                print "internal error!"
        except:
            print "socket error"

