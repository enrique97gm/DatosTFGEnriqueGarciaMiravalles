#encoding: utf-8
#importando mysql
import mysql.connector as mysql
from mysql.connector import errorcode

#Modulo datetime
from datetime import datetime, timedelta

#Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Pandas
import pandas as pd 
import numpy as np

#Librerias de machine learning sklearn
from sklearn import svm
from sklearn.tree import export_graphviz
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor

estaciones = {}
estData = {}

dates = {
    'start': '',
    'finish': ''
}

datesGraph = {
    'start': '',
    'finish': ''
}


#-----------------------------------Base de datos-------------------------#
class BD():

    host = None;
    user = None;
    password = None;
    database = None;
    port = None;
    connection = None;
    cursor = None;

    def __init__(self, object):
        self.host = object['hostDir'];
        self.user = object['serverUser'];
        self.password = object['userPassword'];
        self.port = object['port'];
        self.database =  object['databaseName'];

    def connect(self):
        global mysqlErr;
        try:
            db = mysql.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                port = self.port,
                database = self.database,
                auth_plugin='mysql_native_password'
            );
            self.connection = db;
            self.cursor = db.cursor();
            return True;
        except mysql.Error as err:     
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return 'Usuario o contraseña incorrectos';
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return 'No existe la base de datos especificada';
            else:
                return err;


    #Función para cerrar la base de datos.
    def close(self):
        self.cursor.close()
        self.connection.close()


    #Obtener tablas de la base de datos
    def getTableNames(self, dataBase):
        query = 'select table_name as nombre from information_schema.tables where table_schema = "'+dataBase+'"';
        self.cursor.execute(query);
        result = self.cursor.fetchall();
        for row in result:
            estData.update({row[0]:[]})
            estaciones.update({row[0]: None});
        for est in estData:
            query = "select * from `"+est+"`";
            self.cursor.execute(query);
            result = self.cursor.fetchall();
            for val in result:
                try:
                    estData[est].index('Temperatura');
                except:
                    if(val[1] != None):
                        estData[est].append('Temperatura');
                try:
                    estData[est].index('Viento');
                except:
                    if(val[2] != None):
                        estData[est].append('Viento');
                try:
                    estData[est].index('Dirección');
                except:
                    if(val[3] != None):
                        estData[est].append('Dirección');
                try:
                    estData[est].index('Precipitaciones');
                except:
                    if(val[6] != None):
                        estData[est].append('Precipitaciones');
                try:
                    estData[est].index('Presión');
                except:
                    if(val[7] != None):
                        estData[est].append('Presión');
                try:
                    estData[est].index('Humedad');
                except:
                    if(val[8] != None):
                        estData[est].append('Humedad');

        return estData;


    #Función de bśqueda de datos para los gráficos y datos generales  
    def selectFromTable(self, tabla, fecha1, fecha2):
        if(fecha1 == '' and fecha2 == ''):
            query = "select * from `"+tabla+"`";
            self.cursor.execute(query);
        elif(fecha1 != '' and fecha2 == ''):
            f1 = fecha1.strftime("%Y-%m-%d %H:%M:%S");
            query = "select * from `"+tabla+"` where fecha >= '"+f1+"'";
            self.cursor.execute(query);
        elif(fecha1 == '' and fecha2 != ''):
            f2 = fecha2.strftime("%Y-%m-%d %H:%M:%S");
            query = "select * from `"+tabla+"` where fecha <= '"+f2+"'";
            self.cursor.execute(query);
        elif(fecha1 == fecha2 and fecha1 != ''):
            f1 = fecha1.strftime("%Y-%m-%d");
            query = "select * from `"+tabla+"` where fecha like '%"+f1+"%'";
            self.cursor.execute(query);
        else:
            f1 = fecha1.strftime("%Y-%m-%d %H:%M:%S");
            f2 = fecha2.strftime("%Y-%m-%d %H:%M:%S");
            values = (f1,f2);
            query = "select * from `"+tabla+"` where fecha >= %s and fecha <= %s";
            self.cursor.execute(query, values);
            
        result = self.cursor.fetchall();
        return result;


    #Función de bśqueda de datos para la prediccion   
    def selectDataForecast(self, tabla, iter, all):
        iter = iter*24;
        presion = [];
        humedad = [];
        temperatura = [];
        fecha = [];
        viento = [];
        dir = [];
        data = [];
        date = datetime.now();
        if(all == True):
            if(date.hour < 18):
                f = date.strftime("%Y-%m-%d");
                query = "select * from `"+tabla+"` where fecha < '"+f+"' order by Fecha desc";
            else:
                query = "select * from `"+tabla+"` order by Fecha desc"; 
        else:
            if(date.hour < 18):
                f = date.strftime("%Y-%m-%d");
                query = "select * from `"+tabla+"` where fecha < '"+f+"' order by Fecha desc limit "+ str(iter);
            else:
                query = "select * from `"+tabla+"` order by Fecha desc limit "+ str(iter); 
        
        self.cursor.execute(query);
        result = self.cursor.fetchall();
        for row in result:
            fecha.append(row[0]);
            temperatura.append(row[1]);
            presion.append(row[7]);
            humedad.append(row[8]);
            viento.append(row[2]);
            dir.append(row[3]);

        data.append(fecha);
        data.append(temperatura);
        data.append(presion);
        data.append(humedad);
        data.append(viento);
        data.append(dir);
        return data;



