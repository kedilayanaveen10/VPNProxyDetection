import socket
import sys
import csv
import subprocess
from struct import *

#Create an INET, StreamingSocket

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error as e:
	print('Socket creation failed. Error Code {} Message {}'.format(str(e[0]),str(e[1])))
	sys.exit()

outputFile = open('ProxyCapture.csv','w',newline='')
writer = csv.writer(outputFile)

#Write top row
writer.writerow(['Version', 'Protocol', 'TTL', 'SrcAddress', 'DestAddress', 'SrcPort', 'DestPort', 'SeqNum', 'AckNum', 'Flag', 'DataSize', 'Service', 'Label'])

#Receive packet
while True:
	packet = s.recvfrom(65565)
	
	#Transfer tuple content to string type
	packet = packet[0]
	
	#Take 1st 20 bytes for IP header
	ip_header = packet[0:20]
	
	#Unpack from bytes format
	iph = unpack('!BBHHHBBH4s4s', ip_header)
	version_ihl = iph[0]
	version = version_ihl >> 4
	ihl = version_ihl & 0xF
	iph_length = ihl * 4
	ttl = iph[5]
	protocol = iph[6]
	s_addr = socket.inet_ntoa(iph[8])
	d_addr = socket.inet_ntoa(iph[9])
	
	#TCP header starts right after IP header and is ususally 20 bytes long
	tcp_header = packet[20:40]
	
	#Unpack from byte format
	tcph = unpack('!HHLLBBHHH', tcp_header)
	source_port = tcph[0]
	dest_port = tcph[1]
	sequence = tcph[2]
	ack = tcph[3]
	doff_reserved = tcph[4]
	tcph_length = doff_reserved >> 4
	h_size = iph_length + tcph_length * 4
	data_size = len(packet) - h_size
	
	#Select byte containing TCP flags
	tcpFlag = packet[33:34].hex()
	
	if tcpFlag == "01":
		Flag = "FIN"
	elif tcpFlag == "02":
		Flag = "SYN"
	elif tcpFlag == "03":
		Flag = "FIN-SYN"
	elif tcpFlag == "08":
		Flag = "PSH"
	elif tcpFlag == "09":
		Flag = "FIN-PSH"
	elif tcpFlag == "0A":
		Flag = "SYN-PSH"
	elif tcpFlag == "10":
		Flag = "ACK"
	elif tcpFlag == "11":
		Flag = "FIN-ACK"
	elif tcpFlag == "12":
		Flag = "SYN-ACK"
	elif tcpFlag == "18":
		Flag = "PSH-ACK"
	else:
		Flag = "OTH"
	
	#Select only HTTP/HTTPS packets for logging
	if source_port == 80 or source_port == 443:
		if source_port == 80:
			writer.writerow([str(version), str(protocol), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(ack), Flag, str(data_size), "HTTP", "1"])
			print("Packets captured")
		else:
			writer.writerow([str(version), str(protocol), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(ack), Flag, str(data_size), "HTTPS", "1"])
			print("Packets captured")

outputFile.close()


