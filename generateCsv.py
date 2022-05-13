import os
import csv
import json
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import *
# Gerar 1 arquivo Geral sobre dados comparativos
# Algorithm | input | distance | time | n_veiculos | VAR(dif de max e min de pacotes\\veiculos) 
# Ler arquivo por arquivo
# Captar os dados desejados
def generateGeneralCsv(
    path_outcsv: str, 
    city: str, 
    output: str, 
    path_input: str,
    method: str
):
    output = output + city + "\\" + method + "\\"
    path_input = path_input + city + "\\"
    name = "cvrp-"+city.split("-")[1]+"-"+city.split("-")[0]+"-"
    head = ["Algorithm", "input", "distance", "time", "n_veiculos"]
    f = open(path_outcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    # Construir Cabeçalho
    w.writerow(head) 
    # Read city per city
    outputs = [
        output+name+str(i)+".json"
        for i in range(90,120)
    ]
    # print(outputs)
    for sol_path in outputs:
        path_broke = sol_path.split('\\')
        name_instance = path_broke[len(path_broke)-1]
        inst_path = path_input + name_instance
        ifile = open(inst_path)
        jfile = open(sol_path)
        root = json.load(jfile) 
        line = ["KPPRRF"]
        line.append(root['name'])
        instance = {"": CVRPInstance.from_file(inst_path)}
        solution = {"": CVRPSolution.from_file(sol_path)}
        stems = instance.keys()
        results = [
            evaluate_solution(instance[stem], solution[stem]) for stem in stems
        ]
        line.append(sum(results))
        line.append(root['total_vehicles'])
        line.append(root['time_execution'])
        w.writerow(line)
        instance_broke = inst_path.split('.')
        print(instance_broke)
        name_broke = instance_broke[1].split('-')
        day = name_broke[len(name_broke)-1]
        generateEspecificDay(city, day, root)
        ifile.close()
        jfile.close()

# Gerar 1 arquivo especifico sobre os veículos name-day
# id_vehicle | capacity_used | n_deliveries
def generateEspecificDay(city: str, day: int, root):
    path_out = "output\\csvs\\"+city+"\\especificDay-"+day+".csv"
    head = ["id_vehicle", "capacity_used", "n_deliveries"]
    f = open(path_out, 'w', newline='', encoding = 'utf-8')
    w = csv.writer(f)
    w.writerow(head)
    for id in range(len(root['vehicles'])):
        line = [id]
        line.append(computeCapacityRoute(root['vehicles'][id]))
        line.append(len(root['vehicles'][id]['deliveries']))
        w.writerow(line)

def computeCapacityRoute(vehicle):
    s = 0
    for delivery in vehicle['deliveries']:
        s += delivery['size']
    return s

def main():    
    path_outcsv = "output\\csvs\\general.csv"
    city = "pa-0" 
    output = "data\\results\\"
    path_input = "data\\cvrp-instances-1.0\\dev\\"
    methods = ["lkh3", "kmeans-partition", "kmeans-aggregation", "kpprrf"]
    for method in methods:
        if method == "kpprrf":
            generateGeneralCsv(
                path_outcsv, 
                city, 
                output, 
                path_input,
                method
            )

if __name__ == "__main__":
    main()