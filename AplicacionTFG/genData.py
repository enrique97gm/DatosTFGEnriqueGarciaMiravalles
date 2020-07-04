#encoding: utf-8
#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

mainColor = '#186DDA';
secondaryColor = '#00AEFF';
thirdColor = '#50A0E7';

class GenData():
    
    #Inicialización
    def __init__(self, container):
        self.genDataContainer = Frame(container, bg='white');
        self.filtersContainer = Frame(self.genDataContainer, bg = 'white');
        self.desdeE = Entry(self.filtersContainer,font=('Helvetica 12'), width = 15);
        self.hastaE = Entry(self.filtersContainer,font=('Helvetica 12'), width = 15);
        self.start = StringVar();
        self.finish = StringVar();
        self.textResult = StringVar();
        self.dataContainer = Frame(self.genDataContainer, bg = 'white');
        self.table = Frame(self.dataContainer, bg = 'white');
        self.buttonFilterData = Button(self.filtersContainer, text="Filtrar", cursor = 'hand2');
 
    #Muestra la vista de datos generales
    def showGenData(self):
        self.genDataContainer.grid(row = 0, column = 0, sticky = 'NESW');
        self.genDataContainer.grid_columnconfigure(0, weight = 1);
        self.genDataContainer.grid_rowconfigure(1, weight = 1);

    #Esconde la vista de datos genrales
    def hideGenData(self):
        self.genDataContainer.grid_forget();

    #Completa la vista de datso generales
    def complete(self, estData):
        self.estData = estData;
        #Pestaña de datos generales
        #Filtros de fechas
        self.filtersContainer.grid(row=0, column=0, sticky="NESW");
        self.filtersContainer.grid_columnconfigure(0, weight = 1);
        
        #Etiqueta desde
        desde = Label(self.filtersContainer, text='Desde:');
        desde.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        desde.grid(row=0, column=0, pady=(20,10), padx=(0, 0), sticky='E');
        desde.grid_columnconfigure(0, weight = 1);
        #Entry desde
        self.desdeE.grid(row=0, column=1, pady=(20,10), padx=(2,20), sticky='NESW');

        #Etiqueta hasta
        hasta = Label(self.filtersContainer, text='Hasta:');
        hasta.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        hasta.grid(row=0, column=2, pady=(20,10), sticky='NESW');
        #Entry hasta
        self.hastaE.grid(row=0, column=3, pady=(20,10), padx=(2,20), sticky='NESW');

        #Errores en fechas
        dateError = Label(self.filtersContainer, textvariable = self.textResult);
        dateError.config(fg='red',bg='white',font=('Comic Sans', 11, 'bold'));
        dateError.grid(row=1, column=0, columnspan=4, sticky='E');

        infoContainerGenData = Frame(self.filtersContainer, bg = 'white');
        infoContainerGenData.grid(row=2, column=0, columnspan= 5, sticky="NESW");
        infoContainerGenData.grid_columnconfigure(0, weight = 1);
        infoContainerGenData.grid_columnconfigure(3, weight = 1);

        #Comienzo
        infoIni = Label(infoContainerGenData, text='Datos generales obtenidos entre las fechas ');
        infoIni.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        infoIni.grid(row=0, column=0, pady=(10,10), sticky='E');
        #start
        st = Label(infoContainerGenData, textvariable= self.start);
        st.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        st.grid(row=0, column=1, pady=(10,10), sticky='NESW');
        #Comienzo
        until = Label(infoContainerGenData, text=' y ');
        until.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        until.grid(row=0, column=2, pady=(10,10), sticky='NESW');
        #Finish
        finish = StringVar();
        fin = Label(infoContainerGenData, textvariable= self.finish);
        fin.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        fin.grid(row=0, column=3, pady=(10,10), sticky='W');

        #Contenedor de la tabla
        self.dataContainer.grid(row=1, column=0, sticky="NESW");
        self.dataContainer.grid_rowconfigure(0, weight = 1);
        self.dataContainer.grid_columnconfigure(0, weight = 1);

        #Tabla resumen
        self.table.grid(row=0, column=0, padx=(25,25), sticky="NESW");

        i = 1;
        rowLabels = ['T. Máxima (°C)', 'T. Media (°C)', 'T. Mínima (°C)', 'Viento medio (Km/h)', 'Dir. pred', 'Racha máxima (km/h)', 'Dir. racha máxima', 'Prec. totales (mm)', 'Prec. máximas (mm)', 'Prec. medias (mm)', 'Presión media (hPa)', 'Humedad media (%)'];
        for label in rowLabels:
            label = Label(self.table, text=label, wraplength=90);
            label.config(fg='black', bg=secondaryColor, font='-weight bold', borderwidth=2, relief='solid');
            label.grid(row=0, column=i, ipady=5, ipadx=5, sticky='NESW');
            self.table.grid_columnconfigure(i, weight = 1);
            i = i +1;

        i = 1;
        for estacion in estData:
            estacion = Label(self.table, text=estacion,  wraplength= 90);
            estacion.config(fg='black', bg=secondaryColor, font='-weight bold', borderwidth=2, relief='solid');
            estacion.grid(row=i, column=0, ipady=10, sticky='NESW');
            i = i +1;
            

        #Botón para filtrar los datos por fechas y mostrar los resultados
        self.buttonFilterData.grid(row=0, column=5, pady=(20,10), padx=(0, 25), sticky='NESW');


    #Completa los datos de la tabla
    def changeTableValues(self, estaciones):
        if(self.textResult.get() == ''):
            j = 1;
            for estacion in estaciones:
                for i in range(len(estaciones[estacion])):
                    labName = estacion + str(i);
                    if(estaciones[estacion][i] == None or estaciones[estacion][i] == ''):
                        estaciones[estacion][i] = 'Sin datos';
                    labName = Label(self.table, text = estaciones[estacion][i], wraplength = 90);
                    labName.config(fg='black', bg='white', borderwidth=1.5, relief='solid');
                    labName.grid(row=j, column=i+1, ipady=10, ipadx=5, sticky='NESW');
                    self.table.grid_columnconfigure(i+1, weight = 1);
                j = j + 1;
        
        else:
            j = 1;
            for estacion in estaciones:
                for i in range(len(estaciones[estacion])):
                    labName = Label(self.table, text = 'Sin datos', wraplength = 90);
                    labName.config(fg='black', bg='white', borderwidth=1.5, relief='solid');
                    labName.grid(row=j, column=i+1, ipady=10, ipadx=5, sticky='NESW');
                    self.table.grid_columnconfigure(i+1, weight = 1);
                j = j + 1;