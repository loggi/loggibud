import csv
import pandas as pd
import matplotlib.pyplot as plt

from itertools import zip_longest

from loggibud.v1.types import *
from loggibud.v1.distances import OSRMConfig, calculate_distance_matrix_m

def calculate_distance_vehicle(
    instance: CVRPInstance,
    vehicle: CVRPSolutionVehicle, 
    method: str,
    matrix_distance): #matrix[dep->idu][dep->idu]
    route = [0]
    distance = 0
    dicio = {}
    if method == 'krsof' or method == "kpmipo":
        for d in vehicle.deliveries: #outra possibilidade é trazer o instance para saber a ordem
            route.append(d.idu) #idu ou id??
    else:
        for i in range(len(instance.deliveries)):
            dicio[instance.deliveries[i].id] = i+1
        for d in vehicle.deliveries: #outra possibilidade é trazer o instance para saber a ordem
            route.append(dicio[d.id]) #idu ou id??
    for origem in range(0,len(route)-1):
        destino = origem+1
        distance += matrix_distance[route[origem]][route[destino]]
    return round(distance/1_000, 4)

def calculate_distance_vehicle_per_packet(
    instance: CVRPInstance,
    vehicle, 
    method,
    matrix_distance):
    distance = calculate_distance_vehicle(instance, vehicle, method, matrix_distance)
    packets = len(vehicle.deliveries)
    if packets != 0:
        return round(distance/packets, 4)
    else:
        return round(0,4)

def createCapacities(method, solution):
    line = [method]
    line.append("Capacities")
    for v in solution.vehicles:
        if len(v.deliveries) != 0:
            line.append(sum([d.size for d in v.deliveries]))
        else:
            line.append(0)
    return line
    # w.writerow(line)

def createDistances(
    instance: CVRPInstance, method, matrix_distance, solution):
    line = [method]
    line.append("Distances")
    for v in solution.vehicles:
        line.append(calculate_distance_vehicle_per_packet(instance, v, method, matrix_distance))
    return line
    # w.writerow(line)

def selectSolution(method: str, solution_path: str):
    if method == "kpprrf" or method == "kpmip":
        return CVRPSolutionKpprrf.from_file(solution_path) 
    elif method == "krsof" or method == "kpmipo":
        return CVRPSolutionOPT.from_file(solution_path)
    else:
        return CVRPSolution.from_file(solution_path)

def generateCsvVehicles(
    path_outcsv: str, 
    dir_city: str,
    nameInstance: str,
    output: str, 
    path_input: str,
    methods: list,
    osrm_config: OSRMConfig):
    pathcsv = path_outcsv + dir_city + '/'+nameInstance+'.csv'
    input_path = path_input + dir_city + '/' +nameInstance + '.json'
    instance = CVRPInstance.from_file(input_path)
    points = [instance.origin]
    for d in instance.deliveries:
        points.append(d.point)
    matrix_distance = calculate_distance_matrix_m(
        points, osrm_config
    )
    lines = []
    for method in methods:
        output_path = output + method + '/' + dir_city + '/' + nameInstance + ".json"
        solution = selectSolution(method, output_path)
        lines.append(createCapacities(method, solution))
        lines.append(createDistances(instance, method, matrix_distance, solution))
    columns_data = zip_longest(*lines)
    f = open(pathcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerows(columns_data)
    f.close()
    return pathcsv

def createImages(path_outimgs, name, methods, dados, chave):
    values = []
    x = [i+1 for i in range(len(methods))]
    for method in methods:
        if chave == "Distances":
            ext = ".1"
            key = method+ext
        else:
            key = method
        values.append(dados[key][chave])
    plt.figure(figsize = (11,6))
    colors = ['red', 'lightblue', 'lightgreen', 'purple']
    bplots = plt.boxplot(values, vert = 1, patch_artist=False)
    plt.title("Boxplot de "+chave, loc="center", fontsize=18)
    plt.xlabel("Metodos")
    plt.ylabel(chave)
    plt.xticks(x,methods)
    plt.savefig(path_outimgs+'/'+name+chave+".png")
    plt.close()

def generateImage(path_outimgs, name, pathcsv, methods):
    # ler o csv
    header = pd.read_csv(pathcsv)
    dados = {}
    for chave in header:
        dados[chave] = {}
        dados[chave][header[chave][0]] = [
            float(header[chave][i]) for i in range(1,len(header[chave])) 
            if header[chave][i] != '0' and pd.isnull(header[chave][i]) != True]

    createImages(path_outimgs, name, methods, dados, "Capacities")
    createImages(path_outimgs, name, methods, dados, "Distances")

def main():    
    osrm_config = OSRMConfig(host="http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com")
    path_outcsv = "output/vehicles/"
    path_outimgs = "output/imgs/vehicles/"
    cities = ["pa-0"] 
    num_days = 30
    output = "data/results/"
    path_input = "data/cvrp-instances-1.0/dev/"
    methods = ["kpmip", "kpmipo"]
    for dir_city in cities:
        for day in range(90,90+num_days):
            try:
                mc = dir_city.split("-")
                month = mc[1]
                city = mc[0]
                nameInstance = "cvrp-"+month+"-"+city+"-"+str(day)
                print(nameInstance)
                pathcsv = generateCsvVehicles(
                    path_outcsv, 
                    dir_city,
                    nameInstance,
                    output, 
                    path_input,
                    methods,
                    osrm_config)
                generateImage(
                    path_outimgs + dir_city,
                    nameInstance,
                    pathcsv, 
                    methods)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()