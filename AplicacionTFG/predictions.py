#encoding: utf-8
#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

#Modulo datetime
from datetime import datetime, timedelta

#importamos variables y funciones del sistema
import os

#Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

mainColor = '#186DDA';
secondaryColor = '#00AEFF';
thirdColor = '#50A0E7';

#-----------------------Clase predicciones-------------------#
class Predictions():

    #Inicialización
    def __init__(self, container):
        self.predContainer = Frame(container, bg='white');
        self.predictionDataContainer = Frame(self.predContainer, bg = 'white');
        self.resultPredContainer = Frame(self.predictionDataContainer, bg = 'white');
        self.buttonForecast = Button(self.resultPredContainer, text="Mostrar predicción", cursor = 'hand2');
        self.butHistForecast = Button(self.resultPredContainer, text="Histórico predicciones", cursor = 'hand2');
        self.dayContainer = Frame(self.predictionDataContainer, bg='white');
        self.iterContainer = Frame(self.predictionDataContainer, bg='white');

    def showPredictions(self):
        self.predContainer.grid(row = 0, column = 0, sticky = 'NESW');
        self.predContainer.grid_columnconfigure(0, weight = 1);
        self.predContainer.grid_rowconfigure(1, weight = 1);

    def hidePredictions(self):
        self.predContainer.grid_forget();


    #Ventana de prediccion
    def complete(self, estData):
        self.locVar = estData;
        #Contenedor de filtros
        headerPred = Frame(self.predContainer, bg = 'white');
        headerPred.grid(row=0, column=0, sticky="NESW");
        headerPred.grid_columnconfigure(0, weight = 1);

        #Titulo de la seccion
        date = datetime.now();
        if(date < datetime(date.year, date.month, date.day, 18, 15, 00)):
            date = date.strftime("%d-%m-%Y");
        else:
            date = datetime(date.year,date.month,date.day+1).strftime("%d-%m-%Y");

        titlePred = Label(headerPred, text='Predicción de la temperatura máxima para el día ' + date);
        titlePred.config(fg='black', bg='white', font=('Comic Sans', 14, 'bold'));
        titlePred.grid(row=0, column=0, pady=(30,10), padx=(25), sticky='W');

        #Prediccion container
        self.predictionDataContainer.grid(row=1, column=0, sticky="NESW");
        self.predictionDataContainer.grid_columnconfigure(0, weight = 1);
        self.predictionDataContainer.grid_columnconfigure(1, weight = 1);
        self.predictionDataContainer.grid_columnconfigure(2, weight = 1);
        self.predictionDataContainer.grid_columnconfigure(3, weight = 1);
        self.predictionDataContainer.grid_columnconfigure(4, weight = 1);

        #Contenedor localizaciones
        self.locContainer = Frame(self.predictionDataContainer, bg='white');
        self.locContainer.grid(row = 0, column = 0, padx= (25,0), pady=(10,0), sticky="NESW");

        #Contenedor variables
        varContainer = Frame(self.predictionDataContainer, bg='white');
        varContainer.grid(row = 0, column = 1, pady=(10,0), sticky="NESW");

        #Contenedor modelos
        modContainer = Frame(self.predictionDataContainer, bg='white');
        modContainer.grid(row = 0, column = 2, pady=(10,0), sticky="NESW");

        #Contenedor dias
        self.dayContainer.grid(row = 0, column = 3, pady=(10,0), sticky="NESW");

        #Contenedor iteraciones
        self.iterContainer.grid(row = 0, column = 4, padx= (0, 25), pady=(10,0), sticky="NESW");

        #Etiqueta localizacion
        self.local = Label(self.locContainer, text='Localizaciones');
        self.local.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        self.local.grid(row=0, column=0, pady=(10,5), sticky='NESW');

        #Etiqueta variables
        v = Label(varContainer, text='Variables');
        v.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        v.grid(row=0, column=0, pady=(10,5), sticky='NESW');

        #Etiqueta modelos
        model = Label(modContainer, text='Algoritmos de predicción');
        model.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        model.grid(row=0, column=0, pady=(10,5), sticky='NESW');

        #Etiqueta days
        da = Label(self.dayContainer, text='Días como referencia');
        da.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        da.grid(row=0, column=0, pady=(10,5), sticky='NESW');

        #Etiqueta iteraciones
        it = Label(self.iterContainer, text='Nº de ejemplos para crear el modelo');
        it.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        it.grid(row=0, column=0, pady=(10,5), sticky='NESW');

        self.t = IntVar();
        self.w = IntVar();
        self.d = IntVar();
        self.p = IntVar();
        self.h = IntVar();
        temperature = Checkbutton(varContainer, highlightthickness=0, relief="flat", activebackground='white', text='Temperatura', variable = self.t, bg='white')
        temperature.grid(row=1, column = 0, pady=(0,5), sticky='W');
        wind = Checkbutton(varContainer, highlightthickness=0, relief="flat", activebackground='white', text='Viento', variable = self.w, bg='white')
        wind.grid(row=2, column = 0, pady=(0,5), sticky='W');
        dir = Checkbutton(varContainer, highlightthickness=0, relief="flat", activebackground='white', text='Dirección', variable = self.d, bg='white')
        dir.grid(row=3, column = 0, pady=(0,5), sticky='W');
        pres = Checkbutton(varContainer, highlightthickness=0, relief="flat", activebackground='white', text='Presión', variable = self.p, bg='white')
        pres.grid(row=4, column = 0, pady=(0,5), sticky='W');
        hum = Checkbutton(varContainer, highlightthickness=0, relief="flat", activebackground='white', text='Humedad', variable = self.h, bg='white')
        hum.grid(row=5, column = 0, pady=(0,5), sticky='W');

        def setVariables():
            self.butHistForecast.grid_forget();
            self.resultPredContainer.grid_columnconfigure(2, weight = 0);
            self.predErr.set('');
            self.predResult.set('');
            self.textForecast.set('');
            temperature.grid_forget();
            self.t.set(0);
            wind.grid_forget();
            self.w.set(0);
            dir.grid_forget();
            self.d.set(0);
            pres.grid_forget();
            self.p.set(0);
            hum.grid_forget();
            self.h.set(0);
            i = 1;
            for var in self.locVar[self.loc.get()]:
                if(var == 'Temperatura'):
                    temperature.grid(row=i, column=0, pady=(0,5), sticky='W');
                elif(var == 'Viento'):
                    wind.grid(row=i, column=0, pady=(0,5), sticky='W');
                elif(var == 'Dirección'):
                    dir.grid(row=i, column=0, pady=(0,5), sticky='W');
                elif(var == 'Presión'):
                    pres.grid(row=i, column=0, pady=(0,5), sticky='W');
                elif(var == 'Humedad'):
                    hum.grid(row=i, column=0, pady=(0,5), sticky='W');
                i = i+1;

        self.loc = StringVar();
        self.loc.set(None);
        i = 1;
        for est in self.locVar:
            Radiobutton(self.locContainer, bg='white', highlightthickness=0, relief="flat", activebackground='white', text = est, variable=self.loc, value =  est, command= lambda: setVariables()).grid(row=i, column = 0, pady=(0,5), sticky='W');
            i +=1;

        self.mod = StringVar();
        self.mod.set(None);
        models = ['Regresión lineal', 'Árbol de decisión', 'K-NN', 'Red neuronal'];
        num = 1;
        for m in models:
            Radiobutton(modContainer, bg='white', highlightthickness=0, relief="flat", activebackground='white', text = m, variable = self.mod, value = m, command= lambda: modelVariables()).grid(row=num, column = 0, pady=(0,5), sticky='W');
            num = num + 1;
        
        #Seleccion del numero de vecinos
        knnFra = Frame(modContainer, bg='white');
        labelNeighbours = Label(knnFra, text='Número de vecinos');
        labelNeighbours.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        labelNeighbours.grid(row=0, column=0, pady=(10,5), sticky ='NESW');
        self.neighbors = Scale(knnFra, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=1, to=5);
        self.neighbors.grid(row=1, column = 0, sticky='NESW');

        #Seleccion del maxima profundidad arbol decision
        arbFra = Frame(modContainer, bg='white');
        labelMaxDepth = Label(arbFra, text='Profundidad máxima\n (0 igual a "Sin definir")');
        labelMaxDepth.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        labelMaxDepth.grid(row=0, column=0, pady=(10,5), sticky ='NESW');
        self.maxDepth = Scale(arbFra, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=0, to=20);
        self.maxDepth.grid(row=1, column = 0, sticky='NESW');

        #Seleccion del numero de capas y neuronas por capa
        redNeuFra1 = Frame(varContainer, bg='white');
        redNeuFra2 = Frame(modContainer, bg='white');
        labelLayers = Label(redNeuFra1, text='Número de capas');
        labelLayers.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        labelLayers.grid(row=0, column=0, pady=(5,5), sticky ='NESW');
        self.layers = IntVar();
        self.layers.set(1);
        rdButNeuFra = Frame(redNeuFra1, bg='white');
        rdButNeuFra.grid(row = 1, column = 0, sticky = 'NESW');
        rdButNeuFra.columnconfigure(0, weight =1);
        rdButNeuFra.columnconfigure(1, weight =1);
        rdButNeuFra.columnconfigure(2, weight =1);
        Radiobutton(rdButNeuFra, bg='white', highlightthickness=0, relief="flat", activebackground='white', text ='1', variable=self.layers, value = 1, command= lambda: setNeurons()).grid(row=0, column = 0, pady=(0,5), sticky='W');
        Radiobutton(rdButNeuFra, bg='white', highlightthickness=0, relief="flat", activebackground='white', text ='2', variable=self.layers, value = 2, command= lambda: setNeurons()).grid(row=0, column = 1, pady=(0,5), sticky='W');
        Radiobutton(rdButNeuFra, bg='white', highlightthickness=0, relief="flat", activebackground='white', text ='3', variable=self.layers, value = 3, command= lambda: setNeurons()).grid(row=0, column = 2, pady=(0,5), sticky='W');
        labelNeurons = Label(redNeuFra1, text='Neuronas por capa');
        labelNeurons.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        self.neurons1 = Scale(redNeuFra1, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=1, to=10);
        self.neurons1.grid(row=3, column = 0, sticky='NESW');
        self.neurons2 = Scale(redNeuFra1, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=1, to=10);
        self.neurons3 = Scale(redNeuFra1, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=1, to=10);
        iterLab = Label(redNeuFra2, text='Número de iteraciones');
        iterLab.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        iterLab.grid(row=0, column=0, pady=(5,5), sticky ='NESW');
        self.itersRedNeu = Scale(redNeuFra2, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, orient='horizontal', relief='raised', from_=1, to=1000);
        self.itersRedNeu.grid(row=1, column = 0, sticky='NESW');
        learn = Label(redNeuFra2, text='Constante de aprendizaje');
        learn.config(fg='black', bg='white', font=('Comic Sans', 12, 'bold'));
        learn.grid(row=2, column=0, pady=(10,5), sticky ='NESW');
        self.learnRate = Scale(redNeuFra2, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', resolution=-1, activebackground=secondaryColor, orient='horizontal', relief='raised', from_=0.001, to=1);
        self.learnRate.grid(row=3, column = 0, sticky='NESW');


        #Asigna las escalas al frame dependiendo de las capas
        def setNeurons():
            labelNeurons.grid(row=2, column=0, pady=(5,5), sticky ='NESW');
            self.neurons1.grid_forget();
            self.neurons2.grid_forget();
            self.neurons3.grid_forget();
            if(self.layers.get() == 1):
                self.neurons1.grid(row=3, column = 0, sticky='NESW');
            elif(self.layers.get() == 2):
                self.neurons1.grid(row=3, column = 0, sticky='NESW');
                self.neurons2.grid(row=4, column = 0, sticky='NESW');
            else:
                self.neurons1.grid(row=3, column = 0, sticky='NESW');
                self.neurons2.grid(row=4, column = 0, sticky='NESW');
                self.neurons3.grid(row=5, column = 0, sticky='NESW');


        def forgetGrid():
            knnFra.grid_forget();
            redNeuFra1.grid_forget();
            redNeuFra2.grid_forget();
            arbFra.grid_forget();
            self.butHistForecast.grid_forget();
            self.resultPredContainer.grid_columnconfigure(2, weight = 0);
            self.predErr.set('');
            self.predResult.set('');
            self.textForecast.set('');

        def modelVariables():
            if(self.mod.get() == 'Árbol de decisión'):
                forgetGrid();
                arbFra.grid(row=6, column=0, sticky='NESW');
            elif(self.mod.get() == 'K-NN'):
                forgetGrid()
                knnFra.grid(row=6, column=0, sticky='NESW');
            elif(self.mod.get() == 'Red neuronal'):
                forgetGrid();
                redNeuFra1.grid(row=6, column=0, columnspan = 2, sticky='NESW');
                redNeuFra2.grid(row=6, column=0, columnspan = 2, sticky='NESW');
            else:
                forgetGrid();


        self.dayRef = Scale(self.dayContainer, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, length=250, relief='raised', from_=1, to=20);
        self.dayRef.grid(row=1, column = 0, pady=(0,5), sticky='N');
        self.iter = Scale(self.iterContainer, highlightthickness=1, bg=thirdColor, fg='black', troughcolor='white', activebackground=secondaryColor, length=250, relief='raised', from_=1, to=20);
        self.iter.grid(row=1, column = 0, pady=(0,5), sticky='N');
                        

        #Contenedor con el resultado de error y el boton y valor de la prediccion
        self.resultPredContainer.grid(row = 1, column = 0, columnspan = 5, sticky = 'NESW');
        self.resultPredContainer.grid_columnconfigure(0, weight = 1);
        self.resultPredContainer.grid_columnconfigure(1, weight = 1);

        #Errores en fechas
        self.predErr = StringVar();
        predErrors = Label(self.resultPredContainer, textvariable = self.predErr);
        predErrors.config(fg='red',bg='white',font=('Comic Sans', 11, 'bold'));
        predErrors.grid(row=0, column=0, pady=(10,10), columnspan = 3, sticky='NESW');

        #Resultado de la predicción
        self.predResult = StringVar();
        result = Entry(self.resultPredContainer,font=('Helvetica 16'), width = 20, textvariable = self.predResult);
        result.grid(row=1, column=1, ipady=(5), padx=(0,20), sticky='W');

        #Boton de prediccion
        self.buttonForecast.config(highlightthickness=0, relief="flat", bg=secondaryColor, fg='white', font=('Comic Sans', 16, 'bold'), activebackground=thirdColor, activeforegroun='white');
        self.buttonForecast.grid(row=1, column=0, padx=(20,0), sticky='E');
        #Boton de historico
        self.butHistForecast.config(highlightthickness=0, relief="flat", bg=secondaryColor, fg='white', font=('Comic Sans', 16, 'bold'), activebackground=thirdColor, activeforegroun='white');

        #Texto con resultado
        self.textForecast = StringVar();
        forecastResult = Label(self.resultPredContainer, textvariable = self.textForecast);
        forecastResult.config(bg='white',font=('Comic Sans', 12, 'bold'));
        forecastResult.grid(row=2, column=0, pady=(20,0), columnspan = 3, sticky='NESW');
        

    #Muestra la predicción
    def showPrediction(self, pred):
        if(pred == None):
            self.predErr.set('No se ha podido realizar una predicción debido a que alguno de los datos meteorológicos usados para crear el modelo no existe');
        else:
            date = datetime.now();
            if(date < datetime(date.year, date.month, date.day, 18, 15, 00)):
                date = date.strftime("%d-%m-%Y");
            else:
                date = datetime(date.year,date.month,date.day+1).strftime("%d-%m-%Y");
            self.predResult.set(str(round(pred[0], 5)) + ' °C');
            self.textForecast.set('Se espera una temperatura máxima de ' + self.predResult.get() + ' en ' + self.loc.get() + ' para el día ' + date);
            self.resultPredContainer.grid_columnconfigure(2, weight = 1);
            self.butHistForecast.grid(row=1, column=2, padx=(0,0), sticky='W');

    
    #Muestra el historico
    def showHist(self, figure):
        self.windowGraph = Tk();
        self.windowGraph.title('Histótico de predicciones');
        self.windowGraph.iconbitmap('@'+os.path.abspath('.')+'/Activos/term.xbm')
        self.windowGraph.columnconfigure(0, weight = 1);
        self.windowGraph.rowconfigure(0, weight = 1);
        self.setGraph(figure);
        self.windowGraph.mainloop();
        
        

    #Establece la figura y toolbar en la nueva ventana
    def setGraph(self, figure):
        graph = Frame(self.windowGraph, bg='white');
        graph.grid(row=0, column=0, sticky='NESW');
        canvas = FigureCanvasTkAgg(figure, graph);
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1);
        toolbar_frame = Frame(self.windowGraph);
        toolbar_frame.grid(row=1, column=0, sticky='EW');
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame);
        toolbar.pack(side=BOTTOM, fill=BOTH, expand=1)
        toolbar.update();
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1);
    