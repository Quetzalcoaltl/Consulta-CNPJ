import pandas as pd
import requests as rq
import time as tm
import re
import shutil as st
import os
import openpyxl
import psutil
import json

for proc in psutil.process_iter():
    if proc.name() == "excel.exe":
        proc.kill()
path =r"C:\Users\victor.andrade\OneDrive - SADACORP\Documentos\Chamados COF cnpj.xlsx"
path_destino =r"C:\Users\victor.andrade\OneDrive - SADACORP\Documentos\Chamados COF Destino CNPJ.xlsx"
##### leitura do json de informações unicas
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_json=__location__ + r"\json_cnpj_unicos.json"

with open(path_json,"r") as file:
    rq_unicos_json_txt = file.read()
cnpjs_unicos=json.loads(rq_unicos_json_txt) 
url=r"https://www.receitaws.com.br/v1/cnpj/"
i=0

if os.path.exists(path_destino)==False:
        st.copyfile(path,path_destino)
        print("arquivo copiado!!")
lista_cnpjs_destino = pd.read_excel(path_destino)
if not "CNPJ" in lista_cnpjs_destino:
        os.remove(path_destino)
        raise ValueError("Coluna CNPJ NÃO IDENTIFICADA. VERIFQUE SUA BASE DE DADOS!!")
if not "NOME FANTASIA" in lista_cnpjs_destino:
        lista_cnpjs_destino["NOME FANTASIA"]=""
        print("Coluna NOME FANTASIA criada!!")
if not "NOME" in lista_cnpjs_destino:
        lista_cnpjs_destino["NOME"]=""
        print("Coluna NOME criada!!")
bool_cnpj_novo_inserido=False
#cnpjs_unicos={} #cria ele limpo
for cnpj in lista_cnpjs_destino["CNPJ"]:
        bool_cnpj_novo_inserido=False
        print(f"Linha:{i} CNPJ:{cnpj}")
        try:
                if pd.isna(cnpj):
                        print("cnpj vazio...")
                        i = i + 1
                        continue #se for vazio o valor de cnpj ele vai para outro item da lista_cnpjs_destion["CNPJ"]
                cnpj_numeros = re.sub(r'\D', '', cnpj)
                if lista_cnpjs_destino['NOME'][i] !="" and not pd.isna(lista_cnpjs_destino['NOME'][i]):
                        print("ja preenchido...")
                        print(lista_cnpjs_destino['NOME'][i])
                        cnpjs_unicos[cnpj_numeros]={"fantasia":lista_cnpjs_destino['NOME'][i],"nome":lista_cnpjs_destino['NOME FANTASIA'][i]}
                        i = i + 1
                        continue #é para ir para o proximo item do seu loop,
                response=rq.get(url+cnpj_numeros) #aqui eu realizo a chamada da api
                if not cnpj_numeros in cnpjs_unicos:
                        bool_cnpj_novo_inserido=True
                        response=rq.get(url+cnpj_numeros) #aqui eu realizo a chamada da api
                        
                        tm.sleep(30) #espera 30s para a proxima chamada
                        if not response.status_code==200: # checa se a consulta foi realizada com sucesso
                                print(f"não foi possivel realizar a consulta. Status Code:{response.status_code}...")
                                i = i + 1
                                continue 
                        print("Consulta nova...")
                        data = response.json() #lista_cnpjs_destino["NOME FANTASIA"][i]=data["fantasia"]
                        #estou criando uma base de dados com os cnpjs, todavia não é necessário no caso de um pj simples a linha a seguir faz mais sentido
                        cnpjs_unicos[cnpj_numeros]=data
                        #cnpjs_unicos[cnpj_numeros]={"fantasia":data["fantasia"],"nome":data["nome"]} 
                        with open(path_json, "w") as outfile:  
                                json.dump(cnpjs_unicos, outfile)  
                        if  "message" in data:
                                cnpjs_unicos[cnpj_numeros]={"message":data["message"]}
                                print(cnpjs_unicos[cnpj_numeros]["message"])
                                i = i + 1
                                continue
                if  "message" in cnpjs_unicos[cnpj_numeros]:
                        print(cnpjs_unicos[cnpj_numeros]["message"])
                        i = i + 1
                        continue

                lista_cnpjs_destino.loc[i,["NOME FANTASIA"]]=cnpjs_unicos[cnpj_numeros]["fantasia"]
                lista_cnpjs_destino.loc[i,["NOME"]]=cnpjs_unicos[cnpj_numeros]["nome"]
                """if "fantasia" in data: #verifica se existe a chave fantasia no json
                                lista_cnpjs_destino.loc[i,["NOME FANTASIA"]]=data["fantasia"]
                        if "nome" in data:
                                lista_cnpjs_destino.loc[i,["NOME"]]=data["nome"]
                        if "message" in response.json(): print(f"mensagem da api{0}",data["message"])"""
                if bool_cnpj_novo_inserido or i%100 == 0:
                        print("Salvando arquivo excel, não cancele o processo...")
                        with pd.ExcelWriter(path_destino, engine='openpyxl') as writer:
                                lista_cnpjs_destino.to_excel(writer)
                                print("Excel salvo com sucesso!!!")
        except Exception as e:
                print(f"Error occurred: {e}")
                i = i + 1
                continue
        if i>=3500: break
        i = i + 1

print("Salvando arquivo excel, não cancele o processo...")
with pd.ExcelWriter(path_destino, engine='openpyxl') as writer:
        lista_cnpjs_destino.to_excel(writer)
        print("Excel salvo com sucesso!!!")