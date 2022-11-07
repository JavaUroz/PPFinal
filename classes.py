#Creamos clase abstracta Vehiculo sus atributos y métodos
class Vehiculo(object):
    def __init__(self):
        self.marca = None
        self.modelo = None
        self.version = None
        self.tipo = None
        self.motor_combustible = None
        self.motor_potencia = None
        self.transmision = None
        self.traccion = None

    def get_marca(self):
        return self.marca

    def get_modelo(self):
        return self.modelo

    def get_version(self):
        return self.version

    def get_combustible(self):
        return self.motor_combustible

    def get_tipo(self):
        return self.tipo

    def get_traccion(self):
        return self.traccion
    
    def __str__(self):
        return "Informacion del vehiculo:\n1. Marca: {m}\n2. Modelo: {o}\n3. Version: {v}".format(
            m=self.get_marca(), o=self.get_modelo(), v=self.get_version())

# Definimos clase AutoSuv para darle escalabilidad a otros vehículos y separarla de camioneta, solucionar error del atributo 'cabina'
class AutoSuv(Vehiculo):
    def __init__(self, marca, modelo, version, tipo, combustible, potencia, transmision, traccion):
        self.marca = marca
        self.modelo = modelo
        self.version = version
        self.tipo = tipo
        self.combustible = combustible
        self.potencia = potencia
        self.transmision = transmision
        self.traccion = traccion

# Definimos clase Camioneta con el atributo "cabina" y su getter.
class Camioneta(Vehiculo):
    def __init__(self, marca, modelo, version, tipo, combustible, potencia, transmision, cabina, traccion):
        self.marca = marca
        self.modelo = modelo
        self.version = version
        self.tipo = tipo
        self.combustible = combustible
        self.potencia = potencia
        self.transmision = transmision
        self.cabina = cabina
        self.traccion = traccion

    def get_cabina(self):
        return self.cabina
