import os
import cv2
import numpy as np
import time
from PIL import Image

def data_collect():
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
        
    try:
        with open(f'./users/user_ids.csv.txt', 'r', encoding='utf-8') as file:
            user_ids = file.read().splitlines()
            user_id = str(len(user_ids)+1)
    except:
        user_id = '1'
    print(f'\n\n\t\tUser ID: {user_id}')
    face_id = input('\n\t\tPlease enter the name of the user: ')
    print('\n\n\t\tInitializing camera..')
    count = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite(f'./dataset/User{face_id}_{user_id}_{str(count)}.jpg', gray[y:y+h, x:x+w])
            cv2.imshow('image', img)
        end = cv2.waitKey(100)
        if end == 27:
            break
        elif count >= 30:
            break
    face_ids = []
    user_ids = []

    # try:
    #     with open(f'./users/user_ids.csv.txt', 'r', encoding='utf-8') as file:
    #         # read_ids = file.read().splitlines()
    #         # for line in read_ids:
    #         #     user_ids.append(line.rstrip())
    #         user_ids = file.read().splitlines()
    #         user_ids.append(user_id)
    #     with open(f'./users/face_ids.csv.txt', 'r', encoding='utf-8') as file:
    #         # read_ids = file.read().splitlines()
    #         # for line in read_ids:
    #         #     face_ids.append(line.rstrip())
    #         face_ids = file.read().splitlines()
    #         face_ids.append(face_id)
    #     with open(f'./users/user_ids.csv.txt', 'w', encoding='utf-8') as file:
    #         for line in user_ids:
    #             file.write(line + '\n')
    #     with open(f'./users/face_ids.csv.txt', 'w', encoding='utf-8') as file:
    #         for line in face_ids:
    #             file.write(line + '\n')
    # except:
    #     user_ids.append(user_id)
    #     face_ids.append(face_id)
    #     with open(f'./users/user_ids.csv.txt', 'w', encoding='utf-8') as file:
    #         for line in user_ids:
    #             file.write(line + '\n')
    #     with open(f'./users/face_ids.csv.txt', 'w', encoding='utf-8') as file:
    #         for line in face_ids:
    #             file.write(line + '\n')
    cap.release()
    cv2.destroyAllWindows()

def trainer():
    path = './dataset'
    save_path = './trainer'
    face_read = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    print('\n\n\t\tTraining faces from dataset...')
    faces, ids = get_img_lbl(path, face_cascade)
    face_read.train(faces, np.array(ids))
    face_read.write(f'{save_path}/trainer.yml')
    print(f'\n\t\t{len(np.unique(ids))} faces trained. Exiting trainer..')
    time.sleep(2)
    
def get_img_lbl(path, face_cascade):
    img_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for img_path in img_paths:
        PIL_img = Image.open(img_path).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        user_id = int(os.path.split(img_path)[-1].split('_')[1].split('_')[-1])
        faces = face_cascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)
    return face_samples, ids

def face_detect():
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        cv2.imshow('video', img)
        end = cv2.waitKey(30) & 0xff
        if end == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def face_reco():
    face_read = cv2.face.LBPHFaceRecognizer_create()
    face_read.read('./trainer/trainer.yml')
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    user_id = 0
    user_ids = []
    face_ids = []
    try:
        with open(f'./users/user_ids.csv.txt', 'r', encoding='utf-8') as file:
            read_users = file.readlines()
            for line in read_users:
                user_ids.append(line.rstrip())
        with open(f'./users/face_ids.csv.txt', 'r', encoding='utf-8') as file:
            read_users = file.readlines()
            for line in read_users:
                face_ids.append(line.rstrip())
    except:
        print('\n\n\t\tNo users registered')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    min_W = 0.1*cap.get(3)
    min_H = 0.1*cap.get(4)
    
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(min_W), int(min_H)))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            user_id, confidence = face_read.predict(gray[y:y+h, x:x+w])
            if (confidence < 100):
                index_id = user_ids.index(f'{str(user_id)}')
                for i, index in enumerate(user_ids):
                    if index == user_id:
                        index_id = i
                        break
                user_name = face_ids[index_id]
                confidence = f' {round(100-confidence)}%'
            else:
                user_name = 'Unknown'
                confidence = f' {round(100-confidence)}%'
            cv2.putText(img, str(user_name), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 255), 1)
            
        cv2.imshow('camera', img)
        end = cv2.waitKey(10) & 0xff
        if end == 27:
            break
    print('\n\n\t\tExiting datacapture..')
    time.sleep(2)
    cap.release()
    cv2.destroyAllWindows()