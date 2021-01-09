#importing necessary libraries
import tkinter as tk #for GUI
import tkinter.messagebox
from tkinter.filedialog import askopenfilename #to select test dataset
from tkinter.ttk import Progressbar, Style #to display progress
from toolTipText import * #manually created to display tooltip text
import os #to run other python scripts
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split #for splitting dataset into train and test data
from sklearn.preprocessing import StandardScaler #for scaling the dataset
from sklearn.neighbors import KNeighborsClassifier #KNN classifier
from sklearn.metrics import accuracy_score #to find accuracy of model
from sklearn.tree import DecisionTreeClassifier #Decision Tree Classifier
from sklearn.neural_network import MLPClassifier #MLP Classifier
from sklearn.metrics import f1_score #to find F1 score of model

#window dimensions
HEIGHT = 500
WIDTH = 800
    
#to change buttons state to normal or disabled
def change_buttons_state(state):
	for button in buttons:
		button['state'] = state

#reset progress bar and clear canvas
def clear_ui():
	result['text'] = ""
	progressBar['value'] = 0
	s.configure("LabeledProgressbar", text="")
	update_ui()

def update_ui():
	root.update_idletasks()
	root.update()

#Check blacklisted ip/domain
def check_blacklist():
	clear_ui()
	os.system('python3 rbl_check.py')

def new_capture():
	clear_ui()
	os.system('sudo -A python3 TestPacketCaptureScript.py') #run script to create new packet capture file

#display help
def help():
	clear_ui()
	popup = tk.Tk()
	popup.geometry("1000x500")
	popup.title("Help")

	canvas = tk.Canvas(popup)

	#Create scrollbars
	xScrollBar = tk.Scrollbar(popup, orient='horizontal', command=canvas.xview)
	yScrollBar = tk.Scrollbar(popup, orient='vertical', command=canvas.yview)

	#ok button
	ok = tk.Button(popup, text="OK", command=popup.destroy)

	yScrollBar.pack(side='right', fill='y')
	xScrollBar.pack(side='bottom', fill='x')
	ok.pack(side='bottom')
	canvas.pack(side='top', fill='both', expand='true')

	#Attach canvas to scrollbars
	canvas.configure(xscrollcommand=xScrollBar.set)
	canvas.configure(yscrollcommand=yScrollBar.set)

	#Create frame inside canvas
	frame = tk.Frame(canvas)
	canvas.create_window((0,0), window=frame, anchor='nw')
	frame.bind('<Configure>', lambda event : canvas.configure(scrollregion=canvas.bbox('all'))) 

	#display help content
	text=tk.Text(frame,width=250,height=60)
	text.pack()
	text.config(state="normal")
	helpFile = open('README.md','r')
	lines = helpFile.readlines()
	for k, line in enumerate(lines):
		text.insert('end', line)
	text.config(state="disabled")

	popup.mainloop()		

#function to select the test dataset
def get_test_dataset():
	filename = askopenfilename(title="Choose Test Dataset", filetypes=(("CSV Files","*.csv"),))
	return filename

