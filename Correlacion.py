import numpy as np
from PIL import Image
import pandas as pd
# Cargar las imágenes
path_to_modis = "C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_clo\\clora_01_mapped_AQUA_MODIS.20230103T193500.L2.OC.NRT.x.nc.tif"
imagen_alt = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\predict_modis.tif'
modis_aleat = 'C:\\Users\\luis1\\OneDrive\\Documentos\\Corregistro\\Corregistradas\\modis_mod.tiff'
img_mod = 'C:\\Users\\luis1\\OneDrive\\Documentos\\framework\\results\\predict_modismod.tif'
img1 = Image.open(modis_aleat)
img2 = Image.open(img_mod)

# Convertir las imágenes en matrices NumPy
arr1 = np.array(img1)
arr2 = np.array(img2)

# Restar las matrices
diff = arr1 - arr2
vector_diff = np.ravel(diff)
x1 = abs(vector_diff)
media = pd.Series(x1).mean()
desviacion_estandar = pd.Series(x1).std()

print("La media del vector es:", media)
print("La desviación estándar del vector es:", desviacion_estandar)
# Calcular la correlación de las dos matrices
#corr = np.corrcoef(arr1.flatten(), arr2.flatten())[0, 1]

# Guardar la nueva imagen con los píxeles restados
#Image.fromarray(diff).save('imagen_diff.tif')
#savetxt('vector2.txt', vector_diff)
# Imprimir la correlación
#print('Correlación:', vector_diff)
