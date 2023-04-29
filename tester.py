import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from fnmatch import fnmatch
import cv2 as cv
import netCDF4 as nc
import numpy as np
from os import system
import os
import glob
from osgeo import gdal
import joblib

def roitolog(im,spatialResolution):
	log=[]
	for i in range(im.shape[0]):
		for j in range(im.shape[1]):
			if (i!=spatialResolution or j!=spatialResolution) and im[i][j]!=0.0:
				log.append(im[i][j])
	return log


#carga de modelos
# name_of_model1 = 'D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\modelBayesianRidge_2_.sav'
name_of_model1 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline2.pkl'
loaded_model1 = joblib.load(name_of_model1)

# name_of_model2 = 'D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\\modelBayesianRidge_3_neigh.sav'
name_of_model2 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline3.pkl'
loaded_model2 = joblib.load(name_of_model2)

name_of_model3 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline4.pkl'
loaded_model3 = joblib.load(name_of_model3)

name_of_model4 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline5.pkl'
loaded_model4 = joblib.load(name_of_model4)

name_of_model5 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline6.pkl'
loaded_model5 = joblib.load(name_of_model5)

name_of_model6 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline7.pkl'
loaded_model6 = joblib.load(name_of_model6)

name_of_model7 = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\TPOT\\optimal_pipeline8.pkl'
loaded_model7 = joblib.load(name_of_model7)

#carga de imagen modis
#path_to_modis = "C:\\Users\\Luis Miguel\\Documents\\Corregistro\\Corregistradas\\modis_clo\\clora_01_mapped_AQUA_MODIS.20230103T193500.L2.OC.NRT.x.nc.tif"
path_to_modismod = "C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_mod.tiff"
path_to_modismod2010 = "C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_mod2010.tiff"
raster = gdal.Open(path_to_modismod2010)
modis = raster.ReadAsArray()
confidence_map = np.zeros(modis.shape)
new_modis = np.zeros(modis.shape)

spatialResolution=1
print(modis.shape[0]) #filas
print(modis.shape[1]) #columnas
for fila in range(modis.shape[0]):
	for columna in range(modis.shape[1]):
		if modis[fila][columna]==0.0:
			cond1a=fila-spatialResolution
			cond1b=fila+spatialResolution+1
			cond2a=columna-spatialResolution
			cond2b=columna+spatialResolution+1
			if cond1a>=0 and cond1b<modis.shape[1] and cond2a>=0 and cond2b<modis.shape[0]:
				roi=modis[cond1a:cond1b,cond2a:cond2b]
				total_px=roi.shape[0]*roi.shape[1]
				valNonZeros=cv.countNonZero(roi)
				if valNonZeros==2:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model1.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==3:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model2.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==4:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model3.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==5:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model4.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==6:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model5.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==7:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model6.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
				if valNonZeros==8:
					log=roitolog(roi,spatialResolution)
					px_predicted = loaded_model7.predict([log])
					new_modis[fila][columna]=px_predicted[0]
					confidence_map[fila][columna]=(100.0/total_px)*valNonZeros
		else:
			new_modis[fila][columna]=modis[fila][columna]
			confidence_map[fila][columna]=100.0

#guardar resultados
NoDataValue=-999
driver = gdal.GetDriverByName("GTiff")
# outFileName="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\predict_modis.tif"
outFileName='C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\predict_modismod2010.tif'
outdata = driver.Create(outFileName,modis.shape[1], modis.shape[0], 1, gdal.GDT_Float32)
outdata.SetGeoTransform(raster.GetGeoTransform())
outdata.SetProjection(raster.GetProjection())
outdata.GetRasterBand(1).WriteArray(new_modis)
outdata.GetRasterBand(1).SetNoDataValue(NoDataValue)
outdata.FlushCache()

# outFileName="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\confidence_map.tif"
# outFileName='C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\confidence_mapmod.tif'
# outdata = driver.Create(outFileName,modis.shape[1], modis.shape[0], 1, gdal.GDT_Float32)
# outdata.SetGeoTransform(raster.GetGeoTransform())
# outdata.SetProjection(raster.GetProjection())
# outdata.GetRasterBand(1).WriteArray(confidence_map)
# outdata.GetRasterBand(1).SetNoDataValue(NoDataValue)
# outdata.FlushCache()