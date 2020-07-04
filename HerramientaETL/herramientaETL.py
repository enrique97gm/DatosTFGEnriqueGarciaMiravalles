# coding: utf-8
import wget
from os import remove
import os.path as path
import sys

from dataBase import BD


#Función de descarga de archivos
def checkAndDownload(name, address):
	if path.exists(name+".csv"):
		remove(name+".csv");
		print("Archivo "+ name +".csv borrado");

	return wget.download(address, name+".csv");

				
#Ejecución de metodos y codigo principal
file = open(sys.argv[1], 'r');
i = 0;
for row in file:
	if(i == 0):
		bd = BD();
		bd.creaDB(row);
	elif(i % 2 != 0):
		estacion = row;
		estacion = estacion.replace('\n','');
	else:
		vall = checkAndDownload(estacion, row);
		bd.creaTable(vall, estacion);
		bd.formatInsert(vall, estacion);

	i += 1;

print("Datos insertados correctamente");


#Función de borrado de datos
#bd.borrarTodosDatos(estaciones);

#Función de borrado de tablas
#bd.borrarTablas(estaciones);




