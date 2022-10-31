import streamlit as st
import pandas as pd
from modules.functions import agrega_precios
from modules.functions import define_interfaz
# from sqlalchemy import create_engine

# Definición de los controles de la barra lateral
level_user = st.sidebar.selectbox(label='Nivel de usuario', options=['Novato', 'Experto'])

# Conexión con SQLAlchemy
# path = '.\data/'
# database = 'DSS.db'
# my_conn=create_engine('sqlite:///'+path+database)

# Carga los datos de la aplicación
data_vehiculos = pd.read_csv('./data/vehiculos.csv')
data_precios = pd.read_csv('./data/precios.csv', dtype={'Precio': float})
# data_vehiculos = pd.read_sql_table('autos', my_conn)
# data_precios = pd.read_sql_table('precios', my_conn)
# data_criterios = pd.read_sql_table('criterios', my_conn)

# Fusiona los precios con la base de datos de vehículos.
data = agrega_precios(data_vehiculos, data_precios)

# Definición del panel central
st.header('Sistema de apoyo para la elección de vehículos')
define_interfaz(level_user, data)
