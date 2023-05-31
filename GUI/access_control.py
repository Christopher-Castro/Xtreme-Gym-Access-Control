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
import serial

from tkinter import messagebox

from db.model import User as User
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1" 
)
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1" 
)


class AccessControl:
    def __init__(self, root):
        self.root = root
        self.accessControlFrame = Frame(self.root)
        self.accessControlFrame.pack(side=LEFT, fill=X)
        # Variables
        self.cap = None
        self.detcolor = 0
        self.detfaces = 0
        self.userName_ = StringVar()
        self.userDateInit_ = StringVar()
        self.userDateFinish_ = StringVar()
        self.daysCount = StringVar()

        # Load the cascade
        # self.cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
        # self.haar_model = os.path.join(self.cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
        # # self.haar_model = './assets/haarcascade_frontalface_default.xml'
        # self.face_cascade = cv2.CascadeClassifier(self.haar_model)

        # # Fondo
        # imagenF = PhotoImage(file="../assets/Fondo.png")
        # background = Label(image = imagenF, text = "Fondo")
        # background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        # Finalizar Video
        # self.imagenBF = PhotoImage(file="../assets/Finalizar.png")
        # self.fin = Button(self.accessControlFrame, text="Finalizar", image= self.imagenBF, height="40", width="200", command=self.finalizar)
        self.fin = Button(self.accessControlFrame, text="Regresar", width=10, command=self.finalizar, bd=0, cursor="hand2", bg="#ff1909", fg="black", font=("Impact", 15))
        self.fin.grid(row=0, column=0, padx=10, pady=20)

        # Interfaz
        self.texto1 = Label(self.accessControlFrame, text="VIDEO EN TIEMPO REAL: ", font=("Impact", 35))
        self.texto1.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Botones
        # Iniciar Video
        # self.imagenBI = PhotoImage(file="../assets/Inicio.png")
        # self.inicio = Button(self.accessControlFrame, text="Iniciar", image=self.imagenBI, height="40", width="200", command=self.iniciar)
        # self.inicio.grid(row=2, column=0, padx=10, pady=20, sticky="w")

        # Video
        self.lblVideo = Label(self.accessControlFrame)
        self.lblVideo.grid(row=1, column=1, padx=10, pady=20)

        # Labels
        self.label = Label(self.accessControlFrame, text="", fg="Red", font=("Helvetica", 28))
        self.label.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        self.face_found=False
        self.face_timer = -10


        # self.lblVideo2 = Label(self.accessControlFrame)
        # self.lblVideo2.place(x = 470, y = 500)
        # mask = imutils.resize(mask, width=360)
        self.arduino = serial.Serial("COM4", 9600)
        self.registrationControlsFrame()
        self.iniciar()
        # self.accessControlFrame.mainloop()

    # Funcion Visualizar
    def visualizar(self):
        # Leemos la videocaptura
        self.userName_.set("")
        self.userDateInit_.set("")
        self.userDateFinish_.set("")
        self.daysCount.set("")
        if self.cap is not None:
            try:
                # self.img_resp = urlopen(self.cap)
                # self.imgnp = np.asarray(bytearray(self.img_resp.read()), dtype=np.uint8)
                # self.frame = cv2.imdecode(self.imgnp, -1)
                # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                with mp_face_detection.FaceDetection(
                    model_selection=0, min_detection_confidence=1.0) as face_detection:
                    ret, self.frame = self.cap.read()
                    self.frame.flags.writeable = False
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    results = face_detection.process(self.frame)

                    # Draw the face detection annotations on the image.
                    self.frame.flags.writeable = True
                    # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                    
                    # Si es correcta
                    # if self.frame is not None:
                    if ret is not None:
                        # Convert to grayscale
                        # self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                        # Detect the faces
                        # self.faces = self.face_cascade.detectMultiScale(self.gray_frame, 1.2, 3, minSize=(200, 200))
                        # Draw the rectangle around each face
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
                                self.face_found = True
                                self.face_timer = -10
                                # convert to jpeg and save in variable
                                self.image_bytes = cv2.imencode('.jpg', self.frame)[1].tobytes()
                                self.response = rekognition.search_faces_by_image(
                                    CollectionId='facerecognition_collection',
                                    Image={'Bytes': self.image_bytes},
                                    MaxFaces=1
                                )
                                self.found = False
                                for match in self.response['FaceMatches']:
                                    print(match['Face']['FaceId'],match['Similarity'])
    
                                    if match['Similarity'] > 99.5:
                                        # self.face = dynamodb.get_item(
                                        #     TableName='facerecognition',
                                        #     Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                                        # )
                                        self.face = User.get(match['Face']['FaceId'])
                                        
                                        if self.face:
                                            self.found=True
                                            print("Found person: ", f'{self.face.to_json()}')
                                            access_allowed = False
                                            if 'createdOn' in self.face.access_history[0]:
                                                access_allowed = True
                                            else:
                                                last_date = datetime.strptime(self.face.access_history[0], '%d/%m/%Y %H:%M:%S')
                                                if (datetime.now().replace(microsecond=0) - last_date)/timedelta(days=1) > 0.3:
                                                    access_allowed = True
                                            
                                            if self.face.RekognitionId in ['c5fe0f64-bc82-4026-ab81-2286223bf377', 'c0732fba-2df2-49c6-85ba-ea2bae3ec139', 'c60be0c3-99a5-492e-97aa-5d6ea033250d', '1570fd41-1846-4b8b-807b-5723aaa42c43', '1f8aaa82-c4bb-4da9-a2bd-27a2a612bf51'] :
                                                access_allowed = True

                                            if access_allowed:
                                                self.userName_.set(self.face.FullName)
                                                self.userDateInit_.set(self.face.suscription_start)
                                                self.userDateFinish_.set(self.face.suscription_end)
                                                daysCount_ = int((datetime.strptime(self.face.suscription_end, '%d/%m/%Y') - datetime.now().replace(second=0, microsecond=0))/timedelta(days=1))
                                                if daysCount_>=0:
                                                    self.label.configure(text=f'Persona reconocida. Bien venido!', fg="Green")
                                                    self.daysCount.set(str(daysCount_))
                                                    self.arduino.write(b'1')
                                                    self.face.update(actions=[
                                                        User.access_history.set(
                                                            User.access_history.prepend([datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
                                                        )
                                                    ])
                                                else:
                                                    self.label.configure(text=f'Persona reconocida con membresia expirada.')
                                                    self.daysCount.set("Expirado")
                                            else:
                                                self.label.configure(text=f'Doble acceso!!!\nÚltima visita: {self.face.access_history[0]}')
                                                self.userName_.set(self.face.FullName)
                                                self.userDateInit_.set(self.face.suscription_start)
                                                self.userDateFinish_.set(self.face.suscription_end)
                                            break

                                if not self.found:
                                    self.label.configure(text=(f'Persona no reconocida'))
                            else:
                                self.face_found = False
                                if self.face_timer == 500:
                                    self.label.configure(text='Reconociendo rostro...')
                                else:
                                    if len(results.detections) == 1:
                                        self.label.configure(text=(f'Detectando rostro {(self.face_timer)/5} %'), fg="Red")
                                    else:
                                        self.label.configure(text=(f'Detección de más de un rostro!'), fg="Red")
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
                        self.lblVideo.after(5000 if self.face_found else 10, self.visualizar)
                    else:
                        # cap.release()
                        print("frame not found")
            except Exception as error:
                print("error in frame creation")
                print(error)
                self.visualizar()
                # cap.release()

    # Funcion iniciar
    def iniciar(self):
        # Elegimos la camara
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.visualizar()

    def iniciar_esp(self):
        # Elegimos la camara
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap = r'http://192.168.100.146/800x600.jpg'
        self.cap = r'http://192.168.100.146/640x480.jpg'
        # cap = r'http://192.168.100.146/480x320.jpg'
        # cap = r'http://192.168.100.146/400x296.jpg'
        self.visualizar()
        print("XtremeGym Access Control by Christopher Castro")

    # Funcion finalizar
    def finalizar(self):
        self.cap.release()
        # cv2.DestroyAllWindows()
        # print("FIN")
        self.arduino.close()
        self.accessControlFrame.destroy()
        self.registrationControlFrame.destroy()
        instructor.InstructorControls(self.root)
    
    def registrationControlsFrame(self):
        # User Name
        self.registrationControlFrame = Frame(self.root)
        self.registrationControlFrame.pack(side=RIGHT, fill=X)
        self.labelUPhone = Label(self.registrationControlFrame, text="Nombre", font=("Times New Roman", 22, "bold"), fg="black")
        self.labelUPhone.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txtUName = Entry(self.registrationControlFrame, textvariable=self.userName_, font=("Times New Roman", 20), width=40)
        self.txtUName.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # User Date init
        self.labelDateInit = Label(self.registrationControlFrame, text="Fecha inicio", font=("Times New Roman", 22, "bold"), fg="black")
        self.labelDateInit.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entryDateInit = Entry(self.registrationControlFrame, textvariable=self.userDateInit_, font=("Times New Roman", 40), width=40)
        self.entryDateInit.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # User date finish
        self.labelDateFinish = Label(self.registrationControlFrame, text="Fecha fin", font=("Times New Roman", 22, "bold"), fg="black")
        self.labelDateFinish.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entryDateFinish = Entry(self.registrationControlFrame, textvariable=self.userDateFinish_, font=("Times New Roman", 40), width=40)
        self.entryDateFinish.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Dias restantes
        self.labelDateFinish = Label(self.registrationControlFrame, text="Días restantes", font=("Times New Roman", 22, "bold"), fg="black")
        self.labelDateFinish.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entryDateFinish = Entry(self.registrationControlFrame, textvariable=self.daysCount, font=("Times New Roman", 100, "bold"), width=20)
        self.entryDateFinish.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # User History
        # self.labelHistory = Label(self.registrationControlFrame, text="Historial de acceso", font=("Times New Roman", 16, "bold"), bg="#5856a0",
        #                           fg="white")
        # self.labelHistory.grid(row=6, column=3, padx=10, pady=10, sticky="w")
        # self.txtUHistory = Text(self.registrationControlFrame, font=("Times New Roman", 15), width=82, height=5)
        # self.txtUHistory.grid(row=6, column=4, padx=10, pady=10, sticky="w", columnspan=4)
