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
            return str(round(float(calc)/1024/1024,2)) + " Mbps"

        else:
            return  str(round(float(calc)/1024,2)) + " Kbps"
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
        time.sleep(3)
        brake = 0

    if name=="receive2":
        conn2, info = s2.accept()
        t2 = time.time()
        print 'Connected by', info # client's IP address and port number
        while 1:
            recv_recv_size = conn2.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if time.time() - t2 > 20 or (len(recv_recv_size) == 4 and recv_recv_size=="done"):    # finish signal from sender
                recv_size = 4
                time.sleep(1)
                #conn2.shutdown(socket.SHUT_RDWR)
                conn2.close()
                break
    if name=="receive3":
        conn3, info = s3.accept()
        t3 = time.time()
        print 'Connected by', info # client's IP address and port number
        while 1:
            recv_recv_size = conn3.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if time.time() - t3 > 20 or (len(recv_recv_size) == 4 and recv_recv_size=="done"):    # finish signal from sender
                recv_size = 4
                time.sleep(3)
                #conn3.shutdown(socket.SHUT_RDWR)
                conn3.close()
                break
    if name=="receive4":
        conn4, info = s4.accept()
        t4 = time.time()
        print 'Connected by', info # client's IP address and port number
        while 1:
            recv_recv_size = conn4.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if time.time() - t4 > 20 or (len(recv_recv_size) == 4 and recv_recv_size=="done"):    # finish signal from sender
                recv_size = 4
                time.sleep(5)
                #conn4.shutdown(socket.SHUT_RDWR)
                conn4.close()
                break
    if name=="receive5":
        conn5, info = s5.accept()
        t5 = time.time()
        print 'Connected by', info # client's IP address and port number
        while 1:
            recv_recv_size = conn5.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if time.time() - t5 > 20 or (len(recv_recv_size) == 4 and recv_recv_size=="done"):    # finish signal from sender
                recv_size = 4
                time.sleep(7)
                #conn5.shutdown(socket.SHUT_RDWR)
                conn5.close()
                break
    if name=="receive":
        conn, Client_info = s.accept()
        t1 = time.time()
        print 'Connected by', Client_info # client's IP address and port number
        while 1:
            recv_recv_size = conn.recv(2048)
            recv_size = recv_size + len(recv_recv_size) + 54    # payload len and header len
            if time.time() - t1 > 20 or (len(recv_recv_size) == 4 and recv_recv_size=="done"):    # finish signal from sender
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
    PORT2 = 50008
    PORT3 = 50009
    PORT4 = 50010
    PORT5 = 50011
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        PORT2 = PORT + 1
        PORT3 = PORT + 2
        PORT4 = PORT + 3
        PORT5 = PORT + 4
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
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s2.bind((HOST, PORT2))
            s3.bind((HOST, PORT3))
            s4.bind((HOST, PORT4))
            s5.bind((HOST, PORT5))
            s.listen(1)
            s2.listen(1)
            s3.listen(1)
            s4.listen(1)
            s5.listen(1)
            recv_size = 0
            brake = 1
            try:
                speed = multi("speed")
                receive = multi("receive")
                receive2 = multi("receive2")
                receive3 = multi("receive3")
                receive4 = multi("receive4")
                receive5 = multi("receive5")

                speed.start()
                receive.start()
                receive2.start()
                receive3.start()
                receive4.start()
                receive5.start()
            except:
                print "internal error!"
        except:
            print "socket error"
