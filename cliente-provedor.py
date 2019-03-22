from flask import Flask,jsonify
from flask import request
from flask_pymongo import PyMongo
import requests
import json
import requests
import random
import threading;

# ------------  Ligar server Mongo ------------------
# cd Desktop\mongodb-win32-x86_64-2008plus-ssl-4.0.5\bin
# mongod
# ------------ Ligar cliente Mongo ------------------
# cd Desktop\mongodb-win32-x86_64-2008plus-ssl-4.0.5\bin
# mongo.exe
#------------- Instruçoes Mongo ---------------------
#

def ouvir(prov,contador):

    while(1):
        print("Digite a opção \n1-Divulgação do Provedor\n2-Consulta do Cliente\n3-Usar\n4-Liberar")
        opc = int(input())

        if opc == 1:
            print("Digite a vCPU, RAM, HD e o Preço por hora (separado por Enters)")
            datas = {'vCPU':int(input()), 'RAM':int(input()), 'HD':int(input()), 'RS':int(input()), 'Disp': 1, 'Prov':prov, 'Maq':contador}
            contador = contador + 1

            files = [('datas', ('datas', json.dumps(datas), 'application/json')),]
            url = "https://trabalho-sd.herokuapp.com/Provedor"
            r = requests.post(url, files=files)

            print (r.json()['Mensagem'])

        if opc == 2:
            print("Digite a vCPU, RAM e HD separado por Enters)")
            datas = {'vCPU':int(input()), 'RAM':int(input()), 'HD':int(input())}

            url = "https://trabalho-sd.herokuapp.com/cliente"

            files = [('datas', ('datas', json.dumps(datas), 'application/json')),]

            r = requests.post(url, files=files)
            print(r.json()['Mensagem'])
        
        if opc == 3:
            print('Digite qual provedor deseja se comunicar')
            curl = input()
            url = 'http://127.0.0.1:',str(curl),'/usar'
            url =''.join(url)
            print('Maquina: ')
            datas = {'Maq':int(input())}
            files = [('datas', ('datas', json.dumps(datas), 'application/json')),]
            r = requests.post(url, files=files)
            print (r.json()['Mensagem'])
        
        if opc == 4:
            print('Digite qual provedor deseja liberar')
            curl = input()
            url = 'http://127.0.0.1:',str(curl),'/liberar'
            url =''.join(url)
            print('Maquina :')
            datas = {'Maq':int(input())}
            files = [('datas', ('datas', json.dumps(datas), 'application/json')),]
            r = requests.post(url, files=files)
            print (r.json()['Mensagem'])


prov = random.randint(5001,40000)
contador = 0

oi = Flask(__name__)


@oi.route('/usar', methods=['POST'])
def usar():
    received_data = json.load(request.files['datas'])
    
    datas = {'Prov':prov, 'Maq':received_data['Maq']}

    url = "https://trabalho-sd.herokuapp.com/usa"

    files = [('datas', ('datas', json.dumps(datas), 'application/json')),]

    r = requests.post(url, files=files)
    print(r.json()['Mensagem'])
    if r.json()['Mensagem']=='Sucesso':
    
        msg = 'Obrigado por nos escolher, aproveite'
        resposta = {'Mensagem':''.join(msg)}
        return jsonify(resposta)

@oi.route('/liberar', methods=['POST'])
def liberar():
    received_data = json.load(request.files['datas'])
    
    datas = {'Prov':prov, 'Maq':received_data['Maq']}

    url = "https://trabalho-sd.herokuapp.com/libera"

    files = [('datas', ('datas', json.dumps(datas), 'application/json')),]

    r = requests.post(url, files=files)
    print(r.json()['Mensagem'])
    if r.json()['Mensagem']=='Sucesso':
    
        msg = 'Obrigado por nos escolher, volte sempre'
        resposta = {'Mensagem':''.join(msg)}
        return jsonify(resposta)



t_ouvir = threading.Thread(target=ouvir,args=(prov,contador));
t_ouvir.start();

if __name__=="__main__" :oi.run(host='127.0.0.1',port=prov)  



