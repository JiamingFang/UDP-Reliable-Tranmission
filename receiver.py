from socket import *
import sys
import packet

def main():
    if len(sys.argv) == 5:
        host_adr = sys.argv[1]
        port_ack = int(sys.argv[2])
        port_data = int(sys.argv[3])
        file_name = sys.argv[4]

        f = open(file_name, "w")
        arrivelog = open("arrival.log", "w")
        expecteseq = 0

        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('',port_data))


        sndpkt = packet.packet.create_ack(-1)

        while True:
            data,clientAddress = serverSocket.recvfrom(2048)
            packet1 = packet.packet.parse_udp_data(data)
            #log arrival
            if packet1.data != '':
                arrivelog.write(packet1.data + '\n')
            #if expected packet arrives
            if packet1.type == 1 and packet1.seq_num == expecteseq and packet1.data != '':
                f.write(packet1.data)
                sndpkt = packet.packet.create_ack(expecteseq)
                serverSocket.sendto(sndpkt.get_udp_data(),(host_adr,port_ack))
                expecteseq= (1 + expecteseq)%32 
            #if arrived is not expected
            elif packet1.type == 1 and packet1.data != '':
                serverSocket.sendto(sndpkt.get_udp_data(),(host_adr,port_ack))
            #if EOT,close socket, send back EOT
            elif packet1.type == 2:
                serverSocket.sendto(packet1.get_udp_data(),(host_adr,port_ack))
                serverSocket.close()
                print("break")
                break
        f.close()


main()