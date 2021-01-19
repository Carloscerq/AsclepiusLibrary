import requests
from const import PORT as port
from const import URL as url
from cryptography.fernet import Fernet, InvalidToken
from tkinter import *


def createdata(doctorID, Pacient, data, key):
    f = Fernet(key.encode('utf-8'))
    dataCryto = f.encrypt(data.encode('utf-8'))
    dataCryto = dataCryto.decode('utf-8')
    requests.get(f'{url}/nodes/resolve')
    requests.get(
        f'{url}/Data/new?Doctorid={doctorID}&data={dataCryto}&Pacient={Pacient}')
    block = requests.get(f'{url}/mine')

    return block


def blockchainGetData(key):
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'{url}/chain')
    top = Toplevel()
    top.title("Get Data")
    top.geometry('400x400')
    f = Fernet(key.encode('utf-8'))
    chain = response.json()['chain']
    for block in chain:
        if block['data'] != []:
            blockdata = block['data'][0]
            try:
                data = blockdata['data'].encode('utf-8')
                data = f.decrypt(data)
                data = data.decode('utf-8')
                Label(top, text=f'Data: {data}').pack()
                Label(top, text="DoctorID:" + blockdata['DoctorId']).pack()
                Label(top, text="Pacient:" + blockdata['Pacient']).pack()
                Label(top, text="=============================================")
            except InvalidToken:
                continue


def addNode(node):
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'{node}/nodes/register?newnode={url}')
    print(response.json())
    nodeList = response.json()['nodes']
    for node in nodeList:
        requests.get(f'http://{node}/nodes/register?newnode={url}')



def newKey():
    key = Fernet.generate_key().decode('utf-8')
    print(key)
    return key

def gainPermission():
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'{url}/nodes')
    nodeList = response.json()['nodes']
    for node in nodeList:
        requests.get(f'http://{node}/nodes/getpermission?url={url}')