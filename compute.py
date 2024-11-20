"""
"""

from pathlib import Path
import os

from oemof.solph import EnergySystem, Model, processing

# DONT REMOVE THIS LINE!
from oemof.tabular import datapackage  # noqa
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
#from oemof.tabular.examples.scripting.compute import results_path
from oemof.tabular.facades import TYPEMAP
from oemof.tabular.postprocessing import calculations

scenario_name="dispatch_tsam"

datapackage_path=Path(Path(__file__).parent,scenario_name)
results_path=Path(datapackage_path,'results')

if not results_path.exists():
    Path.mkdir(results_path)

# create energy system object
es = EnergySystem.from_datapackage(
    os.path.join(datapackage_path, "datapackage.json"),
    attributemap={},
    typemap=TYPEMAP,
)

# create model from energy system (this is just oemof.solph)
m = Model(es)

# add constraints from datapackage to the model
m.add_constraints_from_datapackage(
    os.path.join(datapackage_path, "datapackage.json"),
    constraint_type_map=CONSTRAINT_TYPE_MAP,
)

# if you want dual variables / shadow prices uncomment line below
# m.receive_duals()

# select solver 'gurobi', 'cplex', 'glpk' etc
m.solve('cbc')

es.params = processing.parameter_as_dict(es)
es.results = m.results()
# now we use the write results method to write the results in oemof-tabular
# format
postprocessed_results = calculations.run_postprocessing(es)

postprocessed_results.to_csv(os.path.join(results_path, "results.csv"))