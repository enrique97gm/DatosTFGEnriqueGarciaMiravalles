#encoding: utf-8
from genData import GenData
from model import BD, Functions
from graphs import Graphs
from predictions import Predictions
from info import Info
from window import Window

#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

#Modulo datetime
from datetime import datetime, timedelta

#importamos variables y funciones del sistema
import os

#-------------------------------Variables globales---------------------------------#

mainColor = '#186DDA';
secondaryColor = '#00AEFF';
thirdColor = '#50A0E7';

global db;

connectionData = {
    'hostDir': '',
    'serverUser': '',
    'userPassword': '',
    'databaseName': '',
    'port': '',
}

#-------------------------- Clase aplicacion-----------------------------#
class Aplicacion():
    
    #Inicialización
    def __init__(self):
        self.window=Tk();
        self.window.protocol("WM_DELETE_WINDOW", self.finishApp);
        self.window.title('Herramienta de prueba para la predicción');
        ico = PhotoImage(file=os.path.abspath('.')+'/Activos/term.png')
        self.window.call('wm', 'iconphoto', self.window._w, ico)
        self.window.config(bg=mainColor);
        self.window.attributes("-zoomed", False);
        self.window.minsize(width = 300, height = 300);

        #Peso 100% en self.window
        self.window.grid_rowconfigure(0, weight = 1);
        self.window.grid_columnconfigure(0, weight = 1);

        #Ventana principal fija sin ajuste de tamaño
        self.window.resizable(False,False);

        #Centrar ventana en función de las dimendsiones del contenedor de inicio
        self.center(450, 490);

        self.view = Window(self.window);
        self.functions = Functions();

        self.infoW = Info(self.view.dataContainer);
        self.genDataW = GenData(self.view.dataContainer);
        self.predW = Predictions(self.view.dataContainer);
        self.graphsW = Graphs(self.view.dataContainer);

        #Botones de las acciones del usuario
        self.view.buttonDisconnect.bind("<Button>", self.disconnect);
        self.view.buttonToBD.bind("<Button>", self.changeToConnect);
        self.view.buttonConnect.bind("<Button>", self.checkConnection);
        self.view.infoButton.bind("<Button>", lambda event: self.switchSelector(self.view.predButton, self.view.graphButton, self.view.genDataButton, self.view.infoButton,1));
        self.view.genDataButton.bind("<Button>", lambda event: self.switchSelector(self.view.infoButton, self.view.predButton, self.view.graphButton, self.view.genDataButton,2));
        self.view.predButton.bind("<Button>", lambda event: self.switchSelector(self.view.infoButton, self.view.graphButton, self.view.genDataButton, self.view.predButton,3));
        self.view.graphButton.bind("<Button>", lambda event: self.switchSelector(self.view.infoButton, self.view.genDataButton, self.view.predButton, self.view.graphButton,4));
        self.genDataW.buttonFilterData.bind("<Button>", lambda event: self.getNewGenData());
        self.graphsW.buttonGetGraph.bind("<Button>", lambda event: self.getGraphsData());
        self.predW.buttonForecast.bind("<Button>", self.getForecast);
        self.predW.butHistForecast.bind("<Button>", self.getHistForecast);

        #Ventana principal actualizaciones
        self.window.mainloop();

    #Centra la ventana
    def center(self, width, height):
        w = self.window.winfo_screenwidth();
        h = self.window.winfo_screenheight();
        x = int((w - width) / 2);
        y = int((h - height) / 2);
        self.window.geometry('+{}+{}'.format(x, y));


    #Función para comprobar a conexión con la base de datos con los parametros introducidos
    def checkConnection(self, event):
        global connectionData;
        connectionData['hostDir'] = self.view.dir.get();
        connectionData['serverUser'] = self.view.user.get();
        connectionData['userPassword'] = self.view.password.get();
        connectionData['port'] = self.view.portEntry.get();
        connectionData['databaseName'] = self.view.dataB.get();
        if(connectionData['hostDir'] == None or connectionData['hostDir'] == ''):
            resultConnection = 'Debe indicar la dirección del servidor';
        elif(connectionData['serverUser'] == None or connectionData['serverUser'] == ''):
            resultConnection = 'Debe introducir un usuario';
        elif(connectionData['userPassword'] == None):        
            resultConnection =  'Debe introducir una contraseña';
        elif(connectionData['port'] == None or connectionData['port'] == ''):
            resultConnection = 'Debe indicar el puerto de conexión';
        elif(connectionData['databaseName'] == None or connectionData['databaseName'] == ''):
            resultConnection = 'Debe indicar la base de datos a usar';
        else:
            global bd;
            bd = BD(connectionData);
            resultConnection = bd.connect();
        self.view.setConnectionResult(self.window, resultConnection);
        if(resultConnection == True):
            #Se obtienen los nombres de las tablas a mostrar
            estData = bd.getTableNames(connectionData['databaseName']);
            #Se olvida el frame de conexion
            self.view.firstContainer.grid_forget();
            #Ventana principal fija sin ajuste de tamaño
            self.window.resizable(True,True);
            #Se establece el frame princial y sus widgets
            self.view.mainView(self.window);
            self.genDataW.complete(estData)
            self.predW.complete(estData);
            self.graphsW.complete(estData);
            self.getNewGenData();
            self.getGraphsData();
            self.genDataW.hideGenData()
            self.predW.hidePredictions();
            self.graphsW.hideGraphs();
            self.infoW.showInfo();


    #Pasar a la vista de conexxion
    def changeToConnect(self, event):
        #Olvidar el grid de start container y eliminarlo
        self.view.startContainer.grid_forget();
        self.view.startContainer.destroy();
        self.view.firstContainer.grid(row=0, column=0);


    #Función para elegir pestaña en la ventana principal
    def switchSelector(self, button1, button2, button3, button4, number):
        if(number == 1):
            self.genDataW.hideGenData()
            self.predW.hidePredictions();
            self.graphsW.hideGraphs();
            self.infoW.showInfo();
        elif(number == 2):
            self.infoW.hideInfo();
            self.predW.hidePredictions();
            self.graphsW.hideGraphs();
            self.genDataW.showGenData()
        elif(number == 3):
            self.infoW.hideInfo();
            self.genDataW.hideGenData()
            self.graphsW.hideGraphs();
            self.predW.showPredictions();
        else:
            self.infoW.hideInfo();
            self.genDataW.hideGenData()
            self.predW.hidePredictions();
            self.graphsW.showGraphs();

        button1.config(bg=mainColor, activebackground=thirdColor);
        button2.config(bg=mainColor, activebackground=thirdColor);
        button3.config(bg=mainColor, activebackground=thirdColor);
        button4.config(bg=secondaryColor, activebackground=secondaryColor);


    #Filtra los datos que se tienen que mostrar en la pestaña de datos generales
    def getNewGenData(self):
        self.genDataW.textResult.set('');
        if(self.genDataW.desdeE.get() != '' and self.genDataW.hastaE.get() != ''):
            try:
                d = datetime(int(self.genDataW.desdeE.get()[0:4]),int(self.genDataW.desdeE.get()[5:7]),int(self.genDataW.desdeE.get()[8:10]));
                h = datetime(int(self.genDataW.hastaE.get()[0:4]),int(self.genDataW.hastaE.get()[5:7]),int(self.genDataW.hastaE.get()[8:10]), 23, 00, 00);
                if(d <= h):
                    result =1;
                    result = self.functions.getGenData(bd, d, h);
                else: 
                    self.genDataW.textResult.set('La primera fecha debe ser menor que la segunda');
                    return;
            except:
                self.genDataW.textResult.set('El formato de las fechas es incorrecto');
                return;
        elif(self.genDataW.desdeE.get() == '' and self.genDataW.hastaE.get() != ''):
            try:
                h = datetime(int(self.genDataW.hastaE.get()[0:4]),int(self.genDataW.hastaE.get()[5:7]),int(self.genDataW.hastaE.get()[8:10]), 23, 00, 00);
                result = self.functions.getGenData(bd, self.genDataW.desdeE.get(), h);
            except:
                self.genDataW.textResult.set('El formato de las fechas es incorrecto');
                return;
        elif(self.genDataW.desdeE.get() !='' and self.genDataW.hastaE.get() == ''):
            try:
                d = datetime(int(self.genDataW.desdeE.get()[0:4]),int(self.genDataW.desdeE.get()[5:7]),int(self.genDataW.desdeE.get()[8:10]));
                result = self.functions.getGenData(bd, d, self.genDataW.hastaE.get());
            except:
                self.genDataW.textResult.set('El formato de las fechas es incorrecto');
                return;
        else:
            result = self.functions.getGenData(bd, self.genDataW.desdeE.get(), self.genDataW.hastaE.get());
        if(result == None):
            self.genDataW.textResult.set('No hay datos para las fechas seleccionadas');
        else:
            self.genDataW.start.set(result[1]);
            self.genDataW.finish.set(result[2]);
            self.genDataW.changeTableValues(result[0]);


    #Filtra los datos de los gráficos
    def getGraphsData(self):
            self.graphsW.textGraphResult.set('');
            estacion = self.graphsW.localization.get();
            meteoData = self.graphsW.atr.get();
            if(estacion == ''):
                self.graphsW.textGraphResult.set('Debe elegir una localización');
            elif(meteoData == ''):
                self.graphsW.textGraphResult.set('Debe elegir una variable');
            else:
                if(self.graphsW.dgEntry.get() != '' and self.graphsW.hgEntry.get() != ''):
                    try:
                        d = datetime(int(self.graphsW.dgEntry.get()[0:4]),int(self.graphsW.dgEntry.get()[5:7]),int(self.graphsW.dgEntry.get()[8:10]));
                        h = datetime(int(self.graphsW.hgEntry.get()[0:4]),int(self.graphsW.hgEntry.get()[5:7]),int(self.graphsW.hgEntry.get()[8:10]), 23, 00, 00);
                        if(d <= h):
                            result =1;
                            result = bd.selectFromTable(estacion, d, h);
                        else: 
                            self.graphsW.textGraphResult.set('La primera fecha debe ser menor que la segunda');
                            return;
                    except:
                        self.graphsW.textGraphResult.set('El formato de las fechas es incorrecto');
                        return;
                elif(self.graphsW.dgEntry.get() == '' and self.graphsW.hgEntry.get() != ''):
                    try:
                        h = datetime(int(self.graphsW.hgEntry.get()[0:4]),int(self.graphsW.hgEntry.get()[5:7]),int(self.graphsW.hgEntry.get()[8:10]), 23, 00, 00);
                        result = bd.selectFromTable(estacion, self.graphsW.dgEntry.get(), h);
                    except:
                        self.graphsW.textGraphResult.set('El formato de las fechas es incorrecto');
                        return;
                elif(self.graphsW.dgEntry.get() !='' and self.graphsW.hgEntry.get() == ''):
                    try:
                        d = datetime(int(self.graphsW.dgEntry.get()[0:4]),int(self.graphsW.dgEntry.get()[5:7]),int(self.graphsW.dgEntry.get()[8:10]));
                        result = bd.selectFromTable(estacion, d, self.graphsW.hgEntry.get());
                    except:
                        self.graphsW.textGraphResult.set('El formato de las fechas es incorrecto');
                        return;
                else:
                    result = bd.selectFromTable(estacion, self.graphsW.dgEntry.get(), self.graphsW.hgEntry.get());
                    
                if(len(result) == 0):
                    self.graphsW.textGraphResult.set('No hay datos para las fechas seleccionadas');

                else:
                    figure = self.functions.graphData(self.graphsW.localization.get(), self.graphsW.atr.get(), result);
                    self.graphsW.newGraph(figure);


    #Función al pulsar el botón de predecir
    def getForecast(self, event):
        self.predW.butHistForecast.grid_forget();
        self.predW.resultPredContainer.grid_columnconfigure(2, weight = 0);
        self.predW.predErr.set('');
        self.predW.predResult.set('');
        self.predW.textForecast.set('');
        atr = [];
        vars = [];
        if(self.predW.loc.get() == 'None'):
            self.predW.predErr.set('Debe seleccionar una localización para poder completar la predicción');
            return;
        elif(self.predW.t.get() == 0 and self.predW.w.get() == 0 and self.predW.p.get() == 0 and self.predW.h.get() == 0 and self.predW.d.get() == 0):
            self.predW.predErr.set('Debe seleccionar al menos una variable para poder completar la predicción');
            return;
        elif(self.predW.mod.get() == 'None'):
            self.predW.predErr.set('Debe seleccionar una modelo de predicción para poder completar la predicción');
            return;
        else:
            if(self.predW.t.get() == 1):
                atr.append('temperatura');
            if(self.predW.w.get() == 1):
                atr.append('viento');
            if(self.predW.d.get() == 1):
                atr.append('direccion');
            if(self.predW.p.get() == 1):
                atr.append('presion');
            if(self.predW.h.get() == 1):
                atr.append('humedad');

            if(self.predW.mod.get() == 'K-NN'):
                vars.append(self.predW.neighbors.get());
            elif(self.predW.mod.get() == 'Red neuronal'):
                vars.append(self.predW.layers.get());
                vars.append(self.predW.neurons1.get());
                vars.append(self.predW.neurons2.get());
                vars.append(self.predW.neurons3.get());
                vars.append(self.predW.itersRedNeu.get());
                vars.append(self.predW.learnRate.get());
            elif(self.predW.mod.get() == 'Árbol de decisión'):
                if(self.predW.maxDepth.get() != 0):
                    vars.append(self.predW.maxDepth.get());
                else:
                    vars.append(None);
            else:
                None;

            res = bd.selectDataForecast(self.predW.loc.get(), self.predW.iter.get()+int(self.predW.dayRef.get()), False);
            result = self.functions.valoresTempMaximas(res);
            pred = self.functions.dataForecast(result, self.predW.mod.get(), atr, vars, int(self.predW.dayRef.get()), self.predW.iter.get());
            self.predW.showPrediction(pred);


    #Mostrar gráfico con historico de predicciones
    def getHistForecast(self, event):
        self.predW.predErr.set('');
        atr = [];
        vars = [];
        if(self.predW.loc.get() == 'None'):
            self.predW.predErr.set('Debe seleccionar una localización para poder completar la predicción');
            return;
        elif(self.predW.t.get() == 0 and self.predW.w.get() == 0 and self.predW.p.get() == 0 and self.predW.h.get() == 0 and self.predW.d.get() == 0):
            self.predW.predErr.set('Debe seleccionar al menos una variable para poder completar la predicción');
            return;
        elif(self.predW.mod.get() == 'None'):
            self.predW.predErr.set('Debe seleccionar una modelo de predicción para poder completar la predicción');
            return;
        else:
            if(self.predW.t.get() == 1):
                atr.append('temperatura');
            if(self.predW.w.get() == 1):
                atr.append('viento');
            if(self.predW.d.get() == 1):
                atr.append('direccion');
            if(self.predW.p.get() == 1):
                atr.append('presion');
            if(self.predW.h.get() == 1):
                atr.append('humedad');

            if(self.predW.mod.get() == 'K-NN'):
                vars.append(self.predW.neighbors.get());
            elif(self.predW.mod.get() == 'Red neuronal'):
                vars.append(self.predW.layers.get());
                vars.append(self.predW.neurons1.get());
                vars.append(self.predW.neurons2.get());
                vars.append(self.predW.neurons3.get());
                vars.append(self.predW.itersRedNeu.get());
                vars.append(self.predW.learnRate.get());
            elif(self.predW.mod.get() == 'Árbol de decisión'):
                if(self.predW.maxDepth.get() != 0):
                    vars.append(self.predW.maxDepth.get());
                else:
                    vars.append(None);
            else:
                None;

            res = bd.selectDataForecast(self.predW.loc.get(), self.predW.iter.get()+int(self.predW.dayRef.get()), True);
            result = self.functions.valoresTempMaximas(res);
            figure = self.functions.AllForecast(result, self.predW.mod.get(), atr, vars, int(self.predW.dayRef.get()), self.predW.iter.get());
            self.predW.showHist(figure);
            
                

    #Función para descconectar de la base de datos
    def disconnect(self, event):
        global bd;
        self.view.execute = False;
        try:
            bd.close();
        except:
            None;
        #Olvidar self.mainContainer
        self.view.mainContainer.grid_forget();
        #Atributos de la ventana
        self.window.attributes("-zoomed", False);
        self.window.geometry('450x490');
        self.center(450, 490);
        self.window.resizable(False,False);
        #Cargar connection container
        self.view.firstContainer.grid(row = 0, column = 0);
        self.view.connectionView(self.window);


    def finishApp(self):
        global bd;
        self.view.execute = False;
        try:
            bd.close();
        except:
            None;
        try:
            self.view.t1.join(0);
            self.view.t2.join(1);
        except:
            None;

        sys.exit(0);  


#Se crea una instancia de la clase aplicación
if __name__=="__main__":
    Aplicacion()