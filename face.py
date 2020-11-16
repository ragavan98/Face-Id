import face_recognition as fr
import cv2
import os
import threading

face_encodings = []
FACES_DIR = "D:\\Faces"
N_FACES = len(os.listdir(FACES_DIR))


class Face:
    def __init__(self, enc, file):
        self.enc = enc
        self.file = file


def get_face_encodings():
    global face_encodings, FACES_DIR
    faces = os.listdir(FACES_DIR)
    for face in faces:
        file = FACES_DIR + "\\" + face
        face = cv2.imread(file)
        try:
            enc = fr.face_encodings(face)[0]
        except IndexError:
            continue
        f = Face(enc, file)
        face_encodings += [f]


get_face_encodings()


def detect_faces(img):
    global N_FACES, FACES_DIR
    img = cv2.imread(img)
    faces = fr.face_locations(img)
    print(faces)
    if len(fr.face_encodings(img)) > 0 and len(faces) == 1:
        cv2.imwrite(f"{FACES_DIR}\\{N_FACES+1}.jpg", img)
        N_FACES += 1
        threading.Thread(target=get_face_encodings).start()
        return f"{FACES_DIR}\\{N_FACES}.jpg"
    return False


def recognise_face(img):
    global face_encodings
    img = cv2.imread(img)
    img_enc = fr.face_encodings(img)
    if len(img_enc) > 0:
        for face in face_encodings:
            res = fr.compare_faces([face.enc], img_enc[0])
            if res[0]:
                print(res[0])
                return face.file
    return False

