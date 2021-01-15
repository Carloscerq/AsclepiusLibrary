import requests


url = 'http://localhost:5000/'


def createdata(doctorID, Pacient, data):
    requests.get(f'{url}/nodes/resolve')
    requests.get(
        f'{url}/Data/new?Doctorid={doctorID}&data={data}&Pacient={Pacient}')
    block = requests.get(f'{url}/mine')

    return block

def blockchainGetData():
    response = requests.get(f'{url}/chain')
    return response.json()['chain']