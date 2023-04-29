from fnmatch import fnmatch
import cv2 as cv
import netCDF4 as nc
import numpy as np
from os import system
import os
import glob
from osgeo import gdal
from NetCDFModule import NetCDFModule

class ImageProcessing(NetCDFModule):
	def __init__(self):
		self.raster=None
		self.satelliteImages=[]
		self.ModisNorm=[]
		self.fullMask=None
		self.names_images=[]
	def loadTifFile(self,fn):
		os.chdir(fn)
		os.getcwd() 
		lista=glob.glob("*.tif")
		for imagen in lista:
			path=fn+'\\'+imagen
			self.names_images.append(imagen)
			self.raster = gdal.Open(path)
			self.image = self.raster.ReadAsArray()
			self.satelliteImages.append(self.image)
	def createCloudMask(self,cloudIMaskList,path):
		cont=np.ones(cloudIMaskList[0].shape)
		for im in cloudIMaskList:
			cont=cont*im
		NoDataValue=-999
		driver = gdal.GetDriverByName("GTiff")
		outFileName=path+'fullCloudMask.tif'
		outdata = driver.Create(outFileName,cont.shape[1], cont.shape[0], 1, gdal.GDT_Float32)
		outdata.SetGeoTransform(self.raster.GetGeoTransform())
		outdata.SetProjection(self.raster.GetProjection())
		outdata.GetRasterBand(1).WriteArray(cont)
		outdata.GetRasterBand(1).SetNoDataValue(NoDataValue)
		outdata.FlushCache()
	def applyCloudMask(self,path_to_MODISImages,path_to_TifCloudMask,path_dest):
		path_dest=path_dest+"modis_norm" #modis a las cuales se les aplicó la máscara de nubes
		if not os.path.isdir(path_dest):
			os.makedirs(path_dest)
		os.chdir(path_dest)
		os.getcwd()
		self.satelliteImages=[]
		self.names_images=[]
		self.loadTifFile(path_to_MODISImages)
		rasterFullCloud = gdal.Open(path_to_TifCloudMask)
		CloudMask = rasterFullCloud.ReadAsArray()
		for imodis in self.satelliteImages:
			imodis_norm=imodis*CloudMask
			self.ModisNorm.append(imodis_norm)
		NoDataValue=-999
		driver = gdal.GetDriverByName("GTiff")

		#########################################Warning: Parámetro absoluto cambiar##############################
		# path_to_ref_im="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\ref_im.tif"
		path_to_ref_im = "C:\\Users\\Luis Miguel\\Documents\\framework\\ref_im.tif"
		ref_raster = gdal.Open(path_to_ref_im)
		#########################################Warning: Parámetro absoluto cambiar##############################

		keyword="norm"
		for i in range(len(self.ModisNorm)):
			outFileName=path_dest+'\\'+keyword+'_'+self.names_images[i]
			outdata = driver.Create(outFileName,self.ModisNorm[i].shape[1], self.ModisNorm[i].shape[0], 1, gdal.GDT_Float32)
			outdata.SetGeoTransform(ref_raster.GetGeoTransform())
			outdata.SetProjection(ref_raster.GetProjection())
			outdata.GetRasterBand(1).WriteArray(self.ModisNorm[i])
			outdata.GetRasterBand(1).SetNoDataValue(NoDataValue)
			outdata.FlushCache()
	