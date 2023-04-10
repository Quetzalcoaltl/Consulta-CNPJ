import os
import json
print("---------------------------------")
diretorio_atual=os.getcwd()
diretorio_entrada_dados=diretorio_atual + r"\entrada"
diretorio_saida_dados=diretorio_atual + r"\saida"
diretorio_cache=diretorio_atual + r"\cache"
if not os.path.exists(diretorio_entrada_dados):
    os.mkdir(diretorio_entrada_dados)
if not os.path.exists(diretorio_saida_dados):
    os.mkdir(diretorio_saida_dados) 
if not os.path.exists(diretorio_cache):
    os.mkdir(diretorio_cache)
print(diretorio_atual)


'''
path_diretorio=os.path.realpath(__file__).split("Scripts")
#print(os.listdir(path_diretorio[0]))
print(os.listdir(path_diretorio[0]+ "Arquivos Entrada\\"))

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)

path_json=__location__ + "\\json_totalmente_nao_suspeito.json"

with open(path_json,"r") as file:
    rq_unicos_json_txt = file.read()

requests_unicos=json.loads(rq_unicos_json_txt) 
print(requests_unicos)
#print(__location__)

#print(os.listdir(__location__))


'''