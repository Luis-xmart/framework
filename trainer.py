import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from lightgbm import LGBMRegressor
from xgboost.sklearn import XGBRegressor
#from catboost import CatBoostRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn import tree
#métricas de validación
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import joblib

# datasetFile="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\modis_norm\\dataset_8_neigh.csv"
datasetFile="C:\\Users\\Luis Miguel\\Documents\\framework\\results\\modis_norm\\dataset_2_neigh.csv"
# name_of_model = 'D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\modelBayesianRidge_8_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\TreeDecision\\TreeDecision_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\LinearRegression\\LinearRegression_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\LGBMRegressor\\LGBMRegressor_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\SGDRegressor\\SGDRegressor_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\KernelRidge\\KernelRidge_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\ElasticNet\\ElasticNet_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\BayesianRidge\\BayesianRidge_2_neigh.sav'
#name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\GradientBoosting\\GradientBoosting_2_neigh.sav'
name_of_model = 'C:\\Users\\Luis Miguel\\Documents\\framework\\results\\SVR\\SVR_2_neigh.sav'

df = pd.read_csv(open(datasetFile, 'rb'))
y_last = df['clor_val']
x = df.drop(columns='clor_val')
column_names = x.columns.values
x_train, x_test, y_train, y_test  = train_test_split(x,y_last,test_size=0.30,random_state=42)

#reg = tree.DecisionTreeRegressor(max_depth=1000,min_samples_split=3,random_state=1)
#reg = LinearRegression()
#reg = LGBMRegressor()
#reg = SGDRegressor()
#reg = KernelRidge()
#reg = ElasticNet()
#reg = BayesianRidge()
#reg = GradientBoostingRegressor()
reg = SVR()

reg = reg.fit(x_train, y_train)
pred=reg.predict(x_test)
print("Error: ",mean_absolute_error(y_test,pred))
print("Correlación: ",r2_score(y_test,pred))

joblib.dump(reg, name_of_model)
print("modelo guardado en carpeta results")