from functions import *

# Obtenemos datos en dataframe
data = conexion_datos()

# Formulario que define la interfaz como parametro
level_user = formulario_interfaz()
define_interfaz(level_user, data)

# if level_user == None:
#     formulario_interfaz()
#     level_user = formulario_interfaz()
#     define_interfaz(level_user, data)
# else:    
#     define_interfaz(level_user, data)
