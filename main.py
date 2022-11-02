import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from functions import agrega_tablas
from functions import define_interfaz

# Definición de los controles de la barra lateral
level_user = st.sidebar.selectbox(label='Nivel de usuario', options=['Novato', 'Experto'])

# # Conexión con SQLAlchemy
path = 'data/'
database = 'DSS-Autos.db'
my_conn = create_engine('sqlite:///'+path+database)

# Carga los datos de la aplicación
vehiculos = pd.read_sql_table('autos',my_conn)
precios = pd.read_sql_table('precios',my_conn)
criterios = pd.read_sql_table('criterios', my_conn)

# Fusiona los precios y criterios relevantes con la tabla de vehículos.
data = agrega_tablas(vehiculos, precios, criterios)

# Definición del panel central
st.header('Sistema de apoyo para la elección de vehículos')
define_interfaz(level_user, data)
