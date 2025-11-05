import asyncio
from tkinter import *
from sendscriptv2 import sendscript as sender
from serverreceive import receiver as receive
root =  Tk() 
root.title('testasync')

message = StringVar()

def send():
    print(message.get())
    message.set('')

header = Label(root,text='Messager')
lastmessage = Label(root,text='')
sendfield = Entry(root,textvariable=message)
sendbutton = Button(root,text='send', command=send)

async def checker():
    ...




header.grid(column=0,row=0,columnspan=3,pady=5)
lastmessage.grid(column=0,row=1,columnspan=3,pady=5)
sendfield.grid(column=0,row=2,columnspan=2,padx=10,pady=5)
sendbutton.grid(column=2,row=2,columnspan=1,pady=5)

root.mainloop()