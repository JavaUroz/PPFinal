import streamlit as st
import pandas as pd
from functions import agrega_precios
from functions import define_interfaz

# Definición de los controles de la barra lateral
level_user = st.sidebar.selectbox(label='Nivel de usuario', options=['Novato', 'Experto'])

# Carga los datos de la aplicación
vehiculos = pd.read_csv('./data/vehiculos.csv')
precios = pd.read_csv('./data/precios.csv', dtype={'Precio': float})
# Fusiona los precios con la base de datos de vehículos.
data = agrega_precios(vehiculos, precios)

# Definición del panel central
st.header('Sistema de apoyo para la elección de vehículos')
define_interfaz(level_user, data)
