import csv

from loggibud.v1.types import *
from loggibud.v1.distances import OSRMConfig, calculate_distance_matrix_m

def calculate_distance_vehicle(
    vehicle: CVRPSolutionVehicle, 
    matrix_distance): #matrix[dep->idu][dep->idu]
    route = [0]
    distance = 0
    for d in vehicle.deliveries: #outra possibilidade é trazer o instance para saber a ordem
        route.append(d.idu) #idu ou id??
    for origem in range(0,len(vehicle.deliveries)-1):
        destino = origem+1
        distance += matrix_distance[origem][destino]
    return distance

def createCapacities(w, method, solution):
    line = [method]
    line.append("Capacities")
    for v in solution.vehicles:
        line.append(sum([d.size for d in v.deliveries]))
    w.writerow(line)

def createDistances(w, method, matrix_distance, solution):
    line = [method]
    line.append("Distances")
    for v in solution.vehicles:
        line.append(calculate_distance_vehicle(v, matrix_distance))
    w.writerow(line)

def selectSolution(method: str, solution_path: str):
    if method == "kprf":
        return CVRPSolutionKpprrf.from_file(solution_path) 
    elif method == "kprfo":
        return CVRPSolutionOPT.from_file(solution_path)
    else:
        return CVRPSolution.from_file(solution_path)

def generateCsvVehicles(
    path_outcsv: str, 
    city: str,
    mc: str,
    month: str,
    day: int,
    output: str, 
    path_input: str,
    methods: list,
    osrm_config: OSRMConfig):
    nameInstance = "cvrp-"+month+"-"+city+"-"+str(day)
    pathcsv = path_outcsv + city + '/'+nameInstance+'.csv'
    instance = CVRPInstance.from_file(path_input)
    points = [instance.origin]
    for d in instance.deliveries:
        points.append(d.point)
    matrix_distance = calculate_distance_matrix_m(
        points, osrm_config
    )
    f = open(pathcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    for method in methods:
        output_path = output + method + '/' + mc + '/' + nameInstance + ".json"
        solution = selectSolution(method, output_path)
        createCapacities(w, method, solution)
        createDistances(w, method, matrix_distance, solution)
    f.close()

def generateImage(path_outimgs, name):
    # ler o csv
    # fazer box_plot das capacidades 
    # fazer box_plot das distancias

def main():    
    osrm_config = OSRMConfig(host="http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com")
    path_outcsv = "output/vehicles/"
    path_outimgs = "output/imgs/vehicles/"
    cities = ["pa-0"] 
    num_days = 30
    output = "data/results/"
    path_input = "data/cvrp-instances-1.0/dev/"
    methods = ["krsof", "lkh3", "kmeans-partition", "kmeans-aggregation"]
    for cit in cities:
        for day in range(90,90+num_days):
            mc = cit.split("-")
            month = mc[0]
            city = mc[1]
            generateCsvVehicles(
                path_outcsv, 
                city, 
                mc,
                month,
                day,
                output, 
                path_input,
                methods,
                osrm_config)
            generateImage(
                path_outimgs,
                name)

if __name__ == "__main__":
    main()