#function to analyse packets for vpn
def vpn_check():
	change_buttons_state('disabled')
	result['text'] = ""
	progressBar['value'] = 0
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(0))
	update_ui()

	#load datasets
	vpnData = pd.read_csv('Datasets/Training/vpnDataset.csv')
	testFileName = get_test_dataset()
	if not testFileName:
		change_buttons_state('normal')
		return
	testData = pd.read_csv(testFileName)

	cols = ['Version', 'Protocol', 'TTL', 'SrcAddress', 'DestAddress', 'SrcPort', 'DestPort', 'SeqNum', 'AckNum', 'Flag', 'DataSize', 'Service']
	test_cols = list(testData.columns.values)

	if cols != test_cols:
		tk.messagebox.showerror("Invalid Dataset","Dataset is not of required specifications!!!\nLook at instructions by clicking at '?' button for dataset specifications.")
		change_buttons_state('normal')
		return

	if testData.empty:
		tk.messagebox.showerror("Dataset Empty", "The dataset is empty. Make sure you have captured the packets properly.\nRecommended to keep capturing for 1-2 minutes")
		change_buttons_state('normal')
		return

	dataset_size_limit = 700000	#in bytes
	if os.stat(testFileName).st_size > dataset_size_limit:
		if not messagebox.askyesno("Large Dataset","The dataset seems to be very large. It could take several minutes and may use a lot of system resources. Are you sure you want to continue?"):
			change_buttons_state('normal')
			return

	#drop irrelevant columns
	drop_cols = ['Version', 'Protocol', 'SrcAddress', 'DestAddress']

	vpnData = vpnData.drop(drop_cols,1)
	testData = testData.drop(drop_cols,1)

	#Drop duplicates in training dataset
	vpnData = vpnData.drop_duplicates()

	progressBar['value'] = 10
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(10))
	update_ui()

	X = vpnData.iloc[:,:-1]
	y = vpnData.iloc[:,-1]

	X_testSet = testData.iloc[:,:]

	#Using One Hot encoding to encode string data to numerical data
	oneHotFeatures = ['Flag','Service']

	def encode_and_bind(original_dataframe, feature_to_encode):
	    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
	    res = pd.concat([original_dataframe, dummies], axis=1)
	    res = res.drop([feature_to_encode], axis=1)
	    return(res) 

	frames = [X, X_testSet]
	temp = pd.concat(frames)

	for feature in oneHotFeatures:
	    temp = encode_and_bind(temp, feature)

	X = temp.iloc[0:len(X),:]
	X_testSet = temp.iloc[-len(X_testSet):,:]

	progressBar['value'] = 20
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(20))

	update_ui()

	#split data into train and test set
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

	#Scaling the data
	scaler = StandardScaler()
	X_train = scaler.fit_transform(X_train)
	X_test = scaler.transform(X_test)
	X_testSet = scaler.transform(X_testSet)

	progressBar['value'] = 30
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(30))
	update_ui()

	#KNN - Classifier
	knn = KNeighborsClassifier(n_neighbors=15,metric='minkowski',p=2)
	knn.fit(X_train,y_train)
	y_pred = knn.predict(X_test)
	y_predTest = knn.predict(X_testSet)

	result['text'] = '\n\n------------------------'
	result['text'] += '\nKNN-Classifier'

	result['text'] += "\nAccuracy of model on training dataset: " + str(accuracy_score(y_test,y_pred))
	knn_prob = sum(y_predTest)/len(y_predTest)
	result['text'] += "\nProbability that VPN was used: " + str(knn_prob)

	progressBar['value'] = 50
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(50))
	update_ui()

	#Decision Tree Classifier
	DTC = DecisionTreeClassifier(random_state=0)
	model = DTC.fit(X_train,y_train)
	y_pred = model.predict(X_test)
	y_predTest = model.predict(X_testSet)

	result['text'] += '\n\n------------------------'
	result['text'] += '\nDecision Tree Classifier'

	result['text'] += "\nAccuracy of model on training dataset: " + str(accuracy_score(y_test,y_pred))
	dt_prob = (sum(y_predTest)/len(y_predTest))
	result['text'] += "\nProbability that VPN was used: " + str(dt_prob)

	progressBar['value'] = 70
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(70))
	update_ui()

	#MLP Classifier
	clf = MLPClassifier(max_iter=1500,random_state=1)
	clf.fit(X_train,y_train)
	y_pred = clf.predict(X_test)
	y_predTest = clf.predict(X_testSet)

	result['text'] += '\n\n------------------------'
	result['text'] += '\nMLP Classifier'

	result['text'] += "\nModel F1 score: " + str(f1_score(y_test,y_pred))
	mlp_prob = (sum(y_predTest)/len(y_predTest))
	result['text'] += "\nProbability that VPN was used: " + str(mlp_prob)
	progressBar['value'] = 100
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(100))
	update_ui()
	tk.messagebox.showinfo("VPN Probability", "Possibility of VPN being used: {:.2%}".format(((knn_prob+dt_prob+mlp_prob)/3.0)))
	change_buttons_state('normal')


