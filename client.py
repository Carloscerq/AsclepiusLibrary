from tkinter import *
from flask import Flask, jsonify, request
from clientfunctions import createdata

root = Tk()
root.title("Asclepius Library")
root.geometry("500x500")


def createdataWindow():
    top = Toplevel()
    top.title("Create Data")
    top.geometry('400x400')
    myLabel = Label(top, text="Doctor ID: ").pack()
    doctorIDinput = Entry(top, width=50)
    doctorIDinput.pack()
    myLabel2 = Label(top, text="Pacient: ").pack()
    pacientInput = Entry(top, width=50)
    pacientInput.pack()
    myLabel3 = Label(top, text="Data: ").pack()
    dataInput = Entry(top, width=50)
    dataInput.pack()

    confirmButton = Button(top, text="Confirm", command=lambda: createdata(
        doctorIDinput.get(), pacientInput.get(), dataInput.get()))
    confirmButton.pack()

def getDataWindow():
    


myButton = Button(root, text='Create Data', command=createdataWindow)
myButton.pack()

root.mainloop()
