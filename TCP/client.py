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
    global recv_size,speed_sum,count,period,start_measure,stop_measure
    if name=="speed":
        stop_calc = 0    # anchor to indicate when to send message once
        while True:
            time.sleep(1)         # pause for 1 second
            if recv_size == 4:    # finish signal "done" size
                break
            if recv_size > 0:
                count  = count + 1    # how many second after starting to record
            if count > start_measure and count <=stop_measure:    # record only in this period
                speed_sum = speed_sum + recv_size    
            if recv_size == 0 and count > 9:
                if stop_calc == 0:
                    print "Waiting for Response..."
                    stop_calc = 1
            else:
                print speed_convert(recv_size)    # print realtime speed statistics for debugging
            recv_size = 0
    if name=="receive":
        while 1:
            recv_data = s.recv(1460)
            recv_size = recv_size + len(recv_data) + 54
            if len(recv_data) == 4 and recv_data=="done":    # finish signal from sender
                recv_size = 4
                break
        print "\n######### Download Speed: " + speed_convert(speed_sum/period) + " #########\n"
        s.close()
    if name=="send":
        print "Uploading..."   
        garbage = "Hello, World!" * 112    # payload
        t = time.time()                    # Start time
        while True:
            s.send(garbage)                # send garbage
            if time.time() - t > second:   # if sending for N seconds
                time.sleep(7)              # wait for retransmission
                s.send("done")             # send finish signal
                break
        print "All recv_size sent to server"
        recv_data, addr = s.recvfrom(2048)    # receive average speed statistic from receiver
        print "\n######### Upload Speed: " + recv_data + " #########"  # print statistic
        time.sleep(1)
        print(" ")
        print "Waiting for download test..."
        try:
            speed = multi("speed")
            receive = multi("receive")

            speed.start()
            receive.start()
        except:
            print "internal error!"
      
if __name__ == "__main__":
    second = 10
    HOST = '192.168.1.119'    # The default host
    recv_size = 0             # receive recv_size size
    speed_sum = 0             # accumulate every one second speed avg
    count = 0                 # receive data for N seconds
    start_measure = 4         # what time to accumulate speed avg to $speed_sum
    stop_measure = 9          # what time to stop accumulate speed avg
    period = stop_measure - start_measure  # the time from $start_measure to $stop_measure

    if len(sys.argv) > 1:
        HOST = sys.argv[1]    # assign server IP address
    PORT = 50007              # port used by the server
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp socket

    try:
        s.connect((HOST, PORT))
        try:
            send = multi("send")   
            send.start()
        except:
            print "internal error!"
            system("pause")
    except:
        print "connection refused!"
        system("pause")


