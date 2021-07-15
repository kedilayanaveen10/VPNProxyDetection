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
import requests
import tkinter as tk
import tkinter.simpledialog as simpledialog
from toolTipText import *
import re #regular expression
from cryptography.fernet import Fernet

HEIGHT = 300
WIDTH = 500

def update_ui():
	root.update_idletasks()
	root.update()

#utility method for ip validation
def is_ipv4(i):
	try:
		return str(int(i)) == i and 0<=int(i)<=255
	except:
		return False

#method to validate ip address
def validate_ip(ip):
	if ip.count(".")==3 and all(is_ipv4(i) for i in ip.split(".")):
		return True
	return False

def validate_domain(domain):
	regex = "^((?!-)[A-Za-z0-9]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}" #regex to validate domain name
	p = re.compile(regex) #compile regex
	if re.search(p,domain):
		return True
	return False

def ip_check():
	ip_addr = simpledialog.askstring(title="IP Address", prompt="Enter the IP address to check: ")
	if ip_addr is None:
		return
	if not validate_ip(ip_addr):
		tk.messagebox.showerror("Invalid IP", "The IP address entered is not a valid IP address")
		return
	#api call to check ip address
	url = "https://api.hetrixtools.com/v2/" + api_key + "/blacklist-check/ipv4/" + ip_addr + "/"
	ip_label['text'] = "Checking..."
	update_ui()
	response = requests.get(url)
	result = response.json()
	ip_label['text'] = ""
	update_ui()
	tk.messagebox.showinfo("Result", format_response(result))

def domain_check():
	domain_name = simpledialog.askstring(title="Domain", prompt="Enter the domain name to check: ")
	if domain_name is None:
		return
	if not validate_domain(domain_name):
		tk.messagebox.showerror("Invalid Domain Name", "The domain name entered is not a valid domain name")
		return
	#api call to check domain name
	url = "https://api.hetrixtools.com/v2/" + api_key + "/blacklist-check/domain/" + domain_name + "/"
	domain_label['text'] = "Checking..."
	update_ui()
	response = requests.get(url)
	result = response.json()
	domain_label['text'] = ""
	update_ui()
	tk.messagebox.showinfo("Result", format_response(result))

#method to format the json result into response string
def format_response(result):
	try:
		status = result['status']
		calls_left = result['api_calls_left']
		credits_left = result['blacklist_check_credits_left']
		blacklist_count = result['blacklisted_count']
		listings = ""
		if blacklist_count>0:
			listings = "Listed on:\n"
			for rbl in result['blacklisted_on']:
				listings += ">" + rbl['rbl'] + "\n" #+ rbl['delist'] + "\n"
		formatted_response = "Status: %s\nBlacklisted on %s databases\n%s" % (status,blacklist_count,listings)
	except Exception as e:
		formatted_response = "Formatting error: " + e
	return formatted_response

#key for api call

f = open("encryptedData","r")
key = bytes(f.readline(),"utf-8")
encoded_api = bytes(f.readline(),"utf-8")
f.close()
cipher_suite = Fernet(key)
api_key = cipher_suite.decrypt(encoded_api).decode("utf-8")

root = tk.Tk()
root.title("Real-time Blacklist Check")
root.option_add('*Dialog.msg.font', 'Helvetica 12') #change font of popup messages

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#adding background image
bg_img = tk.PhotoImage(file='images/blacklist.png')
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1,relheight=1)

#creating frame for buttons
frame = tk.Frame(root, bg='black', bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.3,anchor='n')

ipCheckButton = tk.Button(frame, text="Check IP", font=('Courier',12), bg='gray', command=lambda: ip_check())
ipCheckButton.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.5)
CreateToolTip(ipCheckButton, text="Check if an IP address is blacklisted in RBL databases")

domainCheckButton = tk.Button(frame, text="Check Domain", font=('Courier',12), bg='gray', command=lambda: domain_check())
domainCheckButton.place(relx=0.6, rely=0.1, relwidth=0.35, relheight=0.5)
CreateToolTip(domainCheckButton, text="Check if a domain is blacklisted in RBL databases")

ip_label = tk.Label(frame, font=('Courier',12), anchor='s', justify='left', bd=1)
ip_label.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.3)
ip_label.config(bg='black', foreground='white')

domain_label = tk.Label(frame, font=('Courier',12), anchor='s', justify='left', bd=1)
domain_label.place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.3)
domain_label.config(bg='black', foreground='white')

root.mainloop()
#api_key = '186634fde8f72bb688f0f95f952f66e1'