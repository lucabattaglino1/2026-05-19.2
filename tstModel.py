# tstModel.py
from model.model import Model

mdl = Model()
mdl.buildGraph('Rock')
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")
