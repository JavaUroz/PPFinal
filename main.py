from functions import *

# Obtenemos datos en dataframe
data = conexion_datos()

# Formulario que define la interfaz como parametro
level_user = formulario_interfaz()

# Interfaz visualizada de acuerdo a seleccion
define_interfaz(level_user, data)

