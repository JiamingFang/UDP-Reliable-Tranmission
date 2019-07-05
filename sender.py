from socket import *
import sys
import packet
import time
import threading

if len(sys.argv) == 5:
    host_adr = sys.argv[1]
    port_data = int(sys.argv[2])
    port_ack = int(sys.argv[3])
    file_name = sys.argv[4]
    sndpkt = []

    start = None

    base = 0
    nextseq = 0
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    readAll = False
    EOT = False

def send():
    global sndpkt
    global nextseq
    global start
    global readAll

    f = open(file_name, "r")
    seqlog = open("seqnum.log", "w")


    while True:
        #if eot break loop
        if EOT:
            print("break2")
            break
        #send data
        if(nextseq < (base+10)%32 or nextseq < base+10):
            if not readAll:
                character = f.read(500)
                if character == '':
                    readAll = True
                    f.close()
                print("char: "+character)
                if len(sndpkt) == 32:
                    sndpkt[nextseq] = packet.packet.create_packet(nextseq , character)
                else:
                    sndpkt.append(packet.packet.create_packet(nextseq , character))
                clientSocket.sendto(sndpkt[nextseq].get_udp_data(),(host_adr,port_data))
                if not readAll:
                    seqlog.write(str(nextseq)+'\n')
            if (base == nextseq):
                start = time.time()
            if not readAll:
                nextseq = (1 + nextseq)%32


        now = time.time()
        #check timeout
        if start != None and now != None and (now-start)*1000 > 200:
            print("TIMEOUT")
            start = time.time()
            if nextseq >= base:
                for i in range(base,nextseq):
                    seqlog.write(str(i)+'\n')
                    clientSocket.sendto(sndpkt[i].get_udp_data(),(host_adr,port_data))
            else:
                for i in range(base,32):
                    seqlog.write(str(i)+'\n')
                    clientSocket.sendto(sndpkt[i].get_udp_data(),(host_adr,port_data))
                for i in range(0,nextseq):
                    seqlog.write(str(i)+'\n')
                    clientSocket.sendto(sndpkt[i].get_udp_data(),(host_adr,port_data))
    


def recieve():
    global start
    global base
    global EOT
    acklog = open("ack.log", "w")
    clientSocket.bind(('',port_ack))

    while True:
        data,clientAddress = clientSocket.recvfrom(2048)
        packet1 = packet.packet.parse_udp_data(data)
        #if ack
        if packet1.type == 0:
            base = (packet1.seq_num + 1)%32
            acklog.write(str(packet1.seq_num)+'\n')
            print("base: "+str(base))
            if base == nextseq:
                start = None
            else:
                start = time.time()
        #EOT signal recieved from receiver, close socket
        elif packet1.type == 2:
            clientSocket.close()
            print("break2")
            break
        #if all packets send and recieved, send EOT
        if readAll and base == nextseq:
            packet1 = packet.packet.create_eot(nextseq)
            clientSocket.sendto(packet1.get_udp_data(),(host_adr,port_data))
            EOT = True
            print("EOT")


def create():
    #create second thread to recieve ack
    x = threading.Thread(target=recieve)
    x.start()


create()
send()