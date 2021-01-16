from tkinter import *
from clientfunctions import createdata, url, blockchainGetData, addNode

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

    closeButton = Button(top, text="Close", command=top.destroy)
    closeButton.pack()


def getDataWindow():
    top = Toplevel()
    top.title("Get Data")
    top.geometry('400x400')
    blockchain = blockchainGetData()
    closeButton = Button(top, text="Close", command=top.destroy)
    closeButton.pack()
    for block in blockchain:
        Label(top, text=block['data']).pack()


def addNodeWindow():
    top = Toplevel()
    top.title("Add Node")
    top.geometry('200x200')
    LabelNode = Label(top, text="Node name: ").pack()
    nodeInput = Entry(top)
    nodeInput.pack()
    confirmButton = Button(top, text="Add Node",
                           command=lambda: addNode(nodeInput.get()))
    confirmButton.pack()
    closeButton = Button(top, text="Close", command=top.destroy)
    closeButton.pack()


createdataButton = Button(root, text='Create Data', command=createdataWindow)
createdataButton.pack()

getDataButton = Button(root, text='See Data', command=getDataWindow)
getDataButton.pack()

createnodeButton = Button(root, text='Add Node', command=addNodeWindow)
createnodeButton.pack()

if __name__ == '__main__':
    root.mainloop()
