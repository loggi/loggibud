import csv
import json
from matplotlib import pyplot as plt
import pandas as pd

from loggibud.v1.distances import OSRMConfig
from loggibud.v1.plotting.plot_solution import plot_cvrp_solution
from loggibud.v1.types import CVRPInstance, CVRPSolution, CVRPSolutionVehicle, Point, Delivery
from loggibud.v1.baselines.task1 import lkh_3, kmeans_aggregation_ortools, kmeans_partition_ortools
from pathlib import Path

def ploter_map(number):
  solJson = open("../cvrp-0-pa-"+str(number)+".json")
  data = json.load(solJson)
  vehicles = []
  for v in data['vehicles']:
    deliveries = []
    for d in v['deliveries']:
      point = Point(lat = d['point']['lat'], lng = d['point']['lng'])
      delivery = Delivery(id = d['id'], point = point, size = d['size'])
      deliveries.append(delivery)
    pointOrigin = Point(lat = v['origin']['lat'], lng = v['origin']['lng'])
    vehicle = CVRPSolutionVehicle(origin = pointOrigin, deliveries=deliveries)
    vehicles.append(vehicle)
  solution = CVRPSolution(name = data['name'], vehicles = vehicles)
  plot_cvrp_solution(solution)

def solve_with_lkh3(osrm_config, input:str, output: str):
  instance = CVRPInstance.from_file(input)
  lkh_params = lkh_3.LKHParams(osrm_config=osrm_config)
  start = 0.0
  solution = lkh_3.solve(instance, params=lkh_params)
  finish = 0.0
  output_dir = Path(output or '.')
  output_dir.mkdir(parents=True, exist_ok=True)
  solution.to_file(output_dir / f"{instance.name}.json")
  solution.time_exec = finish-start
  return solution

def solve_partition(osrm_config, input:str, output: str):
  instance = CVRPInstance.from_file(input)
  start = 0.0
  solution = kmeans_partition_ortools.solve(instance)
  finish = 0.0
  output_dir = Path(output or '.')
  output_dir.mkdir(parents=True, exist_ok=True)
  solution.time_exec = finish-start
  solution.to_file(output_dir / f"{instance.name}.json")
  return solution
  
def solve_aggregation(osrm_config, input:str, output: str):
  instance = CVRPInstance.from_file(input)
  start = 0.0
  solution = kmeans_aggregation_ortools.solve(instance)
  finish = 0.0
  output_dir = Path(output or '.')
  output_dir.mkdir(parents=True, exist_ok=True)
  solution.time_exec = finish-start  
  solution.to_file(output_dir / f"{instance.name}.json")
  return solution

def solve_loggibud(alg: str, osrm_config, input: str, output: str):
  if alg == "lkh3":
    return solve_with_lkh3(osrm_config, input, output)
  elif alg == "kmeans-aggregation":
    return solve_aggregation(osrm_config, input, output)
  elif alg == "kmeans-partition":
    return solve_partition(osrm_config, input, output)
  else:
    return "Not implemented"

def execute_methods_loggibud():
    methods = ["lkh3", "kmeans-aggregation", "kmeans-partition"]
    cities = ["pa-0", "df-0", "rj-0"]
    num_days = 20
    input_dir = "./data/cvrp-instances-1.0/dev/"
    output = "../output/"
  
    osrm_config = OSRMConfig(host="http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com")
    for method in methods:
        for city in cities:
            for i in range(num_days):
                output_complement = output + method + '/' + city + '/'
                cit = city.split("-")
                instance = "cvrp-"+str(cit[1])+"-"+str(cit[0])+"-"+str(i)+".json"
                input = input_dir + city + "/" + instance
                solution = solve_loggibud(method, osrm_config, input, output_complement)

def main():
    execute_methods_loggibud()

if __name__ == "__main__":
    main()