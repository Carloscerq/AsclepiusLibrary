
#Rest API que faz com que as coisas da interface grafica funcionem
import requests
from const import PORT as port
from const import URL as url
from cryptography.fernet import Fernet, InvalidToken
from tkinter import *


def createdata(doctorID, Pacient, data, key):
#Manda um request primeiro para atualizar a chain,
#dps disso para add os dados e por utimo minerar
    f = Fernet(key.encode('utf-8'))
    dataCryto = f.encrypt(data.encode('utf-8'))
    dataCryto = dataCryto.decode('utf-8')
    requests.get(f'{url}/nodes/resolve')
    requests.get(
        f'{url}/Data/new?Doctorid={doctorID}&data={dataCryto}&Pacient={Pacient}')
    block = requests.get(f'{url}/mine')

    return block


def blockchainGetData(key):
#pega os dados que vem da blockchain e filtra somente aqueles em que
#a chave é valida por conta do InvalidToken error 
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
                Label(top, text="=============================================").pack()
            except InvalidToken:
                continue


def addNode(node):
#Torna o processo de add nodes mais facil por só 
#precisar add de forma manual apenas uma das nodes
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'http://{node}/nodes/register?newnode={url}')
    nodeList = response.json()['nodes']
    for node in nodeList:
        requests.get(f'http://{node}/nodes/register?newnode={url}')



def newKey(): #gera uma chave
    key = Fernet.generate_key().decode('utf-8')
    print(key)
    return key

def gainPermission():
#Ganha permissão
#Levando em consideração apenas usuarios bem comportados.
#Em uma aplicação real vale mais a pena fazer apenas com que nodes que já tenham esse status possam add mais nodes
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'{url}/nodes')
    nodeList = response.json()['nodes']
    requests.get(f'{url}/nodes/getpermission?url={url}')
    for node in nodeList:
        requests.get(f'http://{node}/nodes/getpermission?url={url}')