import streamlit as st

class Vehiculo:
  def __init__(self, marca, modelo, version, tipo, combustible, potencia, transmision, cabina, traccion):
    self.marca = marca
    self.modelo = modelo
    self.version = version
    self.motor_combustible = combustible
    self.motor_potencia = potencia
    self.transmision = transmision
    self.cabina = cabina
    self.traccion = traccion

  def get_marca(self):
      return self.marca

  def get_modelo(self):
      return self.modelo

  def get_version(self):
      return self.version

  def get_combustible(self):
      return self.motor_combustible

  def get_traccion(self):
      return self.traccion

  def get_cabina(self):
    return self.cabina