#Funciones para obtener los datos, lógica de negocio
class Functions():
    #Función para obtener datos generales de cada estacion meteorológica
    def getGenData(self, bd, fInicio, fFin):
        global estaciones;
        for estacion in estaciones:
            result = bd.selectFromTable(estacion, fInicio, fFin);
            if(len(result) == 0):
                return None;
            tMax = result[0][1];
            tMin = result[0][1];
            tMedia = 0;
            vMedio = 0;
            dirPredo = None;
            rMax = result[0][6];
            dirRMax = '';
            precTot = 0;
            precMax = result[0][6];
            precMedia = None;
            presMedia = 0;
            humMedia = 0;
            direcciones = {
                'Norte': 0,
                'Nordeste': 0,
                'Este': 0,
                'Sudeste': 0,
                'Sur': 0,
                'Sudoeste': 0,
                'Oeste': 0,
                'Noroeste': 0,
                'Calma': 0,
            }
            for res in result:
                if(res[1] != None):
                    if(tMax != None):
                        if(res[1] > tMax):
                            tMax = res[1];

                        if(tMin > res[1]):
                            tMin = res[1];
                    else:
                        tMax = res[1];
                        tMin = res[1];
                    
                    tMedia = tMedia + res[1];

                if(res[2] != None):
                    vMedio = vMedio + res[2];

                if(res[3] != None):
                    direcciones[res[3]] = direcciones[res[3]] + 1;

                if(res[4] != None):
                    if(rMax != None):
                        if(rMax < res[4]):
                            rMax = res[4];
                        
                        if(rMax == res[4]):
                            dirRMax = res[5];
                    else:
                        rMax = res[4];
                        dirRMax = res[5];

                if(res[6] != None):
                    precTot = precTot + res[6];
                    if(precMax != None):
                        if(precMax < res[6]):
                            precMax = res[6]; 
                    else:
                        precMax = res[6];

                if(res[7] != None):
                    presMedia = presMedia + res[7];
                if(res[8] != None):
                    humMedia = humMedia + res[8];

            tMedia = round((tMedia / len(result)), 5);
            vMedio = round((vMedio / len(result)), 5);
            cuenta = 0;
            for dir in direcciones:
                if(cuenta < direcciones[dir]):
                    cuenta = direcciones[dir];
                    dirPredo = dir;
            
            precTot  = round(precTot, 2);
            precMedia = round((precTot / len(result)), 5);
            presMedia = round((presMedia / len(result)), 5);
            if(presMedia == 0):
                presMedia = None;
            if(rMax == 0):
                rMax = None;
            if(vMedio == 0):
                vMedio = None;
            humMedia = round((humMedia / len(result)), 5);
            estaciones[estacion] = [tMax, tMedia, tMin, vMedio, dirPredo, rMax, dirRMax, precTot, precMax, precMedia, presMedia, humMedia];
        return [estaciones, result[0][0], result[len(result)-1][0]];


    #Funcion de obtencion de las temperaturas maximas de cada dia
    def valoresTempMaximas(self, result):
        data = {
            'fecha': [],
            'temperatura': [],
            'viento': [],
            'direccion': [],
            'presion': [],
            'humedad': [],
        }
        for i in range(len(result[0])):
            day = result[0][i].day;
            month = result[0][i].month;
            existe = False;
            temp = -273;
            for j in range(len(result[0])):
                if(day == result[0][j].day and month == result[0][j].month):
                    if(result[1][j] != None):
                        if(result[1][j] > temp):
                            fech = result[0][j];
                            temp = result[1][j];
                            pres = result[2][j];
                            hum = result[3][j];
                            vi = result[4][j];
                            if(result[5][j] == 'Norte'):
                                dir = [1,0,0,0,0,0,0,0,0];
                            elif(result[5][j] == 'Noreste'):
                                dir = [0,1,0,0,0,0,0,0,0];
                            elif(result[5][j] == 'Este'):
                                dir = [0,0,1,0,0,0,0,0,0];
                            elif(result[5][j] == 'Sudeste'):
                                dir = [0,0,0,1,0,0,0,0,0];
                            elif(result[5][j] == 'Sur'):
                                dir = [0,0,0,0,1,0,0,0,0];
                            elif(result[5][j] == 'Sudoeste'):
                                dir = [0,0,0,0,0,1,0,0,0];
                            elif(result[5][j] == 'Oeste'):
                                dir = [0,0,0,0,0,0,1,0,0];
                            elif(result[5][j] == 'Noroeste'):
                                dir = [0,0,0,0,0,0,0,1,0];
                            else:
                                dir = [0,0,0,0,0,0,0,0,1];

            for i in data['fecha']:
                if((i.day == day and i.month == month) or i == fech):
                    existe = True;
                
            if(existe == False):
                if(temp == -273):
                    data['temperatura'].append(0);
                else:
                    data['temperatura'].append(temp);
                data['fecha'].append(fech);
                data['presion'].append(pres);
                data['humedad'].append(hum);
                data['viento'].append(vi);
                data['direccion'].append(dir);
        
        return data;


    #Funcion de prediccion de temperatura y seleccion de modelo de prediccion
    def dataForecast(self, data, type, attr, vars, days, iter):
        if(len(data['temperatura']) < days+iter):
            return None;

        forData = [];
        next = False;
        for i in range(iter):
            arr = [];
            t = True;
            for value in attr:
                for dat in data:
                    if(dat == 'temperatura' and t==True):
                        arr.append(data['temperatura'][i]);
                        t = False;
                    if(dat == value):
                        for j in range(days):
                            if(dat == 'direccion'):
                                for dir in data[value][(1+i+j)]:
                                    if(pd.isnull(dir) == True):
                                        next = True;
                                    arr.append(dir);
                            else:
                                if(pd.isnull(data[value][(1+i+j)]) == True):
                                    next = True;
                                arr.append(data[value][(1+i+j)]);

            forData.append(arr);

        forData = pd.DataFrame(forData);
        values = forData.values;
        x, y = values[:, 1:], values[ : , 0];
        predValues = [];
        for val in attr:
            for dat in data:
                if(dat == val):
                    for i in range(days):
                        if(dat == 'direccion'):
                            for dir in data[dat][i]:
                                if(pd.isnull(dir) == True):
                                    next = True;
                                predValues.append(dir);
                        else:
                            if(pd.isnull(data[dat][i]) == True):
                                    next = True;
                            predValues.append(data[dat][i]);

        if(next == True):
            return None;

        predValues = pd.DataFrame(predValues);
        predValues = predValues.values.reshape(1,-1); 
        if(type == 'Árbol de decisión'):  
            model = DecisionTreeRegressor(max_depth = vars[0]);
        elif(type == 'Regresión lineal'):
            model = linear_model.LinearRegression();
        elif(type == 'K-NN'):
            model = KNeighborsRegressor(n_neighbors=vars[0], weights='distance')
        elif(type == 'Red neuronal'):
            if(vars[0] == 1):
                model = MLPRegressor(hidden_layer_sizes = (vars[1],),solver="lbfgs", max_iter = vars[4], learning_rate_init = vars[5],  alpha = 0.001);
            elif(vars[0] == 2):
                model = MLPRegressor(hidden_layer_sizes = (vars[1], vars[2],),solver="lbfgs", max_iter = vars[4], learning_rate_init = vars[5], alpha = 0.001);
            else:
                model = MLPRegressor(hidden_layer_sizes = (vars[1], vars[2], vars[3]),solver="lbfgs", max_iter = vars[4], learning_rate_init = vars[5], alpha = 0.001);
        else:
            return None;
            
        model.fit(x, y);
        pred = model.predict(predValues);
        return pred;


    #Funcion para mostrar el historico de predicciones
    def AllForecast(self, data, type, attr, vars, days, iter):
        dataGraphs = {
            'date': [],
            'forecasts': [],
        };
        for sum in range(len(data['fecha'])-(days+iter)):
            next = False;
            forData = [];
            for i in range(iter):
                arr = [];
                t = True;
                for value in attr:
                    for dat in data:
                        if(dat == 'temperatura' and t==True):
                            arr.append(data['temperatura'][sum + i]);
                            t = False;
                        if(dat == value):
                            for j in range(days):
                                if(dat == 'direccion'):
                                    for dir in data[value][(sum+1+i+j)]:
                                        if(pd.isnull(dir) == True):
                                            next = True;
                                        arr.append(dir);
                                else:
                                    if(pd.isnull(data[value][(sum+1+i+j)]) == True):
                                            next = True;
                                    arr.append(data[value][(sum+1+i+j)]);

                forData.append(arr);

            forData = pd.DataFrame(forData);
            values = forData.values;
            x, y = values[:, 1:], values[ : , 0];
            predValues = [];
            for val in attr:
                for dat in data:
                    if(dat == val):
                        for i in range(days):
                            if(dat == 'direccion'):
                                for dir in data[dat][sum+i]:
                                    if(pd.isnull(dir) == True):
                                        next = True;
                                    predValues.append(dir);
                            else:
                                if(pd.isnull(data[dat][sum+i]) == True):
                                    next = True;
                                predValues.append(data[dat][sum+i]);

            if(next == True):
                continue;

            predValues = pd.DataFrame(predValues);
            predValues = predValues.values.reshape(1,-1); 
            if(type == 'Árbol de decisión'):  
                model = DecisionTreeRegressor(max_depth = vars[0]);
            elif(type == 'Regresión lineal'):
                model = linear_model.LinearRegression();
            elif(type == 'K-NN'):
                model = KNeighborsRegressor(n_neighbors=vars[0], weights='distance')
            elif(type == 'Red neuronal'):
                if(vars[0] == 1):
                    model = MLPRegressor(hidden_layer_sizes = (vars[1],),solver="lbfgs", max_iter = 10000, alpha = 0.001);
                elif(vars[0] == 2):
                    model = MLPRegressor(hidden_layer_sizes = (vars[1], vars[2],),solver="lbfgs", max_iter = 10000, alpha = 0.001);
                else:
                    model = MLPRegressor(hidden_layer_sizes = (vars[1], vars[2], vars[3]),solver="lbfgs", max_iter = 10000, alpha = 0.001);
            else:
                return None;
                
            model.fit(x, y);
            pred = model.predict(predValues);
            date = data['fecha'][sum];
            date = date + timedelta(days=1);
            dataGraphs['date'].append(date);
            if(pred[0] > 50 or pred[0] < -20):
                pred[0] = None;
            dataGraphs['forecasts'].append(pred[0]);

        
        dates = [];
        forcastTemps = [];
        realTemperatures = [];
        for i in range(len(dataGraphs['date'])):
            for j in range(len(data['fecha'])):
                if(data['fecha'][len(data['fecha'])-(1+j)].strftime("%Y-%m-%d") == dataGraphs['date'][len(dataGraphs['date'])-(1+i)].strftime("%Y-%m-%d")):
                    realTemperatures.append(data['temperatura'][len(data['temperatura'])-(1+j)]);
                    dates.append(dataGraphs['date'][len(dataGraphs['date'])-(1+i)].strftime("%Y-%m-%d"));
                    forcastTemps.append(dataGraphs['forecasts'][len(dataGraphs['forecasts'])-(1+i)]);

        sumErrors = 0;
        averError = 0;
        ejs = 0;  
        for i in range(len(dataGraphs['date'])):
            for j in range(len(data['fecha'])):
                if(data['fecha'][j].strftime("%Y-%m-%d") == dataGraphs['date'][i].strftime("%Y-%m-%d")):
                    if(pd.isnull(data['temperatura'][j]) or pd.isnull(dataGraphs['forecasts'][i])):
                        continue;
                    sumErrors = sumErrors + abs(data['temperatura'][j] - dataGraphs['forecasts'][i]);
                    ejs = ejs +1;

        averError = round(float(sumErrors) / ejs, 5);
            
        f = plt.figure(figsize=(12,7), dpi=100);
        ax = f.add_subplot(111);
        f.subplots_adjust(top = 0.90, left = 0.06, bottom = 0.2, right=0.80);
        ax.set_title('Representación de las temperaturas reales y las predicciones realizadas con el modelo y variables seleccionadas');
        ax.plot(dates, realTemperatures, 'o-', color='red', label='Temperaturas reales (°C)');
        ax.plot(dates, forcastTemps, 'o-', color='blue', label='Predicciones (°C)');
        ax.set_ylabel('Temperatura (°C)');
        ax.legend(loc='center left', bbox_to_anchor=(0.995, 0.5));
        ax.text(1.1,0.3, 'Número de casos: '+ str(len(dataGraphs['forecasts']))+ '\n Error medio: '+str(averError), color='black', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
        ax.grid(True);
        if(len(dates) > 12):
            plt.xticks(rotation = 65);
        if(len(dates) > 25 and len(dates) <= 50):
            var = 2;
        elif(len(dates) > 50 and len(dates) <= 75):
            var = 3;
        elif(len(dates) > 75 and len(dates) <= 100):
            var = 4;
        elif(len(dates) > 100):
            var = 5;
        else:
            var = 1;
        for n,label in enumerate(ax.xaxis.get_ticklabels()):
            if n % var != 0:
                label.set_visible(False);
        ax.set_xlabel('Días');
        return f;


    #Funcion para obtener los gráficos
    def graphData(self, estacion, meteoData, result):
        dataGraph = {
            'days': [],
            'data1': [],
            'data2': [],
            'data3': [],
        }
        direcciones = {
            'Norte': 0,
            'Nordeste': 0,
            'Este': 0,
            'Sudeste': 0,
            'Sur': 0,
            'Sudoeste': 0,
            'Oeste': 0,
            'Noroeste': 0,
            'Calma': 0,
        }
        global datesGraph;
        datesGraph['start'] = result[0][0];
        datesGraph['finish'] = result[len(result)-1][0];
        fi = datesGraph['start'].strftime("%Y-%m-%d %H:%M:%S");
        ff = datesGraph['finish'].strftime("%Y-%m-%d %H:%M:%S");
        if(meteoData == 'Temperatura'):
            max = result[0][1];
            med = 0;
            min = result[0][1];
        elif(meteoData == 'Viento'):
            max = result[0][2];
            med = 0;
            min = result[0][2];
        elif(meteoData == 'Precipitaciones'):
            max = result[0][6];
            med = 0;
            min = result[0][6];
        elif(meteoData == 'Presión'):
            max = result[0][7];
            med = 0;
            min = result[0][7];
        elif(meteoData == 'Humedad'):
            max = result[0][8];
            med = 0;
            min = result[0][8];
        day = datesGraph['start'] = result[0][0].strftime("%Y-%m-%d");
        i = 0;
        for res in result:
            if(meteoData != 'Dirección'):
                if(meteoData == 'Temperatura' and res[1] != None):
                    value = res[1];
                if(meteoData == 'Viento' and res[2] != None):
                    value = res[2];
                if(meteoData == 'Precipitaciones' and res[6] != None):
                    value = res[6];
                if(meteoData == 'Presión' and res[7] != None):
                    value = res[7];
                if(meteoData == 'Humedad' and res[8] != None):
                    value = res[8];

                if(day != res[0].strftime("%Y-%m-%d")):
                    dataGraph['days'].append(day);
                    dataGraph['data1'].append(max);
                    if(meteoData == 'Precipitaciones'):
                        dataGraph['data2'].append(med);
                    else:
                        dataGraph['data2'].append(med/i);
                    dataGraph['data3'].append(min);
                    day = res[0].strftime("%Y-%m-%d");
                    max = value;
                    min = value;
                    med = value;
                    i = 1;
                else:
                    i = i + 1;
                    med = med + value;
                    if(min > value):
                        min = value;
                    if(max < value):
                        max = value;
            else:
                if(res[3] != None):
                    direcciones[res[3]] = direcciones[res[3]] + 1;


        if(meteoData != 'Dirección'):
            dataGraph['days'].append(day);
            dataGraph['data1'].append(max);
            if(meteoData == 'Precipitaciones'):
                dataGraph['data2'].append(med);
            else:
                dataGraph['data2'].append(med/i);
            dataGraph['data3'].append(min);
        else:
            dir = [];
            hours = [];
            for d in direcciones:
                if(direcciones[d] != 0):
                    dir.append(d);
                    hours.append(direcciones[d]/len(result)*100);

        f = plt.figure(figsize=(11,5), dpi=100);
        ax = f.add_subplot(111);
        f.subplots_adjust(top = 0.95, left = 0.08, bottom = 0.2, right=0.85);
        ax.set_title(meteoData +" en "+ estacion +" entre las fechas "+fi+ " y "+ff);
        if(meteoData == 'Temperatura'):
            ax.plot(dataGraph['days'], dataGraph['data1'], 'o-', color='red', label='Temperatura\nmáxima (°C)');
            ax.plot(dataGraph['days'], dataGraph['data2'], 'o-', color='green', label='Temperatura\nmedia (°C)');
            ax.plot(dataGraph['days'], dataGraph['data3'], 'o-', color='blue', label='Temperatura\nmínima (°C)');
            ax.set_ylabel('Temperatura (°C)');
        elif(meteoData == 'Viento'):
            ax.plot(dataGraph['days'], dataGraph['data1'], 'o-', color='red', label='Viento\nmáximo (km/h)');
            ax.plot(dataGraph['days'], dataGraph['data2'], 'o-', color='green', label='Viento\nmedio (km/h)');
            ax.plot(dataGraph['days'], dataGraph['data3'], 'o-', color='blue', label='Viento\nmínimo (km/h)');
            ax.set_ylabel('Viento (km/h)');
        elif(meteoData == 'Presión'):
            ax.plot(dataGraph['days'], dataGraph['data1'], 'o-', color='red', label='Presión\nmáxima (hPa)');
            ax.plot(dataGraph['days'], dataGraph['data2'], 'o-', color='green', label='Presión\nmedia (hPa)');
            ax.plot(dataGraph['days'], dataGraph['data3'], 'o-', color='blue', label='Presión\nmínima (hPa)');
            ax.set_ylabel('Presión (hPa)');
        elif(meteoData == 'Humedad'):
            ax.plot(dataGraph['days'], dataGraph['data1'], 'o-', color='red', label='Humedad\nmáxima (%)');
            ax.plot(dataGraph['days'], dataGraph['data2'], 'o-', color='green', label='Humedad\nmedia (%)');
            ax.plot(dataGraph['days'], dataGraph['data3'], 'o-', color='blue', label='Humedad\nmínima (%)');
            ax.set_ylabel('Humedad (%)');
        elif(meteoData == 'Precipitaciones'):
            ax.bar(dataGraph['days'], dataGraph['data2'], label='Precipitaciones\n(mm)')
            ax.set_ylabel('Precipitaciones (mm)');
        elif(meteoData == 'Dirección'):
            f.subplots_adjust(bottom = 0);
            ax.pie(hours, labels=dir, autopct='%1.1f%%', startangle=90);
            ax.set_title("Porcentaje de horas respecto de la dirección del viento entre las fechas "+fi+ " y "+ff);

        if(meteoData != 'Dirección'):
            if(len(dataGraph['days']) > 12):
                plt.xticks(rotation = 65);
            if(len(dataGraph['days']) > 25 and len(dataGraph['days']) <= 50):
                var = 2;
            elif(len(dataGraph['days']) > 50 and len(dataGraph['days']) <= 75):
                var = 3;
            elif(len(dataGraph['days']) > 75 and len(dataGraph['days']) <= 100):
                var = 4;
            elif(len(dataGraph['days']) > 100):
                var = 5;
            else:
                var = 1;
            for n,label in enumerate(ax.xaxis.get_ticklabels()):
                if n % var != 0:
                    label.set_visible(False);
            ax.legend(loc='center left', bbox_to_anchor=(0.995, 0.5));
            ax.grid(True);
            ax.set_xlabel('Días');
        return f; 
