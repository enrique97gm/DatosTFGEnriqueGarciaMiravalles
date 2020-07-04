#encoding: utf-8
#importando la interfaz grafica
from tkinter import *
from tkinter import ttk

#importando threading
import threading

#importamos variables y funciones del sistema
import os

#Para imagenes
from PIL import ImageTk,Image

#importando el modulo para delay
import time

mainColor = '#186DDA';
secondaryColor = '#00AEFF';
thirdColor = '#50A0E7';

#----------------------------Vistas de la aplicación--------------------------# 
class Window():

    #Inicialización
    def __init__(self, window):
        #Contenedor de inicio
        self.startContainer = Frame(window, bg=mainColor);
        self.startContainer.grid(row=0, column=0);
        self.buttonToBD = Button(self.startContainer, text="Siguiente", cursor = 'hand2');
        self.start();

        #Contenedor de conexion
        self.firstContainer = Frame(window, bg=mainColor);
        self.buttonConnect = Button(self.firstContainer, text="Conectar", cursor = 'hand2');
        self.connectionContainer = Frame(self.firstContainer, bg=mainColor);
        self.dir = Entry(self.connectionContainer, font=('Helvetica 12'));
        self.user = Entry(self.connectionContainer, font=('Helvetica 12'));
        self.password = Entry(self.connectionContainer, font=('Helvetica 12'), show="*");
        self.portEntry = Entry(self.connectionContainer, font=('Helvetica 12'));
        self.dataB = Entry(self.connectionContainer,font=('Helvetica 12'));
        self.textResult = StringVar();
        self.connectionError = Label(self.connectionContainer, textvariable = self.textResult, wraplength=350);
        self.connectionView(window);

        #Contenedor de incio de aplicaion
        self.mainContainer = Frame(window, bg=mainColor);

        #Contenedor de seleccion.
        self.selectorContainer = Frame(self.mainContainer, width=window.winfo_screenwidth()*0.2, height=window.winfo_screenheight()*0.8, bg=mainColor); 
        #Contenedor de datos generales.
        self.dataContainer = Frame(self.mainContainer, width=window.winfo_screenwidth()*0.8, height=window.winfo_screenheight()*0.8, bg='white');
        
        #Botones de seleccion
        self.infoButton = Button(self.selectorContainer, cursor = 'hand2');
        self.genDataButton = Button(self.selectorContainer, cursor = 'hand2');
        self.predButton = Button(self.selectorContainer, cursor = 'hand2');
        self.graphButton = Button(self.selectorContainer, cursor = 'hand2');

        #Boton de desconexion 
        self.buttonDisconnect = Button(self.selectorContainer, text="Desconectar", cursor = 'hand2'); 

    #Establece el resultado de la conexion
    def setConnectionResult(self, window, resultConnection):
        if(resultConnection != True):
            self.textResult.set(resultConnection);
        else:
            self.connectionError.config(fg='lime green');
            self.textResult.set('Se ha conectado con éxito');
            window.update();
            time.sleep(0.8);

    #-----------------------------Vista de comienzo de app----------------------#
    def start(self):
        #configuracion del frame
        self.startContainer.config(bg=mainColor);
        self.startContainer.grid_columnconfigure(0, weight = 1);
        self.startContainer.grid_rowconfigure(0, weight = 1);
            
        #Labels
        welcome = Label(self.startContainer, text='Bienvenido!!!');
        welcome.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 28, 'bold')
                        );
        welcome.grid(row=0, column=0, padx=80, pady=(40,20), sticky='NESW');

        #Titulo de la app
        titleLabel = Label(self.startContainer, text='Herramienta de prueba para la predicción de temperaturas máximas');
        titleLabel.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 18, 'bold'),
                        wraplength = 380,
                        );
        titleLabel.grid(row=1, column=0, pady=(0,20), sticky='NESW');

        #Breve descripcion
        infoLabel = Label(self.startContainer, text='Heramienta diseñada durante el desarrollo del TFG para  la visualización de  datos y  creación de  modelos  de  predicción  de  temperaturas  máximas a partir de los datos obtenidos de un sistema de almacenamiento externo.');
        infoLabel.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12),
                        wraplength = 380,
                        justify = LEFT,
                        anchor = 'w'
                        );
        infoLabel.grid(row=2, column=0, padx=(35), pady=(0, 20), sticky='NESW');

        #Indicador de avance
        continueLabel = Label(self.startContainer, text='Para realizar la conexión con la base de datos externa y  obtener  los datos  meteorológicos con los que trabajar, pulse en "siguiente".');
        continueLabel.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12),
                        wraplength = 380,
                        justify = LEFT,
                        anchor = 'w'
                        );
        continueLabel.grid(row=3, column=0, padx=(35), pady=(0, 20), sticky='NESW');

        #Botón para acceder al apartado de conexion
        self.buttonToBD.grid(row=4, column=0, padx=(70), pady=(0,40), sticky='E');


    #-------------------------------vista conexión----------------------------#
    #Vista para conectar con la base de datos
    def connectionView(self, window):
        #configuracion del frame
        self.firstContainer.config(width=600, height=600);
        self.firstContainer.grid_rowconfigure(0, weight=1);
        self.firstContainer.grid_rowconfigure(1, weight=1);
        self.firstContainer.grid_columnconfigure(0, weight=1);
        
        info = Label(self.firstContainer, text='Datos de conexión');
        info.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 18, 'bold')
                        );
        info.grid(row=0, column=0, padx=100, pady=(45,30), sticky='WE');

        #Introduccion de datos.
        self.connectionContainer.grid(row=1, column=0, pady=(0,0));

        #Servidor de base de datos
        serverDB = Label(self.connectionContainer, text='Dirección del servior de base de datos:');
        serverDB.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12)
                        );
        serverDB.grid(row=0, column=0, sticky='W');
        #Entry de la direccion
        self.dir.delete(0, END);
        self.dir.grid(row=1, column=0, sticky='WE');

        #Usuario a usar
        userDB = Label(self.connectionContainer, text='Usuario:');
        userDB.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12)
                        );
        userDB.grid(row=2, column=0, pady=(10,0), sticky='W');
        #Entry del usuario
        self.user.delete(0, END);
        self.user.grid(row=3, column=0, sticky='WE');

        #Contraseña del usuario
        passBd = Label(self.connectionContainer, text='Contraseña:');
        passBd.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12)
                        );
        passBd.grid(row=4, column=0, pady=(10,0), sticky='W');
        #Entry de contraseña
        self.password.delete(0, END);
        self.password.grid(row=5, column=0, sticky='WE');

        #Puerto de conexion
        port = Label(self.connectionContainer, text='Puerto:');
        port.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12)
                        );
        port.grid(row=6, column=0, pady=(10,0), sticky='W');
        #Entry de contraseña
        self.portEntry.delete(0, END);
        self.portEntry.grid(row=7, column=0, sticky='WE');


        #Base de datos a usar
        dataBase = Label(self.connectionContainer, text='Base de datos:');
        dataBase.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 12)
                        );
        dataBase.grid(row=8, column=0, pady=(10,0), sticky='W');
        #Entry de la base de datos
        self.dataB.delete(0, END);
        self.dataB.grid(row=9, column=0, pady=(0,10), sticky='WE');

        self.textResult.set('');
        #Errores conexion
        self.connectionError.config(fg='red',
                    bg=mainColor,
                    font=('Comic Sans', 11, 'bold')
                    );
        self.connectionError.grid(row=10, column=0, pady=(5,5), sticky='E');

        self.buttonConnect.grid(row=2, column=0, sticky='E', padx=75, pady=(0,40));


    #--------------------------------Vista principal----------------------------#
    #Ventana principal con todas las operaciones
    def mainView(self, window):
        
        #Pantalla ampliada a True
        window.attributes("-zoomed", True);

        #Configuracion de self.mainContainer
        self.mainContainer.config(width=window.winfo_screenwidth(), height=window.winfo_screenheight(), bg=mainColor);
        self.mainContainer.grid(row=0, column=0, sticky='NESW');
        self.mainContainer.grid_rowconfigure(1, weight = 1);
        self.mainContainer.grid_columnconfigure(1, weight = 1);

        #Contenedor de barra de desconexión.
        topBar = Frame(self.mainContainer, width=window.winfo_screenwidth(), height=window.winfo_screenheight()*0.2, bg=mainColor);
        
        self.dataContainer.grid(row=1, column=1, sticky='NESW');
        self.dataContainer.grid_columnconfigure(0, weight = 1);
        self.dataContainer.grid_rowconfigure(0, weight = 1);
        topBar.grid(row=0, column=0, columnspan=2, sticky='NESW');
        topBar.grid_columnconfigure(0, weight = 1);
        topBar.grid_columnconfigure(1, weight = 1);
        topBar.grid_columnconfigure(2, weight = 1);
        self.selectorContainer.grid(row=1, column=0, sticky='NESW');
        self.selectorContainer.grid_rowconfigure(4, weight = 1);
        
        

        #Botones seleccion de vista
        self.infoButton.config(highlightthickness=0, relief="flat", text="Información", bg=secondaryColor, fg='white', font=('Comic Sans', 14, 'bold'), activebackground=secondaryColor, activeforegroun='white');
        self.infoButton.grid(row=0, column=0, sticky='EW');
        self.genDataButton.config(highlightthickness=0, relief="flat", text="Datos generales", bg=mainColor, fg='white', font=('Comic Sans', 14, 'bold'), activebackground=thirdColor, activeforegroun='white');
        self.genDataButton.grid(row=1, column=0, sticky='EW');
        self.predButton.config(highlightthickness=0, relief="flat", text="Predicciones", bg=mainColor, fg='white', font=('Comic Sans', 14, 'bold'), activebackground=thirdColor, activeforegroun='white');
        self.predButton.grid(row=2, column=0, sticky='EW');
        self.graphButton.config(highlightthickness=0, relief="flat", text="Gráficos", bg=mainColor, fg='white', font=('Comic Sans', 14, 'bold'), activebackground=thirdColor, activeforegroun='white');
        self.graphButton.grid(row=3, column=0, sticky='EW');

        #Label TopBar
        title = Label(topBar, text='Herramienta de prueba para la predicción');
        title.config(fg='white',
                        bg=mainColor,
                        font=('Comic Sans', 28, 'bold')
                        );
        title.grid(row=0, column=1, pady=(10,10), sticky='NESW');

        self.execute = True;
        imageList1 = [os.path.abspath('.')+'/Activos/termometro/frame-1.gif', os.path.abspath('.')+'/Activos/termometro/frame-2.gif']
        firstImage = Label(topBar, bg=mainColor);
        firstImage.grid(row= 0, column = 0, pady=10, padx=(0,20), sticky='E');
        #Primera imagen
        def gif1():
            image = 0;
            while self.execute == True:
                for image in imageList1:
                    if(self.execute == True):
                        img1 = Image.open(image).resize((40,80));
                        try:
                            image1 = ImageTk.PhotoImage(img1, format='gif');
                        except:
                            return;
                        firstImage.configure(image=image1);
                        firstImage.image = image1;
                        time.sleep(1);
                    else:
                        return;

        imageList2 = [os.path.abspath('.')+'/Activos/sun/frame-1.gif', os.path.abspath('.')+'/Activos/sun/frame-2.gif', os.path.abspath('.')+'/Activos/sun/frame-3.gif', os.path.abspath('.')+'/Activos/sun/frame-4.gif'];
        secondImage = Label(topBar, bg=mainColor);
        secondImage.grid(row= 0, column = 2, pady=10, padx=(20,20), sticky='W');
        #Primera imagen
        def gif2():
            while self.execute == True:
                for image in imageList2:
                    if(self.execute == True):
                        img2 = Image.open(image).resize((80,80));
                        try:
                            image2 = ImageTk.PhotoImage(img2, format='gif');
                        except:
                            return;
                        secondImage.configure(image=image2);
                        secondImage.image = image2;
                        time.sleep(0.5);
                    else:
                        return;
                    
        #Hilos para los gif
        self.t1 = threading.Thread(target = gif1);
        self.t1.start();
        self.t2 = threading.Thread(target = gif2);
        self.t2.start();

        self.buttonDisconnect.grid(row=4, column=0, pady=(50,30), padx=10, sticky='S');
