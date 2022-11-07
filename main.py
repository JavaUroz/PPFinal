# Importamos todas las funciones de functions.py 
from functions import conexion_datos, formulario_interfaz, define_interfaz

# Obtenemos datos en dataframe
data = conexion_datos()

# Formulario que define la interfaz como parametro
level_user = formulario_interfaz()

# Interfaz visualizada de acuerdo a seleccion
define_interfaz(level_user, data)

