import streamlit as st

from classes import AutoSuv, Camioneta

def formulario_interfaz():
    level_user = None
    with st.form("form_interfaz"):
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
        submitted = st.form_submit_button("Definir Interfaz")
        if submitted:
            if (cv and fp and nafta and gasoil and conocimiento > 6):    
                level_user = 'Experto'
            elif ((hp or wt) and (gasolina or biodiesel or querosene) and (fe or fs) and (conocimiento <= 6)):    
                level_user = 'Novato'
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
# Creamos la función que agrega los precios
def agrega_tablas(dataframe1, dataframe2):
    merge = dataframe1.merge(dataframe2, left_on='Version', right_on='Version')
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
    st.sidebar.caption('Seleccione sus preferencias generales para usuario NOVATO (default)')
    select_consumo = st.sidebar.slider('Bajo Consumo', 1, 5)
    select_potencia = st.sidebar.slider('Potencia', 1, 5)
    select_seguridad = st.sidebar.slider('Seguridad', 1, 5)
    # Habilita las opciones de filtrado
    st.markdown('**USUARIO NOVATO**')
    with st.expander('Seleccione los criterios de filtrado de su preferencia'):
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
        st.markdown('Listado de vehiculos recomendados')
        st._arrow_table(
        ponderacion.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                               ascending=False),
        )

def interfaz_experto(data):
    # Opciones de interfaz para usuarios expertos
    st.markdown('**USUARIO EXPERTO**')
    st.sidebar.caption('Seleccione los criterios de filtrado de su preferencia')
    select_consumo=st.sidebar.slider('Bajo Consumo', 1, 5)
    select_potencia=st.sidebar.slider('Potencia', 1, 5)
    select_seguridad=st.sidebar.slider('Seguridad', 1, 5)
    select_confort=st.sidebar.slider('Confort', 1, 5)
    # Habilita las opciones de filtrado
    with st.expander('Seleccione los criterios de filtrado de su preferencia para usuario EXPERTO'):
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
    else:
        st.markdown('Listado de vehiculos recomendados')        
        st._arrow_table(
        ponderacion.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                               ascending=False),
        )
