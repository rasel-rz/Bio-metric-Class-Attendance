#!/usr/bin/python3

# importing stuffs
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import serial
from time import sleep
import serial.tools.list_ports
import sqlite3
import datetime

# getting today's date
dateof = datetime.datetime.today()

# Alert window
ALERT_DURATION = 2000 # Default duration 2 sec
def alertWin(msg):
  alert = Toplevel()
  alert.title('Welcome')
  Message(alert, text=msg, padx=20, pady=20).pack()
  alert.after(ALERT_DURATION, alert.destroy)

def setEntry(entry, msg):
  entry.delete(0,END)
  entry.insert(0,msg)

# Get data from SQLite3 to show on UI
def getSqData(id):
  conn = sqlite3.connect('students.db')
  c = conn.cursor()

  c.execute("SELECT * FROM students WHERE FingerID=?", (str(id)))
  data = c.fetchone()
  #print(data)
  conn.commit()
  conn.close()
  return data

def updateAttDB(roll, date):
  conn = sqlite3.connect('students.db')
  c = conn.cursor()

  c.execute("INSERT INTO attSheet Values(?, ?)", (roll, date))
  conn.commit()
  conn.close()

def emptyDB():
  conn = sqlite3.connect('students.db')
  c = conn.cursor()

  c.execute("DELETE FROM students")
  conn.commit()
  print("Students Table Deleted!")

  c.execute("DELETE FROM attSheet")
  conn.commit()
  print("Attendence Sheet Deleted!")
  conn.close()

# Set data to SQLite3 when Enroll
def setSqData(name, roll, id):
  conn = sqlite3.connect('students.db')
  c = conn.cursor()
  c.execute("INSERT INTO students VALUES(?, ?, ?)", (roll, name, str(id)))
  conn.commit()
  conn.close()

# Set data on GUI from Attaining
def attendenceManager(fngrID=0):
  if(fngrID != 0):
    dbData = getSqData(fngrID)

    setEntry(nameEntry, dbData[1])
    setEntry(rollEntry, str(dbData[0]))
    print(dbData)

# Enrolling stuffs go here
def Enroll():
  if((nameEntry.get() == '') or (rollEntry.get() == '')):
    messagebox.showerror("Empty fields!", "Input field(s) are empty.\nPlease input some data.")
    return
  data = 'E'
  ard.write(data.encode())
  myData = ""
  while(True):
    if ("EF" not in myData):
      sleep(0.1)
      data = ard.readline(ard.inWaiting())
      if (str(data) != "b''" and str(data) != "b'.'" and data != b'.\r\n'):
        myData = data.decode('utf-8')
        print(myData)
        #serialMonitor.config(text=myData)
    else:
      dataSplited = myData.split(':')
      print(dataSplited)
      if ("64" not in dataSplited[1]):
        print("Data enroll faillllll")
        messagebox.showerror("Failed!", "Data enroll failed, try again.")
      else:
        setSqData(nameEntry.get(), rollEntry.get(), int(dataSplited[2]))
        print("Data enroll success!")
        messagebox.showinfo("Success!", "Data enroll success.")
      break

# Attaining stuff goes here
def Attain():
  data = 'A'
  ard.write(data.encode())
  myData = ""
  while(True):
    if ("AF" not in myData):
      sleep(0.1)
      data = ard.readline(ard.inWaiting())
      if (str(data) != "b''"):
        myData = data.decode('utf-8')
        print(myData)
        #Serial Monitor. Not working. ;(
    else:
      sleep(0.1)
      print(myData)
      dataSplited = myData.split(':')
      print(dataSplited)
      attendenceManager(int(dataSplited[1]))
      dbData = getSqData(int(dataSplited[1]))
      attStr = str("Attendence success for: \nName: {} \nRoll: {}".format(dbData[1], dbData[0]))
      messagebox.showinfo("Attendence Success!", attStr)
      dateText = str(dateof.day) + '-' + str(dateof.month) + '-' + str(dateof.year + ' ' + str(dateof.hour) + ':' + str(dateof.minute))
      updateAttDB(dbData[0], dateText)
      break

# Showing the full Database!
#def ShowData():
#    data = 'V'
#    ard.write(data.encode())
#    sleep(0.1)
#    data = ard.readline(ard.inWaiting())
#    serialMonitor.config(text=str(data))

def Reset():
    data = 'R'
    ard.write(data.encode())
    sleep(0.1)
    data = ard.readline(ard.inWaiting())
    emptyDB()

# Setting up the GUI
root = Tk()
root.title("Attendence Holder")
root.configure(bg='gray')
default_font = font.nametofont("TkFixedFont")
default_font.configure(size=16)
root.option_add("*Font", default_font)
root.option_add('*Dialog.msg.font', 'Helvetica 12')

# Window Size Modifier
#root.minsize(width=360, height=180)
#root.geometry('640x480+0+0')

infoFrame = Frame(root)
Label(infoFrame, text="Name: ").grid(row=0, column=0)
Label(infoFrame, text="Roll: ").grid(row=1, column=0)
nameEntry = Entry(infoFrame, width=30)
nameEntry.grid(row=0, column=1)
rollEntry = Entry(infoFrame, width=30)
rollEntry.grid(row=1, column=1)
infoFrame.grid(row=0, column=0, padx=8, pady=8)

dateFrame = Frame(root)
Label(dateFrame, text="Day:").grid(row=0, column=0)
dayEntry = Entry(dateFrame, width=3)
dayEntry.grid(row=0, column=1)
Label(dateFrame, text="Month:").grid(row=0, column=2)
monthEntry = Entry(dateFrame, width=3)
monthEntry.grid(row=0, column=3)
Label(dateFrame, text="Year:").grid(row=0, column=4)
yearEntry = Entry(dateFrame, width=4)
yearEntry.grid(row=0, column=5)
dateFrame.grid(row=1, column=0, pady=8)

buttFrame = Frame(root)
Button(buttFrame, text="Attain", command=Attain, padx=32, bg='cyan').grid(row=4, column=2, sticky=EW)
Button(buttFrame, text="Enroll", command=Enroll, padx=32, bg='green').grid(row=4, column=3, sticky=EW)
#Button(buttFrame, text="Sheets", command=ShowData, padx=32, bg='blue').grid(row=4, column=4, sticky=EW)
Button(buttFrame, text="Reset", command=Reset, padx=32, bg='red').grid(row=4, column=5, sticky=EW)
buttFrame.grid(row=2, column=0, pady=8)

setEntry(dayEntry, dateof.day)
setEntry(monthEntry, dateof.month)
setEntry(yearEntry, dateof.year)

# Finding Arduino Port
ports = list(serial.tools.list_ports.comports())
if (ports):
  for p in ports:
      print (p)
  ardPort = str(p).split()
  if ("Arduino" in p.description) or ("Serial" in p.description):
    print("Arduino found!")
    ard = serial.Serial(ardPort[0], 9600)
    sleep(2)
    #print (ard.readline(ard.inWaiting()))
  else:
    print("Arduino not found. Check connection!")
    messagebox.showerror("Error!", "Arduino not found. Check connection!")
    root.destroy()
else:
  print("No working port found. Check connection!")
  messagebox.showerror("Error!", "No working port found. Check connection!")
  root.destroy()

root.mainloop()