#function to analyse packets for proxy
def proxy_check():
	change_buttons_state('disabled')
	result['text'] = ""
	progressBar['value'] = 0
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(0))
	update_ui()

	#load datasets
	proxyData = pd.read_csv('Datasets/Training/proxyDataset.csv')
	testFileName = get_test_dataset()
	if not testFileName:
		change_buttons_state('normal')
		return
	testData = pd.read_csv(testFileName)

	cols = ['Version', 'Protocol', 'TTL', 'SrcAddress', 'DestAddress', 'SrcPort', 'DestPort', 'SeqNum', 'AckNum', 'Flag', 'DataSize', 'Service']
	test_cols = list(testData.columns.values)

	if cols != test_cols:
		tk.messagebox.showerror("Invalid Dataset","Dataset is not of required specifications!!!\nLook at instructions by clicking at '?' button for dataset specifications.")
		change_buttons_state('normal')
		return

	if testData.empty:
		tk.messagebox.showerror("Dataset Empty", "The dataset is empty. Make sure you have captured the packets properly.\nRecommended to keep capturing for 1-2 minutes")
		change_buttons_state('normal')
		return

	dataset_size_limit = 700000	#in bytes
	if os.stat(testFileName).st_size > dataset_size_limit:
		if not messagebox.askyesno("Large Dataset","The dataset seems to be very large. It could take several minutes and may use a lot of system resources. Are you sure you want to continue?"):
			change_buttons_state('normal')
			return

	progressBar['value'] = 10
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(10))
	update_ui()

	#drop irrelevant columns
	drop_cols = ['Version', 'Protocol', 'SrcAddress', 'DestAddress']

	proxyData = proxyData.drop(drop_cols,1)
	testData = testData.drop(drop_cols,1)

	#Drop duplicates in training dataset
	proxyData = proxyData.drop_duplicates()

	progressBar['value'] = 20
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(20))
	update_ui()

	X = proxyData.iloc[:,:-1]
	y = proxyData.iloc[:,-1]

	X_testSet = testData.iloc[:,:]

	#Using One Hot encoding to encode string data to numerical data
	oneHotFeatures = ['Flag','Service']

	def encode_and_bind(original_dataframe, feature_to_encode):
	    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
	    res = pd.concat([original_dataframe, dummies], axis=1)
	    res = res.drop([feature_to_encode], axis=1)
	    return(res) 

	frames = [X, X_testSet]
	temp = pd.concat(frames)

	for feature in oneHotFeatures:
	    temp = encode_and_bind(temp, feature)

	X = temp.iloc[0:len(X),:]
	X_testSet = temp.iloc[-len(X_testSet):,:]

	progressBar['value'] = 30
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(30))
	update_ui()

	#split data into train and test set
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

	#Scaling the data
	scaler = StandardScaler()
	X_train = scaler.fit_transform(X_train)
	X_test = scaler.transform(X_test)
	X_testSet = scaler.transform(X_testSet)

	progressBar['value'] = 40
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(40))
	update_ui()

	#KNN - Classifier
	knn = KNeighborsClassifier(n_neighbors=7,metric='minkowski',p=2)
	knn.fit(X_train,y_train)
	y_pred = knn.predict(X_test)
	y_predTest = knn.predict(X_testSet)

	result['text'] = '\n\n------------------------'
	result['text'] += '\nKNN-Classifier'

	result['text'] += "\nAccuracy of model on training dataset: " + str(accuracy_score(y_test,y_pred))
	knn_prob = sum(y_predTest)/len(y_predTest)
	result['text'] += "\nProbability that proxy was used: " + str(knn_prob)

	progressBar['value'] = 70
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(70))
	update_ui()

	#MLP Classifier
	clf = MLPClassifier(max_iter=1500,random_state=1)
	clf.fit(X_train,y_train)
	y_pred = clf.predict(X_test)
	y_predTest = clf.predict(X_testSet)

	result['text'] += "\n\n------------------------"
	result['text'] += '\nMLP Classifier'

	result['text'] += "\nModel F1 score: " + str(f1_score(y_test,y_pred))
	mlp_prob = sum(y_predTest)/len(y_predTest)
	result['text'] += "\nProbability that VPN was used: " + str(mlp_prob)
	progressBar['value'] = 100
	s.configure("LabeledProgressbar", text="Analysed: {0}%".format(100))
	update_ui()
	tk.messagebox.showinfo("VPN Probability", "Possibility of Proxy being used: {:.2%}".format(((knn_prob+mlp_prob)/2.0)))
	change_buttons_state('normal')


