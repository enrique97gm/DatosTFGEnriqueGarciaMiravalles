#encoding: utf-8
#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

#Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Graphs():

    #Inicialización
    def __init__(self, container):
        self.graphContainer = Frame(container, bg='white');
        self.gContainer = Frame(self.graphContainer, bg = 'white');
        self.filtersGraph = Frame(self.graphContainer, bg = 'white');
        self.textGraphResult = StringVar();
        self.localization = StringVar();
        self.atr = StringVar();
        self.dgEntry = Entry(self.filtersGraph,font=('Helvetica 12'), width = 15);
        self.hgEntry = Entry(self.filtersGraph,font=('Helvetica 12'), width = 15);
        self.buttonGetGraph = Button(self.filtersGraph, text="Filtrar", cursor = 'hand2');
        
    #Muestra la pestaña de gráfico
    def showGraphs(self):
        self.graphContainer.grid(row = 0, column = 0, sticky = 'NESW');
        self.graphContainer.grid_columnconfigure(0, weight = 1);
        self.graphContainer.grid_rowconfigure(1, weight = 1);

    #Esconde la pestaña de gráficos
    def hideGraphs(self):
        self.graphContainer.grid_forget();

    #Completa la pestaña
    def complete(self, estData):
        self.estData = estData;
        #Contenedor de filtros
        self.filtersGraph.grid(row=0, column=0, sticky="NESW");
        self.filtersGraph.grid_columnconfigure(0, weight = 1);

        #Etiqueta localización
        where = Label(self.filtersGraph, text='Localización:');
        where.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        where.grid(row=0, column=0, pady=(20,10), padx=(20, 0), sticky='E');
        where.grid_columnconfigure(0, weight = 1);

        def getUpdateData(self):
            var['values'] = estData[stations.get()];
    
        #Etiqueta variable
        selectVariable = Label(self.filtersGraph, text='Variable: ');
        selectVariable.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        selectVariable.grid(row=0, column=2, pady=(20,10), sticky='NESW');
        #Selector variable
        self.atr.set('Temperatura');
        var = ttk.Combobox(self.filtersGraph, font=('Helvetica 12'), width = 18);
        var.config(textvariable = self.atr);
        var.grid(row=0, column=3, pady=(20,10), padx=(2,20), sticky='NESW');

        #Selector localización
        estaciones = [];
        for est in estData:
            estaciones.append(est);
        self.localization.set('Valladolid');
        stations = ttk.Combobox(self.filtersGraph, font=('Helvetica 12'), width = 18);
        stations.config(textvariable = self.localization);
        stations['values'] = estaciones;
        stations.bind('<<ComboboxSelected>>', getUpdateData);
        stations.grid(row=0, column=1, pady=(20,10), padx=(2,20), sticky='NESW');

        #Etiqueta desde
        desdeGraph = Label(self.filtersGraph, text='Desde:');
        desdeGraph.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        desdeGraph.grid(row=0, column=4, pady=(20,10), sticky='NESW');
        #Entry desde
        self.dgEntry.grid(row=0, column=5, pady=(20,10), padx=(2,20), sticky='NESW');

        #Etiqueta hasta
        hastaGraph = Label(self.filtersGraph, text='Hasta:');
        hastaGraph.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        hastaGraph.grid(row=0, column=6, pady=(20,10), sticky='NESW');
        #Entry hasta
        self.hgEntry.grid(row=0, column=7, pady=(20,10), padx=(2,20), sticky='NESW');

        #Errores en fechas
        graphError = Label(self.filtersGraph, textvariable = self.textGraphResult);
        graphError.config(fg='red',bg='white',font=('Comic Sans', 11, 'bold'));
        graphError.grid(row=1, column=0, columnspan=8, sticky='E');

        #Contenedor de los graficos y el toolbar
        self.gContainer.grid(row=1, column=0, sticky="NESW");
        self.gContainer.grid_columnconfigure(0, weight = 1);
        self.gContainer.grid_rowconfigure(0, weight = 1);

        #Botón para filtrar los datos por fechas y mostrar los resultados
        self.buttonGetGraph.grid(row=0, column=8, pady=(20,10), padx=(0, 25), sticky='NESW');

    #Crea el gráfico
    def newGraph(self, figure):
        graph = Frame(self.gContainer, bg='white');
        graph.grid(row=0, column=0, pady=(0,20), sticky='NESW');
        canvas = FigureCanvasTkAgg(figure, graph);
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True);
        toolbar_frame = Frame(self.gContainer);
        toolbar_frame.grid(row=1, column=0, sticky='EW');
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame);
        toolbar.pack(side=TOP, fill=BOTH, expand=True)
        toolbar.update();
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True);

    
