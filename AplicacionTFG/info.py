
#encoding: utf-8
#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

#importamos variables y funciones del sistema
import os

#Para imagenes
from PIL import ImageTk,Image

class Info():
    
    #Inicialización
    def __init__(self, container):
        self.infoContainer = Frame(container, bg='white');
        self.complete();

    def showInfo(self):
        self.infoContainer.grid(row = 0, column = 0, sticky = 'NESW');
        self.infoContainer.grid_columnconfigure(0, weight = 1);
        self.infoContainer.grid_rowconfigure(1, weight = 1);

    def hideInfo(self):
        self.infoContainer.grid_forget();


    def complete(self):
        #Pestaña de informacion
        #Comtenedor de imágenes
        imageFrame = Frame(self.infoContainer, bg = 'white');
        imageFrame.grid(row=0, column=0, sticky = 'NESW');
        imageFrame.columnconfigure(0, weight = 1);
        imageFrame.columnconfigure(1, weight = 1);
        imageFrame.columnconfigure(2, weight = 1);

        #Imágenes
        images = [];
        img3 = Image.open(os.path.abspath('.')+'/Activos/escudo_uva.png').resize((100, 100));
        logUva = ImageTk.PhotoImage(img3);
        images.append(logUva);

        img4 = Image.open(os.path.abspath('.')+'/Activos/inf_logo.png').resize((100, 100));
        logInf = ImageTk.PhotoImage(img4);
        images.append(logInf);

        img5 = Image.open(os.path.abspath('.')+'/Activos/aemet_logo.jpg').resize((100, 100));
        logAemet = ImageTk.PhotoImage(img5);
        images.append(logAemet);
        for i in range(len(images)):
            label = Label(imageFrame, bg='white', image = images[i]);
            label.image = images[i];
            label.grid(row = 0, column = i, pady=10, sticky = 'NESW');

        #Contenedor de la información para mantener margenes
        infoCenterContainer = Frame(self.infoContainer, bg='white');
        infoCenterContainer.grid(row=1, column=0, padx=50, pady=(0,20), sticky='NESW');

        #Etiqueta comienzo
        stInfo = Label(infoCenterContainer, text='La presente herramienta permite mostrar datos generales en diversos formatos o la realización de predicciones meteorológicas, en concreto sobre la temperatura máxima diaria mediante modelos estadísticos.');
        stInfo.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        stInfo.grid(row=0, column=0, pady=(0, 10), sticky='NESW');
        #Más datos
        secInfo = Label(infoCenterContainer, text='Los  datos  meteorológicos se  obtienen de la  herramienta  externa de  almacenamiento con la que se ha realizado previamente la conexión. A su vez estos datos fuerón adquiridos previamente, para su almacenamiento, de la Agencia Estatal de Meteorología (AEMET).');
        secInfo.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        secInfo.grid(row=1, column=0, pady=(0, 10), sticky='NESW');

        #Info pestañas
        totalAreas = Label(infoCenterContainer, text='En la presente herramienta podemos distinguir 4 pestañas con las que interactuar:');
        totalAreas.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        totalAreas.grid(row=2, column=0, pady=(0, 10), sticky='NESW');

        #Info negrita
        infNeg = Label(infoCenterContainer, text='-Pestaña de información: ');
        infNeg.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10, 'bold'),
                        justify = LEFT,
                        );
        infNeg.grid(row=3, column=0, pady=(0, 0), sticky='W');

        #Info pestañas
        infLab = Label(infoCenterContainer, text='Pestaña actual, donde se puede consultar el funcionamiento de la apliación en global.');
        infLab.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        infLab.grid(row=4, column=0, pady=(0, 10), sticky='W');

        #Datos generales negrita
        datGenNeg = Label(infoCenterContainer, text='-Pestaña de datos generales: ');
        datGenNeg.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10, 'bold'),
                        justify = LEFT,
                        );
        datGenNeg.grid(row=5, column=0, pady=(0, 0), sticky='W');

        #Dtos generales info
        datGenLab = Label(infoCenterContainer, text='Se muestra un resumen de los datos meteorológicos para cada una de las localizaciones usadas en el estudio, permitiendo filtrar el conjunto de datos sobre el que realizar las operaciones mediante un rango de fechas que deberán registrarse con el formato "AAAA-MM-DD".');
        datGenLab.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        datGenLab.grid(row=6, column=0, pady=(0, 10), sticky='W');

        #Predicciones negrita
        predNeg = Label(infoCenterContainer, text='-Pestaña de predicciones: ');
        predNeg.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10, 'bold'),
                        justify = LEFT,
                        );
        predNeg.grid(row=7, column=0, pady=(0, 0), sticky='NW');

        #Predicciones info
        predLab = Label(infoCenterContainer, text='En esta  sección se  pueden realizar  predicciones de  temperaturas máximas  para  una localización concreta  a elegir, mediante la creación de diferentes modelos estadísticos  que usarán  como variables de  entrada para realizar  la predicción  de la temperatura  otras variables meteorológicas,  los días  que  se usarán  como referencia, el número de ejemplos que harán falta para realizar el modelo o las variables propias del modelo elegido. A mayores se podrá visualizar un histórico de predicciones con la configuración escogida para la predicción.');
        predLab.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        predLab.grid(row=8, column=0, pady=(0, 10), sticky='W');

        #Graficos negrita
        grafNeg = Label(infoCenterContainer, text='-Pestaña de gráficos: ');
        grafNeg.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10, 'bold'),
                        justify = LEFT,
                        );
        grafNeg.grid(row=9, column=0, pady=(0, 0), sticky='NW');

        #Graficos info
        grafLab = Label(infoCenterContainer, text='Se muestran diferentes gráficas filtrando por la localización, la variable a mostrar y el rango de fechas sobre el que realizar la gráfica. Las fechas al igual que en la pestaña de datos generales deberá seguir el formato "AAAA-MM-DD".');
        grafLab.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        grafLab.grid(row=10, column=0, pady=(0, 10), sticky='W');

        #Info botón de desconexion
        descButtonLab = Label(infoCenterContainer, text='En la parte  inferior del  "side bar" donde se  encentra el selector de pestañas, podemos encontrar el botón de desconexión que nos permite desconectar de la base de datos actual para configurar una nueva conexión.');
        descButtonLab.config(fg='black',
                        bg='white',
                        font=('Comic Sans', 10),
                        justify = LEFT,
                        anchor = 'w',
                        wraplength = 1070
                        );
        descButtonLab.grid(row=11, column=0, pady=(0, 10), sticky='W');
