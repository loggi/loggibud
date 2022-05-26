import os
import csv
import json
from statistics import mean
from loggibud.v1.distances import OSRMConfig
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import *

def convertToSolution(solutionOPT: CVRPSolutionOPT, inst: CVRPInstance):
    namee = solutionOPT.name
    timee = solutionOPT.time_exec
    vehicless = []
    for v in solutionOPT.vehicles:
        deliveriess = []
        for d in v.deliveries:
            if d.size != 0:
                delivery = Delivery(
                    id = inst.deliveries[d.idu].id,
                    point = d.point,
                    size = d.size
                )
                deliveriess.append(delivery)
        originn = inst.origin
        vehicle = CVRPSolutionVehicle(
            origin = originn,
            deliveries = deliveriess
        )
        vehicless.append(vehicle)
    solution = CVRPSolution(
        name = namee,
        vehicles = vehicless,
        time_exec = timee
    )
    sol = {"": solution}
    return solution, sol

def rowCreateOptimizate(inst_path, sol_path, w, method, osrm_config):
    line = [method]
    inst = CVRPInstance.from_file(inst_path)
    instance = {"": CVRPInstance.from_file(inst_path)}
    solutionOPT = CVRPSolutionOPT.from_file(sol_path)
    solution, sol = convertToSolution(solutionOPT, inst)
    line.append(solution.name)
    stems = instance.keys()
    results = [
        evaluate_solution(instance[stem], sol[stem], osrm_config) for stem in stems
    ]
    line.append(sum(results))
    line.append(solution.time_exec)
    line.append(len(solution.vehicles))
    line.append(mean([sum([d.size for d in v.deliveries]) for v in solution.vehicles]))
    w.writerow(line)

def rowCreateBasicsMethods(inst_path, sol_path, w, method, osrm_config):
    line = [method]
    instance = {"": CVRPInstance.from_file(inst_path)}
    solution = CVRPSolution.from_file(sol_path)
    sol = {"": CVRPSolution.from_file(sol_path)}
    line.append(solution.name)
    stems = instance.keys()
    results = [
        evaluate_solution(instance[stem], sol[stem], osrm_config) for stem in stems
    ]
    line.append(sum(results))
    line.append(solution.time_exec)
    line.append(len(solution.vehicles))
    line.append(mean([sum([d.size for d in v.deliveries]) for v in solution.vehicles]))
    w.writerow(line)


def rowCreateKpprrf(inst_path, sol_path, w, method, osrm_config):
    # pathsa = sol_path.split('/')
    # path_s = pathsa[0]+"/"+pathsa[1]+"/kmeansp/"+pathsa[3]+pathsa[4].split(".")[0] + "-kmeans.json"
    # solKmeans = KmeansSolution.from_file(path_s)
    line = [method]
    instance = {"": CVRPInstance.from_file(inst_path)}
    solution = CVRPSolutionKpprrf.from_file(sol_path)
    sol = {"": CVRPSolutionKpprrf.from_file(sol_path)}
    line.append(solution.name)
    stems = instance.keys()
    results = [
        evaluate_solution(instance[stem], sol[stem], osrm_config) for stem in stems
    ]
    line.append(sum(results))
    line.append(solution.time_execution) # + solKmeans.time_execution
    line.append(solution.total_vehicles)
    line.append(mean([sum([d.size for d in v.deliveries]) for v in solution.vehicles]))
    w.writerow(line)
    # instance_broke = inst_path.split('.')
    # print(instance_broke)
    # name_broke = instance_broke[1].split('-')
    # day = name_broke[len(name_broke)-1]
    # generateEspecificDay(city, day, root)
# Gerar 1 arquivo Geral sobre dados comparativos
# Algorithm | input | distance | time | n_veiculos | VAR(dif de max e min de pacotes\\veiculos) 
# Ler arquivo por arquivo
# Captar os dados desejados
def generateGeneralCsv(
    path_outcsv: str, 
    city: str, 
    output: str, 
    path_input: str,
    methods: list,
    osrm_config: OSRMConfig,
    num_days: int
):
    path_input = path_input + city + "/"
    name = "cvrp-"+city.split("-")[1]+"-"+city.split("-")[0]+"-"
    head = ["Algorithm", "input", "distance", "time", "n_veiculos"]
    f = open(path_outcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerow(head) 
    for method in methods:
        outputx = output + method + "/" + city + "/"
        outputs = [
            outputx+name+str(i)+".json"
            for i in range(90,90+num_days)
        ]
        for sol_path in outputs:
            path_broke = sol_path.split('/')
            name_instance = path_broke[len(path_broke)-1]
            inst_path = path_input + name_instance
            # metodo
            print(sol_path)
            try:
                if method == "kpprrf":
                    rowCreateKpprrf(inst_path, sol_path, w, method, osrm_config)
                elif method == "krs" or method == "krso" or method == "krsof":
                    rowCreateOptimizate(inst_path, sol_path, w, method, osrm_config)
                else:
                    rowCreateBasicsMethods(inst_path, sol_path, w, method, osrm_config)
            except Exception as e:
                print(e)
    # Construir Cabeçalho
    # Read city per city
    # print(outputs)
    

# Gerar 1 arquivo especifico sobre os veículos name-day
# id_vehicle | capacity_used | n_deliveries
def generateEspecificDay(city: str, day: int, root):
    path_out = "output/csvs/"+city+"/especificDay-"+day+".csv"
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
    osrm_config = OSRMConfig(host="http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com")
    path_outcsv = "output/csvs/"
    cities = ["rj-0"] 
    num_days = 30
    output = "data/results/"
    path_input = "data/cvrp-instances-1.0/dev/"
    methods = ["krsof"]
    for city in cities:
        pathcsv = path_outcsv + city + '/generalCity.csv'
        generateGeneralCsv(
            pathcsv, 
            city, 
            output, 
            path_input,
            methods,
            osrm_config, 
            num_days
        )

if __name__ == "__main__":
    main()