import os
from threading import Thread

def browsing():
	os.system('python3 AutomaticBrowsingScript.py')
	
def packetCapture():
	os.system('sudo python3 PacketCaptureScript.py')
	
Thread(target = browsing).start()	#Start browsing thread
Thread(target = packetCapture).start()	#Start packet capture thread
