import csv

from loggibud.v1.types import *
from loggibud.v1.distances import OSRMConfig

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

def generateCsvVehicles(
    path_outcsv: str, 
    city: str, 
    month: str,
    day: int,
    output: str, 
    path_input: str,
    methods: list,
    osrm_config: OSRMConfig):
    nameInstance = "cvrp-"+month+"-"+city+"-"+str(day)
    pathcsv = path_outcsv + city + '/'+nameInstance+'.csv'
    f = open(pathcsv, 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    for method in methods:
        createCapacities(w, method,)
        createDistances(w, method)

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