root = tk.Tk()
root.title("VPN-Proxy Detection")
root.option_add('*Dialog.msg.font', 'Helvetica 12')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#adding background image
background_img = tk.PhotoImage(file='images/vpn.png')
background_label = tk.Label(root, image=background_img)
background_label.place(relwidth=1, relheight=1)

#creating a frame for buttons
frame = tk.Frame(root, bg='black', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

#button to check proxy
proxyTestButton = tk.Button(frame, text="Proxy Check", font=('Courier', 12), bg='gray', command=lambda: proxy_check())
proxyTestButton.place(relwidth=0.3, relheight=1)
CreateToolTip(proxyTestButton,text="Check if a proxy was used on a .csv packet capture file")

#button to check blacklisted ip/domain
rblCheckButton = tk.Button(frame, text="RBL Check", font=('Courier', 12), bg='gray', command=lambda: check_blacklist())
rblCheckButton.place(relx=0.35, relwidth=0.3, relheight=1)
CreateToolTip(rblCheckButton,text="Check if an IP address or a domain is blacklisted in the RBL databases")

#button to check vpn
vpnTestButton = tk.Button(frame, text="VPN Check", font=('Courier',12), bg='gray', command=lambda: vpn_check())
vpnTestButton.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
CreateToolTip(vpnTestButton,text="Check if a VPN was used on a .csv packet capture file")

#creating frame to display results
lower_frame = tk.Frame(root, bg='black', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#adding a progress bar
s = Style(lower_frame)
s.layout("LabeledProgressbar",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
s.configure("LabeledProgressbar", foreground='black', background='#00FF00')
progressBar = Progressbar(lower_frame, orient='horizontal', length=100, mode='determinate', style="LabeledProgressbar")
progressBar.place(relwidth=1)

#display final result here
result = tk.Label(lower_frame, font=('Courier',8), anchor='nw', justify='left', bd=4)
result.place(rely=0.1, relwidth=1, relheight=0.9)

#button to clear canvas
clearButton = tk.Button(root, text="Clear", bd=3, font=('Courier',12), bg='gray', command=lambda:clear_ui())
clearButton.place(relx=0.77,rely=0.85)
CreateToolTip(clearButton,text="Clear the entries in canvas")

#adding help
help_img = tk.PhotoImage(file='images/help.gif')
helpButton = tk.Button(root, bd=3, command=lambda:help())
helpButton.config(image=help_img)
helpButton.place(relx=0.8, rely=0.93, relwidth=0.05, relheight=0.07)
CreateToolTip(helpButton,text="Instructions to use")

#button to create new test capture file
newCaptureButton = tk.Button(root, text="New Capture", bd=3, font=('Courier',12), bg='gray', command=lambda:new_capture())
newCaptureButton.place(relx=0.1, rely=0.9, relwidth=0.2, relheight=0.1)
CreateToolTip(newCaptureButton,text="Create a new test packet capture")

#variable holding all button variables
buttons = [proxyTestButton, vpnTestButton, rblCheckButton, clearButton, helpButton, newCaptureButton]

def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()