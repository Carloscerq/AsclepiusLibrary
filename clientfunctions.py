import requests
from blockchain import port

url = f'http://localhost:{port}/'


def createdata(doctorID, Pacient, data):
    requests.get(f'{url}/nodes/resolve')
    requests.get(
        f'{url}/Data/new?Doctorid={doctorID}&data={data}&Pacient={Pacient}')
    block = requests.get(f'{url}/mine')

    return block


def blockchainGetData():
    requests.get(f'{url}/nodes/resolve')
    response = requests.get(f'{url}/chain')
    return response.json()['chain']


def addNode(node):
    print(url)
    response = requests.get(f'{url}/nodes/register?newnode={node}')
    nodeList = response.json()['nodes']
    for node in nodeList:
        requests.get(f'{url}/nodes/register?newnode={node}')

    print(response.json()['message'])
