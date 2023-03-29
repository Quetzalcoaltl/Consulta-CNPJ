import os
import json
path_diretorio=os.path.realpath(__file__).split("Scripts")
#print(os.listdir(path_diretorio[0]))

print(os.listdir(path_diretorio[0]+ "Arquivos Entrada\\"))

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_json=__location__ + "\\json_totalmente_nao_suspeito.json"

with open(path_json,"r") as file:
    rq_unicos_json_txt = file.read()

requests_unicos=json.loads(rq_unicos_json_txt) 
print(requests_unicos)
#print(__location__)

#print(os.listdir(__location__))


