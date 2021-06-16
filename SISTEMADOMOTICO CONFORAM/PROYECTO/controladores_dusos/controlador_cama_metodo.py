#Instalar skfuzzy con pip install pip install scikit-fuzzy
"""
Created on Sat Oct 31 16:15:14 2020

@author: Anthony Sanchez, Mafer Revelo
"""

#importamos las bibliotecas
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control  as ctrl
import requests
from requests.api import get
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth 

def Input_Presion_ejercida():
    #Variables de entrada
    presion_ejercida=ctrl.Antecedent( np.arange(0,100,1), 'presion_ejercida')
    #Variable presion_ejercida
    presion_ejercida ['alta']=fuzz.trimf(presion_ejercida.universe,[50, 100, 100])
    presion_ejercida ['media']=fuzz.trimf(presion_ejercida.universe,[20, 50, 70])
    presion_ejercida ['baja']=fuzz.trimf(presion_ejercida.universe,[0, 0, 30])
    return presion_ejercida

def Input_Frecuencia_cardiaca():
    frecuencia_cardiaca=ctrl.Antecedent(np.arange(40, 100, 1), 'frecuencia_cardiaca')
    #Variable frecuencia_cardiaca
    frecuencia_cardiaca ['despierto']=fuzz.trapmf(frecuencia_cardiaca.universe,[55, 60, 100, 100])
    frecuencia_cardiaca ['medio_despierto']=fuzz.trimf(frecuencia_cardiaca.universe,[45, 50, 60])
    frecuencia_cardiaca ['dormido']=fuzz.trimf(frecuencia_cardiaca.universe,[40, 40, 50])
    return frecuencia_cardiaca

def Input_Movimiento():
    movimiento=ctrl.Antecedent(np.arange(0, 100, 1),'movimiento')
    #Variable movimiento
    movimiento ['alta']=fuzz.trimf(movimiento.universe,[40, 70, 100])
    movimiento ['media']=fuzz.trimf(movimiento.universe,[10, 30, 50])
    movimiento ['baja']=fuzz.trimf(movimiento.universe,[0, 0, 20])
    return movimiento

def Output_Estado_foco():
    estado_foco=ctrl.Consequent(np.arange(0,100,1),'estado_foco')
    #Variable de salida estado_foco
    estado_foco ['prendido']=fuzz.trapmf(estado_foco.universe,[50, 70, 100, 100])
    estado_foco ['medio_prendido']=fuzz.trimf(estado_foco.universe,[10, 40, 70])
    estado_foco ['apagado']=fuzz.trapmf(estado_foco.universe,[0, 0,10, 30])
    return estado_foco

def Generating_Rules_Cama (presion_ejercida, frecuencia_cardiaca, movimiento, estado_foco ):
    #Reglas
    regla1_controlador_cama=ctrl.Rule(presion_ejercida['baja'] | frecuencia_cardiaca['dormido']| movimiento['baja'],estado_foco['apagado'])
    regla2_controlador_cama=ctrl.Rule(presion_ejercida['media'] | frecuencia_cardiaca['dormido']| movimiento['media'],estado_foco['apagado'])
    regla3_controlador_cama=ctrl.Rule(presion_ejercida['media'] |frecuencia_cardiaca['dormido']| movimiento['alta'],estado_foco['apagado'])
    regla4_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['dormido']| movimiento['baja'],estado_foco['apagado'])
    regla5_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['dormido']| movimiento['media'],estado_foco['apagado'])
    regla6_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['dormido']| movimiento['alta'],estado_foco['apagado'])
    regla7_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['medio_despierto']| movimiento['baja'],estado_foco['apagado'])
    regla8_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['medio_despierto']| movimiento['media'],estado_foco['apagado'])
    regla9_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['medio_despierto']| movimiento['alta'],estado_foco['medio_prendido'])
    regla10_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']| movimiento['baja'],estado_foco['medio_prendido'])
    regla11_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']| movimiento['media'],estado_foco['medio_prendido'])
    regla12_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']| movimiento['alta'],estado_foco['medio_prendido'])
    regla13_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']| movimiento['baja'],estado_foco['prendido'])
    regla14_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']|movimiento['media'],estado_foco['prendido'])
    regla15_controlador_cama=ctrl.Rule(presion_ejercida['alta'] | frecuencia_cardiaca['despierto']| movimiento['alta'],estado_foco['prendido'])

    foco_ctrl = ctrl.ControlSystem ([regla1_controlador_cama,regla2_controlador_cama,regla3_controlador_cama,regla4_controlador_cama,regla5_controlador_cama,regla6_controlador_cama,regla7_controlador_cama,regla8_controlador_cama,regla9_controlador_cama, regla10_controlador_cama,regla11_controlador_cama,regla12_controlador_cama,regla13_controlador_cama,regla14_controlador_cama,regla15_controlador_cama])
    foco_intensidad = ctrl.ControlSystemSimulation(foco_ctrl)
    return foco_intensidad

