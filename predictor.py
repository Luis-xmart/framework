from NetCDFModule import NetCDFModule
from ImageProcessing import ImageProcessing
from builderDataset import builderDataset

module_ImageProcessing=False
module_builderDataset=True

if module_ImageProcessing is False:
	#extraer variables de clorofila y máscara de nubes, almacenarlas en formato tif
	# path="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\Imagenes\\"
	path="C:\\Users\\Luis Miguel\\Documents\\Corregistro\\Corregistradas\\"
	ImsNetCDF=NetCDFModule(path)
	print(ImsNetCDF)
	ImsNetCDF.load()

	#cargar imágenes de nubes por mes
	# path_cloud = "D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\Imagenes\\modis_cloud\\"
	path_cloud = "C:\\Users\\Luis Miguel\\Documents\\Corregistro\\Corregistradas\\modis_cloud\\"
	CloudGral = ImageProcessing()
	CloudGral.loadTifFile(path_cloud)

	#crear máscara general de nubes correspondiente a la serie temporal
	# path_fullCloudMask="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\"
	path_fullCloudMask="C:\\Users\\Luis Miguel\\Documents\\framework\\results\\"
	CloudGral.createCloudMask(CloudGral.satelliteImages,path_fullCloudMask)

	#normalizar las imágenes modis conforme a la máscara general de nubes
	# path_to_MODISImages="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\Imagenes\\modis_clo\\"
	path_to_MODISImages="C:\\Users\\Luis Miguel\\Documents\\Corregistro\\Corregistradas\\modis_clo\\"
	# path_to_TifCloudMask="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\fullCloudMask.tif"
	path_to_TifCloudMask="C:\\Users\\Luis Miguel\\Documents\\framework\\results\\fullCloudMask.tif"
	# path_dest_MODISNorm="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\"
	path_dest_MODISNorm="C:\\Users\\Luis Miguel\\Documents\\framework\\results\\"
	CloudGral.applyCloudMask(path_to_MODISImages,path_to_TifCloudMask,path_dest_MODISNorm)

if module_builderDataset is True:
	#construir conjunto de datos
	# path_to_modis="D:\\UNICOMFACAUCA_2022_II\\trabajos-de-grado\\CarlosSebastian\\code\\framework\\results\\modis_norm\\"
	path_to_modis="C:\\Users\\Luis Miguel\\Documents\\framework\\results\\modis_norm\\"
	spatial_resolution=1
	time_resolution=0
	px_features = 8
	builder = builderDataset(path_to_modis,spatial_resolution,time_resolution,px_features,"dataset_8_neigh.csv")
	builder.loadImages()
	builder.builder()