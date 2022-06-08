import json
from unicodedata import name
from loggibud.v1.types import * 
from collections import defaultdict

def constructVehicles(instance : CVRPInstance, params: ParamsVehicles):
    vehicles = []
    id_v = 1
    for v in range(len(params.types)):
        for num in params.num_types:
            for i in range(num):
                vehicle = Vehicle(
                    id = id_v,
                    type_vehicle = params.types[v],
                    capacity = params.capacities[v],
                    cust = params.custs[v],
                    origin = instance.origin
                )
                vehicles.append(vehicle)
                id_v += 1
    return vehicles



def instanceToHeterogene(
    instance : CVRPInstance, paramsVehicles : ParamsVehicles):
    name = instance.name
    region = instance.region
    origin = instance.origin
    vehicles = constructVehicles(paramsVehicles)
    deliveries = instance.deliveries
    return CVRPInstanceHeterogeneous(
        name,
        region,
        origin,
        vehicles,
        deliveries
    )

def recreate(dayStart, dayFinish, cities):
    nameDirIn = "data/cvrp-instances-1.0/dev/"
    nameDirOut = "data/cvrp-instances-2.0/dev/"
    nameParams = "data/cvrp-instances-2.0/params/"
    for city in cities:
        for day in range(dayStart, dayFinish):
            instanceDir = nameDirIn + city + "/"
            nameInstance = "cvrp-0"+city+"-"+day
            fileDir = instanceDir + nameInstance
            instance = CVRPInstance.from_file(fileDir)
            instance_heterogeneoun = instanceToHeterogene(instance)

    return 

if __name__ == "__main__":
    cities = ["pa-0","df-0","rj-0"]
    dayStart = 90
    dayFinish = 119
    recreate(dayStart, dayFinish, cities)