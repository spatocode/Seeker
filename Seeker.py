import os
import time
import socket
import struct
from ctypes import *

class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_ulong),
        ("dst",             c_ulong),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dest_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            print("protocol_number_ip", self.protocol_num)
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class Sniffer():
    def __init__(self, *args, **kwargs):
        print("Sniffing started")
        host = "127.0.0.1"
        #socket.gethostbyname(socket.gethostname())
        
        if os.name == "nt":
            # sniff all coming packets regardless of protocol
            socket_protocol = socket.IPPROTO_IP
            packet_interface = socket.AF_INET
        else:
            socket_protocol = socket.IPPROTO_ICMP
            packet_interface = socket.AF_PACKET

        sniffer = socket.socket(packet_interface, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        # include IP headers in the capture
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # send IOCTL to setup promiscious mode on windows
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        
        try:
            no = 0
            while True:
                if self.shouldrun == False:
                    return
                # read in a packet
                raw_buffer = sniffer.recvfrom(65565)[0]
                
                #create an IP header from the first 20 bytes of the buffer
                ip_header = IP(raw_buffer[0:20])

                # print out the protocol that was detected and the hosts
                print("[%s] %s: %s -> %s" % (time.asctime(), ip_header.protocol, ip_header.src_address, ip_header.dst_address))

            # handle CTRL-C
        except KeyboardInterrupt:
            # turn off promiscuos mode on windows
            if os.name == "nt":
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == "__main__":
    Sniffer()