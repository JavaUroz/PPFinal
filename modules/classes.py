from types import NoneType
from typing_extensions import Self
import streamlit as st

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

  def get_tipo(self):
      return self.tipo

  def get_combustible(self):
      return self.motor_combustible

  def get_potencia(self):
      return self.motor_potencia

  def get_traccion(self):
      return self.traccion

class Auto_Suv(Vehiculo):
    def __init__(self, marca, modelo, version, tipo, combustible, potencia, transmision, traccion):
        self.marca = marca
        self.modelo = modelo
        self.version = version
        self.tipo = tipo
        self.combustible = combustible
        self.potencia = potencia
        self.transmision = transmision
        self.traccion = traccion

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

class Factoria(object):
    def get_vehiculo(self, marca, modelo, version, tipo, combustible, potencia, transmision, cabina, traccion):
        if (cabina != ''):
            return Camioneta(marca, modelo, version, tipo, combustible, potencia, transmision, cabina, traccion)
        else:
            return Auto_Suv(marca, modelo, version, tipo, combustible, potencia, transmision, traccion)
