import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from classes import AutoSuv, Camioneta

def conexion_datos():
    # # Conexión con SQLAlchemy
    path = 'data/'
    database = 'DSS.db'
    my_conn = create_engine('sqlite:///'+path+database)

    # Carga los datos de la aplicación
    vehiculos = pd.read_sql_table('autos',my_conn)
    precios = pd.read_sql_table('precios',my_conn)
    criterios = pd.read_sql_table('criterios', my_conn)
    
    # Fusiona los precios con la tabla de vehículos.
    data = agrega_tablas(vehiculos, precios, criterios)
    return data

# Funcion interfaz para definir tipo de usuario
def formulario_interfaz():
    st.markdown('<div style="text-align: right;"><a href="https://github.com/JavaUroz/PPFinal1/blob/main/README.md">Readme</a></div>', unsafe_allow_html=True)
    st.title('Sistema de ayuda para la elección de su vehículo 0km')

    # Elegimos criterios para definir usuario
    with st.sidebar:
        st.write("[Como usar esta aplicación](https://github.com/JavaUroz/PPFinal1/blob/main/GUIA%20DE%20USUARIO.md)") 
        st.subheader('Elija que tipo de usuario es:')
        level_user = st.selectbox('Tipo de usuario',('No sé','Novato','Experto'))         
    if (level_user == 'No sé'):
        with st.expander('Realice este breve cuestionario para definir su perfil:'):             
            primer_auto = st.radio('¿Es su primer auto?',['Si', 'No'])
            mecanica = st.radio('¿Cuán importante es la mecánica para usted?', ['Poco' , 'Algo', 'Mucho'])
            col1, col2 = st.columns(2)
            investigo = col1.select_slider('¿Ha investigado acerca de las opciones disponibles en el mercado?',['Nada' , 'Algo', 'Suficiente', 'Todo'])        
            st.write('Opciones de financiamiento')       
            contado = st.checkbox('Contado/Efectivo o transferencia, valores al día')
            financiado_parcial = st.checkbox('Financiamiento con entrega de anticipo/usado')
            financiado_total = st.checkbox('Financiado 100%')    
        if (primer_auto == 'No' and mecanica == 'Mucho' and (investigo == 'Suficiente' or investigo == 'Todo') and (contado or financiado_parcial)):
            level_user = "Experto"
        elif (financiado_total or financiado_parcial or contado):
            level_user = 'Novato'
        else:
            level_user = None        
    return level_user

# Creamos la función de la matriz de decision para usuarios novatos
def matriz_decision_novato(dataframe, a, b, c):    
    dataframe['Puntuacion'] = (dataframe['C'] * (1 - a) + 10) + \
                              (dataframe['P'] * b + 10) + (dataframe['S'] * c)
    return dataframe

# Creamos la función de la matriz de decision para usuarios expertos
def matriz_decision_experto(dataframe, a, b, c, d):
    dataframe['Puntuacion'] = (dataframe['C'] * (1 - a) + 10) + \
                              (dataframe['P'] * b + 10) + (dataframe['S'] * c) + \
                              (dataframe['C.1'] * (1 - d))
    return dataframe
# Creamos la función que agrega los precios y especificaciones avanzadas
def agrega_tablas(dataframe1, dataframe2, dataframe3):
    merge1 = dataframe1.merge(dataframe2, left_on='Version', right_on='Version')
    merge = merge1.merge(dataframe3, left_on='Version', right_on='Version')
    return merge

def explora_vehiculo(version, data):
    vehicle = data[data['Version']==version]
    if vehicle.tipoVehiculo == 'Camioneta':
        explorer = Camioneta(vehicle.Marca, vehicle.Modelo, vehicle.Version, vehicle.TipoVehiculo, vehicle.Combustible, vehicle.Potencia, vehicle.Transmisión, vehicle.Cabina, vehicle.Traccion)
    else:
        explorer = AutoSuv(vehicle.Marca, vehicle.Modelo, vehicle.Version, vehicle.TipoVehiculo, vehicle.Combustible, vehicle.Potencia, vehicle.Transmisión, vehicle.Traccion)
    return explorer

# Creamos la función que presenta la interfaz
def define_interfaz(level_user, data):    
    if level_user == 'Novato':
        interfaz_novato(data)
    elif level_user == 'Experto':
        interfaz_experto(data)

