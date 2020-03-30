import os
import cv2
import numpy as np
import time
from PIL import Image

def spara():
    ansikts_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
        
    try:
        with open(f'./users/user_ids.csv.txt', 'r', encoding='utf-8') as file:
            user_ids = file.read().splitlines()
            user_id = str(len(user_ids)+1)
    except:
        user_id = 2
    print(f'användar ID: {user_id}')
    face_id = input('skriv in namnet på användaren: ')
    räknare = 0
    while True:
        ret, img = cap.read()
        grå = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ansikte = ansikts_cascade.detectMultiScale(grå, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in ansikte:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            räknare += 1
            cv2.imwrite(f'./dataset/user{face_id}_{user_id}_{str(räknare)}.jpg', grå[y:y+h, x:x+w])
            cv2.imshow('image', img)
        end = cv2.waitKey(100)
        if end == 27:
            break
        elif räknare >= 30:
            break
    face_ids = []
    user_ids = []
    
    cap.release()
    cv2.destroyAllWindows()

def träna():
    path = './data'
    save_path = './train'
    läsa = cv2.face.LBPHFaceRecognizer_create()
    ansikts_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    ansikte, ids = hämta_bild(path, ansikts_cascade)
    läsa.train(ansikte, np.array(ids))
    läsa.write(f'{save_path}/train.yml')
    print(f'{len(np.unique(ids))} användare sparad')
    time.sleep(2)
    
def hämta_bild(path, ansikts_cascade):
    img_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for img_path in img_paths:
        PIL_img = Image.open(img_path).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        user_id = int(os.path.split(img_path)[-1].split('_')[1].split('_')[-1])
        ansikte = ansikts_cascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in ansikte:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)
    return face_samples, ids

def igenkänning():
    läsa = cv2.face.LBPHFaceRecognizer_create()
    läsa.read('./train/train.yml')
    ansikts_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
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
        print('ingen användare registrerad')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    min_W = 0.1*cap.get(3)
    min_H = 0.1*cap.get(4)
    
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ansikte = ansikts_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(min_W), int(min_H)))
        for (x, y, w, h) in ansikte:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            user_id, confidence = läsa.predict(gray[y:y+h, x:x+w])
            if (confidence < 100):
                index_id = user_ids.index(f'{(user_id)}')
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
    time.sleep(2)
    cap.release()
    cv2.destroyAllWindows()