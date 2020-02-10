import os
import subprocess
import time
import ctypes, sys
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from pyautogui import press, typewrite, hotkey, moveTo, click, mouseDown, FAILSAFE
from PyPDF2 import PdfFileReader

kurzweil = subprocess.Popen(["python"], stdout=subprocess.PIPE)

def getConfig(key):
	#open config file
	configFile = open("config.txt", "r")
	
	#read through the file
	for line in configFile:
		if line.startswith("#"):
			# Ignore, line is comment
		elif line.split("=")[0] == key:
			#Key found, return value
			return line.split("=")[1]
		else:
			#No Key found
			print("No key of '%s' found in config file!" % key)

	configFile.close()

    
def openKurzweil():
    #open kurzweil
    FAILSAFE = False

	kurzweil3000path = getConfig("InstallDir") 
    kurzweil = subprocess.Popen([r"".join(kurzweil3000path)], stdout=subprocess.PIPE)
    
    
def login():
    #wait for login screen to appear
    time.sleep(5)

    #login with creditentials
	username = getConfig("Username")
	password = getConfig("Password")

    typewrite(username, interval=0.1) #enter username
    press('tab')
    typewrite(password, interval=0.1) #enter password

    press('enter') #login
    
    #wait for kuzweil to load
    time.sleep(12)

def openFile(in_fname):
    #open the open file dialog
    hotkey('ctrl', 'o')

    #wait for open file dialog to appear
    time.sleep(1)

    #enter the file path of the file to open
    typewrite(in_fname, interval=0.01)

    #open the file
    press('enter')

    #wait for the conversion options to appear
    time.sleep(0.5)

    # confirm conversion options
    press('enter')

def saveFile(out_fname):
    # open the save file dialog
    hotkey('ctrl', 's')

    #wait for save file dialog to appear 
    time.sleep(0.5)

    # enter the file path of the file to save
    typewrite(out_fname, interval=0.01)

    # save to file
    press('enter')

    # wait
    time.sleep(2)

    #close current kes file
    hotkey('ctrl', 'f4')

    # wait
    time.sleep(1)
    

def closeKurzweil():
    #close kurzweil
    if kurzweil is not None:
        kurzweil.terminate()

def getWaitTime(in_fname):
    pdf = PdfFileReader(open(in_fname, 'rb'))
    pages = pdf.getNumPages()
    wait_time = pages * 3
    
    return wait_time

def wait(in_fname):
    wait_time = getWaitTime(in_fname)
    time.sleep(wait_time)

top = Tk()
ent_val = StringVar()

def main():
    file_count = 0
    
    for curdir, subdirs, files in os.walk(ent_val.get()):
        for fname in files:
            in_path = os.path.join(os.path.abspath(curdir), fname)
            if fname.endswith(".pdf") and os.path.getsize(in_path) < 25000000:
                file_count += 1

                in_path = os.path.join(os.path.abspath(curdir), fname)
                kurzweil_dir = curdir.replace(curdir.split("\\")[len(curdir.split("\\")) - 1], "Kurzweil")
                print(kurzweil_dir)

                if not os.path.exists(os.path.abspath(kurzweil_dir)):
                    os.mkdir(os.path.abspath(kurzweil_dir))
                
                out_path = os.path.join(os.path.abspath(kurzweil_dir), fname.replace(".pdf", ".kes"))

                # Open Kuzweil
                openKurzweil()
                # Login
                login()
                # Open File
                openFile(in_path)
                # Wait While Kurzweil Processes File
                wait(in_path)
                # Save File
                saveFile(out_path)

    # Close Kurzweil
    closeKurzweil()

def showGUI():

    filename = ""
    filename_path = ""
    
    Label(top, text="Textbook Path: ").grid(row=0)

    ent = Entry(top, textvariable=ent_val)
    ent.grid(row=0, column=1)

    def browse():
        filename = askdirectory()
        ent_val.set(filename)
        filename_path = ent_val.get()
    
    browsebtn = Button(top, text="...", command=browse)
    browsebtn.grid(row=0, column=2)

    convertbtn = Button(top, text="Convert!", command=main)
    convertbtn.grid(row=1)
        
    top.mainloop()

showGUI()
