""" 
    The program when run, detects the use of anonymizing services in a test dataset
    
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import socket
import csv
from struct import *
import tkinter as tk
from threading import Thread
from pathvalidate import ValidationError, validate_filename
import tkinter.simpledialog as simpledialog
import platform
from toolTipText import *

#test_file is the name of the .csv file
def packet_capture(test_file):
	c = True
	#Create an INET, StreamingSocket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	except socket.error as e:
		tk.messagebox.showerror("Socket Error",e)
		c = False
	except Exception as e:
		tk.messagebox.showerror("Error!!!",e)
		c = False
	finally:
		if not c:
			startButton['state'] = 'normal'
			stopButton['state'] = 'disabled'
			label['text'] = ""
			return

	#create a csv file to store the captured packets
	outputFile = open('Datasets/Test/'+test_file,'w',newline='')
	writer = csv.writer(outputFile)

	#Write top row
	writer.writerow(['Version', 'Protocol', 'TTL', 'SrcAddress', 'DestAddress', 'SrcPort', 'DestPort', 'SeqNum', 'AckNum', 'Flag', 'DataSize', 'Service'])

	#Receive packet
	while True:
		if stop == 1:
			label['text'] = ""
			startButton['state'] = 'normal'
			break
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
				writer.writerow([str(version), str(protocol), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(ack), Flag, str(data_size), "HTTP"])
				print("Packets captured")
			else:
				writer.writerow([str(version), str(protocol), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(ack), Flag, str(data_size), "HTTPS"])
				print("Packets captured")

	#after stopping capture
	outputFile.close()
	tk.messagebox.showinfo("Capture Complete", "Test Capture is complete. You may now close the window")

#create thread to capture packets
def start_capture():
	startButton['state'] = 'disabled'
	stopButton['state'] = 'normal'
	#ask for file name
	test_file_name = simpledialog.askstring(title="File Name", prompt="Enter the test file name (without .csv extension): ", initialvalue='test')
	if test_file_name is None:
		startButton['state'] = 'normal'
		stopButton['state'] = 'disabled'
		return
	try:
		validate_filename(test_file_name, platform=platform.system()) #validate the filename for current OS
	except ValidationError as e:
		tk.messagebox.showerror("Invalid Filename", "The entered filename is invalid:\n" + str(e))
		startButton['state'] = 'normal'
		stopButton['state'] = 'disabled'
		return
	test_file_name += '.csv'
	global stop
	stop = 0

	t1 = Thread(target=packet_capture, args=(test_file_name,))
	t1.start()
	label['text'] = "Capturing packets..."

#complete execution of thread
def stop_capture():
	stopButton['state'] = 'disabled'
	global stop
	stop = 1
	label['text'] = 'Please wait...'

#main window
root = tk.Tk()
root.title("Packet Capture")
root.geometry("450x100")
root.resizable(False,False)
root.option_add('*Dialog.msg.font', 'Helvetica 12') #change font of popup messages

app = tk.Frame(root)
app.grid()

startButton = tk.Button(app, text="Start capture", width=15, font=('Courier',12), bg='gray', command=lambda: start_capture())
stopButton = tk.Button(app, text="Stop capture", width=15, font=('Courier',12), bg='gray', state='disabled', command=stop_capture)

CreateToolTip(startButton, text="Start packet capture")
CreateToolTip(stopButton, text="Stop packet capture")
startButton.grid(row=0,column=0)
stopButton.grid(row=0,column=1)

label = tk.Label(app, text="For better accuracy, capture packets for 1-2 minutes!", font=('Courier',9), anchor='w', justify='left')
label.grid(row=1, column=0, columnspan=2)

app.mainloop()
