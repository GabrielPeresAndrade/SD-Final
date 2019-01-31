from flask import Flask,jsonify
from flask import request
from flask_pymongo import PyMongo
import json
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://new:adm@sd-dva53.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)
# ------------  Ligar server Mongo ------------------
# cd Desktop\mongodb-win32-x86_64-2008plus-ssl-4.0.5\bin
# mongod
# ------------ Ligar cliente Mongo ------------------
# cd Desktop\mongodb-win32-x86_64-2008plus-ssl-4.0.5\bin
# mongo.exe
#------------- Instruçoes Mongo ---------------------
#
@app.route('/')
def hello_world():
    return 'Bem Vindo A Nuvem Quebrada, por favor va para /provedor ou /cliente'


#-----------------------------------------  1  ---------------------------------------------


@app.route('/Provedor', methods=['POST']) #BROKER
def cloud_Cadastrando():

    received_data = json.load(request.files['datas'])
    mongo.db.test1.insert(received_data)
    
    vCPU = received_data['vCPU']
    RAM = received_data['RAM']
    HD = received_data['HD']
    PRECO = received_data['RS']
    
    msg = 'CADASTRADO COM SUCESSO:\nvCPUS : ',str(vCPU),'\nRAM :', str(RAM),'  GB\nHD :', str(HD),'  GB\nPREÇO R$ ', str(PRECO)
    resposta = {'Mensagem':''.join(msg)}



    print ('CADASTRADO COM SUCESSO:\nvCPUS : ',vCPU,'\nRAM :', RAM,'GB\nHD :', HD,'GB\nPREÇO R$', PRECO)
    return jsonify(resposta)


#------------------------------------------   2   --------------------------------------------------------------------


@app.route('/cliente', methods=['POST'])
def cloud_consultando():
    received_data = json.load(request.files['datas'])
    vCPU = received_data['vCPU']
    RAM = received_data['RAM']
    HD = received_data['HD']
    a = mongo.db.test1.find({"$and":[ {'vCPU':{"$gte" : vCPU}},{'RAM':{"$gte" : RAM}},{'HD':{"$gte" : HD}},{'Disp': 1}]}).sort('RS').limit(1)
    try:
        print ('Foi Achado essa VM:\n')
        print (a[0])
        msg = 'Foi Achado um com as seguintes configuraçoes:\nvCPUS : ',str(a[0]['vCPU']),'\nRAM :',str(a[0]['RAM']),'  GB\nHD :',str(a[0]['HD']),'  GB\nPREÇO R$ ',str(a[0]['RS']),'\nLink de Acesso: 127.0.0.1:',str(a[0]['Prov']),'\nMaquina : ',str(a[0]['Maq'])
        resposta = {'Mensagem':''.join(msg)} 
    except:
        msg ='Nenhum Recurso com essas especificações foi encontrado'
        print(msg)
        resposta = {'Mensagem':''.join(msg)}      
    return jsonify(resposta)


#-----------------------------------------------  3  ------------------------------------------------- 


@app.route('/usa', methods=['POST'])
def cliente_usa():
    received_data = json.load(request.files['datas'])
    try:
        a = mongo.db.test1.update({'Prov':received_data['Prov'],'Maq':received_data['Maq']},{'$set' : {'Disp':0}})
        print ('Um registro alterado')
        msg = 'Sucesso'
    except:
        print('Erro, maquina inexistente')
        msg = 'Erro'
    return jsonify({'Mensagem': msg}) 
    


#--------------------------------------------   4   ---------------------------------------------------

@app.route('/libera', methods=['POST'])
def cliente_liberando():
    received_data = json.load(request.files['datas'])
    try:
        a = mongo.db.test1.update({'Prov':received_data['Prov'],'Maq':received_data['Maq']},{'$set' : {'Disp':1}})
        print ('Um registro alterado')
        msg = 'Sucesso'
    except:
        print('Erro, maquina inexistente')
        msg = 'Erro'
    return jsonify({'Mensagem': msg}) 
    
