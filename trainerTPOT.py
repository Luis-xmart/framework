from tpot import TPOTRegressor
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import joblib
from sklearn.model_selection import StratifiedKFold
datasetFile = "C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\modis_norm\\dataset_8_neigh.csv"
name_of_model = 'C:\\Users\\luis1\\Documents\\framework\\results\\TPOT\\optimal_pipeline8.pkl'

df = pd.read_csv(open(datasetFile, 'rb'))
y_last = df['clor_val']
x = df.drop(columns='clor_val')
column_names = x.columns.values
print(column_names)
x_train, x_test, y_train, y_test  = train_test_split(x,y_last,test_size=0.35,random_state=1)

tpot = TPOTRegressor(generations=5, population_size=35,verbosity=2, n_jobs=-1, random_state=1)

tpot.fit(x_train, y_train)

pred1 = tpot.predict(x_test)
best_model = tpot.fitted_pipeline_
joblib.dump(best_model, name_of_model)
print("Error: ", mean_absolute_error(y_test, pred1))
print("Correlación: ", r2_score(y_test, pred1))
print('model', best_model)
#print('Model1', pred1)

# tpot.export(name_of_model)

# print("modelo guardado en carpeta results")

# model = joblib.load(name_of_model)
# pred2 = model.predict(x_test)
# print("Model2",pred2)