def interfaz_novato(data):
    # Opciones de interfaz para usuarios novatos                           
    # Habilita las opciones de filtrado      
    st.sidebar.subheader('Criterios de selección:')
    select_consumo = st.sidebar.slider('Bajo Consumo', 1, 5)
    select_potencia = st.sidebar.slider('Potencia', 1, 5)
    select_seguridad = st.sidebar.slider('Seguridad', 1, 5)
    st.subheader("Interfaz para usuario Novato")
    with st.expander('Seleccione los elementos de filtrado:'):
        col1, col2 = st.columns(2)           
        marca = col1.multiselect('Marca del vehículo', sorted(data['Marca'].unique().tolist()))        
        if marca == []:
            col1.error('Elija al menos una marca de vehículo')
        tipo = col2.multiselect('Tipo de carrocería', sorted(data['TipoVehiculo'].unique().tolist()))
        if tipo == []:
            col2.error('Elija al menos un tipo de carrocería')
        precio_max = st.slider('Precio en miles de pesos', 0, 30000)
        
        # Aplica las opciones de filtrado
        filtrado = data[(data['Marca'].isin(marca)) & (data['Precio'] < precio_max)]

        # Aplica la matriz de decisión y la guarda en la variable ponderacion.
        ponderacion = matriz_decision_novato(filtrado, select_consumo, select_potencia, select_seguridad)
        
        # Devuelve los resultados de la recomendación ordenados por puntuación descendente.    
        if marca == [] or tipo == [] or precio_max == 0:
            st.warning('Elija sus preferencias para ver las recomendaciones')
        else:
            st.header('Listado de vehiculos recomendados')
            st._arrow_table(
            ponderacion.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                                    ascending=False),
            )

def interfaz_experto(data):
    # Opciones de interfaz para usuarios expertos
    st.write("[Readme](https://github.com/JavaUroz/PPFinal1/blob/main/README.md)")
    st.write("[Guía de usuario](https://github.com/JavaUroz/PPFinal1/blob/main/GUIA%20DE%20USUARIO.md)") 
    st.sidebar.subheader('Criterios de selección:')
    select_consumo=st.sidebar.slider('Bajo Consumo', 1, 5)
    select_potencia=st.sidebar.slider('Potencia', 1, 5)
    select_seguridad=st.sidebar.slider('Seguridad', 1, 5)
    select_confort=st.sidebar.slider('Confort', 1, 5)
    st.subheader("Interfaz para usuario Experto")
    # Habilita las opciones de filtrado
    with st.expander('Seleccione los elementos de filtrado:'):
        col1, col2=st.columns(2)
        marca = col1.multiselect('Marca del vehículo', sorted(data['Marca'].unique().tolist()))
        if marca == []:
            col1.error('Elija al menos una marca de vehículo')
        tipo = col1.multiselect('Tipo de vehículo',sorted(data['TipoVehiculo'].unique().tolist()))
        if tipo == []:
            col1.error('Elija al menos un tipo de vehículo')
        transmision = col2.multiselect('Transmisión',['Manual','Automática'])
        if transmision == []:
            col2.error('Elija al menos un tipo de transmisón')
        combustible = col2.multiselect('Combustible', ['Nafta', 'Diesel', 'Híbrido'])
        if combustible == []:
            col2.error('Elija al menos un tipo de combustible')
        precio_max=st.slider('Precio en miles de pesos', 0, 30000)        
    
        # Aplica las opciones de filtrado
        filtrado=data[(data['Marca'].isin(marca)) & (data['Precio'] < precio_max) & (data['Transmisión'].isin(transmision)) & (data['TipoVehiculo'].isin(tipo)) & (data['Combustible'].isin(combustible))]        
        
        # Aplica la matriz de decisión y la guarda en la variable ponderacion.
        ponderacion=matriz_decision_experto(filtrado, select_consumo, select_potencia, select_seguridad, select_confort)
        
        # Devuelve los resultados de la recomendación ordenados por puntuación descendente.
        if marca == [] or tipo == [] or transmision == [] or combustible == [] or precio_max == 0:
            st.warning('Elija sus preferencias para ver las recomendaciones')               
        data = st.dataframe(
            ponderacion.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Cilindrada(cc)', 'Potencia(CV)', 'Consumo(Lt/100km)','LinkMasInfo' , 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                                ascending=False),
            )