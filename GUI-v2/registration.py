from tkinter import *
from tkinter import ttk
from tkcalendar import *
from datetime import *
import boto3
import cv2
import os
import numpy as np
from urllib.request import urlopen
from PIL import Image, ImageTk
import instructor
import imutils

from tkinter import messagebox

from aws.rekognition import index_face
from db.model import User as User

import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

class Registration:
    def __init__(self, root):
        self.root = root
        self.accessControlFrame = Frame(self.root)
        self.accessControlFrame.pack(side=LEFT, fill=X)
        # Variables
        self.cap = None
        self.detcolor = 0
        self.detfaces = 0

        # # Load the cascade
        # # self.cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
        # # self.haar_model = os.path.join(self.cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
        # self.haar_model = './assets/haarcascade_frontalface_default.xml'
        # self.face_cascade = cv2.CascadeClassifier(self.haar_model)

        # # Fondo
        # imagenF = PhotoImage(file="../assets/Fondo.png")
        # background = Label(image = imagenF, text = "Fondo")
        # background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        # Interfaz
        self.texto1 = Label(self.accessControlFrame, text="VIDEO EN TIEMPO REAL: ", font=("Impact", 35))
        self.texto1.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Finalizar Video
        # self.imagenBF = PhotoImage(file="../assets/Finalizar.png")
        # self.fin = Button(self.accessControlFrame, text="Finalizar", image= self.imagenBF, height="40", width="200", command=self.finalizar)
        self.fin = Button(self.accessControlFrame, text="Regresar", width=15, command=self.finalizar, bd=0, cursor="hand2", bg="#ff1909", fg="black", font=("Impact", 15))
        self.fin.grid(row=0, column=0, padx=10, pady=20)

        # Video
        self.lblVideo = Label(self.accessControlFrame)
        self.lblVideo.grid(row=1, column=1, padx=10, pady=20)

        # Labels
        self.label = Label(self.accessControlFrame, text="", fg="Red", font=("Helvetica", 28))
        self.label.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        self.face_found=False
        self.face_timer = -10

        # Botones
        # Iniciar Video
        # self.imagenBI = PhotoImage(file="../assets/Inicio.png")
        self.inicio = Button(self.accessControlFrame, text="Repetir Foto", width=15, command=self.iniciar, bd=0, cursor="hand2", bg="#ff1909", fg="black", font=("Impact", 15))
        self.inicio.grid(row=2, column=0, padx=10, pady=20)
        
        # self.lblVideo2 = Label(self.accessControlFrame)
        # self.lblVideo2.place(x = 470, y = 500)
        # mask = imutils.resize(mask, width=360)

        # local variables
        self.userName = StringVar()
        self.userPhone = StringVar()
        self.userEmail = StringVar()
        self.userLocation = StringVar()
        self.userDateInit = StringVar()
        self.userDateFinish = StringVar()

        self.registrationControlsFrame()
        self.iniciar()
        # self.accessControlFrame.mainloop()

    # Funcion Visualizar
    def visualizar(self):
        # Leemos la videocaptura
        if self.cap is not None:
            try:
                # self.img_resp = urlopen(self.cap)
                # self.imgnp = np.asarray(bytearray(self.img_resp.read()), dtype=np.uint8)
                # self.frame = cv2.imdecode(self.imgnp, -1)
                # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                with mp_face_detection.FaceDetection(
                    model_selection=0, min_detection_confidence=0.7) as face_detection:
                    ret, self.frame = self.cap.read()
                    self.frame.flags.writeable = False
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    results = face_detection.process(self.frame)

                    # Draw the face detection annotations on the image.
                    self.frame.flags.writeable = True

                    # Si es correcta
                    # if self.frame is not None:
                    if ret is not None:
                        # Convert to grayscale
                        # self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                        # # Detect the faces
                        # self.faces = self.face_cascade.detectMultiScale(self.gray_frame, 1.2, 3, minSize=(200, 200))
                        self.frame_ = self.frame.copy()
                        if results.detections:
                            for detection in results.detections:
                                mp_drawing.draw_detection(self.frame_, detection)
                        # if len(self.faces) > 0 :
                        #     for (x, y, w, h) in self.faces:
                        #         cv2.rectangle(self.frame_, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        #         break
                            if len(results.detections) == 1:
                                self.face_timer = self.face_timer + 10
                            else:
                                self.face_timer = -10
                            if self.face_timer == 510:
                                self.face_timer = -10
                                self.inicio.grid(row=2, column=0, padx=10, pady=20)
                                self.face_found = True
                                self.label.configure(text='Rostro detectado.', fg="Green")
                                # convert to jpeg and save in variable
                                self.image_bytes = cv2.imencode('.jpg', self.frame)[1].tobytes()
                            else:
                                self.face_found = False
                                if len(results.detections) == 1:
                                    self.label.configure(text=(f'Detectando rostro {(self.face_timer)/5} %'), fg="Red")
                                else:
                                    self.label.configure(text=(f'Detección de más de un rostro!'), fg="Red")
                            # if self.face_timer == 500:
                            #     self.cap = r'http://192.168.100.146/1600x1200.jpg'
                        else:
                            self.face_timer = -10
                            self.face_found = False
                            self.label.configure(text='')

                        # Rendimensionamos el video
                        self.frame_ = imutils.resize(self.frame_, width=640)

                        # Convertimos el video
                        self.im = Image.fromarray(self.frame_)
                        self.img = ImageTk.PhotoImage(image=self.im)

                        # Mostramos en el GUI
                        self.lblVideo.configure(image=self.img)
                        self.lblVideo.image = self.img
                        if not self.face_found:
                            self.lblVideotimer = self.lblVideo.after(10, self.visualizar)
                        else:
                            self.lblVideo.after_cancel(self.lblVideotimer)
                    else:
                        # cap.release()
                        print("frame not found")
            except:
                print("error in frame creation")
                self.visualizar()
                # cap.release()

    # Funcion iniciar
    def iniciar(self):
        # Elegimos la camara
        if not self.cap:
            self.cap = cv2.VideoCapture(1)
        self.inicio.grid_remove()
        self.image_bytes = None
        self.visualizar()

    def iniciar_esp(self):
        # Elegimos la camara
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap = r'http://192.168.100.146/800x600.jpg'
        self.cap = r'http://192.168.100.146/640x480.jpg'
        # cap = r'http://192.168.100.146/480x320.jpg'
        # cap = r'http://192.168.100.146/400x296.jpg'
        self.inicio.grid_remove()
        self.image_bytes = None
        self.visualizar()

    # Funcion finalizar
    def finalizar(self):
        self.cap.release()
        # cv2.DestroyAllWindows()
        # print("FIN")
        self.accessControlFrame.destroy()
        self.registrationControlFrame.destroy()
        instructor.InstructorControls(self.root)
    
    def registrationControlsFrame(self):
        # User Name
        self.registrationControlFrame = Frame(self.root)
        self.registrationControlFrame.pack(side=RIGHT, fill=X)
        self.labelUPhone = Label(self.registrationControlFrame, text="Nombre", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelUPhone.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txtUName = Entry(self.registrationControlFrame, textvariable=self.userName, font=("Times New Roman", 15), width=40)
        self.txtUName.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # User Phone
        self.labelUPhone = Label(self.registrationControlFrame, text="Teléfono", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelUPhone.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.txtUPhone = Entry(self.registrationControlFrame, textvariable=self.userPhone, font=("Times New Roman", 15), width=40)
        self.txtUPhone.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # User Email
        self.labelEmail = Label(self.registrationControlFrame, text="Email", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelEmail.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txtEmail = Entry(self.registrationControlFrame, textvariable=self.userEmail, font=("Times New Roman", 15), width=40)
        self.txtEmail.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # User Location
        self.labelLocation = Label(self.registrationControlFrame, text="Locación", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelLocation.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.comboLocation = ttk.Combobox(self.registrationControlFrame, textvariable=self.userLocation, font=("Times New Roman", 15),
                                        width=40,
                                        state="readonly")
        self.comboLocation['values'] = ("Platinum")
        self.comboLocation.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # User Date init
        self.labelDateInit = Label(self.registrationControlFrame, text="Fecha inicio", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelDateInit.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entryDateInit = DateEntry(self.registrationControlFrame, setmode='day', date_pattern='dd/mm/yyyy', textvariable=self.userDateInit,
                                  font=("Times New Roman", 12), width=40, locale='es_ES')
        self.entryDateInit.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # User date finish
        self.labelDateFinish = Label(self.registrationControlFrame, text="Fecha fin", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelDateFinish.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entryDateFinish = DateEntry(self.registrationControlFrame, setmode='day', date_pattern='dd/mm/yyyy', textvariable=self.userDateFinish,
                                  font=("Times New Roman", 12), width=40, locale='es_ES')
        self.entryDateFinish.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # User History
        # self.labelHistory = Label(self.registrationControlFrame, text="Historial de acceso", font=("Times New Roman", 16, "bold"), bg="#5856a0",
        #                           fg="white")
        # self.labelHistory.grid(row=6, column=3, padx=10, pady=10, sticky="w")
        # self.txtUHistory = Text(self.registrationControlFrame, font=("Times New Roman", 15), width=82, height=5)
        # self.txtUHistory.grid(row=6, column=4, padx=10, pady=10, sticky="w", columnspan=4)

        # Add a new Record
        self.btnAdd = Button(self.registrationControlFrame, command=self.regUser, text="Registrar Usuario", bd=0, cursor="hand2",
                             bg="#ff1909",
                             fg="black", width=15, font=("Impact", 15))
        self.btnAdd.grid(row=6, column=1, padx=10)

    def regUser(self):
        try:
            if self.txtUName.get() == "" or self.entryDateFinish.get() == "" or self.txtUPhone.get() == "" or self.entryDateInit.get() == "" or self.txtEmail.get() == "" or self.comboLocation.get() == "":
                messagebox.showerror("Error!", "Por favor, llene todos los campos!")
                return
            if self.image_bytes is None:
                messagebox.showerror("Error!", "No se ha cargado ninguna fotografía")
                return
            user_id = index_face(self.image_bytes)
            if isinstance(user_id, dict):
                if user_id['register']:
                    messagebox.showerror("Error!", f'Rostro registrado previamente bajo el nombre: {user_id["register"].FullName}')
                    return
                else:
                    messagebox.showerror("Error!", f'Rostro conocido pero sin registro. Se utilizará el ID existente para crear el nuevo registro.')
                    print(user_id['id'])
                    user_id = user_id['id']
            user = User(user_id, FullName=self.txtUName.get(), phone=self.txtUPhone.get(), email=self.txtEmail.get(), location=self.comboLocation.get(), access_history=[f'createdOn {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'], suscription_start=self.entryDateInit.get(), suscription_end=self.entryDateFinish.get())
            user.save()
            # db.insertStudent(self.txtUName.get(), self.txtUPhone.get(), self.txtEmail.get(), self.entryDateInit.get(),
            #                 self.comboLocation.get(),
            #                 self.entryDateFinish.get(), self.txtUHistory.get(1.0, END))

            messagebox.showinfo("Success!", "Registro creado existosamente!")
        except AttributeError as error:
            print(error)
            messagebox.showerror("Error!", "Please View and Select a Student to Book a Session!")
        # self.resetForm()
        # self.viewStudents()