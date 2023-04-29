from osgeo import gdal
import numpy as np
import random
path_to_modis = "C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_clo\\clora_03_mapped_A2010005183500.L2_LAC_OC.x.nc.tif"
nueva_imagen = "C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_mod2010.tiff"
# raster = gdal.Open(path_to_modis)
# rows = raster.RasterYSize
# cols = raster.RasterXSize
# modis = raster.ReadAsArray()
# confidence_map = np.zeros(modis.shape)
# new_modis = np.zeros(modis.shape)

# Ruta de la imagen de entrada y salida
input_file = 'input.tif'
output_file = 'output.tif'

# Abrir la imagen utilizando la biblioteca GDAL
ds = gdal.Open(path_to_modis)

# Obtener el ancho y la altura de la imagen
rows = ds.RasterYSize
cols = ds.RasterXSize

# Convertir la imagen en una matriz NumPy
band = ds.GetRasterBand(1)
data = band.ReadAsArray(0, 0, cols, rows)

# Crear una copia de la matriz original
data_copy = data.copy()

# Calcular la cantidad de píxeles a eliminar aleatoriamente
num_pixels_to_remove = int(rows * cols * 0.1) # por ejemplo, eliminar el 10% de los píxeles

# Crear una lista aleatoria de índices de fila y columna para los píxeles a eliminar
pixel_indices = random.sample(range(rows * cols), num_pixels_to_remove)
pixel_indices = [(i // cols, i % cols) for i in pixel_indices]

# Establecer los valores de los píxeles correspondientes a cero en la matriz copiada
for pixel in pixel_indices:
    data_copy[pixel] = 0

# Crear una nueva imagen TIFF utilizando la matriz copiada y las propiedades de la imagen original
driver = gdal.GetDriverByName('GTiff')
new_ds = driver.Create(nueva_imagen, cols, rows, 1, gdal.GDT_Float32)
new_ds.SetGeoTransform(ds.GetGeoTransform())
new_ds.SetProjection(ds.GetProjection())
new_band = new_ds.GetRasterBand(1)
new_band.WriteArray(data_copy)
new_band.FlushCache()

# Cerrar los objetos GDAL
# ds = None
# new_ds = None
