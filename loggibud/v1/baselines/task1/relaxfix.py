import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.casa = pyo.Var(bounds=(0,None), domain=Integers)
model.predio = pyo.Var(bounds=(0,None), domain=Integers)

casas = model.casa
predios = model.predio

model.obj = pyo.Objective(expr = 3000*casas+5000*predios, sense=maximize)

model.pedreiro = pyo.Constraint(expr = 2*casas+3*predios <= 30)
model.servente = pyo.Constraint(expr = 4*casas+8*predios <= 70)

objetive = model.obj
pedreiros = model.pedreiro
serventes = model.servente

opt = SolverFactory('gurobi')
opt.solve(model)

model.pprint()
print('================================================')
print('Nº casas', pyo.value(casas))
print('Nº predios', pyo.value(predios))
print('Lucro', pyo.value(objetive))
print('Nº pedreiros', pyo.value(pedreiros))
print('Nº serventes', pyo.value(serventes))