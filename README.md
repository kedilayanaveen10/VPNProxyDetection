
Required Operating System: Ubuntu 20.04 or later


NECESSARY MODULES/LIBRARIES and PREREQUISITES:

	-tkinter (sudo apt-get install python3-tk)
	
	-tkscrolledframe (pip3 install tkScrolledFrame)
	
	-numpy (pip3 install numpy)
	
	-pandas (pip3 install pandas)
	
	-sklearn (pip3 install -U scikit-learn)

	-pathvalidate (sudo pip3 install pathvalidate)
	
	-ssh-askpass (sudo apt-get install -y ssh-askpass)
	
	-ssh-askpass-gnome (sudo apt-get install -y ssh-askpass-gnome)
	
	-SUDO_ASKPASS environment variable should be set to the path to ssh-askpass-gnome



INSTRUCTIONS:

1.How to run:

	-Open terminal
	
	-Run the script 'vpn_proxy_detection.py' using the below command
	
	-python3 vpn_proxy_detection.py
	
	-Make sure Datasets/Training/ folder contains 2 files: proxyDataset.csv and vpnDataset.csv

2.Proxy/VPN Check

	-on clicking proxy/vpn check, a prompt appears asking for the .csv file
	
	-by default the test files are stored in /Datasets/Test/ directory (it's a relative path)
	
	-the test capture should have the attributes ['Version', 'Protocol', 'TTL', 'SrcAddress', 'DestAddress', 'SrcPort', 'DestPort', 'SeqNum', 'AckNum', 'Flag', 'DataSize', 'Service'] in the same order
	
	-this application trains and test the data on machine learning models, recommended to have atleast 4 GB RAM

3.RBL Check

	-Real-time Blacklist checks if an IP address/domain is blacklisted in any of the RBL databases
	
	-an API is used to check the RBL databases, which is limited for a free version
	
	-2000 free API calls every month
	
	-100 free blacklist check credits every month
	
	-every API call will be cached for 30 min, if the result is found in cache then the check credits will not be used
	
	-free API calls and check credits left are not carried over to next month

4.New Capture

	-before capturing it asks for the file name; don't mention the .csv extension
	
	-this will generate a csv test capture of the required specifications
	
	-SUDO_ASKPASS environment variable should be set to path of ssh-askpass-gnome
	
	-SUDO_ASKPASS is necessary because the capture script needs root access to run, SUDO_ASKPASS will prompt you to enter the password
	
	-after clicking "Start Capture", the script starts packet capture in the background
	
	-clicking "Stop Capture" stops the background script
	
	-close the window only after it prompts "Safe to close" to ensure there are no zombie processes created
	
	-the test capture will be saved in (relative path) - /Datasets/Test/

5.Quick Check

	-This feature will check if an IP address or a domain is a VPN, Active VPN, Proxy, Tor endpoint, or an active tor endpoint.

	-an API call is made to check the IP address or the domain name entered for VPN, Proxy or tor endpoint.

	-the API call return the result in a matter of seconds and will not use any client-side resources.

6.Get CSV file from Wireshark capture

	-The file 'WiresharkToCSV.docx' contains the step by step instructions on how to get csv file of required specifications from a wireshark capture.


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