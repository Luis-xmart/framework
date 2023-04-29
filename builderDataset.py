from fnmatch import fnmatch
import cv2 as cv
import netCDF4 as nc
import numpy as np
from os import system
import os
import glob
from osgeo import gdal
from NetCDFModule import NetCDFModule
import csv

class builderDataset(object):
	def __init__(self,_path_to_modis,_spatialResolution,_timeResolution,_px_features,_name_dataset):
		self.path_to_modis=_path_to_modis
		self.spatialResolution=_spatialResolution
		self.timeResolution=_timeResolution
		self.px_features=_px_features
		self.images=[]
		self.dataset=[]
		self.name_dataset=_name_dataset
	def loadImages(self):
		os.chdir(self.path_to_modis)
		os.getcwd()
		lista=glob.glob("*.tif")
		for imagen in lista:
			path=self.path_to_modis+imagen
			raster = gdal.Open(path)
			image = raster.ReadAsArray()
			self.images.append(image)
	def builder(self):
		if self.timeResolution > 0:
			#temporal
			pass
		else:
			#espacial
			for im in self.images:
				for i in range(im.shape[1]):
					for j in range(im.shape[0]):
						if im[j][i]!=0.0:
							log=self.logDataset(im,i,j)
							if(len(log)!=0):
								self.dataset.append(log)
			self.saveDataset2()
	def logDataset(self,im,px,py):
		log=[]
		cond1a=py-self.spatialResolution
		cond1b=py+self.spatialResolution+1
		cond2a=px-self.spatialResolution
		cond2b=px+self.spatialResolution+1
		if cond1a>=0 and cond1b<im.shape[1] and cond2a>=0 and cond2b<im.shape[0]:
			roi=im[cond1a:cond1b,cond2a:cond2b]
			valNonZeros=cv.countNonZero(roi)-1
			if valNonZeros==self.px_features:
				for i in range(roi.shape[1]):
					for j in range(roi.shape[0]):
						if (i!=self.spatialResolution or j!=self.spatialResolution) and roi[i][j]!=0.0:
							log.append(roi[i][j])
				log.append(roi[self.spatialResolution][self.spatialResolution])
		return log
	def saveDataset(self):
		with open(self.name_dataset, 'w') as f:
			write = csv.writer(f)
			#write.writerow(fields)
			write.writerows(self.dataset)
		print("dataset almacenado en carpeta modis_norm")
	def saveDataset2(self):
		key='feature_'
		header=[]
		for i in range(len(self.dataset[0])):
			if(i<len(self.dataset[0])-1):
				h=key+str(i)
				header.append(h)
			else:
				header.append("clor_val")
		print(header)
		DS = []
		DS.append(header)
		for i in self.dataset:
			DS.append(i)
		np.savetxt(self.name_dataset, DS, delimiter =",", fmt ='% s')
		print("dataset almacenado en carpeta modis_norm")