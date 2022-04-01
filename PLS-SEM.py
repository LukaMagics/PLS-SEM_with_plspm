import pandas.util.testing as tm
import plspm.config as c
from plspm.plspm import Plspm
from plspm.scheme import Scheme
from plspm.scale import Scale
from plspm.mode import Mode
import pandas as pd
import numpy as np
import random
pd.set_option('display.max_columns', None)

data = pd.read_csv('C:/_Projects/Statistical Analysis/PLS/test_data_328raws.csv')
print(data.head())

# Drawing Structure
structure = c.Structure() 

structure.add_path(["FAM","SIM"], ["TIM"]) # add_path([IV1, IV2], [DV])
structure.add_path(["SEC", "CCA", "FBM"], ["TIP"]) 
structure.add_path(["TIM"], ["TIP"])
structure.add_path(["TIM", "TIP"], ["PI"])

# Allocating Measurements and Input data
config = c.Config(structure.path(), scaled=False)
config.add_lv_with_columns_named("FAM", Mode.A, data, "fam") # ex) measurements col name = FAM1, FAM2, ...
config.add_lv_with_columns_named("SIM", Mode.A, data, "sim")
config.add_lv_with_columns_named("SEC", Mode.A, data, "sec")
config.add_lv_with_columns_named("CCA", Mode.A, data, "cca")
config.add_lv_with_columns_named("FBM", Mode.A, data, "fbm")
config.add_lv_with_columns_named("TIM", Mode.A, data, "tim")
config.add_lv_with_columns_named("TIP", Mode.A, data, "tip")
config.add_lv_with_columns_named("PI", Mode.A, data, "pi")

# Calculating PLS-SEM
plspm_calc = Plspm(data, config, Scheme.CENTROID)

# Show Results
print(plspm_calc.outer_model()) # Outer Loading
print(plspm_calc.unidimensionality()) # Cronbach's alpah, rho
print(plspm_calc.inner_summary()) # R square, AVE
path_analysis = plspm_calc.inner_model() # Path Coefficient, t-value, p-value
path_analysis['p>|t|'] = np.round(path_analysis['p>|t|'], 3) # Restricting three decimal places of p-value.
print(path_analysis)