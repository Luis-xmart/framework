import netCDF4 as nc
import numpy as np

# Ruta al archivo NetCDF
# ruta_netcdf = "C:\\Users\\Personal\\Documents\\subset_0_of_01_mapped_AQUA_MODIS.20230103T193500.L2.OC.nc"
# ruta_netcdf = "C:\\Users\\Personal\\Documents\\subset_02_of_03_mapped_A2010005183500.L2_LAC_OC.nc"
# ruta_netcdf = "C:\\Users\\Personal\\Documents\\subset_13_of_predict_modis.nc"
# ruta_netcdf = "C:\\Users\\Personal\\Documents\\subset_16_of_predict_modis1.nc"
ruta_netcdf = "C:\\Users\\Personal\\Documents\\subset_17_of_predict_modismod2010.nc"



# Nombre de la variable (banda) de interés (ajusta según tus datos)
# nombre_variable = "chlor_a"
nombre_variable = "band_1"


# Umbral para considerar píxeles con información
umbral = 0.0  # Ajusta según tus necesidades

# Abrir el archivo NetCDF en modo lectura
with nc.Dataset(ruta_netcdf, 'r') as archivo_netcdf:
    # Leer la variable (banda) como una matriz NumPy
    variable_chlor_a = archivo_netcdf.variables[nombre_variable][:]

    # Obtener la cantidad de píxeles sin información (valores nulos)
    píxeles_sin_información = np.sum(variable_chlor_a == umbral)
    # Obtener el total de píxeles en la banda
    total_pixeles = variable_chlor_a.size
    # Obtener la cantidad de píxeles con información (no nulos)
    pixeles_con_informacion = np.sum(~np.isnan(variable_chlor_a))
     # Obtener la cantidad de píxeles con información (mayores al umbral)
    pixeles_con_informacion = np.sum(variable_chlor_a > umbral)
    

# Imprimir el resultado
print(f"Cantidad de píxeles sin información en {nombre_variable}: {píxeles_sin_información}")
print(f"Total de píxeles en {nombre_variable}: {total_pixeles}")
print(f"Cantidad de píxeles con información en {nombre_variable}: {pixeles_con_informacion}")
print(f"Cantidad de píxeles con información en {nombre_variable}: {pixeles_con_informacion}")
