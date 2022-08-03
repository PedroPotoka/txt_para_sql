import pyodbc
import pandas as pd
import os
import time

class Cortador:

    # SQL
    server = '127.0.0.1'
    database = 'DB_TESTE'
    username = 'sa'
    password = 'qwe123@#'

    sqlC='DRIVER={SQL Server};'
    sqlC+='SERVER='+server+';'
    sqlC+='DATABASE='+database+';'
    sqlC+='UID='+username+';'
    sqlC+='PWD='+ password

    dir = os.getcwd() + "/arquivo.txt"
    
    lista = []
    cpf = []
    nome = []
    sexo = []
    nasc = []

    tamanho_lista = 10

    ciclo = 0
    
    #Inicializando SQL
    db = pyodbc.connect(sqlC)
    cursor = db.cursor()

    insert_txt = "INSERT INTO GER_PESSOA (PES_NOME,PES_CPF,PES_SEXO,PES_NASC) VALUES"

    def __init__(self):
        print("Tamanho do Ciclo definido para: " + str(self.tamanho_lista))     
        self.Pegar_Lista()
        del self.lista[0]
        print("A lista de Arquivos tem: " + str(len(self.lista)) + " registros")
        self.Corta_Lista()
        print("Finalizado!")
        
    def Pegar_Lista(self):
        arquivo = open(self.dir, 'r')
        self.lista = arquivo.readlines()
        arquivo.close()

    def Corta_Lista(self):
        for y in self.lista:
            x = y.split("|")
            self.cpf.append(x[0])
            self.nome.append(x[1])
            self.sexo.append(x[2][0])
            self.nasc.append(x[3][:10])
            self.Verifica_Tamanho(False)
        self.Verifica_Tamanho(True)

    def Verifica_Tamanho(self,value):
        if ((len(self.cpf) == self.tamanho_lista) or (value)):
            self.Monta_Insert()
            self.Inserir()
            self.Limpa_Lista()
            self.ciclo+=1
            print("Ciclo N " + str(self.ciclo))

    def Monta_Insert(self):
        for x in range(0,len(self.cpf)):
            nome_temp = self.nome[x].replace("'", "''")
            self.insert_txt += f"('{nome_temp}', '{self.cpf[x]}', '{self.sexo[x]}',"
            if (len(self.nasc[x]) != 10):
                self.insert_txt += f" '')"
            else:
                self.insert_txt += f" '{self.nasc[x]}')"
            if (x != len(self.cpf)-1):
                self.insert_txt += ","

    def Inserir(self):
        self.cursor.execute(self.insert_txt)
        self.db.commit()

    def Limpa_Lista(self):
        self.cpf.clear()
        self.nome.clear()
        self.sexo.clear()
        self.nasc.clear()
        self.insert_txt = "INSERT INTO GER_PESSOA (PES_NOME,PES_CPF,PES_SEXO,PES_NASC) VALUES"


inicio = time.time()
teste = Cortador()
fim = time.time()
print(fim - inicio)