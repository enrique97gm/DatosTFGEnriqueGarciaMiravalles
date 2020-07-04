
# coding: utf-8
#importando MySQL connector
import mysql.connector as mysql

#import csv
import csv

#Import para formato fechas
from datetime import datetime

#Clase base de datos, con todos los métodos propios de la funcionalidad de una BD       
class BD:

	db = mysql.connect(
		host = "direccion_servidor",
		user = "usuario",
		passwd = "contraseña",
		port = "puerto",
		auth_plugin='mysql_native_password',
	);

	cursor = db.cursor();


	#Función para crear la base de datos
	def creaDB(self, name):
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS "+ name +" CHARACTER SET utf8");
		self.cursor.execute("USE "+name);



	#Función de creado de tablas
	def creaTable(self, fileName, tableName):
		with open(fileName, 'r') as myFile:
			reader = csv.reader(myFile, delimiter=',',  quotechar='"');
			for row in reader:
				if(len(row)<3):
					continue;
				else:
					if(row[0]=="Fecha y hora oficial"):
						self.cursor.execute("CREATE TABLE IF NOT EXISTS `"+tableName+"` (Fecha DATETIME PRIMARY KEY, Temperatura FLOAT, Viento int, Direccion varchar(255), Racha int, DirRacha varchar(255), Precipitaciones float, Presion float, Humedad int)");

		self.db.commit();


	
	#Función de inserción de todos los datos
	def formatInsert(self, fileName, tableName):
		with open(fileName, 'r') as myFile:
			reader = csv.reader(myFile, delimiter=',',  quotechar='"');
			datos = False;
			query = "";
			for row in reader:
				if(len(row)<3):
					continue;
				elif(datos == False):
					if(row[0]=="Fecha y hora oficial"):
						datos = True;
				else:
					query = "REPLACE INTO `"+tableName+"` (Fecha, Temperatura, Viento, Direccion, Racha, DirRacha, Precipitaciones, Presion, Humedad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)";
					values = (toDate(row[0]), casting(row[1],'float'), casting(row[2], 'int'), casting(row[3], 'str'), casting(row[4], 'int'), casting(row[5], 'str') , casting(row[6], 'float'), casting(row[7], 'float'), casting(row[9], 'float'));

					self.cursor.execute(query, values);
		self.db.commit();


	
	#Funión de borrado de datos
	def borrarTodosDatos(self, tablas):
		for tab in tablas:
			self.cursor.execute("TRUNCATE TABLE "+tab);

		self.db.commit();
		print("Los datos de todas las tablas han sido borrados");


	#Función de borrado de tablas
	def borrarTablas(self, tablas):
		for tab in tablas:
			self.cursor.execute("DROP TABLE "+tab);

		self.db.commit();
		print("Todas las tablas han sido borradas");


#Conversión a tipo datetime del primer campo de los ficheros
def toDate(a):
	day = a[0:2];
	month = a[3:5];
	year = a[6:10];
	hour = a[11:13];
	minute = a[14:16];
	return datetime(int(year), int(month), int(day), int(hour), int(minute));


#Casting de los valores para insertarlos correctamente
def casting(value, tipo):
	if(type(value)==str and tipo=="int"):
		try:
			int(value);
		except:
			return None;

	elif(type(value)==str and tipo=="float" and value != ''):
		try:
			float(value);
		except:
			return None;

	elif(type(value)==str and tipo=="str" and value != ''):
		try:
			str(value);
		except:
			return None;

	elif(type(value)==str and value==''):
		return None;

	elif(type(value)==str and value==unknown):
		return None;

	return value;