import os
import csv
import json
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import *
# Gerar 1 arquivo Geral sobre dados comparativos
# Algorithm | input | K | distance | n_veiculos | VAR(dif de max e min de pacotes\\veiculos) | time 
# Ler arquivo por arquivo
# Captar os dados desejados
def generateGeneralCsv(
    path_outcsv: str, 
    city: str, 
    output: str, 
    path_input: str
):
    output = output + city + "\\"
    path_input = path_input + city + "\\"
    head = ["Algorithm", "input", "K", "distance", "n_veiculos", "time"]
    f = open(path_outcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    # Construir Cabeçalho
    w.writerow(head) 
    # Read city per city
    outputs = [
        os.path.join(output, solution) 
        for solution in os.listdir(output)
    ]
    for sol_path in outputs:
        path_broke = sol_path.split('\\')
        name_instance = path_broke[len(path_broke)-1]
        inst_path = path_input + name_instance
        ifile = open(inst_path)
        jfile = open(sol_path)
        root = json.load(jfile) 
        line = ["KPPRRF"]
        line.append(root['name'])
        line.append(root['k-regions'])
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
    output = "data\\cvrp-instances-1.0\\benchs\\"
    path_input = "data\\cvrp-instances-1.0\\train\\"
    generateGeneralCsv(
        path_outcsv, 
        city, 
        output, 
        path_input
    )

if __name__ == "__main__":
    main()