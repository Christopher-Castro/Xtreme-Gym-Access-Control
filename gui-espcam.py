# Importamos librerias
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import os
import boto3
from urllib.request import urlopen

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

# Funcion Visualizar
def visualizar():
    global pantalla, frame, face_found, face_timer
    # Leemos la videocaptura
    if cap is not None:
        # ret, frame = cap.read()
        try:
            img_resp = urlopen(cap)
            imgnp = np.asarray(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Si es correcta
            if frame is not None:
                # Convert to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Detect the faces
                faces = face_cascade.detectMultiScale(gray_frame, 1.3, 6)
                # Draw the rectangle around each face
                frame_ = frame.copy()
                if len(faces) > 0 :
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame_, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        break
                    face_timer = face_timer + 10
                    if face_timer == 510:
                        face_found = True
                        label.configure(text='Reconociendo rostro...')
                        # convert to jpeg and save in variable
                        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                        response = rekognition.search_faces_by_image(
                            CollectionId='facerecognition_collection',
                            Image={'Bytes': image_bytes}
                        )
                        found = False
                        for match in response['FaceMatches']:
                            print(match['Face']['FaceId'],match['Similarity'])

                            face = dynamodb.get_item(
                                TableName='facerecognition',
                                Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                            )

                            if 'Item' in face:
                                print("Found person: ", face['Item']['FullName']['S'])
                                label.configure(text=f'Persona reconocida: {face["Item"]["FullName"]["S"]}')
                                found=True
                        if not found:
                            print('Persona no reconocida')
                    else:
                        face_found = False
                        label.configure(text=(f'Detectando rostro {(face_timer)/5} %'))
                else:
                    face_timer = -10
                    face_found = False
                    label.configure(text='')

                # Rendimensionamos el video
                # frame_ = imutils.resize(frame_, width=640)

                # Convertimos el video
                im = Image.fromarray(frame_)
                img = ImageTk.PhotoImage(image=im)

                # Mostramos en el GUI
                lblVideo.configure(image=img)
                lblVideo.image = img
                lblVideo.after(3000 if face_found else 10, visualizar)
            else:
                # cap.release()
                print("frame not found")
        except:
            print("error in frame creation")
            visualizar()
            # cap.release()

# Funcion iniciar
def iniciar():
    global cap
    # Elegimos la camara
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap = r'http://192.168.100.146/800x600.jpg'
    cap = r'http://192.168.100.146/640x480.jpg'
    # cap = r'http://192.168.100.146/480x320.jpg'
    # cap = r'http://192.168.100.146/400x296.jpg'
    visualizar()
    print("XtremeGym Access Control by Christopher Castro")

# Funcion finalizar
def finalizar():
    # cap.release()
    cv2.DestroyAllWindows()
    print("FIN")


# Variables
cap = None
detcolor = 0
detfaces = 0

# Load the cascade
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(haar_model)

#  Ventana Principal
# Pantalla
pantalla = Tk()
pantalla.title("Control de Acceso | Xtreme Gym | By: Christopher Castro")
pantalla.geometry("1280x720")  # Asignamos la dimension de la ventana

# Fondo
imagenF = PhotoImage(file="assets/Fondo.png")
background = Label(image = imagenF, text = "Fondo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Interfaz
texto1 = Label(pantalla, text="VIDEO EN TIEMPO REAL: ")
texto1.place(x = 580, y = 10)

texto2 = Label(pantalla, text="CONVERSION DE COLOR: ")
texto2.place(x = 1010, y = 100)

texto3 = Label(pantalla, text="DETECCION DE COLOR: ")
texto3.place(x = 110, y = 100)

# Botones
# Iniciar Video
imagenBI = PhotoImage(file="assets/Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imagenBI, height="40", width="200", command=iniciar)
inicio.place(x = 100, y = 580)

# Finalizar Video
imagenBF = PhotoImage(file="assets/Finalizar.png")
fin = Button(pantalla, text="Finalizar", image= imagenBF, height="40", width="200", command=finalizar)
fin.place(x = 980, y = 580)

# Labels
label = Label(text="", fg="Red", font=("Helvetica", 18))
label.place(x=600,y=580)
face_found=False
face_timer = -10

# Video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x = 470, y = 500)
# mask = imutils.resize(mask, width=360)

# # Convertimos el video
# im2 = Image.fromarray(mask)
# img2 = ImageTk.PhotoImage(image=im2)

# # Mostramos en el GUI
# lblVideo2.configure(image=img2)
# lblVideo2.image = img2
# lblVideo2.after(10, colores)

pantalla.mainloop()

