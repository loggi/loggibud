import sys
import csv
import json
import os
import time
from pandas.io.json import json_normalize
from csv import writer

python_execute = "python3 -m "
caminho_para_task1 = "loggibud.v1.baselines.run_task1 "
solves_task1 = [
    "lkh_3",
    "kmeans_partition_ortools",
    "kmeans_aggregation_ortools"
]
extension_py = ".py"
extension_csv = ".csv"
extension_json = ".json"

solution = "data/output/results.csv"
way_method = "loggibud.v1.baselines.task1."
way_to_dirs_not = "data/cvrp-instances-1.0/train" 

def main():
    cities = [
        "df-0"
    ]
    
    output = solution
    with open(output, "w+") as f:
        w = writer(f)
        w.writerow(["cidade","entrada","metodo","qtd_rotas","tempo_exec"])
        for city in cities:
            pasta = way_to_dirs_not+"/"+city    
            caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
            instances = [arq for arq in caminhos if os.path.isfile(arq)]
            execute_methods(w,city,instances)
        f.close()

def extract_routes_output(instance,method):
    print(instance)
    with open(instance) as data_file:
        json_obj = json.load(data_file)
    
    qtd_rotas = len(json_obj["vehicles"])
    return qtd_rotas

def execute_methods(w,cite,instances):
    create_csv(w,cite,instances)

# def execute_methods_teste(cite,instances):
#     create_csv_teste(cite,instances)

def create_csv(w,cite,instances):
    for intance in instances:
        for method in solves_task1:
            name_file_with_extension = intance.split("/")
            name_file = name_file_with_extension[len(name_file_with_extension)-1].split(".")
            output_file = "output/" + method +"/"
            awaymethod = way_method + method
            # tempo inicio antes do programa
            print(python_execute + caminho_para_task1 + " --instances "+ intance +" --module "+ awaymethod +" --output "+ output_file)
            time_init = time.time()
            os.system(python_execute + caminho_para_task1 + " --instances "+ intance +" --module "+ awaymethod +" --output "+ output_file)
            time_finish = time.time()
            # tempo final do programa
            time_run = time_finish - time_init
            name_output = output_file+name_file_with_extension[len(name_file_with_extension)-1]
            qtd_rotas = extract_routes_output(name_output,method)
            w.writerow([cite,intance,method,qtd_rotas,time_run])

def create_csv_test(instances,solves):
    for intance in instances:
        for method in solves:
            name_file_with_extension = intance.split("/")
            name_file = name_file_with_extension[len(name_file_with_extension)-1].split(".")
            output_file = "output/" + method +"/"
            awaymethod = way_method + method
            # tempo inicio antes do programa
            print(python_execute + caminho_para_task1 + " --instances "+ intance +" --module "+ awaymethod )
            time_init = time.time()
            os.system(python_execute + caminho_para_task1 + " --instances "+ intance +" --module "+ awaymethod )
            time_finish = time.time()
            # tempo final do programa
            time_run = time_finish - time_init
            print("tempo exec = ")
            print(time_run)


if __name__ == "__main__":
    main()

