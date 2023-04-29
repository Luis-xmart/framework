import numpy as np
from PIL import Image
import random
from osgeo import gdal
import pandas as pd
# Cargar las imágenes
path_to_modis = "C:\\Users\\Personal\\Documents\\Corregistro\\Corregistradas\\modis_clo\\clora_01_mapped_AQUA_MODIS.20230103T193500.L2.OC.NRT.x.nc.tif"
path_to_modis2010 = "C:\\Users\\Personal\\Documents\\Corregistro\\Corregistradas\\modis_clo\\clora_03_mapped_A2010005183500.L2_LAC_OC.x.nc.tif"
imagen_alt = 'C:\\Users\\Personal\\Documents\\framework\\results\\predict_modis.tif'
modis_mod= 'C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_mod.tiff'
img_mod = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\predict_modismod.tif'
img_mod2010= 'C:\\Users\\Personal\\Documents\\framework\\results\\predict_modismod2010.tif'
# Cargar las imágenes original y predicha
# imgOriginal = np.array(Image.open(modis_mod))
imgPredicha = np.array(Image.open(img_mod2010))
raster = gdal.Open(path_to_modis2010)
modis = raster.ReadAsArray()
# Obtener el ancho y la altura de la imagen
rows = raster.RasterYSize
cols = raster.RasterXSize
# Crear matriz de ceros con la misma forma que las imágenes
diff = np.zeros(modis.shape, dtype=np.int16)

# Calcular la cantidad de píxeles a eliminar aleatoriamente
num_pixels_to_remove = int(rows * cols * 0.1) # por ejemplo, eliminar el 10% de los píxeles

# Crear una lista aleatoria de índices de fila y columna para los píxeles a eliminar
pixel_indices = random.sample(range(rows * cols), num_pixels_to_remove)
pixel_indices = [(i // cols, i % cols) for i in pixel_indices]

# Calcular la diferencia solo para los puntos que se quitaron
for punto in pixel_indices:
    i, j = punto
    diff[i, j] = modis[i, j] - imgPredicha[i, j]

# Obtener vector de diferencias
vector_diff = np.ravel(diff)
x1 = abs(vector_diff)
media = pd.Series(x1).mean()
desviacion_estandar = pd.Series(x1).std()

print("La media del vector es:", media)
print("La desviación estándar del vector es:", desviacion_estandar)
# Imprimir vector de diferencias
#print(vector_diff)
