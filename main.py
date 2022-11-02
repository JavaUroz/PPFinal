import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from functions import agrega_tablas
from functions import define_interfaz

level_user = None

st.title('Sistema de apoyo para la elección de vehículos')
st.header('Conteste estas preguntas para definir su perfil')
st.markdown('Cuál es la unidad de medida de la potencia de un vehículo?')
hp = st.checkbox('HP')
wt = st.checkbox('WAT')
cv = st.checkbox('CV')
st.markdown('Que es el torque del motor?')
fe = st.checkbox('Es la fuerza de explosion del motor')
fp = st.checkbox('Es la fuerza aplicada en una palanca')
fs = st.checkbox('Es la fuerza aplicada a una superficie')
st.markdown('Cuales son las opciones de alimentacion mas conocidas en el pais?')
col1, col2=st.columns(2)
gasolina = col1.checkbox('Gasolina')
gasoil = col1.checkbox('Gasoil')
biodiesel = col1.checkbox('Biodiesel')
nafta = col2.checkbox('Nafta')
electricidad = col2.checkbox('Electricidad')
querosene = col2.checkbox('Querosene')
st.markdown('Cual es su conocimiento general sobre vehiculos?')
conocimiento = st.slider('Nivel de conocimiento', 1 , 10)
# Elegimos criterios para definir usuario   
if (cv and fp and nafta and gasoil and conocimiento > 6):    
    level_user = 'Experto'
elif ((hp or wt) and (gasolina or biodiesel or querosene) and (fe or fs) and (conocimiento <= 6)):    
    level_user = 'Novato'

# level_user = st.sidebar.selectbox(label='Nivel de usuario', options=['Novato', 'Experto'])

# # Conexión con SQLAlchemy
path = 'data/'
database = 'DSS-Autos.db'
my_conn = create_engine('sqlite:///'+path+database)

# Carga los datos de la aplicación
vehiculos = pd.read_sql_table('autos',my_conn)
precios = pd.read_sql_table('precios',my_conn)
criterios = pd.read_sql_table('criterios', my_conn)

# Fusiona los precios con la tabla de vehículos.
data = agrega_tablas(vehiculos, precios)

# Definición del panel central
#if st.button('Comprobar nivel'):
define_interfaz(level_user, data)