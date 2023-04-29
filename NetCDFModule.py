from fnmatch import fnmatch
import cv2 as cv
import netCDF4 as nc
import numpy as np
from os import system
import os
import glob
from osgeo import gdal

class NetCDFModule(object):
	def __init__(self,_fn=None): #_fn: directorio imágenes netcdf
		self.fn=_fn
		self.LImgClor=[]
		self.LImgCloud=[]
		self.names_images=[]
		self.ref_raster=None
		self.load_ref_raster()

	def load(self):
		os.chdir(self.fn)
		os.getcwd() 
		lista=glob.glob("*.nc")
		for imagen in lista:
			path=self.fn+'\\'+imagen
			ds = nc.Dataset(path)
			clo_cloud = ds['chlor_a_count'][:]
			clo = ds['chlor_a'][:]
			self.LImgClor.append(clo)
			self.LImgCloud.append(clo_cloud)
			self.names_images.append(imagen)
		self.create_folder()

	def load_ref_raster(self):
		self.ref_raster = gdal.Open('ref_im.tif')

	def create_folder(self):
		path_dest1=self.fn+"modis_clo"
		path_dest2=self.fn+"modis_cloud"
		if not os.path.isdir(path_dest1):
			os.makedirs(path_dest1)
		if not os.path.isdir(path_dest2):
			os.makedirs(path_dest2)
		self.save(path_dest1,self.LImgClor,self.names_images,'clora')
		self.save(path_dest2,self.LImgCloud,self.names_images,'cloud')

	def save(self,path_dest,list_images,list_names,keyword):
		NoDataValue=-999
		driver = gdal.GetDriverByName("GTiff")
		for i in range(len(list_images)):
			outFileName=path_dest+'\\'+keyword+'_'+list_names[i]+'.tif'
			outdata = driver.Create(outFileName,list_images[i].shape[1], list_images[i].shape[0], 1, gdal.GDT_Float32)
			outdata.SetGeoTransform(self.ref_raster.GetGeoTransform())
			outdata.SetProjection(self.ref_raster.GetProjection())
			outdata.GetRasterBand(1).WriteArray(list_images[i])
			outdata.GetRasterBand(1).SetNoDataValue(NoDataValue)
			outdata.FlushCache()