def PyFuzzyComputation(foco_intensidad,ppresion_ejercida, pfrecuencia_cardiaca, pmovimiento):
    foco_intensidad.input['presion_ejercida']=ppresion_ejercida
    foco_intensidad.input['frecuencia_cardiaca']=pfrecuencia_cardiaca
    foco_intensidad.input['movimiento']=pmovimiento
    foco_intensidad.compute()
    return foco_intensidad.output['estado_foco']


def Get_IoT_Data(endpoint, object_iot, resource):
        response = requests.get(endpoint + '/' + object_iot + '/' + resource)
        #if response.status_code == 200:
        if response.status_code == 401:      
            r = requests.get(endpoint + '/' + object_iot + '/' + resource, 
            auth=HTTPBasicAuth('anthony.sanchez@pucese.edu.ec', 'Casio19735*'))
            return r.text
        if response.status_code != 200:
            r = requests.get(endpoint + '/' + object_iot + '/' + resource, 
            auth=HTTPBasicAuth('anthony.sanchez@pucese.edu.ec', 'Casio19735*'))
            return r.text
  
def PyFuzzyControlloing(endpoint, object_iot, resource, value):
    user = 'anthony.sanchez@pucese.edu.ec'
    passwd = 'Casio19735*'
    response = requests.put(endpoint + '/' + object_iot + '/' + resource,
                data=value,                        
                auth=(user, passwd),
                headers={'content-type':'text/plain'} )
    return response


#=====================================Controlador con openhab===============================================   


#Variables para obtener varlores random 
# Presion ejercida 
endpoint="https://home.myopenhab.org/rest/items"
object_iot_presion="MasterBedroom_Presion_ejercida"
#Frecuencia cardiaca
object_iot_frecuencia="MasterBedroom_Frecuencia_cardiaca"
#Frecuencia movimiento
object_iot_movimiento="MasterBedroom_Movimiento"
resource= "state"


#obtiene valores random para utilizarlos en el controlador cama
#Presion
presion_get=Get_IoT_Data(endpoint,object_iot_presion,resource)
print("Precion de CONFORAM===> ")
print([presion_get])
#Frecuencia
frecuencia_cardiaca_get=Get_IoT_Data(endpoint,object_iot_frecuencia,resource)
print("Frecuencia cardiaca de CONFORAM===>")
print([frecuencia_cardiaca_get])
#Movimiento
movimiento_get=Get_IoT_Data(endpoint,object_iot_movimiento,resource)
print("Movimiento de CONFORAM===>")
print([movimiento_get])

#Variables de entrada
presion_ejercida=Input_Presion_ejercida()
frecuencia_cardiaca=Input_Frecuencia_cardiaca()
movimiento=Input_Movimiento()

#Variable de salida
#estado_foco=PyFuzzyComputation()
#print(estado_foco)

#answer = PyFuzzyComputation(lighting, float(mode_iot), int(motion_iot_), float(illum_iot))
#print('Value for ligthing', answer)